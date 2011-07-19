#!/usr/bin/env python
'''
GAEUnit: Google App Engine Unit Test Framework

Usage:

1. Put gaeunit.py into your application directory.  Modify 'app.yaml' by
   adding the following mapping below the 'handlers:' section:

   - url: /test.*
     script: gaeunit.py

2. Write your own test cases by extending unittest.TestCase.

3. Launch the development web server.  To run all tests, point your browser to:

   http://localhost:8080/test     (Modify the port if necessary.)

   For plain text output add '?format=plain' to the above URL.
   See README.TXT for information on how to run specific tests.

4. The results are displayed as the tests are run.

Visit http://code.google.com/p/gaeunit for more information and updates.

------------------------------------------------------------------------------
Copyright (c) 2008-2009, George Lei and Steven R. Farley.  All rights reserved.

Distributed under the following BSD license:

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
------------------------------------------------------------------------------
'''

__author__ = "George Lei and Steven R. Farley"
__email__ = "George.Z.Lei@Gmail.com"
__version__ = "#Revision: 1.2.8 $"[11:-2]
__copyright__= "Copyright (c) 2008-2009, George Lei and Steven R. Farley"
__license__ = "BSD"
__url__ = "http://code.google.com/p/gaeunit"

import base64
import cgi
import logging
import os
import re
import sys
import time
import unittest
import urlparse

import appengine_config

from django.template import add_to_builtins
add_to_builtins('base.custom_filters')

import django.utils.simplejson
from django.test import client

from xml.sax.saxutils import unescape
from google.appengine.ext import webapp
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import datastore_file_stub
from google.appengine.api import urlfetch
from google.appengine.api.memcache import memcache_stub
from google.appengine.api.taskqueue import taskqueue_stub
from google.appengine.ext.webapp.util import run_wsgi_app

_LOCAL_TEST_DIR = 'test'  # location of files
_WEB_TEST_DIR = '/test'   # how you want to refer to tests on your web server
_LOCAL_DJANGO_TEST_DIR = '../../gaeunit/test'

# or:
# _WEB_TEST_DIR = '/u/test'
# then in app.yaml:
#   - url: /u/test.*
#     script: gaeunit.py

##################################################
## Django support

def django_test_runner(request):
    unknown_args = [arg for (arg, v) in request.REQUEST.items()
                    if arg not in ("format", "package", "name")]
    if len(unknown_args) > 0:
        errors = []
        for arg in unknown_args:
            errors.append(_log_error("The request parameter '%s' is not valid." % arg))
        from django.http import HttpResponseNotFound
        return HttpResponseNotFound(" ".join(errors))

    format = request.REQUEST.get("format", "html")
    package_name = request.REQUEST.get("package")
    test_name = request.REQUEST.get("name")
    if format == "html":
        return _render_html(package_name, test_name)
    elif format == "plain":
        return _render_plain(package_name, test_name)
    else:
        error = _log_error("The format '%s' is not valid." % cgi.escape(format))
        from django.http import HttpResponseServerError
        return HttpResponseServerError(error)

def _render_html(package_name, test_name):
    suite, error = _create_suite(package_name, test_name, _LOCAL_DJANGO_TEST_DIR)
    if not error:
        content = _MAIN_PAGE_CONTENT % (_test_suite_to_json(suite), _WEB_TEST_DIR, __version__)
        from django.http import HttpResponse
        return HttpResponse(content)
    else:
        from django.http import HttpResponseServerError
        return HttpResponseServerError(error)

def _render_plain(package_name, test_name):
    suite, error = _create_suite(package_name, test_name, _LOCAL_DJANGO_TEST_DIR)
    if not error:
        from django.http import HttpResponse
        response = HttpResponse()
        response["Content-Type"] = "text/plain"
        runner = unittest.TextTestRunner(response)
        response.write("====================\n" \
                        "GAEUnit Test Results\n" \
                        "====================\n\n")
        _run_test_suite(runner, suite)
        return response
    else:
        from django.http import HttpResponseServerError
        return HttpResponseServerError(error)

def django_json_test_runner(request):
    from django.http import HttpResponse
    response = HttpResponse()
    response["Content-Type"] = "text/javascript"
    test_name = request.REQUEST.get("name")
    _load_default_test_modules(_LOCAL_DJANGO_TEST_DIR)
    suite = unittest.defaultTestLoader.loadTestsFromName(test_name)
    runner = JsonTestRunner()
    _run_test_suite(runner, suite)
    runner.result.render_to(response)
    return response

