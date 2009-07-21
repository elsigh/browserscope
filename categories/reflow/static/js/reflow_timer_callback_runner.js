(function(){
  Beacon.SERVER = 'http://ua-profiler.appspot.com';
  Beacon.SERVER = 'http://localhost:8084';
  Beacon.ADDTL_PARAMS = '&csrf_override=elsigh';
  var t = new ReflowTimer(true);
  t.run();
})();
