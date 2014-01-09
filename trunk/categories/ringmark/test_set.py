#!/usr/bin/python2.4
#
# Copyright 20012 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License')
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Ringmark Tests Definitions."""

import logging

from categories import test_set_base
from models import user_test

_CATEGORY = 'ringmark'

# Ringmark's User Test record.
_USER_TEST_CATEGORY = 'usertest_agt1YS1wcm9maWxlcnINCxIEVGVzdBiS1dcRDA'

_TEST_URL = 'http://www.rng.io'


class RingmarkTest(test_set_base.TestBase):
    TESTS_URL_PATH = _TEST_URL
    CATEGORY = None


class CategoryRingmarkTest(RingmarkTest):
    def __init__(self, key, name, doc):
        """Initialze a test.

        Args:
            key: key for this in dict's
            name: a human readable label for display
            doc: a description of the test
        """
        # This way we can assign tests to a test group, i.e. apply, unapply, etc..
        test_set_base.TestBase.__init__(
            self,
            key=key,
            name=name,
            url=self.TESTS_URL_PATH,
            doc=doc,
            min_value=0,
            max_value=1,
            cell_align='center')


class IndividualRingmarkTest(RingmarkTest):
    def __init__(self, key):
        """Initialze a test.

        Args:
            key: key for this in dict's
            name: a human readable label for display
        """
        test_set_base.TestBase.__init__(
            self,
            key=key,
            name=key,
            url=self.TESTS_URL_PATH,
            doc=None,
            min_value=0,
            max_value=user_test.MAX_VALUE,
            is_hidden_stat=True)


class Ring0RingmarkTest(IndividualRingmarkTest):
    CATEGORY = 'ring:0'


class Ring1RingmarkTest(IndividualRingmarkTest):
    CATEGORY = 'ring:1'


class Ring2RingmarkTest(IndividualRingmarkTest):
    CATEGORY = 'ring:2'


CATEGORIES = sorted(['ring:0', 'ring:1', 'ring:2'])


_TESTS = [
    # key, name, doc
    CategoryRingmarkTest('ring:0', 'Ring 0', ''),
    CategoryRingmarkTest('ring:1', 'Ring 1', ''),
    CategoryRingmarkTest('ring:2', 'Ring 2', ''),
]

# Ring 0
for key in ['appcache',  'canvas', 'csscolor', 'csscolor-standard', 'cssbackground', 'css3dtransforms', 'css2-1selectors', 'cssminmax', 'cssanimation', 'csstext', 'csstransforms', 'csstransitions', 'cssui', 'cssvalues', 'dataurl', 'geolocation', 'viewport', 'doctype', 'json', 'postmessage', 'progress', 'prompts', 'selector', 'video', 'webstorage']:
    _TESTS.append(Ring0RingmarkTest(key))

# Ring 1
for key in ['audio-multi', 'blobbuilder', 'cssanimation-standard', 'cssmediaqueries', 'cssoverflow', 'cssoverflow-standard', 'cssbackground-standard', 'cssposition', 'csstransforms-standard', 'csstransitions-standard', 'cssui-standard', 'webworkers', 'deviceorientation', 'filesaver', 'filewriter', 'xhr2', 'hashchange', 'formdata', 'touchevents', 'forms', 'history', 'html-media-capture', 'indexeddb', 'indexeddb-standard', 'multitouch', 'offline', 'track', 'filereader', 'filesystem', 'network']:
    _TESTS.append(Ring1RingmarkTest(key))

# Ring 2
for key in ['animationtiming', 'canvas-3d', 'canvas-3d-standard', 'css-unspecified',  'cssimages', 'cssimages-standard', 'cssfont', 'cssflexbox', 'cssflexbox-standard', 'csscanvas', 'cssborderimage', 'dataset', 'fullscreen', 'html5', 'iframe', 'svg', 'svganimation', 'svginline', 'navigationtiming', 'sharedworkers', 'webrtc', 'notifications', 'vibration', 'masking', 'visibilitystate']:
    _TESTS.append(Ring2RingmarkTest(key))


class RingmarkTestSet(test_set_base.TestSet):
    def __init__(self):
        test_set_base.TestSet.__init__(
            self,
            category=_CATEGORY,
            category_name='Ringmark',
            summary_doc='Ringmark tests',
            tests=_TESTS,
            test_page=_TEST_URL)
        self.user_test_category = _USER_TEST_CATEGORY

    def GetTotalRunsForTestKey(self, test_key, num_scores):
        #logging.info('ringmark GetTestScoreAndDisplayValue %s, %s' %
        #             (test_key, num_scores))
        category_tests = self.GetTestsByCategory(test_key)
        total_runs = 0
        for category_test in category_tests:
                total_runs = max(total_runs, num_scores[category_test.key])
        return total_runs

    def GetTestScoreAndDisplayValue(self, test_key, raw_scores):
        """Get a normalized score (0 to 100) and a value to output to the display.

        Args:
            test_key: a key for a test_set test.
            raw_scores: a dict of raw_scores indexed by test keys.
        Returns:
            score, display_value
                    # score is from 0 to 100.
                    # display_value is the text for the cell.
        """
        category_tests = self.GetTestsByCategory(test_key)
        logging.info('GetTestScoreAndDisplayValue (ringmark) test_key: %s' %
                     test_key)
        num_tests = len(category_tests)
        if sorted(raw_scores.keys()) == CATEGORIES:
            display_score = int(raw_scores[test_key])
        else:
            display_score = 0
            for category_test in category_tests:
                raw_score = raw_scores.get(category_test.key)
                if raw_score is None:
                    # This could happen if we don't have any results for a new test.
                    num_tests -= 1
                else:
                    display_score += raw_score

        if num_tests <= 0:
            score = 0
            display = ''
        else:
            score = int(round(100.0 * display_score / num_tests))
            display = '%s/%s' % (display_score, num_tests)
        return score, display

    def GetTestsByCategory(self, category):
        logging.info('GetTestsByCategory %s', category)
        return [test for test in self.tests if test.CATEGORY == category]

    def GetRowScoreAndDisplayValue(self, results):
        """Get the overall score for this row of results data.

        Args:
            results: {
                    'test_key_1': {'score': score_1, 'raw_score': raw_score_1, ...},
                    'test_key_2': {'score': score_2, 'raw_score': raw_score_2, ...},
                    ...
                    }
        Returns:
            score, display_value
                    # score is from 0 to 100.
                    # display_value is the text for the cell.
        """
        logging.info('GetRowScoreAndDisplayValue ringmark: %s', results)
        total_passed = 0
        total_tests = 0
        for test_key, test_results in results.items():
            display = test_results['display']
            if display == '':
                # If we ever see display == '', we know we can just walk away.
                return 0, ''
            passed, total = display.split('/')
            total_passed += int(passed)
            total_tests += int(total)
        score = int(round(100.0 * total_passed / total_tests))
        display = '%s/%s' % (total_passed, total_tests)
        logging.info('score %s, display %s' % (score, display))
        return score, display


TEST_SET = RingmarkTestSet()