########################################################

class GAETestCase(unittest.TestCase):
    """TestCase parent class that provides the following assert functions
        * assertHtmlEqual - compare two HTML string ignoring the
            out-of-element blanks and other differences acknowledged in standard.
    """

    def assertHtmlEqual(self, html1, html2):
        if html1 is None or html2 is None:
            raise self.failureException, "argument is None"
        html1 = self._formalize(html1)
        html2 = self._formalize(html2)
        if not html1 == html2:
            error_msg = self._findHtmlDifference(html1, html2)
            error_msg = "HTML contents are not equal" + error_msg
            raise self.failureException, error_msg

    def _formalize(self, html):
        html = html.replace("\r\n", " ").replace("\n", " ")
        html = re.sub(r"[ \t]+", " ", html)
        html = re.sub(r"[ ]*>[ ]*", ">", html)
        html = re.sub(r"[ ]*<[ ]*", "<", html)
        return unescape(html)

    def _findHtmlDifference(self, html1, html2):
        display_window_width = 41
        html1_len = len(html1)
        html2_len = len(html2)
        for i in range(html1_len):
            if i >= html2_len or html1[i] != html2[i]:
                break

        if html1_len < html2_len:
            html1 += " " * (html2_len - html1_len)
            length = html2_len
        else:
            html2 += " " * (html1_len - html2_len)
            length = html1_len

        if length <= display_window_width:
            return "\n%s\n%s\n%s^" % (html1, html2, "_" * i)

        start = i - display_window_width / 2
        end = i + 1 + display_window_width / 2

        if start < 0:
            adjust = -start
            start += adjust
            end += adjust
            pointer_pos = i
            leading_dots = ""
            ending_dots = "..."
        elif end > length:
            adjust = end - length
            start -= adjust
            end -= adjust
            pointer_pos = i - start + 3
            leading_dots = "..."
            ending_dots = ""
        else:
            pointer_pos = i - start + 3
            leading_dots = "..."
            ending_dots = "..."
        return '\n%s%s%s\n%s\n%s^' % (leading_dots, html1[start:end], ending_dots, leading_dots+html2[start:end]+ending_dots, "_" * (i - start + len(leading_dots)))

    assertHtmlEquals = assertHtmlEqual


##############################################################################
# Main request handler
##############################################################################


class MainTestPageHandler(webapp.RequestHandler):
    def get(self):
        unknown_args = [arg for arg in self.request.arguments()
                        if arg not in ("format", "package", "name")]
        if len(unknown_args) > 0:
            errors = []
            for arg in unknown_args:
                errors.append(_log_error("The request parameter '%s' is not valid." % arg))
            self.error(404)
            self.response.out.write(" ".join(errors))
            return

        format = self.request.get("format", "html")
        package_name = self.request.get("package")
        test_name = self.request.get("name")
        if format == "html":
            self._render_html(package_name, test_name)
        elif format == "plain":
            self._render_plain(package_name, test_name)
        else:
            error = _log_error("The format '%s' is not valid." % cgi.escape(format))
            self.error(404)
            self.response.out.write(error)

    def _render_html(self, package_name, test_name):
        suite, error = _create_suite(package_name, test_name, _LOCAL_TEST_DIR)
        if not error:
            self.response.out.write(_MAIN_PAGE_CONTENT % (_test_suite_to_json(suite), _WEB_TEST_DIR, __version__))
        else:
            self.error(404)
            self.response.out.write(error)

    def _render_plain(self, package_name, test_name):
        self.response.headers["Content-Type"] = "text/plain"
        runner = unittest.TextTestRunner(self.response.out)
        suite, error = _create_suite(package_name, test_name, _LOCAL_TEST_DIR)
        if not error:
            self.response.out.write("====================\n" \
                                    "GAEUnit Test Results\n" \
                                    "====================\n\n")
            _run_test_suite(runner, suite)
        else:
            self.error(404)
            self.response.out.write(error)


##############################################################################
# JSON test classes
##############################################################################


class JsonTestResult(unittest.TestResult):
    def __init__(self):
        unittest.TestResult.__init__(self)
        self.testNumber = 0

    def render_to(self, stream):
        result = {
            'runs': self.testsRun,
            'total': self.testNumber,
            'errors': self._error_tuples_to_dicts(self.errors),
            'failures': self._error_tuples_to_dicts(self.failures),
            # TODO(slamm): Add times.
            # TODO(slamm): Add logs.
            }
        stream.write(django.utils.simplejson.dumps(result))

    def _error_tuples_to_dicts(self, errors):
        """Convert errors and failures into simple datastructures."""
        return [{
            'short_description': test.shortDescription() or '',
            'traceback': cgi.escape(traceback_string),
            } for test, traceback_string in errors]


