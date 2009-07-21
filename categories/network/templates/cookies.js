
// Create a namespace.
var PERFICATURE = PERFICATURE || {};

PERFICATURE.getCookie = function(name) {
  name = ' ' + name + '=';
  var i, cookies;
  cookies = ' ' + document.cookie + ';';
  if ((i=cookies.indexOf(name)) >= 0) {
    i += name.length;
    cookies = cookies.substring(i, cookies.indexOf(';', i));
    return cookies;
  }
  return '';
}


// Get a subvalue within a cookie.
PERFICATURE.getSubCookie = function(name, subname) {
  // Prepend subname with '&' to avoid confusing "foo" and "afoo".
  subname = '&' + subname + '=';

  var i, subcookie;
  subcookie = PERFICATURE.getCookie(name);
  subcookie = '&' + subcookie + '&';
  if ((i=subcookie.indexOf(subname)) >= 0) {
    subcookie = subcookie.substring(
        i + subname.length, subcookie.indexOf('&', i + subname.length));
    return subcookie;
  }
  return '';
}


// Set a cookie.
PERFICATURE.setCookie = function(name, value, exp, path, domain, sec) {
  var nameval = name + '=' + value;
  var str = nameval +
      (exp ? '; expires=' + exp : '') +
      (path ? '; path=' + path : '') +
      (domain ? '; domain=' + domain : '') +
      (sec ? '; secure' : '');

  if (name.length > 0 && nameval.length < 4000) {
    document.cookie = str;
    // Confirm it was set (could be blocked by user's settings, etc.)
    return value == PERFICATURE.getCookie(name);
  }
  return 0;
}


// Remove a cookie.
PERFICATURE.removeCookie = function(name, domain) {
  var exp = new Date(90, 1, 1);
  return PERFICATURE.setCookie(name, '', exp.toGMTString(), '/', domain);
}


PERFICATURE.saveResult = function(name, value) {
  var curValue = PERFICATURE.getCookie('RES');
  PERFICATURE.setCookie(
      'RES', curValue + (curValue ? '&' : '') + name + '=' + value);
}


PERFICATURE.startTest = function() {
  PERFICATURE.setCookie('RES', 'start=' + Number(new Date()));
}