class JsonTestRunner:
    def run(self, test):
        self.result = JsonTestResult()
        self.result.testNumber = test.countTestCases()
        startTime = time.time()
        test(self.result)
        stopTime = time.time()
        timeTaken = stopTime - startTime
        return self.result


class JsonTestRunHandler(webapp.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/javascript"
        test_name = self.request.get("name")
        _load_default_test_modules(_LOCAL_TEST_DIR)
        suite = unittest.defaultTestLoader.loadTestsFromName(test_name)
        runner = JsonTestRunner()
        _run_test_suite(runner, suite)
        runner.result.render_to(self.response.out)


# This is not used by the HTML page, but it may be useful for other client test runners.
class JsonTestListHandler(webapp.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/javascript"
        suite, error = _create_suite(self.request) #TODO
        if not error:
            self.response.out.write(_test_suite_to_json(suite))
        else:
            self.error(404)
            self.response.out.write(error)


##############################################################################
# Module helper functions
##############################################################################


def _create_suite(package_name, test_name, test_dir):
    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite()

    error = None

    try:
        if not package_name and not test_name:
                modules = _load_default_test_modules(test_dir)
                for module in modules:
                    suite.addTest(loader.loadTestsFromModule(module))
        elif test_name:
                _load_default_test_modules(test_dir)
                suite.addTest(loader.loadTestsFromName(test_name))
        elif package_name:
                package = reload(__import__(package_name))
                module_names = package.__all__
                for module_name in module_names:
                    suite.addTest(loader.loadTestsFromName('%s.%s' % (package_name, module_name)))

        if suite.countTestCases() == 0:
            raise Exception("'%s' is not found or does not contain any tests." %  \
                            (test_name or package_name or 'local directory: \"%s\"' % _LOCAL_TEST_DIR))
    except Exception:
        import traceback
        error = traceback.format_exc()
        print error
        _log_error(error)

    return (suite, error)


def _load_default_test_modules(test_dir):
    if not test_dir in sys.path:
        sys.path.append(test_dir)
    module_names = [mf[0:-3] for mf in os.listdir(test_dir) if mf.endswith(".py")]
    emacs_temp_files = [mf for mf in module_names if mf.startswith(".#")]
    if emacs_temp_files:
        raise Exception("Found emacs temporary files (indicates unsaved files): %s" %
                        ", ".join(["%s.py" % x for x in emacs_temp_files]))
    return [reload(__import__(name)) for name in module_names]


def _get_tests_from_suite(suite):
    for test in suite:
        if isinstance(test, unittest.TestSuite):
            for t in _get_tests_from_suite(test):
                yield t
        else:
            yield test


def _test_suite_to_json(suite):
    """Convert a test suite to a json string.

    Returns:
        A json string of the following python structure:
        {module_name: {class_name: [method_name, ...], ...}, ...}
    """
    test_dict = {}
    for test in _get_tests_from_suite(suite):
        test_dict.setdefault(
            type(test).__module__, {}).setdefault(
                type(test).__name__, []).append(
                   test._testMethodName)
    return django.utils.simplejson.dumps(test_dict)


class TestingTaskQueueService(taskqueue_stub.TaskQueueServiceStub):

    def _Dynamic_Add(self, request, response):
        logging.info("gaeunit faking a taskqueue Add")
        taskqueue_stub.TaskQueueServiceStub._Dynamic_Add(
            self, request, response)
        self._ExecuteTasksImmediately()

    def _Dynamic_BulkAdd(self, request, response):
        logging.info("gaeunit faking a taskqueue BulkAdd")
        taskqueue_stub.TaskQueueServiceStub._Dynamic_BulkAdd(
            self, request, response)
        self._ExecuteTasksImmediately()

    def _ExecuteTasksImmediately(self):
        logging.info("gaeunit executing tasks immediately")
        if hasattr(self, '_is_executing') and self._is_executing:
            return
        self._is_executing = True
        try:
            while 1:
                task = None
                for queue in self.GetQueues():
                    queue_name = queue['name']
                    tasks = self.GetTasks(queue_name)
                    if tasks:
                        task = tasks[0]
                        break
                if task is None:
                    break

                headers = dict((k.lower(), v) for k, v in task['headers'])
                content_type = headers['content-type']
                c = client.Client()
                if task['method'] == 'GET':
                    try:
                        # Only Django 1.1 or greater can handle a query string.
                        url_parts = list(urlparse.urlsplit(task['url']))
                        query = url_parts[3]
                        query_data = {}
                        if query:
                            query_data = dict(
                                kv.split('=') for kv in url_parts[3].split('&'))
                        url_parts[3] = ''
                        url = urlparse.urlunsplit(url_parts)
                        logging.info("Execute task immediately: GET %s, query=%s", url, query_data)
                        c.get(url, query_data, content_type=content_type)
                    except:
                        import traceback
                        error = traceback.format_exc()
                        _log_error(error)
                        raise
                elif task['method'] == 'POST':
                    body = base64.b64decode(task['body'])
                    logging.info("Execute task immediately: POST %s, body=%s", task['url'], body)
                    c.post(task['url'], data=body, content_type=content_type)
                else:
                    raise NotImplementedError
                self.DeleteTask(queue_name, task['name'])
        finally:
            self._is_executing = False

def _run_test_suite(runner, suite):
    """Run the test suite.

    Preserve the current development apiproxy, create a new apiproxy and
    replace the datastore with a temporary one that will be used for this
    test suite, run the test suite, and restore the development apiproxy.
    This isolates the test datastore from the development datastore.

    """
    original_apiproxy = apiproxy_stub_map.apiproxy
    try:
       apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
       apiproxy_stub_map.apiproxy.RegisterStub(
           'datastore',
           datastore_file_stub.DatastoreFileStub(
               'GAEUnitDataStore', datastore_file=None, trusted=True))
       apiproxy_stub_map.apiproxy.RegisterStub(
           'memcache',
           memcache_stub.MemcacheServiceStub())
       apiproxy_stub_map.apiproxy.RegisterStub(
           'taskqueue',
           TestingTaskQueueService(root_path='.'))
       # Allow the other services to be used as-is for tests.
       for name in ('user', 'urlfetch', 'mail', 'images'):
           apiproxy_stub_map.apiproxy.RegisterStub(
               name, original_apiproxy.GetStub(name))
       # TODO(slamm): add coverage tool here.
       runner.run(suite)
    finally:
       apiproxy_stub_map.apiproxy = original_apiproxy


def _log_error(s):
   logging.warn(s)
   return s


################################################
# Browser HTML, CSS, and Javascript
################################################


# This string uses Python string formatting, so be sure to escape percents as %%.
_MAIN_PAGE_CONTENT = """
<html>
<head>
    <style>
        body {font-family:arial,sans-serif}
        #title {font-family:"Times New Roman","Times Roman",TimesNR,times,serif; font-size:28px; font-weight:bold}
        #version {font-size:87%%}
        #weblink {font-style:italic; padding-top:7px; padding-bottom:7px}
        #results {padding-top:20px; margin:0pt; font-weight:bold;}
        #testindicator {width:750px; height:16px; border-style:solid; border-width:2px 1px 1px 2px; background-color:#f8f8f8;}
        #footerarea {font-size:83%%; padding-top:25px}
        #errorarea {padding-top:25px}
        .error {border-color: #c3d9ff; border-style: solid; border-width: 2px 1px 2px 1px; padding:1px; margin:0pt; text-align:left}
        .errtitle {background-color:#c3d9ff; font-weight:bold}
        pre {
        white-space: pre-wrap;       /* css-3 */
        white-space: -moz-pre-wrap;  /* Mozilla, since 1999 */
        white-space: -pre-wrap;      /* Opera 4-6 */
        white-space: -o-pre-wrap;    /* Opera 7 */
        word-wrap: break-word;       /* Internet Explorer 5.5+ */
        }
    </style>
    <script language="javascript" type="text/javascript">
        var testsToRun = %s;
        var totalRuns = 0;
        var totalErrors = 0;
        var totalFailures = 0;

        function newXmlHttp() {
          try { return new XMLHttpRequest(); } catch(e) {}
          try { return new ActiveXObject("Msxml2.XMLHTTP"); } catch (e) {}
          try { return new ActiveXObject("Microsoft.XMLHTTP"); } catch (e) {}
          alert("XMLHttpRequest not supported");
          return null;
        }

        function requestTestRun(moduleName, className, methodName) {
            var methodSuffix = "";
            if (methodName) {
                methodSuffix = "." + methodName;
            }
            var xmlHttp = newXmlHttp();
            xmlHttp.open("GET", "%s/run?name=" + moduleName + "." + className + methodSuffix, true);
            xmlHttp.onreadystatechange = function() {
                if (xmlHttp.readyState != 4) {
                    return;
                }
                if (xmlHttp.status == 200) {
                    var result = eval("(" + xmlHttp.responseText + ")");

                    totalRuns += parseInt(result.runs);
                    totalErrors += result.errors.length;
                    totalFailures += result.failures.length;
                    document.getElementById("testran").innerHTML = totalRuns;
                    document.getElementById("testerror").innerHTML = totalErrors;
                    document.getElementById("testfailure").innerHTML = totalFailures;
                    if (totalErrors == 0 && totalFailures == 0) {
                        testSucceed();
                    } else {
                        testFailed();
                    }
                    var error_groups = [['ERROR', result.errors],
                                        ['FAILURE', result.failures]];
                    var details = "";
                    for (var i=0; i < error_groups.length; i++) {
                        var label = error_groups[i][0];
                        var items = error_groups[i][1];
                        var module_url = '?' + 'name=' + moduleName;
                        var class_url = module_url + '.' + className;
                        var method_url = class_url + '.' + methodName;
                        for (var j=0; j < items.length; j++) {
                            details +=
                                '<p><div class="error"><div class="errtitle">' +
                                label +
                                '   <a href="' + module_url + '">' + moduleName + '</a>' +
                                ' . <a href="' + class_url + '">' + className + '</a>' +
                                ' . <a href="' + method_url + '">' + methodName + '</a>' +
                                items[j].short_description +
                                '</div><div class="errdetail"><pre>' +
                                items[j].traceback + '</pre></div></div></p>';
                        }
                    }
                    var errorArea = document.getElementById("errorarea");
                    errorArea.innerHTML += details;
                } else {
                    document.getElementById("errorarea").innerHTML = xmlHttp.responseText;
                    testFailed();
                }
            };
            xmlHttp.send(null);
        }

        function testFailed() {
            document.getElementById("testindicator").style.backgroundColor="red";
        }

        function testSucceed() {
            document.getElementById("testindicator").style.backgroundColor="green";
        }

        function runTests() {
            // Run each test asynchronously (concurrently).
            var totalTests = 0;
            for (var moduleName in testsToRun) {
                var classes = testsToRun[moduleName];
                for (var className in classes) {
                    // TODO: Optimize for the case where tests are run by class so we don't
                    //       have to always execute each method separately.  This should be
                    //       possible when we have a UI that allows the user to select tests
                    //       by module, class, and method.
                    //requestTestRun(moduleName, className);
                    methods = classes[className];
                    for (var i = 0; i < methods.length; i++) {
                        totalTests += 1;
                        var methodName = methods[i];
                        requestTestRun(moduleName, className, methodName);
                    }
                }
            }
            document.getElementById("testtotal").innerHTML = totalTests;
        }

    </script>
    <title>GAEUnit: Google App Engine Unit Test Framework</title>
</head>
<body onload="runTests()">
    <div id="headerarea">
        <div id="title">GAEUnit: Google App Engine Unit Test Framework</div>
        <div id="version">Version %s</div>
    </div>
    <div id="resultarea">
        <table id="results"><tbody>
            <tr><td colspan="3"><div id="testindicator"> </div></td</tr>
            <tr>
                <td>Runs: <span id="testran">0</span>/<span id="testtotal">0</span></td>
                <td>Errors: <span id="testerror">0</span></td>
                <td>Failures: <span id="testfailure">0</span></td>
            </tr>
        </tbody></table>
    </div>
    <div id="errorarea"></div>
    <div id="footerarea">
        <div id="weblink">
        <p>
            Please visit the <a href="http://code.google.com/p/gaeunit">project home page</a>
            for the latest version or to report problems.
        </p>
        <p>
            Copyright 2008-2009 <a href="mailto:George.Z.Lei@Gmail.com">George Lei</a>
            and <a href="mailto:srfarley@gmail.com">Steven R. Farley</a>
        </p>
        </div>
    </div>
</body>
</html>
"""


##############################################################################
# Script setup and execution
##############################################################################


application = webapp.WSGIApplication([('%s'      % _WEB_TEST_DIR, MainTestPageHandler),
                                      ('%s/run'  % _WEB_TEST_DIR, JsonTestRunHandler),
                                      ('%s/list' % _WEB_TEST_DIR, JsonTestListHandler)],
                                      debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
