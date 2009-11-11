var a, goog = goog || {};
goog.global = this;
goog.DEBUG = true;
goog.LOCALE = "en";
goog.evalWorksForGlobals_ = null;
goog.provide = function(name) {
  goog.exportPath_(name)
};
goog.exportPath_ = function(name, opt_object, opt_objectToExportTo) {
  var parts = name.split("."), cur = opt_objectToExportTo || goog.global;
  !(parts[0] in cur) && cur.execScript && cur.execScript("var " + parts[0]);
  for(var part;parts.length && (part = parts.shift());)if(!parts.length && goog.isDef(opt_object))cur[part] = opt_object;
  else cur = cur[part] ? cur[part] : (cur[part] = {})
};
goog.getObjectByName = function(name, opt_obj) {
  for(var parts = name.split("."), cur = opt_obj || goog.global, part;part = parts.shift();)if(cur[part])cur = cur[part];
  else return null;
  return cur
};
goog.globalize = function(obj, opt_global) {
  var global = opt_global || goog.global;
  for(var x in obj)global[x] = obj[x]
};
goog.addDependency = function() {
};
goog.require = function() {
};
goog.useStrictRequires = false;
goog.basePath = "";
goog.nullFunction = function() {
};
goog.identityFunction = function() {
  return arguments[0]
};
goog.abstractMethod = function() {
  throw Error("unimplemented abstract method");
};
goog.addSingletonGetter = function(ctor) {
  ctor.getInstance = function() {
    return ctor.instance_ || (ctor.instance_ = new ctor)
  }
};
goog.typeOf = function(value) {
  var s = typeof value;
  if(s == "object")if(value) {
    if(value instanceof Array || !(value instanceof Object) && Object.prototype.toString.call(value) == "[object Array]" || typeof value.length == "number" && typeof value.splice != "undefined" && typeof value.propertyIsEnumerable != "undefined" && !value.propertyIsEnumerable("splice"))return"array";
    if(!(value instanceof Object) && (Object.prototype.toString.call(value) == "[object Function]" || typeof value.call != "undefined" && typeof value.propertyIsEnumerable != "undefined" && !value.propertyIsEnumerable("call")))return"function"
  }else return"null";
  else if(s == "function" && typeof value.call == "undefined")return"object";
  return s
};
goog.propertyIsEnumerableCustom_ = function(object, propName) {
  if(propName in object)for(var key in object)if(key == propName && Object.prototype.hasOwnProperty.call(object, propName))return true;
  return false
};
goog.propertyIsEnumerable_ = function(object, propName) {
  return object instanceof Object ? Object.prototype.propertyIsEnumerable.call(object, propName) : goog.propertyIsEnumerableCustom_(object, propName)
};
goog.isDef = function(val) {
  return val !== undefined
};
goog.isNull = function(val) {
  return val === null
};
goog.isDefAndNotNull = function(val) {
  return val != null
};
goog.isArray = function(val) {
  return goog.typeOf(val) == "array"
};
goog.isArrayLike = function(val) {
  var type = goog.typeOf(val);
  return type == "array" || type == "object" && typeof val.length == "number"
};
goog.isDateLike = function(val) {
  return goog.isObject(val) && typeof val.getFullYear == "function"
};
goog.isString = function(val) {
  return typeof val == "string"
};
goog.isBoolean = function(val) {
  return typeof val == "boolean"
};
goog.isNumber = function(val) {
  return typeof val == "number"
};
goog.isFunction = function(val) {
  return goog.typeOf(val) == "function"
};
goog.isObject = function(val) {
  var type = goog.typeOf(val);
  return type == "object" || type == "array" || type == "function"
};
goog.getHashCode = function(obj) {
  if(obj.hasOwnProperty && obj.hasOwnProperty(goog.HASH_CODE_PROPERTY_))return obj[goog.HASH_CODE_PROPERTY_];
  obj[goog.HASH_CODE_PROPERTY_] || (obj[goog.HASH_CODE_PROPERTY_] = ++goog.hashCodeCounter_);
  return obj[goog.HASH_CODE_PROPERTY_]
};
goog.removeHashCode = function(obj) {
  "removeAttribute" in obj && obj.removeAttribute(goog.HASH_CODE_PROPERTY_);
  try {
    delete obj[goog.HASH_CODE_PROPERTY_]
  }catch(ex) {
  }
};
goog.HASH_CODE_PROPERTY_ = "closure_hashCode_" + Math.floor(Math.random() * 2147483648).toString(36);
goog.hashCodeCounter_ = 0;
goog.cloneObject = function(proto) {
  var type = goog.typeOf(proto);
  if(type == "object" || type == "array") {
    if(proto.clone)return proto.clone.call(proto);
    var clone = type == "array" ? [] : {};
    for(var key in proto)clone[key] = goog.cloneObject(proto[key]);
    return clone
  }return proto
};
goog.bind = function(fn, selfObj) {
  var context = selfObj || goog.global;
  if(arguments.length > 2) {
    var boundArgs = Array.prototype.slice.call(arguments, 2);
    return function() {
      var newArgs = Array.prototype.slice.call(arguments);
      Array.prototype.unshift.apply(newArgs, boundArgs);
      return fn.apply(context, newArgs)
    }
  }else return function() {
    return fn.apply(context, arguments)
  }
};
goog.partial = function(fn) {
  var args = Array.prototype.slice.call(arguments, 1);
  return function() {
    var newArgs = Array.prototype.slice.call(arguments);
    newArgs.unshift.apply(newArgs, args);
    return fn.apply(this, newArgs)
  }
};
goog.mixin = function(target, source) {
  for(var x in source)target[x] = source[x]
};
goog.now = Date.now || function() {
  return(new Date).getTime()
};
goog.globalEval = function(script) {
  if(goog.global.execScript)goog.global.execScript(script, "JavaScript");
  else if(goog.global.eval) {
    if(goog.evalWorksForGlobals_ == null) {
      goog.global.eval("var _et_ = 1;");
      if(typeof goog.global._et_ != "undefined") {
        delete goog.global._et_;
        goog.evalWorksForGlobals_ = true
      }else goog.evalWorksForGlobals_ = false
    }if(goog.evalWorksForGlobals_)goog.global.eval(script);
    else {
      var doc = goog.global.document, scriptElt = doc.createElement("script");
      scriptElt.type = "text/javascript";
      scriptElt.defer = false;
      scriptElt.appendChild(doc.createTextNode(script));
      doc.body.appendChild(scriptElt);
      doc.body.removeChild(scriptElt)
    }
  }else throw Error("goog.globalEval not available");
};
goog.typedef = true;
goog.getCssName = function(className, opt_modifier) {
  var cssName = className + (opt_modifier ? "-" + opt_modifier : "");
  return goog.cssNameMapping_ && cssName in goog.cssNameMapping_ ? goog.cssNameMapping_[cssName] : cssName
};
goog.setCssNameMapping = function(mapping) {
  goog.cssNameMapping_ = mapping
};
goog.getMsg = function(str, opt_values) {
  var values = opt_values || {};
  for(var key in values)str = str.replace(new RegExp("\\{\\$" + key + "\\}", "gi"), values[key]);
  return str
};
goog.exportSymbol = function(publicPath, object, opt_objectToExportTo) {
  goog.exportPath_(publicPath, object, opt_objectToExportTo)
};
goog.exportProperty = function(object, publicName, symbol) {
  object[publicName] = symbol
};
goog.inherits = function(childCtor, parentCtor) {
  function tempCtor() {
  }
  tempCtor.prototype = parentCtor.prototype;
  childCtor.superClass_ = parentCtor.prototype;
  childCtor.prototype = new tempCtor
};
goog.MODIFY_FUNCTION_PROTOTYPES = true;
if(goog.MODIFY_FUNCTION_PROTOTYPES) {
  Function.prototype.bind = function(selfObj) {
    if(arguments.length > 1) {
      var args = Array.prototype.slice.call(arguments, 1);
      args.unshift(this, selfObj);
      return goog.bind.apply(null, args)
    }else return goog.bind(this, selfObj)
  };
  Function.prototype.partial = function() {
    var args = Array.prototype.slice.call(arguments);
    args.unshift(this, null);
    return goog.bind.apply(null, args)
  };
  Function.prototype.inherits = function(parentCtor) {
    goog.inherits(this, parentCtor)
  };
  Function.prototype.mixin = function(source) {
    goog.mixin(this.prototype, source)
  }
};goog.array = {};
goog.array.ArrayLike = goog.typedef;
goog.array.peek = function(array) {
  return array[array.length - 1]
};
goog.array.indexOf = function(arr, obj, opt_fromIndex) {
  if(arr.indexOf)return arr.indexOf(obj, opt_fromIndex);
  if(Array.indexOf)return Array.indexOf(arr, obj, opt_fromIndex);
  for(var i = opt_fromIndex == null ? 0 : opt_fromIndex < 0 ? Math.max(0, arr.length + opt_fromIndex) : opt_fromIndex;i < arr.length;i++)if(i in arr && arr[i] === obj)return i;
  return-1
};
goog.array.lastIndexOf = function(arr, obj, opt_fromIndex) {
  var fromIndex = opt_fromIndex == null ? arr.length - 1 : opt_fromIndex;
  if(arr.lastIndexOf)return arr.lastIndexOf(obj, fromIndex);
  if(Array.lastIndexOf)return Array.lastIndexOf(arr, obj, fromIndex);
  if(fromIndex < 0)fromIndex = Math.max(0, arr.length + fromIndex);
  for(var i = fromIndex;i >= 0;i--)if(i in arr && arr[i] === obj)return i;
  return-1
};
goog.array.forEach = function(arr, f, opt_obj) {
  if(arr.forEach)arr.forEach(f, opt_obj);
  else if(Array.forEach)Array.forEach(arr, f, opt_obj);
  else for(var l = arr.length, arr2 = goog.isString(arr) ? arr.split("") : arr, i = 0;i < l;i++)i in arr2 && f.call(opt_obj, arr2[i], i, arr)
};
goog.array.forEachRight = function(arr, f, opt_obj) {
  for(var l = arr.length, arr2 = goog.isString(arr) ? arr.split("") : arr, i = l - 1;i >= 0;--i)i in arr2 && f.call(opt_obj, arr2[i], i, arr)
};
goog.array.filter = function(arr, f, opt_obj) {
  if(arr.filter)return arr.filter(f, opt_obj);
  if(Array.filter)return Array.filter(arr, f, opt_obj);
  for(var l = arr.length, res = [], resLength = 0, arr2 = goog.isString(arr) ? arr.split("") : arr, i = 0;i < l;i++)if(i in arr2) {
    var val = arr2[i];
    if(f.call(opt_obj, val, i, arr))res[resLength++] = val
  }return res
};
goog.array.map = function(arr, f, opt_obj) {
  if(arr.map)return arr.map(f, opt_obj);
  if(Array.map)return Array.map(arr, f, opt_obj);
  for(var l = arr.length, res = [], resLength = 0, arr2 = goog.isString(arr) ? arr.split("") : arr, i = 0;i < l;i++)if(i in arr2)res[resLength++] = f.call(opt_obj, arr2[i], i, arr);
  return res
};
goog.array.reduce = function(arr, f, val, opt_obj) {
  if(arr.reduce)return opt_obj ? arr.reduce(goog.bind(f, opt_obj), val) : arr.reduce(f, val);
  var rval = val;
  goog.array.forEach(arr, function(val, index) {
    rval = f.call(opt_obj, rval, val, index, arr)
  });
  return rval
};
goog.array.reduceRight = function(arr, f, val, opt_obj) {
  if(arr.reduceRight)return opt_obj ? arr.reduceRight(goog.bind(f, opt_obj), val) : arr.reduceRight(f, val);
  var rval = val;
  goog.array.forEachRight(arr, function(val, index) {
    rval = f.call(opt_obj, rval, val, index, arr)
  });
  return rval
};
goog.array.some = function(arr, f, opt_obj) {
  if(arr.some)return arr.some(f, opt_obj);
  if(Array.some)return Array.some(arr, f, opt_obj);
  for(var l = arr.length, arr2 = goog.isString(arr) ? arr.split("") : arr, i = 0;i < l;i++)if(i in arr2 && f.call(opt_obj, arr2[i], i, arr))return true;
  return false
};
goog.array.every = function(arr, f, opt_obj) {
  if(arr.every)return arr.every(f, opt_obj);
  if(Array.every)return Array.every(arr, f, opt_obj);
  for(var l = arr.length, arr2 = goog.isString(arr) ? arr.split("") : arr, i = 0;i < l;i++)if(i in arr2 && !f.call(opt_obj, arr2[i], i, arr))return false;
  return true
};
goog.array.find = function(arr, f, opt_obj) {
  var i = goog.array.findIndex(arr, f, opt_obj);
  return i < 0 ? null : goog.isString(arr) ? arr.charAt(i) : arr[i]
};
goog.array.findIndex = function(arr, f, opt_obj) {
  for(var l = arr.length, arr2 = goog.isString(arr) ? arr.split("") : arr, i = 0;i < l;i++)if(i in arr2 && f.call(opt_obj, arr2[i], i, arr))return i;
  return-1
};
goog.array.findRight = function(arr, f, opt_obj) {
  var i = goog.array.findIndexRight(arr, f, opt_obj);
  return i < 0 ? null : goog.isString(arr) ? arr.charAt(i) : arr[i]
};
goog.array.findIndexRight = function(arr, f, opt_obj) {
  for(var l = arr.length, arr2 = goog.isString(arr) ? arr.split("") : arr, i = l - 1;i >= 0;i--)if(i in arr2 && f.call(opt_obj, arr2[i], i, arr))return i;
  return-1
};
goog.array.contains = function(arr, obj) {
  if(arr.contains)return arr.contains(obj);
  return goog.array.indexOf(arr, obj) > -1
};
goog.array.isEmpty = function(arr) {
  return arr.length == 0
};
goog.array.clear = function(arr) {
  if(!goog.isArray(arr))for(var i = arr.length - 1;i >= 0;i--)delete arr[i];
  arr.length = 0
};
goog.array.insert = function(arr, obj) {
  goog.array.contains(arr, obj) || arr.push(obj)
};
goog.array.insertAt = function(arr, obj, opt_i) {
  goog.array.splice(arr, opt_i, 0, obj)
};
goog.array.insertArrayAt = function(arr, elementsToAdd, opt_i) {
  goog.partial(goog.array.splice, arr, opt_i, 0).apply(null, elementsToAdd)
};
goog.array.insertBefore = function(arr, obj, opt_obj2) {
  var i;
  arguments.length == 2 || (i = goog.array.indexOf(arr, opt_obj2)) == -1 ? arr.push(obj) : goog.array.insertAt(arr, obj, i)
};
goog.array.remove = function(arr, obj) {
  var i = goog.array.indexOf(arr, obj), rv;
  if(rv = i != -1)goog.array.removeAt(arr, i);
  return rv
};
goog.array.removeAt = function(arr, i) {
  return Array.prototype.splice.call(arr, i, 1).length == 1
};
goog.array.removeIf = function(arr, f, opt_obj) {
  var i = goog.array.findIndex(arr, f, opt_obj);
  if(i >= 0) {
    goog.array.removeAt(arr, i);
    return true
  }return false
};
goog.array.clone = function(arr) {
  if(goog.isArray(arr))return arr.concat();
  else {
    for(var rv = [], i = 0, len = arr.length;i < len;i++)rv[i] = arr[i];
    return rv
  }
};
goog.array.toArray = function(object) {
  if(goog.isArray(object))return object.concat();
  return goog.array.clone(object)
};
goog.array.extend = function(arr1) {
  for(var i = 1;i < arguments.length;i++) {
    var arr2 = arguments[i];
    if(goog.isArrayLike(arr2)) {
      arr2 = goog.array.toArray(arr2);
      arr1.push.apply(arr1, arr2)
    }else arr1.push(arr2)
  }
};
goog.array.splice = function(arr) {
  return Array.prototype.splice.apply(arr, goog.array.slice(arguments, 1))
};
goog.array.slice = function(arr, start, opt_end) {
  return arguments.length <= 2 ? Array.prototype.slice.call(arr, start) : Array.prototype.slice.call(arr, start, opt_end)
};
goog.array.removeDuplicates = function(arr, opt_rv) {
  for(var rv = opt_rv || arr, seen = {}, cursorInsert = 0, cursorRead = 0;cursorRead < arr.length;) {
    var current = arr[cursorRead++], hc = goog.isObject(current) ? goog.getHashCode(current) : current;
    if(!Object.prototype.hasOwnProperty.call(seen, hc)) {
      seen[hc] = true;
      rv[cursorInsert++] = current
    }
  }rv.length = cursorInsert
};
goog.array.binarySearch = function(arr, target, opt_compareFn) {
  for(var left = 0, right = arr.length - 1, compareFn = opt_compareFn || goog.array.defaultCompare;left <= right;) {
    var mid = left + right >> 1, compareResult = compareFn(target, arr[mid]);
    if(compareResult > 0)left = mid + 1;
    else if(compareResult < 0)right = mid - 1;
    else return mid
  }return-(left + 1)
};
goog.array.sort = function(arr, opt_compareFn) {
  Array.prototype.sort.call(arr, opt_compareFn || goog.array.defaultCompare)
};
goog.array.stableSort = function(arr, opt_compareFn) {
  for(var i = 0;i < arr.length;i++)arr[i] = {index:i, value:arr[i]};
  var valueCompareFn = opt_compareFn || goog.array.defaultCompare;
  function stableCompareFn(obj1, obj2) {
    return valueCompareFn(obj1.value, obj2.value) || obj1.index - obj2.index
  }
  goog.array.sort(arr, stableCompareFn);
  for(i = 0;i < arr.length;i++)arr[i] = arr[i].value
};
goog.array.sortObjectsByKey = function(arr, key, opt_compareFn) {
  var compare = opt_compareFn || goog.array.defaultCompare;
  goog.array.sort(arr, function(a, b) {
    return compare(a[key], b[key])
  })
};
goog.array.equals = function(arr1, arr2, opt_equalsFn) {
  if(!goog.isArrayLike(arr1) || !goog.isArrayLike(arr2) || arr1.length != arr2.length)return false;
  for(var l = arr1.length, equalsFn = opt_equalsFn || goog.array.defaultCompareEquality, i = 0;i < l;i++)if(!equalsFn(arr1[i], arr2[i]))return false;
  return true
};
goog.array.compare = function(arr1, arr2, opt_equalsFn) {
  return goog.array.equals(arr1, arr2, opt_equalsFn)
};
goog.array.defaultCompare = function(a, b) {
  return a > b ? 1 : a < b ? -1 : 0
};
goog.array.defaultCompareEquality = function(a, b) {
  return a === b
};
goog.array.binaryInsert = function(array, value, opt_compareFn) {
  var index = goog.array.binarySearch(array, value, opt_compareFn);
  if(index < 0) {
    goog.array.insertAt(array, value, -(index + 1));
    return true
  }return false
};
goog.array.binaryRemove = function(array, value, opt_compareFn) {
  var index = goog.array.binarySearch(array, value, opt_compareFn);
  return index >= 0 ? goog.array.removeAt(array, index) : false
};
goog.array.bucket = function(array, sorter) {
  for(var buckets = {}, i = 0;i < array.length;i++) {
    var value = array[i], key = sorter(value, i, array);
    if(goog.isDef(key))(buckets[key] || (buckets[key] = [])).push(value)
  }return buckets
};
goog.array.repeat = function(value, n) {
  for(var array = [], i = 0;i < n;i++)array[i] = value;
  return array
};
goog.array.flatten = function() {
  for(var result = [], i = 0;i < arguments.length;i++) {
    var element = arguments[i];
    goog.isArray(element) ? result.push.apply(result, goog.array.flatten.apply(null, element)) : result.push(element)
  }return result
};
goog.array.rotate = function(array, n) {
  if(array.length) {
    n %= array.length;
    if(n > 0)Array.prototype.unshift.apply(array, array.splice(-n, n));
    else n < 0 && Array.prototype.push.apply(array, array.splice(0, -n))
  }return array
};goog.debug = {};
goog.debug.errorHandlerWeakDep = {protectEntryPoint:function(fn) {
  return fn
}};goog.object = {};
goog.object.forEach = function(obj, f, opt_obj) {
  for(var key in obj)f.call(opt_obj, obj[key], key, obj)
};
goog.object.filter = function(obj, f, opt_obj) {
  var res = {};
  for(var key in obj)if(f.call(opt_obj, obj[key], key, obj))res[key] = obj[key];
  return res
};
goog.object.map = function(obj, f, opt_obj) {
  var res = {};
  for(var key in obj)res[key] = f.call(opt_obj, obj[key], key, obj);
  return res
};
goog.object.some = function(obj, f, opt_obj) {
  for(var key in obj)if(f.call(opt_obj, obj[key], key, obj))return true;
  return false
};
goog.object.every = function(obj, f, opt_obj) {
  for(var key in obj)if(!f.call(opt_obj, obj[key], key, obj))return false;
  return true
};
goog.object.getCount = function(obj) {
  var rv = 0;
  for(var key in obj)rv++;
  return rv
};
goog.object.getAnyKey = function(obj) {
  for(var key in obj)return key
};
goog.object.getAnyValue = function(obj) {
  for(var key in obj)return obj[key]
};
goog.object.contains = function(obj, val) {
  return goog.object.containsValue(obj, val)
};
goog.object.getValues = function(obj) {
  var res = [], i = 0;
  for(var key in obj)res[i++] = obj[key];
  return res
};
goog.object.getKeys = function(obj) {
  var res = [], i = 0;
  for(var key in obj)res[i++] = key;
  return res
};
goog.object.containsKey = function(obj, key) {
  return key in obj
};
goog.object.containsValue = function(obj, val) {
  for(var key in obj)if(obj[key] == val)return true;
  return false
};
goog.object.findKey = function(obj, f, opt_this) {
  for(var key in obj)if(f.call(opt_this, obj[key], key, obj))return key
};
goog.object.findValue = function(obj, f, opt_this) {
  var key = goog.object.findKey(obj, f, opt_this);
  return key && obj[key]
};
goog.object.isEmpty = function(obj) {
  for(var key in obj)return false;
  return true
};
goog.object.clear = function(obj) {
  for(var keys = goog.object.getKeys(obj), i = keys.length - 1;i >= 0;i--)goog.object.remove(obj, keys[i])
};
goog.object.remove = function(obj, key) {
  var rv;
  if(rv = key in obj)delete obj[key];
  return rv
};
goog.object.add = function(obj, key, val) {
  if(key in obj)throw Error('The object already contains the key "' + key + '"');goog.object.set(obj, key, val)
};
goog.object.get = function(obj, key, opt_val) {
  if(key in obj)return obj[key];
  return opt_val
};
goog.object.set = function(obj, key, value) {
  obj[key] = value
};
goog.object.setIfUndefined = function(obj, key, value) {
  return key in obj ? obj[key] : (obj[key] = value)
};
goog.object.clone = function(obj) {
  var res = {};
  for(var key in obj)res[key] = obj[key];
  return res
};
goog.object.transpose = function(obj) {
  var transposed = {};
  for(var key in obj)transposed[obj[key]] = key;
  return transposed
};
goog.object.PROTOTYPE_FIELDS_ = ["constructor", "hasOwnProperty", "isPrototypeOf", "propertyIsEnumerable", "toLocaleString", "toString", "valueOf"];
goog.object.extend = function(target) {
  for(var key, source, i = 1;i < arguments.length;i++) {
    source = arguments[i];
    for(key in source)target[key] = source[key];
    for(var j = 0;j < goog.object.PROTOTYPE_FIELDS_.length;j++) {
      key = goog.object.PROTOTYPE_FIELDS_[j];
      if(Object.prototype.hasOwnProperty.call(source, key))target[key] = source[key]
    }
  }
};
goog.object.create = function() {
  var argLength = arguments.length;
  if(argLength == 1 && goog.isArray(arguments[0]))return goog.object.create.apply(null, arguments[0]);
  if(argLength % 2)throw Error("Uneven number of arguments");for(var rv = {}, i = 0;i < argLength;i += 2)rv[arguments[i]] = arguments[i + 1];
  return rv
};
goog.object.createSet = function() {
  var argLength = arguments.length;
  if(argLength == 1 && goog.isArray(arguments[0]))return goog.object.createSet.apply(null, arguments[0]);
  for(var rv = {}, i = 0;i < argLength;i++)rv[arguments[i]] = true;
  return rv
};goog.string = {};
goog.string.Unicode = {NBSP:"\u00a0"};
goog.string.startsWith = function(str, prefix) {
  return str.indexOf(prefix) == 0
};
goog.string.endsWith = function(str, suffix) {
  var l = str.length - suffix.length;
  return l >= 0 && str.lastIndexOf(suffix, l) == l
};
goog.string.caseInsensitiveStartsWith = function(str, prefix) {
  return goog.string.caseInsensitiveCompare(prefix, str.substr(0, prefix.length)) == 0
};
goog.string.caseInsensitiveEndsWith = function(str, suffix) {
  return goog.string.caseInsensitiveCompare(suffix, str.substr(str.length - suffix.length, suffix.length)) == 0
};
goog.string.subs = function(str) {
  for(var i = 1;i < arguments.length;i++) {
    var replacement = String(arguments[i]).replace(/\$/g, "$$$$");
    str = str.replace(/\%s/, replacement)
  }return str
};
goog.string.collapseWhitespace = function(str) {
  return str.replace(/[\s\xa0]+/g, " ").replace(/^\s+|\s+$/g, "")
};
goog.string.isEmpty = function(str) {
  return/^[\s\xa0]*$/.test(str)
};
goog.string.isEmptySafe = function(str) {
  return goog.string.isEmpty(goog.string.makeSafe(str))
};
goog.string.isBreakingWhitespace = function(str) {
  return!/[^\t\n\r ]/.test(str)
};
goog.string.isAlpha = function(str) {
  return!/[^a-zA-Z]/.test(str)
};
goog.string.isNumeric = function(str) {
  return!/[^0-9]/.test(str)
};
goog.string.isAlphaNumeric = function(str) {
  return!/[^a-zA-Z0-9]/.test(str)
};
goog.string.isSpace = function(ch) {
  return ch == " "
};
goog.string.isUnicodeChar = function(ch) {
  return ch.length == 1 && ch >= " " && ch <= "~" || ch >= "\u0080" && ch <= "\ufffd"
};
goog.string.stripNewlines = function(str) {
  return str.replace(/(\r\n|\r|\n)+/g, " ")
};
goog.string.canonicalizeNewlines = function(str) {
  return str.replace(/(\r\n|\r|\n)/g, "\n")
};
goog.string.normalizeWhitespace = function(str) {
  return str.replace(/\xa0|\s/g, " ")
};
goog.string.normalizeSpaces = function(str) {
  return str.replace(/\xa0|[ \t]+/g, " ")
};
goog.string.trim = function(str) {
  return str.replace(/^[\s\xa0]+|[\s\xa0]+$/g, "")
};
goog.string.trimLeft = function(str) {
  return str.replace(/^[\s\xa0]+/, "")
};
goog.string.trimRight = function(str) {
  return str.replace(/[\s\xa0]+$/, "")
};
goog.string.caseInsensitiveCompare = function(str1, str2) {
  var test1 = String(str1).toLowerCase(), test2 = String(str2).toLowerCase();
  return test1 < test2 ? -1 : test1 == test2 ? 0 : 1
};
goog.string.numerateCompareRegExp_ = /(\.\d+)|(\d+)|(\D+)/g;
goog.string.numerateCompare = function(str1, str2) {
  if(str1 == str2)return 0;
  if(!str1)return-1;
  if(!str2)return 1;
  for(var tokens1 = str1.toLowerCase().match(goog.string.numerateCompareRegExp_), tokens2 = str2.toLowerCase().match(goog.string.numerateCompareRegExp_), count = Math.min(tokens1.length, tokens2.length), i = 0;i < count;i++) {
    var a = tokens1[i], b = tokens2[i];
    if(a != b) {
      var num1 = parseInt(a, 10);
      if(!isNaN(num1)) {
        var num2 = parseInt(b, 10);
        if(!isNaN(num2) && num1 - num2)return num1 - num2
      }return a < b ? -1 : 1
    }
  }if(tokens1.length != tokens2.length)return tokens1.length - tokens2.length;
  return str1 < str2 ? -1 : 1
};
goog.string.encodeUriRegExp_ = /^[a-zA-Z0-9\-_.!~*'()]*$/;
goog.string.urlEncode = function(str) {
  str = String(str);
  if(!goog.string.encodeUriRegExp_.test(str))return encodeURIComponent(str);
  return str
};
goog.string.urlDecode = function(str) {
  return decodeURIComponent(str.replace(/\+/g, " "))
};
goog.string.newLineToBr = function(str, opt_xml) {
  return str.replace(/(\r\n|\r|\n)/g, opt_xml ? "<br />" : "<br>")
};
goog.string.htmlEscape = function(str, opt_isLikelyToContainHtmlChars) {
  if(opt_isLikelyToContainHtmlChars)return str.replace(goog.string.amperRe_, "&amp;").replace(goog.string.ltRe_, "&lt;").replace(goog.string.gtRe_, "&gt;").replace(goog.string.quotRe_, "&quot;");
  else {
    if(!goog.string.allRe_.test(str))return str;
    if(str.indexOf("&") != -1)str = str.replace(goog.string.amperRe_, "&amp;");
    if(str.indexOf("<") != -1)str = str.replace(goog.string.ltRe_, "&lt;");
    if(str.indexOf(">") != -1)str = str.replace(goog.string.gtRe_, "&gt;");
    if(str.indexOf('"') != -1)str = str.replace(goog.string.quotRe_, "&quot;");
    return str
  }
};
goog.string.amperRe_ = /&/g;
goog.string.ltRe_ = /</g;
goog.string.gtRe_ = />/g;
goog.string.quotRe_ = /\"/g;
goog.string.allRe_ = /[&<>\"]/;
goog.string.unescapeEntities = function(str) {
  if(goog.string.contains(str, "&"))return"document" in goog.global && !goog.string.contains(str, "<") ? goog.string.unescapeEntitiesUsingDom_(str) : goog.string.unescapePureXmlEntities_(str);
  return str
};
goog.string.unescapeEntitiesUsingDom_ = function(str) {
  var el = goog.global.document.createElement("a");
  el.innerHTML = str;
  el[goog.string.NORMALIZE_FN_] && el[goog.string.NORMALIZE_FN_]();
  str = el.firstChild.nodeValue;
  el.innerHTML = "";
  return str
};
goog.string.unescapePureXmlEntities_ = function(str) {
  return str.replace(/&([^;]+);/g, function(s, entity) {
    switch(entity) {
      case "amp":
        return"&";
      case "lt":
        return"<";
      case "gt":
        return">";
      case "quot":
        return'"';
      default:
        if(entity.charAt(0) == "#") {
          var n = Number("0" + entity.substr(1));
          if(!isNaN(n))return String.fromCharCode(n)
        }return s
    }
  })
};
goog.string.NORMALIZE_FN_ = "normalize";
goog.string.whitespaceEscape = function(str, opt_xml) {
  return goog.string.newLineToBr(str.replace(/  /g, " &#160;"), opt_xml)
};
goog.string.stripQuotes = function(str, quoteChars) {
  for(var length = quoteChars.length, i = 0;i < length;i++) {
    var quoteChar = length == 1 ? quoteChars : quoteChars.charAt(i);
    if(str.charAt(0) == quoteChar && str.charAt(str.length - 1) == quoteChar)return str.substring(1, str.length - 1)
  }return str
};
goog.string.truncate = function(str, chars, opt_protectEscapedCharacters) {
  if(opt_protectEscapedCharacters)str = goog.string.unescapeEntities(str);
  if(str.length > chars)str = str.substring(0, chars - 3) + "...";
  if(opt_protectEscapedCharacters)str = goog.string.htmlEscape(str);
  return str
};
goog.string.truncateMiddle = function(str, chars, opt_protectEscapedCharacters) {
  if(opt_protectEscapedCharacters)str = goog.string.unescapeEntities(str);
  if(str.length > chars) {
    var half = Math.floor(chars / 2), endPos = str.length - half;
    half += chars % 2;
    str = str.substring(0, half) + "..." + str.substring(endPos)
  }if(opt_protectEscapedCharacters)str = goog.string.htmlEscape(str);
  return str
};
goog.string.jsEscapeCache_ = {"\u0008":"\\b", "\u000c":"\\f", "\n":"\\n", "\r":"\\r", "\t":"\\t", "\u000b":"\\x0B", '"':'\\"', "'":"\\'", "\\":"\\\\"};
goog.string.quote = function(s) {
  s = String(s);
  if(s.quote)return s.quote();
  else {
    for(var sb = ['"'], i = 0;i < s.length;i++)sb[i + 1] = goog.string.escapeChar(s.charAt(i));
    sb.push('"');
    return sb.join("")
  }
};
goog.string.escapeChar = function(c) {
  if(c in goog.string.jsEscapeCache_)return goog.string.jsEscapeCache_[c];
  var rv = c, cc = c.charCodeAt(0);
  if(cc > 31 && cc < 127)rv = c;
  else {
    if(cc < 256) {
      rv = "\\x";
      if(cc < 16 || cc > 256)rv += "0"
    }else {
      rv = "\\u";
      if(cc < 4096)rv += "0"
    }rv += cc.toString(16).toUpperCase()
  }return goog.string.jsEscapeCache_[c] = rv
};
goog.string.toMap = function(s) {
  for(var rv = {}, i = 0;i < s.length;i++)rv[s.charAt(i)] = true;
  return rv
};
goog.string.contains = function(s, ss) {
  return s.indexOf(ss) != -1
};
goog.string.removeAt = function(s, index, stringLength) {
  var resultStr = s;
  if(index >= 0 && index < s.length && stringLength > 0)resultStr = s.substr(0, index) + s.substr(index + stringLength, s.length - index - stringLength);
  return resultStr
};
goog.string.remove = function(s, ss) {
  var re = new RegExp(goog.string.regExpEscape(ss), "");
  return s.replace(re, "")
};
goog.string.removeAll = function(s, ss) {
  var re = new RegExp(goog.string.regExpEscape(ss), "g");
  return s.replace(re, "")
};
goog.string.regExpEscape = function(s) {
  return String(s).replace(/([-()\[\]{}+?*.$\^|,:#<!\\])/g, "\\$1").replace(/\x08/g, "\\x08")
};
goog.string.repeat = function(string, length) {
  return(new Array(length + 1)).join(string)
};
goog.string.padNumber = function(num, length, opt_precision) {
  var s = goog.isDef(opt_precision) ? num.toFixed(opt_precision) : String(num), index = s.indexOf(".");
  if(index == -1)index = s.length;
  return goog.string.repeat("0", Math.max(0, length - index)) + s
};
goog.string.makeSafe = function(obj) {
  return obj == null ? "" : String(obj)
};
goog.string.buildString = function() {
  return Array.prototype.join.call(arguments, "")
};
goog.string.getRandomString = function() {
  return Math.floor(Math.random() * 2147483648).toString(36) + (Math.floor(Math.random() * 2147483648) ^ (new Date).getTime()).toString(36)
};
goog.string.compareVersions = function(version1, version2) {
  for(var order = 0, v1Subs = goog.string.trim(String(version1)).split("."), v2Subs = goog.string.trim(String(version2)).split("."), subCount = Math.max(v1Subs.length, v2Subs.length), subIdx = 0;order == 0 && subIdx < subCount;subIdx++) {
    var v1Sub = v1Subs[subIdx] || "", v2Sub = v2Subs[subIdx] || "", v1CompParser = new RegExp("(\\d*)(\\D*)", "g"), v2CompParser = new RegExp("(\\d*)(\\D*)", "g");
    do {
      var v1Comp = v1CompParser.exec(v1Sub) || ["", "", ""], v2Comp = v2CompParser.exec(v2Sub) || ["", "", ""];
      if(v1Comp[0].length == 0 && v2Comp[0].length == 0)break;
      var v1CompNum = v1Comp[1].length == 0 ? 0 : parseInt(v1Comp[1], 10), v2CompNum = v2Comp[1].length == 0 ? 0 : parseInt(v2Comp[1], 10);
      order = goog.string.compareElements_(v1CompNum, v2CompNum) || goog.string.compareElements_(v1Comp[2].length == 0, v2Comp[2].length == 0) || goog.string.compareElements_(v1Comp[2], v2Comp[2])
    }while(order == 0)
  }return order
};
goog.string.compareElements_ = function(left, right) {
  if(left < right)return-1;
  else if(left > right)return 1;
  return 0
};
goog.string.HASHCODE_MAX_ = 4294967296;
goog.string.hashCode = function(str) {
  for(var result = 0, i = 0;i < str.length;++i) {
    result = 31 * result + str.charCodeAt(i);
    result %= goog.string.HASHCODE_MAX_
  }return result
};
goog.string.uniqueStringCounter_ = goog.now();
goog.string.createUniqueString = function() {
  return"goog_" + goog.string.uniqueStringCounter_++
};
goog.string.toNumber = function(str) {
  var num = Number(str);
  if(num == 0 && goog.string.isEmpty(str))return NaN;
  return num
};goog.userAgent = {};
goog.userAgent.ASSUME_IE = false;
goog.userAgent.ASSUME_GECKO = false;
goog.userAgent.ASSUME_CAMINO = false;
goog.userAgent.ASSUME_WEBKIT = false;
goog.userAgent.ASSUME_MOBILE_WEBKIT = false;
goog.userAgent.ASSUME_OPERA = false;
goog.userAgent.BROWSER_KNOWN_ = goog.userAgent.ASSUME_IE || goog.userAgent.ASSUME_GECKO || goog.userAgent.ASSUME_CAMINO || goog.userAgent.ASSUME_MOBILE_WEBKIT || goog.userAgent.ASSUME_WEBKIT || goog.userAgent.ASSUME_OPERA;
goog.userAgent.getUserAgentString = function() {
  return goog.global.navigator ? goog.global.navigator.userAgent : null
};
goog.userAgent.getNavigator = function() {
  return goog.global.navigator
};
goog.userAgent.init_ = function() {
  goog.userAgent.detectedOpera_ = false;
  goog.userAgent.detectedIe_ = false;
  goog.userAgent.detectedWebkit_ = false;
  goog.userAgent.detectedMobile_ = false;
  goog.userAgent.detectedGecko_ = false;
  goog.userAgent.detectedCamino_ = false;
  var ua;
  if(!goog.userAgent.BROWSER_KNOWN_ && (ua = goog.userAgent.getUserAgentString())) {
    var navigator = goog.userAgent.getNavigator();
    goog.userAgent.detectedOpera_ = ua.indexOf("Opera") == 0;
    goog.userAgent.detectedIe_ = !goog.userAgent.detectedOpera_ && ua.indexOf("MSIE") != -1;
    goog.userAgent.detectedWebkit_ = !goog.userAgent.detectedOpera_ && ua.indexOf("WebKit") != -1;
    goog.userAgent.detectedMobile_ = goog.userAgent.detectedWebkit_ && ua.indexOf("Mobile") != -1;
    goog.userAgent.detectedGecko_ = !goog.userAgent.detectedOpera_ && !goog.userAgent.detectedWebkit_ && navigator.product == "Gecko";
    goog.userAgent.detectedCamino_ = goog.userAgent.detectedGecko_ && navigator.vendor == "Camino"
  }
};
goog.userAgent.BROWSER_KNOWN_ || goog.userAgent.init_();
goog.userAgent.OPERA = goog.userAgent.BROWSER_KNOWN_ ? goog.userAgent.ASSUME_OPERA : goog.userAgent.detectedOpera_;
goog.userAgent.IE = goog.userAgent.BROWSER_KNOWN_ ? goog.userAgent.ASSUME_IE : goog.userAgent.detectedIe_;
goog.userAgent.GECKO = goog.userAgent.BROWSER_KNOWN_ ? goog.userAgent.ASSUME_GECKO || goog.userAgent.ASSUME_CAMINO : goog.userAgent.detectedGecko_;
goog.userAgent.CAMINO = goog.userAgent.BROWSER_KNOWN_ ? goog.userAgent.ASSUME_CAMINO : goog.userAgent.detectedCamino_;
goog.userAgent.WEBKIT = goog.userAgent.BROWSER_KNOWN_ ? goog.userAgent.ASSUME_WEBKIT || goog.userAgent.ASSUME_MOBILE_WEBKIT : goog.userAgent.detectedWebkit_;
goog.userAgent.MOBILE = goog.userAgent.ASSUME_MOBILE_WEBKIT || goog.userAgent.detectedMobile_;
goog.userAgent.SAFARI = goog.userAgent.WEBKIT;
goog.userAgent.determinePlatform_ = function() {
  var navigator = goog.userAgent.getNavigator();
  return navigator && navigator.platform || ""
};
goog.userAgent.PLATFORM = goog.userAgent.determinePlatform_();
goog.userAgent.ASSUME_MAC = false;
goog.userAgent.ASSUME_WINDOWS = false;
goog.userAgent.ASSUME_LINUX = false;
goog.userAgent.ASSUME_X11 = false;
goog.userAgent.PLATFORM_KNOWN_ = goog.userAgent.ASSUME_MAC || goog.userAgent.ASSUME_WINDOWS || goog.userAgent.ASSUME_LINUX || goog.userAgent.ASSUME_X11;
goog.userAgent.initPlatform_ = function() {
  goog.userAgent.detectedMac_ = goog.string.contains(goog.userAgent.PLATFORM, "Mac");
  goog.userAgent.detectedWindows_ = goog.string.contains(goog.userAgent.PLATFORM, "Win");
  goog.userAgent.detectedLinux_ = goog.string.contains(goog.userAgent.PLATFORM, "Linux");
  goog.userAgent.detectedX11_ = !!goog.userAgent.getNavigator() && goog.string.contains(goog.userAgent.getNavigator().appVersion || "", "X11")
};
goog.userAgent.PLATFORM_KNOWN_ || goog.userAgent.initPlatform_();
goog.userAgent.MAC = goog.userAgent.PLATFORM_KNOWN_ ? goog.userAgent.ASSUME_MAC : goog.userAgent.detectedMac_;
goog.userAgent.WINDOWS = goog.userAgent.PLATFORM_KNOWN_ ? goog.userAgent.ASSUME_WINDOWS : goog.userAgent.detectedWindows_;
goog.userAgent.LINUX = goog.userAgent.PLATFORM_KNOWN_ ? goog.userAgent.ASSUME_LINUX : goog.userAgent.detectedLinux_;
goog.userAgent.X11 = goog.userAgent.PLATFORM_KNOWN_ ? goog.userAgent.ASSUME_X11 : goog.userAgent.detectedX11_;
goog.userAgent.determineVersion_ = function() {
  var version = "", re;
  if(goog.userAgent.OPERA && goog.global.opera) {
    var operaVersion = goog.global.opera.version;
    version = typeof operaVersion == "function" ? operaVersion() : operaVersion
  }else {
    if(goog.userAgent.GECKO)re = /rv\:([^\);]+)(\)|;)/;
    else if(goog.userAgent.IE)re = /MSIE\s+([^\);]+)(\)|;)/;
    else if(goog.userAgent.WEBKIT)re = /WebKit\/(\S+)/;
    if(re) {
      var arr = re.exec(goog.userAgent.getUserAgentString());
      version = arr ? arr[1] : ""
    }
  }return version
};
goog.userAgent.VERSION = goog.userAgent.determineVersion_();
goog.userAgent.compare = function(v1, v2) {
  return goog.string.compareVersions(v1, v2)
};
goog.userAgent.isVersionCache_ = {};
goog.userAgent.isVersion = function(version) {
  return goog.userAgent.isVersionCache_[version] || (goog.userAgent.isVersionCache_[version] = goog.string.compareVersions(goog.userAgent.VERSION, version) >= 0)
};goog.Disposable = function() {
};
goog.Disposable.prototype.disposed_ = false;
goog.Disposable.prototype.dispose = function() {
  if(!this.disposed_) {
    this.disposed_ = true;
    this.disposeInternal()
  }
};
goog.Disposable.prototype.disposeInternal = function() {
};
goog.dispose = function(obj) {
  obj && typeof obj.dispose == "function" && obj.dispose()
};goog.events = {};
goog.events.Event = function(type, opt_target) {
  goog.Disposable.call(this);
  this.type = type;
  this.currentTarget = this.target = opt_target
};
goog.inherits(goog.events.Event, goog.Disposable);
a = goog.events.Event.prototype;
a.disposeInternal = function() {
  delete this.type;
  delete this.target;
  delete this.currentTarget
};
a.propagationStopped_ = false;
a.returnValue_ = true;
a.stopPropagation = function() {
  this.propagationStopped_ = true
};
a.preventDefault = function() {
  this.returnValue_ = false
};goog.events.BrowserEvent = function(opt_e, opt_currentTarget) {
  opt_e && this.init(opt_e, opt_currentTarget)
};
goog.inherits(goog.events.BrowserEvent, goog.events.Event);
goog.events.BrowserEvent.MouseButton = {LEFT:0, MIDDLE:1, RIGHT:2};
goog.events.BrowserEvent.IEButtonMap_ = [1, 4, 2];
a = goog.events.BrowserEvent.prototype;
a.target = null;
a.relatedTarget = null;
a.offsetX = 0;
a.offsetY = 0;
a.clientX = 0;
a.clientY = 0;
a.screenX = 0;
a.screenY = 0;
a.button = 0;
a.keyCode = 0;
a.charCode = 0;
a.ctrlKey = false;
a.altKey = false;
a.shiftKey = false;
a.metaKey = false;
a.event_ = null;
a.init = function(e, opt_currentTarget) {
  var type = this.type = e.type;
  this.target = e.target || e.srcElement;
  this.currentTarget = opt_currentTarget;
  var relatedTarget = e.relatedTarget;
  if(relatedTarget) {
    if(goog.userAgent.GECKO)try {
      relatedTarget = relatedTarget.nodeName && relatedTarget
    }catch(err) {
    }
  }else if(type == "mouseover")relatedTarget = e.fromElement;
  else if(type == "mouseout")relatedTarget = e.toElement;
  this.relatedTarget = relatedTarget;
  this.offsetX = e.offsetX !== undefined ? e.offsetX : e.layerX;
  this.offsetY = e.offsetY !== undefined ? e.offsetY : e.layerY;
  this.clientX = e.clientX !== undefined ? e.clientX : e.pageX;
  this.clientY = e.clientY !== undefined ? e.clientY : e.pageY;
  this.screenX = e.screenX || 0;
  this.screenY = e.screenY || 0;
  this.button = e.button;
  this.keyCode = e.keyCode || 0;
  this.charCode = e.charCode || (type == "keypress" ? e.keyCode : 0);
  this.ctrlKey = e.ctrlKey;
  this.altKey = e.altKey;
  this.shiftKey = e.shiftKey;
  this.metaKey = e.metaKey;
  this.event_ = e;
  delete this.returnValue_;
  delete this.propagationStopped_
};
a.stopPropagation = function() {
  this.propagationStopped_ = true;
  if(this.event_.stopPropagation)this.event_.stopPropagation();
  else this.event_.cancelBubble = true
};
goog.events.BrowserEvent.IE7_SET_KEY_CODE_TO_PREVENT_DEFAULT_ = goog.userAgent.IE && !goog.userAgent.isVersion("8");
goog.events.BrowserEvent.prototype.preventDefault = function() {
  this.returnValue_ = false;
  var be = this.event_;
  if(be.preventDefault)be.preventDefault();
  else {
    be.returnValue = false;
    if(goog.events.BrowserEvent.IE7_SET_KEY_CODE_TO_PREVENT_DEFAULT_)try {
      if(be.ctrlKey || be.keyCode >= 112 && be.keyCode <= 123)be.keyCode = -1
    }catch(ex) {
    }
  }
};
goog.events.BrowserEvent.prototype.disposeInternal = function() {
  goog.events.BrowserEvent.superClass_.disposeInternal.call(this);
  this.relatedTarget = this.currentTarget = this.target = this.event_ = null
};goog.events.EventWrapper = function() {
};
goog.events.EventWrapper.prototype.listen = function() {
};
goog.events.EventWrapper.prototype.unlisten = function() {
};goog.structs = {};
goog.structs.SimplePool = function(initialCount, maxCount) {
  goog.Disposable.call(this);
  this.maxCount_ = maxCount;
  this.freeQueue_ = [];
  this.createInitial_(initialCount)
};
goog.inherits(goog.structs.SimplePool, goog.Disposable);
a = goog.structs.SimplePool.prototype;
a.createObjectFn_ = null;
a.disposeObjectFn_ = null;
a.setCreateObjectFn = function(createObjectFn) {
  this.createObjectFn_ = createObjectFn
};
a.getObject = function() {
  if(this.freeQueue_.length)return this.freeQueue_.pop();
  return this.createObject()
};
a.releaseObject = function(obj) {
  this.freeQueue_.length < this.maxCount_ ? this.freeQueue_.push(obj) : this.disposeObject(obj)
};
a.createInitial_ = function(initialCount) {
  if(initialCount > this.maxCount_)throw Error("[goog.structs.SimplePool] Initial cannot be greater than max");for(var i = 0;i < initialCount;i++)this.freeQueue_.push(this.createObject())
};
a.createObject = function() {
  return this.createObjectFn_ ? this.createObjectFn_() : {}
};
a.disposeObject = function(obj) {
  if(this.disposeObjectFn_)this.disposeObjectFn_(obj);
  else if(goog.isFunction(obj.dispose))obj.dispose();
  else for(var i in obj)delete obj[i]
};
a.disposeInternal = function() {
  goog.structs.SimplePool.superClass_.disposeInternal.call(this);
  for(var freeQueue = this.freeQueue_;freeQueue.length;)this.disposeObject(freeQueue.pop());
  delete this.freeQueue_
};goog.userAgent.jscript = {};
goog.userAgent.jscript.ASSUME_NO_JSCRIPT = false;
goog.userAgent.jscript.init_ = function() {
  goog.userAgent.jscript.DETECTED_HAS_JSCRIPT_ = "ScriptEngine" in goog.global && goog.global.ScriptEngine() == "JScript";
  goog.userAgent.jscript.DETECTED_VERSION_ = goog.userAgent.jscript.DETECTED_HAS_JSCRIPT_ ? goog.global.ScriptEngineMajorVersion() + "." + goog.global.ScriptEngineMinorVersion() + "." + goog.global.ScriptEngineBuildVersion() : "0"
};
goog.userAgent.jscript.ASSUME_NO_JSCRIPT || goog.userAgent.jscript.init_();
goog.userAgent.jscript.HAS_JSCRIPT = goog.userAgent.jscript.ASSUME_NO_JSCRIPT ? false : goog.userAgent.jscript.DETECTED_HAS_JSCRIPT_;
goog.userAgent.jscript.VERSION = goog.userAgent.jscript.ASSUME_NO_JSCRIPT ? "0" : goog.userAgent.jscript.DETECTED_VERSION_;
goog.userAgent.jscript.isVersion = function(version) {
  return goog.string.compareVersions(goog.userAgent.jscript.VERSION, version) >= 0
};goog.events.Listener = function() {
};
goog.events.Listener.counter_ = 0;
a = goog.events.Listener.prototype;
a.key = 0;
a.removed = false;
a.callOnce = false;
a.init = function(listener, proxy, src, type, capture, opt_handler) {
  if(goog.isFunction(listener))this.isFunctionListener_ = true;
  else if(listener && listener.handleEvent && goog.isFunction(listener.handleEvent))this.isFunctionListener_ = false;
  else throw Error("Invalid listener argument");this.listener = listener;
  this.proxy = proxy;
  this.src = src;
  this.type = type;
  this.capture = !!capture;
  this.handler = opt_handler;
  this.callOnce = false;
  this.key = ++goog.events.Listener.counter_;
  this.removed = false
};
a.handleEvent = function(eventObject) {
  if(this.isFunctionListener_)return this.listener.call(this.handler || this.src, eventObject);
  return this.listener.handleEvent.call(this.listener, eventObject)
};goog.events.pools = {};
(function() {
  var BAD_GC = goog.userAgent.jscript.HAS_JSCRIPT && !goog.userAgent.jscript.isVersion("5.7");
  function getObject() {
    return{count_:0, remaining_:0}
  }
  function getArray() {
    return[]
  }
  var proxyCallbackFunction;
  goog.events.pools.setProxyCallbackFunction = function(cb) {
    proxyCallbackFunction = cb
  };
  function getProxy() {
    var f = function(eventObject) {
      return proxyCallbackFunction.call(f.src, f.key, eventObject)
    };
    return f
  }
  function getListener() {
    return new goog.events.Listener
  }
  function getEvent() {
    return new goog.events.BrowserEvent
  }
  if(BAD_GC) {
    goog.events.pools.getObject = function() {
      return objectPool.getObject()
    };
    goog.events.pools.releaseObject = function(obj) {
      objectPool.releaseObject(obj)
    };
    goog.events.pools.getArray = function() {
      return arrayPool.getObject()
    };
    goog.events.pools.releaseArray = function(obj) {
      arrayPool.releaseObject(obj)
    };
    goog.events.pools.getProxy = function() {
      return proxyPool.getObject()
    };
    goog.events.pools.releaseProxy = function() {
      proxyPool.releaseObject(getProxy())
    };
    goog.events.pools.getListener = function() {
      return listenerPool.getObject()
    };
    goog.events.pools.releaseListener = function(obj) {
      listenerPool.releaseObject(obj)
    };
    goog.events.pools.getEvent = function() {
      return eventPool.getObject()
    };
    goog.events.pools.releaseEvent = function(obj) {
      eventPool.releaseObject(obj)
    };
    var objectPool = new goog.structs.SimplePool(0, 600);
    objectPool.setCreateObjectFn(getObject);
    var arrayPool = new goog.structs.SimplePool(0, 600);
    arrayPool.setCreateObjectFn(getArray);
    var proxyPool = new goog.structs.SimplePool(0, 600);
    proxyPool.setCreateObjectFn(getProxy);
    var listenerPool = new goog.structs.SimplePool(0, 600);
    listenerPool.setCreateObjectFn(getListener);
    var eventPool = new goog.structs.SimplePool(0, 600);
    eventPool.setCreateObjectFn(getEvent)
  }else {
    goog.events.pools.getObject = getObject;
    goog.events.pools.releaseObject = goog.nullFunction;
    goog.events.pools.getArray = getArray;
    goog.events.pools.releaseArray = goog.nullFunction;
    goog.events.pools.getProxy = getProxy;
    goog.events.pools.releaseProxy = goog.nullFunction;
    goog.events.pools.getListener = getListener;
    goog.events.pools.releaseListener = goog.nullFunction;
    goog.events.pools.getEvent = getEvent;
    goog.events.pools.releaseEvent = goog.nullFunction
  }
})();goog.events.listeners_ = {};
goog.events.listenerTree_ = {};
goog.events.sources_ = {};
goog.events.onString_ = "on";
goog.events.onStringMap_ = {};
goog.events.keySeparator_ = "_";
goog.events.listen = function(src, type, listener, opt_capt, opt_handler) {
  if(type)if(goog.isArray(type)) {
    for(var i = 0;i < type.length;i++)goog.events.listen(src, type[i], listener, opt_capt, opt_handler);
    return null
  }else {
    var capture = !!opt_capt, map = goog.events.listenerTree_;
    type in map || (map[type] = goog.events.pools.getObject());
    map = map[type];
    if(!(capture in map)) {
      map[capture] = goog.events.pools.getObject();
      map.count_++
    }map = map[capture];
    var srcHashCode = goog.getHashCode(src), listenerArray, listenerObj;
    map.remaining_++;
    if(map[srcHashCode]) {
      listenerArray = map[srcHashCode];
      for(i = 0;i < listenerArray.length;i++) {
        listenerObj = listenerArray[i];
        if(listenerObj.listener == listener && listenerObj.handler == opt_handler) {
          if(listenerObj.removed)break;
          return listenerArray[i].key
        }
      }
    }else {
      listenerArray = map[srcHashCode] = goog.events.pools.getArray();
      map.count_++
    }var proxy = goog.events.pools.getProxy();
    proxy.src = src;
    listenerObj = goog.events.pools.getListener();
    listenerObj.init(listener, proxy, src, type, capture, opt_handler);
    var key = listenerObj.key;
    proxy.key = key;
    listenerArray.push(listenerObj);
    goog.events.listeners_[key] = listenerObj;
    goog.events.sources_[srcHashCode] || (goog.events.sources_[srcHashCode] = goog.events.pools.getArray());
    goog.events.sources_[srcHashCode].push(listenerObj);
    if(src.addEventListener) {
      if(src == goog.global || !src.customEvent_)src.addEventListener(type, proxy, capture)
    }else src.attachEvent(goog.events.getOnString_(type), proxy);
    return key
  }else throw Error("Invalid event type");
};
goog.events.listenOnce = function(src, type, listener, opt_capt, opt_handler) {
  if(goog.isArray(type)) {
    for(var i = 0;i < type.length;i++)goog.events.listenOnce(src, type[i], listener, opt_capt, opt_handler);
    return null
  }var key = goog.events.listen(src, type, listener, opt_capt, opt_handler);
  goog.events.listeners_[key].callOnce = true;
  return key
};
goog.events.listenWithWrapper = function(src, wrapper, listener, opt_capt, opt_handler) {
  wrapper.listen(src, listener, opt_capt, opt_handler)
};
goog.events.unlisten = function(src, type, listener, opt_capt, opt_handler) {
  if(goog.isArray(type)) {
    for(var i = 0;i < type.length;i++)goog.events.unlisten(src, type[i], listener, opt_capt, opt_handler);
    return null
  }var capture = !!opt_capt, listenerArray = goog.events.getListeners_(src, type, capture);
  if(!listenerArray)return false;
  for(i = 0;i < listenerArray.length;i++)if(listenerArray[i].listener == listener && listenerArray[i].capture == capture && listenerArray[i].handler == opt_handler)return goog.events.unlistenByKey(listenerArray[i].key);
  return false
};
goog.events.unlistenByKey = function(key) {
  if(!goog.events.listeners_[key])return false;
  var listener = goog.events.listeners_[key];
  if(listener.removed)return false;
  var src = listener.src, type = listener.type, proxy = listener.proxy, capture = listener.capture;
  if(src.removeEventListener) {
    if(src == goog.global || !src.customEvent_)src.removeEventListener(type, proxy, capture)
  }else src.detachEvent && src.detachEvent(goog.events.getOnString_(type), proxy);
  var srcHashCode = goog.getHashCode(src), listenerArray = goog.events.listenerTree_[type][capture][srcHashCode];
  if(goog.events.sources_[srcHashCode]) {
    var sourcesArray = goog.events.sources_[srcHashCode];
    goog.array.remove(sourcesArray, listener);
    sourcesArray.length == 0 && delete goog.events.sources_[srcHashCode]
  }listener.removed = true;
  listenerArray.needsCleanup_ = true;
  goog.events.cleanUp_(type, capture, srcHashCode, listenerArray);
  delete goog.events.listeners_[key];
  return true
};
goog.events.unlistenWithWrapper = function(src, wrapper, listener, opt_capt, opt_handler) {
  wrapper.unlisten(src, listener, opt_capt, opt_handler)
};
goog.events.cleanUp_ = function(type, capture, srcHashCode, listenerArray) {
  if(!listenerArray.locked_)if(listenerArray.needsCleanup_) {
    for(var oldIndex = 0, newIndex = 0;oldIndex < listenerArray.length;oldIndex++)if(listenerArray[oldIndex].removed) {
      var proxy = listenerArray[oldIndex].proxy;
      proxy.src = null;
      goog.events.pools.releaseProxy(proxy);
      goog.events.pools.releaseListener(listenerArray[oldIndex])
    }else {
      if(oldIndex != newIndex)listenerArray[newIndex] = listenerArray[oldIndex];
      newIndex++
    }listenerArray.length = newIndex;
    listenerArray.needsCleanup_ = false;
    if(newIndex == 0) {
      goog.events.pools.releaseArray(listenerArray);
      delete goog.events.listenerTree_[type][capture][srcHashCode];
      goog.events.listenerTree_[type][capture].count_--;
      if(goog.events.listenerTree_[type][capture].count_ == 0) {
        goog.events.pools.releaseObject(goog.events.listenerTree_[type][capture]);
        delete goog.events.listenerTree_[type][capture];
        goog.events.listenerTree_[type].count_--
      }if(goog.events.listenerTree_[type].count_ == 0) {
        goog.events.pools.releaseObject(goog.events.listenerTree_[type]);
        delete goog.events.listenerTree_[type]
      }
    }
  }
};
goog.events.removeAll = function(opt_obj, opt_type, opt_capt) {
  var count = 0, noObj = opt_obj == null, noType = opt_type == null, noCapt = opt_capt == null;
  opt_capt = !!opt_capt;
  if(noObj)goog.object.forEach(goog.events.sources_, function(listeners) {
    for(var i = listeners.length - 1;i >= 0;i--) {
      var listener = listeners[i];
      if((noType || opt_type == listener.type) && (noCapt || opt_capt == listener.capture)) {
        goog.events.unlistenByKey(listener.key);
        count++
      }
    }
  });
  else {
    var srcHashCode = goog.getHashCode(opt_obj);
    if(goog.events.sources_[srcHashCode])for(var sourcesArray = goog.events.sources_[srcHashCode], i = sourcesArray.length - 1;i >= 0;i--) {
      var listener = sourcesArray[i];
      if((noType || opt_type == listener.type) && (noCapt || opt_capt == listener.capture)) {
        goog.events.unlistenByKey(listener.key);
        count++
      }
    }
  }return count
};
goog.events.getListeners = function(obj, type, capture) {
  return goog.events.getListeners_(obj, type, capture) || []
};
goog.events.getListeners_ = function(obj, type, capture) {
  var map = goog.events.listenerTree_;
  if(type in map) {
    map = map[type];
    if(capture in map) {
      map = map[capture];
      var objHashCode = goog.getHashCode(obj);
      if(map[objHashCode])return map[objHashCode]
    }
  }return null
};
goog.events.getListener = function(src, type, listener, opt_capt, opt_handler) {
  var capture = !!opt_capt, listenerArray = goog.events.getListeners_(src, type, capture);
  if(listenerArray)for(var i = 0;i < listenerArray.length;i++)if(listenerArray[i].listener == listener && listenerArray[i].capture == capture && listenerArray[i].handler == opt_handler)return listenerArray[i];
  return null
};
goog.events.hasListener = function(obj, opt_type, opt_capture) {
  var objHashCode = goog.getHashCode(obj), listeners = goog.events.sources_[objHashCode];
  if(listeners) {
    var hasType = goog.isDef(opt_type), hasCapture = goog.isDef(opt_capture);
    if(hasType && hasCapture) {
      var map = goog.events.listenerTree_[opt_type];
      return!!map && !!map[opt_capture] && objHashCode in map[opt_capture]
    }else return hasType || hasCapture ? goog.array.some(listeners, function(listener) {
      return hasType && listener.type == opt_type || hasCapture && listener.capture == opt_capture
    }) : true
  }return false
};
goog.events.expose = function(e) {
  var str = [];
  for(var key in e)e[key] && e[key].id ? str.push(key + " = " + e[key] + " (" + e[key].id + ")") : str.push(key + " = " + e[key]);
  return str.join("\n")
};
goog.events.EventType = {CLICK:"click", DBLCLICK:"dblclick", MOUSEDOWN:"mousedown", MOUSEUP:"mouseup", MOUSEOVER:"mouseover", MOUSEOUT:"mouseout", MOUSEMOVE:"mousemove", SELECTSTART:"selectstart", KEYPRESS:"keypress", KEYDOWN:"keydown", KEYUP:"keyup", BLUR:"blur", FOCUS:"focus", DEACTIVATE:"deactivate", FOCUSIN:goog.userAgent.IE ? "focusin" : "DOMFocusIn", FOCUSOUT:goog.userAgent.IE ? "focusout" : "DOMFocusOut", CHANGE:"change", SELECT:"select", SUBMIT:"submit", CONTEXTMENU:"contextmenu", DRAGSTART:"dragstart", 
ERROR:"error", HASHCHANGE:"hashchange", HELP:"help", LOAD:"load", LOSECAPTURE:"losecapture", READYSTATECHANGE:"readystatechange", RESIZE:"resize", SCROLL:"scroll", UNLOAD:"unload"};
goog.events.getOnString_ = function(type) {
  if(type in goog.events.onStringMap_)return goog.events.onStringMap_[type];
  return goog.events.onStringMap_[type] = goog.events.onString_ + type
};
goog.events.fireListeners = function(obj, type, capture, eventObject) {
  var map = goog.events.listenerTree_;
  if(type in map) {
    map = map[type];
    if(capture in map)return goog.events.fireListeners_(map[capture], obj, type, capture, eventObject)
  }return true
};
goog.events.fireListeners_ = function(map, obj, type, capture, eventObject) {
  var retval = 1, objHashCode = goog.getHashCode(obj);
  if(map[objHashCode]) {
    map.remaining_--;
    var listenerArray = map[objHashCode];
    if(listenerArray.locked_)listenerArray.locked_++;
    else listenerArray.locked_ = 1;
    try {
      for(var length = listenerArray.length, i = 0;i < length;i++) {
        var listener = listenerArray[i];
        if(listener && !listener.removed)retval &= goog.events.fireListener(listener, eventObject) !== false
      }
    }finally {
      listenerArray.locked_--;
      goog.events.cleanUp_(type, capture, objHashCode, listenerArray)
    }
  }return Boolean(retval)
};
goog.events.fireListener = function(listener, eventObject) {
  var rv = listener.handleEvent(eventObject);
  listener.callOnce && goog.events.unlistenByKey(listener.key);
  return rv
};
goog.events.getTotalListenerCount = function() {
  return goog.object.getCount(goog.events.listeners_)
};
goog.events.dispatchEvent = function(src, e) {
  if(goog.isString(e))e = new goog.events.Event(e, src);
  else if(e instanceof goog.events.Event)e.target = e.target || src;
  else {
    var oldEvent = e;
    e = new goog.events.Event(e.type, src);
    goog.object.extend(e, oldEvent)
  }var rv = 1, ancestors, type = e.type, map = goog.events.listenerTree_;
  if(!(type in map))return true;
  map = map[type];
  var hasCapture = true in map, targetsMap;
  if(hasCapture) {
    ancestors = [];
    for(var parent = src;parent;parent = parent.getParentEventTarget())ancestors.push(parent);
    targetsMap = map[true];
    targetsMap.remaining_ = targetsMap.count_;
    for(var i = ancestors.length - 1;!e.propagationStopped_ && i >= 0 && targetsMap.remaining_;i--) {
      e.currentTarget = ancestors[i];
      rv &= goog.events.fireListeners_(targetsMap, ancestors[i], e.type, true, e) && e.returnValue_ != false
    }
  }if(false in map) {
    targetsMap = map[false];
    targetsMap.remaining_ = targetsMap.count_;
    if(hasCapture)for(i = 0;!e.propagationStopped_ && i < ancestors.length && targetsMap.remaining_;i++) {
      e.currentTarget = ancestors[i];
      rv &= goog.events.fireListeners_(targetsMap, ancestors[i], e.type, false, e) && e.returnValue_ != false
    }else for(var current = src;!e.propagationStopped_ && current && targetsMap.remaining_;current = current.getParentEventTarget()) {
      e.currentTarget = current;
      rv &= goog.events.fireListeners_(targetsMap, current, e.type, false, e) && e.returnValue_ != false
    }
  }return Boolean(rv)
};
goog.events.protectBrowserEventEntryPoint = function(errorHandler, opt_tracers) {
  goog.events.handleBrowserEvent_ = errorHandler.protectEntryPoint(goog.events.handleBrowserEvent_, opt_tracers);
  goog.events.pools.setProxyCallbackFunction(goog.events.handleBrowserEvent_)
};
goog.events.handleBrowserEvent_ = function(key, opt_evt) {
  if(!goog.events.listeners_[key])return true;
  var listener = goog.events.listeners_[key], type = listener.type, map = goog.events.listenerTree_;
  if(!(type in map))return true;
  map = map[type];
  var retval, targetsMap;
  if(goog.userAgent.IE) {
    var ieEvent = opt_evt || goog.getObjectByName("window.event"), hasCapture = true in map, hasBubble = false in map;
    if(hasCapture) {
      if(goog.events.isMarkedIeEvent_(ieEvent))return true;
      goog.events.markIeEvent_(ieEvent)
    }var evt = goog.events.pools.getEvent();
    evt.init(ieEvent, this);
    retval = true;
    try {
      if(hasCapture) {
        for(var ancestors = goog.events.pools.getArray(), parent = evt.currentTarget;parent;parent = parent.parentNode)ancestors.push(parent);
        targetsMap = map[true];
        targetsMap.remaining_ = targetsMap.count_;
        for(var i = ancestors.length - 1;!evt.propagationStopped_ && i >= 0 && targetsMap.remaining_;i--) {
          evt.currentTarget = ancestors[i];
          retval &= goog.events.fireListeners_(targetsMap, ancestors[i], type, true, evt)
        }if(hasBubble) {
          targetsMap = map[false];
          targetsMap.remaining_ = targetsMap.count_;
          for(i = 0;!evt.propagationStopped_ && i < ancestors.length && targetsMap.remaining_;i++) {
            evt.currentTarget = ancestors[i];
            retval &= goog.events.fireListeners_(targetsMap, ancestors[i], type, false, evt)
          }
        }
      }else retval = goog.events.fireListener(listener, evt)
    }finally {
      if(ancestors) {
        ancestors.length = 0;
        goog.events.pools.releaseArray(ancestors)
      }evt.dispose();
      goog.events.pools.releaseEvent(evt)
    }return retval
  }var be = new goog.events.BrowserEvent(opt_evt, this);
  try {
    retval = goog.events.fireListener(listener, be)
  }finally {
    be.dispose()
  }return retval
};
goog.events.pools.setProxyCallbackFunction(goog.events.handleBrowserEvent_);
goog.events.markIeEvent_ = function(e) {
  var useReturnValue = false;
  if(e.keyCode == 0)try {
    e.keyCode = -1;
    return
  }catch(ex) {
    useReturnValue = true
  }if(useReturnValue || e.returnValue == undefined)e.returnValue = true
};
goog.events.isMarkedIeEvent_ = function(e) {
  return e.keyCode < 0 || e.returnValue != undefined
};
goog.events.uniqueIdCounter_ = 0;
goog.events.getUniqueId = function(identifier) {
  return identifier + "_" + goog.events.uniqueIdCounter_++
};goog.iter = {};
goog.iter.Iterable = goog.typedef;
goog.iter.StopIteration = "StopIteration" in goog.global ? goog.global.StopIteration : Error("StopIteration");
goog.iter.Iterator = function() {
};
goog.iter.Iterator.prototype.next = function() {
  throw goog.iter.StopIteration;
};
goog.iter.Iterator.prototype.__iterator__ = function() {
  return this
};
goog.iter.toIterator = function(iterable) {
  if(iterable instanceof goog.iter.Iterator)return iterable;
  if(typeof iterable.__iterator__ == "function")return iterable.__iterator__(false);
  if(goog.isArrayLike(iterable)) {
    var i = 0, newIter = new goog.iter.Iterator;
    newIter.next = function() {
      for(;1;) {
        if(i >= iterable.length)throw goog.iter.StopIteration;if(i in iterable)return iterable[i++];
        else i++
      }
    };
    return newIter
  }throw Error("Not implemented");
};
goog.iter.forEach = function(iterable, f, opt_obj) {
  if(goog.isArrayLike(iterable))try {
    goog.array.forEach(iterable, f, opt_obj)
  }catch(ex) {
    if(ex !== goog.iter.StopIteration)throw ex;
  }else {
    iterable = goog.iter.toIterator(iterable);
    try {
      for(;1;)f.call(opt_obj, iterable.next(), undefined, iterable)
    }catch(ex$$4) {
      if(ex$$4 !== goog.iter.StopIteration)throw ex$$4;
    }
  }
};
goog.iter.filter = function(iterable, f, opt_obj) {
  iterable = goog.iter.toIterator(iterable);
  var newIter = new goog.iter.Iterator;
  newIter.next = function() {
    for(;1;) {
      var val = iterable.next();
      if(f.call(opt_obj, val, undefined, iterable))return val
    }
  };
  return newIter
};
goog.iter.range = function(startOrStop, opt_stop, opt_step) {
  var start = 0, stop = startOrStop, step = opt_step || 1;
  if(arguments.length > 1) {
    start = startOrStop;
    stop = opt_stop
  }if(step == 0)throw Error("Range step argument must not be zero");var newIter = new goog.iter.Iterator;
  newIter.next = function() {
    if(step > 0 && start >= stop || step < 0 && start <= stop)throw goog.iter.StopIteration;var rv = start;
    start += step;
    return rv
  };
  return newIter
};
goog.iter.join = function(iterable, deliminator) {
  return goog.iter.toArray(iterable).join(deliminator)
};
goog.iter.map = function(iterable, f, opt_obj) {
  iterable = goog.iter.toIterator(iterable);
  var newIter = new goog.iter.Iterator;
  newIter.next = function() {
    for(;1;) {
      var val = iterable.next();
      return f.call(opt_obj, val, undefined, iterable)
    }
  };
  return newIter
};
goog.iter.reduce = function(iterable, f, val, opt_obj) {
  var rval = val;
  goog.iter.forEach(iterable, function(val) {
    rval = f.call(opt_obj, rval, val)
  });
  return rval
};
goog.iter.some = function(iterable, f, opt_obj) {
  iterable = goog.iter.toIterator(iterable);
  try {
    for(;1;)if(f.call(opt_obj, iterable.next(), undefined, iterable))return true
  }catch(ex) {
    if(ex !== goog.iter.StopIteration)throw ex;
  }return false
};
goog.iter.every = function(iterable, f, opt_obj) {
  iterable = goog.iter.toIterator(iterable);
  try {
    for(;1;)if(!f.call(opt_obj, iterable.next(), undefined, iterable))return false
  }catch(ex) {
    if(ex !== goog.iter.StopIteration)throw ex;
  }return true
};
goog.iter.chain = function() {
  var args = arguments, length = args.length, i = 0, newIter = new goog.iter.Iterator;
  newIter.next = function() {
    try {
      if(i >= length)throw goog.iter.StopIteration;return goog.iter.toIterator(args[i]).next()
    }catch(ex) {
      if(ex !== goog.iter.StopIteration || i >= length)throw ex;else {
        i++;
        return this.next()
      }
    }
  };
  return newIter
};
goog.iter.dropWhile = function(iterable, f, opt_obj) {
  iterable = goog.iter.toIterator(iterable);
  var newIter = new goog.iter.Iterator, dropping = true;
  newIter.next = function() {
    for(;1;) {
      var val = iterable.next();
      if(!(dropping && f.call(opt_obj, val, undefined, iterable))) {
        dropping = false;
        return val
      }
    }
  };
  return newIter
};
goog.iter.takeWhile = function(iterable, f, opt_obj) {
  iterable = goog.iter.toIterator(iterable);
  var newIter = new goog.iter.Iterator, taking = true;
  newIter.next = function() {
    for(;1;)if(taking) {
      var val = iterable.next();
      if(f.call(opt_obj, val, undefined, iterable))return val;
      else taking = false
    }else throw goog.iter.StopIteration;
  };
  return newIter
};
goog.iter.toArray = function(iterable) {
  if(goog.isArrayLike(iterable))return goog.array.toArray(iterable);
  iterable = goog.iter.toIterator(iterable);
  var array = [];
  goog.iter.forEach(iterable, function(val) {
    array.push(val)
  });
  return array
};
goog.iter.equals = function(iterable1, iterable2) {
  iterable1 = goog.iter.toIterator(iterable1);
  iterable2 = goog.iter.toIterator(iterable2);
  var b1, b2;
  try {
    for(;1;) {
      b1 = b2 = false;
      var val1 = iterable1.next();
      b1 = true;
      var val2 = iterable2.next();
      b2 = true;
      if(val1 != val2)return false
    }
  }catch(ex) {
    if(ex !== goog.iter.StopIteration)throw ex;else {
      if(b1 && !b2)return false;
      if(!b2)try {
        iterable2.next();
        return false
      }catch(ex1) {
        if(ex1 !== goog.iter.StopIteration)throw ex1;return true
      }
    }
  }return false
};
goog.iter.nextOrValue = function(iterable, defaultValue) {
  try {
    return goog.iter.toIterator(iterable).next()
  }catch(e) {
    if(e != goog.iter.StopIteration)throw e;return defaultValue
  }
};goog.structs.getCount = function(col) {
  if(typeof col.getCount == "function")return col.getCount();
  if(goog.isArrayLike(col) || goog.isString(col))return col.length;
  return goog.object.getCount(col)
};
goog.structs.getValues = function(col) {
  if(typeof col.getValues == "function")return col.getValues();
  if(goog.isString(col))return col.split("");
  if(goog.isArrayLike(col)) {
    for(var rv = [], l = col.length, i = 0;i < l;i++)rv.push(col[i]);
    return rv
  }return goog.object.getValues(col)
};
goog.structs.getKeys = function(col) {
  if(typeof col.getKeys == "function")return col.getKeys();
  if(typeof col.getValues != "function") {
    if(goog.isArrayLike(col) || goog.isString(col)) {
      for(var rv = [], l = col.length, i = 0;i < l;i++)rv.push(i);
      return rv
    }return goog.object.getKeys(col)
  }
};
goog.structs.contains = function(col, val) {
  if(typeof col.contains == "function")return col.contains(val);
  if(typeof col.containsValue == "function")return col.containsValue(val);
  if(goog.isArrayLike(col) || goog.isString(col))return goog.array.contains(col, val);
  return goog.object.containsValue(col, val)
};
goog.structs.isEmpty = function(col) {
  if(typeof col.isEmpty == "function")return col.isEmpty();
  if(goog.isArrayLike(col) || goog.isString(col))return goog.array.isEmpty(col);
  return goog.object.isEmpty(col)
};
goog.structs.clear = function(col) {
  if(typeof col.clear == "function")col.clear();
  else goog.isArrayLike(col) ? goog.array.clear(col) : goog.object.clear(col)
};
goog.structs.forEach = function(col, f, opt_obj) {
  if(typeof col.forEach == "function")col.forEach(f, opt_obj);
  else if(goog.isArrayLike(col) || goog.isString(col))goog.array.forEach(col, f, opt_obj);
  else for(var keys = goog.structs.getKeys(col), values = goog.structs.getValues(col), l = values.length, i = 0;i < l;i++)f.call(opt_obj, values[i], keys && keys[i], col)
};
goog.structs.filter = function(col, f, opt_obj) {
  if(typeof col.filter == "function")return col.filter(f, opt_obj);
  if(goog.isArrayLike(col) || goog.isString(col))return goog.array.filter(col, f, opt_obj);
  var rv, keys = goog.structs.getKeys(col), values = goog.structs.getValues(col), l = values.length;
  if(keys) {
    rv = {};
    for(var i = 0;i < l;i++)if(f.call(opt_obj, values[i], keys[i], col))rv[keys[i]] = values[i]
  }else {
    rv = [];
    for(i = 0;i < l;i++)f.call(opt_obj, values[i], undefined, col) && rv.push(values[i])
  }return rv
};
goog.structs.map = function(col, f, opt_obj) {
  if(typeof col.map == "function")return col.map(f, opt_obj);
  if(goog.isArrayLike(col) || goog.isString(col))return goog.array.map(col, f, opt_obj);
  var rv, keys = goog.structs.getKeys(col), values = goog.structs.getValues(col), l = values.length;
  if(keys) {
    rv = {};
    for(var i = 0;i < l;i++)rv[keys[i]] = f.call(opt_obj, values[i], keys[i], col)
  }else {
    rv = [];
    for(i = 0;i < l;i++)rv[i] = f.call(opt_obj, values[i], undefined, col)
  }return rv
};
goog.structs.some = function(col, f, opt_obj) {
  if(typeof col.some == "function")return col.some(f, opt_obj);
  if(goog.isArrayLike(col) || goog.isString(col))return goog.array.some(col, f, opt_obj);
  for(var keys = goog.structs.getKeys(col), values = goog.structs.getValues(col), l = values.length, i = 0;i < l;i++)if(f.call(opt_obj, values[i], keys && keys[i], col))return true;
  return false
};
goog.structs.every = function(col, f, opt_obj) {
  if(typeof col.every == "function")return col.every(f, opt_obj);
  if(goog.isArrayLike(col) || goog.isString(col))return goog.array.every(col, f, opt_obj);
  for(var keys = goog.structs.getKeys(col), values = goog.structs.getValues(col), l = values.length, i = 0;i < l;i++)if(!f.call(opt_obj, values[i], keys && keys[i], col))return false;
  return true
};goog.structs.Map = function(opt_map) {
  this.map_ = {};
  this.keys_ = [];
  var argLength = arguments.length;
  if(argLength > 1) {
    if(argLength % 2)throw Error("Uneven number of arguments");for(var i = 0;i < argLength;i += 2)this.set(arguments[i], arguments[i + 1])
  }else opt_map && this.addAll(opt_map)
};
a = goog.structs.Map.prototype;
a.count_ = 0;
a.version_ = 0;
a.getCount = function() {
  return this.count_
};
a.getValues = function() {
  this.cleanupKeysArray_();
  for(var rv = [], i = 0;i < this.keys_.length;i++)rv.push(this.map_[this.keys_[i]]);
  return rv
};
a.getKeys = function() {
  this.cleanupKeysArray_();
  return this.keys_.concat()
};
a.containsKey = function(key) {
  return goog.structs.Map.hasKey_(this.map_, key)
};
a.containsValue = function(val) {
  for(var i = 0;i < this.keys_.length;i++) {
    var key = this.keys_[i];
    if(goog.structs.Map.hasKey_(this.map_, key) && this.map_[key] == val)return true
  }return false
};
a.equals = function(otherMap, opt_equalityFn) {
  if(this === otherMap)return true;
  if(this.count_ != otherMap.getCount())return false;
  var equalityFn = opt_equalityFn || goog.structs.Map.defaultEquals;
  this.cleanupKeysArray_();
  for(var key, i = 0;key = this.keys_[i];i++)if(!equalityFn(this.get(key), otherMap.get(key)))return false;
  return true
};
goog.structs.Map.defaultEquals = function(a, b) {
  return a === b
};
a = goog.structs.Map.prototype;
a.isEmpty = function() {
  return this.count_ == 0
};
a.clear = function() {
  this.map_ = {};
  this.version_ = this.count_ = this.keys_.length = 0
};
a.remove = function(key) {
  if(goog.structs.Map.hasKey_(this.map_, key)) {
    delete this.map_[key];
    this.count_--;
    this.version_++;
    this.keys_.length > 2 * this.count_ && this.cleanupKeysArray_();
    return true
  }return false
};
a.cleanupKeysArray_ = function() {
  if(this.count_ != this.keys_.length) {
    for(var srcIndex = 0, destIndex = 0;srcIndex < this.keys_.length;) {
      var key = this.keys_[srcIndex];
      if(goog.structs.Map.hasKey_(this.map_, key))this.keys_[destIndex++] = key;
      srcIndex++
    }this.keys_.length = destIndex
  }if(this.count_ != this.keys_.length) {
    var seen = {};
    for(destIndex = srcIndex = 0;srcIndex < this.keys_.length;) {
      key = this.keys_[srcIndex];
      if(!goog.structs.Map.hasKey_(seen, key)) {
        this.keys_[destIndex++] = key;
        seen[key] = 1
      }srcIndex++
    }this.keys_.length = destIndex
  }
};
a.get = function(key, opt_val) {
  if(goog.structs.Map.hasKey_(this.map_, key))return this.map_[key];
  return opt_val
};
a.set = function(key, value) {
  if(!goog.structs.Map.hasKey_(this.map_, key)) {
    this.count_++;
    this.keys_.push(key);
    this.version_++
  }this.map_[key] = value
};
a.addAll = function(map) {
  var keys, values;
  if(map instanceof goog.structs.Map) {
    keys = map.getKeys();
    values = map.getValues()
  }else {
    keys = goog.object.getKeys(map);
    values = goog.object.getValues(map)
  }for(var i = 0;i < keys.length;i++)this.set(keys[i], values[i])
};
a.clone = function() {
  return new goog.structs.Map(this)
};
a.transpose = function() {
  for(var transposed = new goog.structs.Map, i = 0;i < this.keys_.length;i++) {
    var key = this.keys_[i];
    transposed.set(this.map_[key], key)
  }return transposed
};
a.__iterator__ = function(opt_keys) {
  this.cleanupKeysArray_();
  var i = 0, keys = this.keys_, map = this.map_, version = this.version_, selfObj = this, newIter = new goog.iter.Iterator;
  newIter.next = function() {
    for(;1;) {
      if(version != selfObj.version_)throw Error("The map has changed since the iterator was created");if(i >= keys.length)throw goog.iter.StopIteration;var key = keys[i++];
      return opt_keys ? key : map[key]
    }
  };
  return newIter
};
goog.structs.Map.hasKey_ = function(obj, key) {
  return Object.prototype.hasOwnProperty.call(obj, key)
};
goog.structs.Map.getCount = function(map) {
  return goog.structs.getCount(map)
};
goog.structs.Map.getValues = function(map) {
  return goog.structs.getValues(map)
};
goog.structs.Map.getKeys = function(map) {
  if(typeof map.getKeys == "function")return map.getKeys();
  var rv = [];
  if(goog.isArrayLike(map))for(var i = 0;i < map.length;i++)rv.push(i);
  else return goog.object.getKeys(map);
  return rv
};
goog.structs.Map.containsKey = function(map, key) {
  if(typeof map.containsKey == "function")return map.containsKey(key);
  if(goog.isArrayLike(map))return Number(key) < map.length;
  return goog.object.containsKey(map, key)
};
goog.structs.Map.containsValue = function(map, val) {
  return goog.structs.contains(map, val)
};
goog.structs.Map.isEmpty = function(map) {
  return goog.structs.isEmpty(map)
};
goog.structs.Map.clear = function(map) {
  goog.structs.clear(map)
};
goog.structs.Map.remove = function(map, key) {
  if(typeof map.remove == "function")return map.remove(key);
  if(goog.isArrayLike(map))return goog.array.removeAt(map, Number(key));
  return goog.object.remove(map, key)
};
goog.structs.Map.add = function(map, key, val) {
  if(typeof map.add == "function")map.add(key, val);
  else if(goog.structs.Map.containsKey(map, key))throw Error('The collection already contains the key "' + key + '"');else goog.structs.Map.set(map, key, val)
};
goog.structs.Map.get = function(map, key, opt_val) {
  if(typeof map.get == "function")return map.get(key, opt_val);
  if(goog.structs.Map.containsKey(map, key))return map[key];
  return opt_val
};
goog.structs.Map.set = function(map, key, val) {
  if(typeof map.set == "function")map.set(key, val);
  else map[key] = val
};goog.structs.Set = function(opt_values) {
  this.map_ = new goog.structs.Map;
  opt_values && this.addAll(opt_values)
};
goog.structs.Set.getKey_ = function(val) {
  var type = typeof val;
  return type == "object" && val || type == "function" ? "o" + goog.getHashCode(val) : type.substr(0, 1) + val
};
a = goog.structs.Set.prototype;
a.getCount = function() {
  return this.map_.getCount()
};
a.add = function(obj) {
  this.map_.set(goog.structs.Set.getKey_(obj), obj)
};
a.addAll = function(set) {
  for(var values = goog.structs.getValues(set), l = values.length, i = 0;i < l;i++)this.add(values[i])
};
a.removeAll = function(set) {
  for(var values = goog.structs.getValues(set), l = values.length, i = 0;i < l;i++)this.remove(values[i])
};
a.remove = function(obj) {
  return this.map_.remove(goog.structs.Set.getKey_(obj))
};
a.clear = function() {
  this.map_.clear()
};
a.isEmpty = function() {
  return this.map_.isEmpty()
};
a.contains = function(obj) {
  return this.map_.containsKey(goog.structs.Set.getKey_(obj))
};
a.intersection = function(set) {
  for(var result = new goog.structs.Set, values = goog.structs.getValues(set), i = 0;i < values.length;i++) {
    var value = values[i];
    this.contains(value) && result.add(value)
  }return result
};
a.getValues = function() {
  return this.map_.getValues()
};
a.clone = function() {
  return new goog.structs.Set(this)
};
a.equals = function(col) {
  return this.getCount() == goog.structs.getCount(col) && this.isSubsetOf(col)
};
a.isSubsetOf = function(col) {
  var colCount = goog.structs.getCount(col);
  if(this.getCount() > colCount)return false;
  if(!(col instanceof goog.structs.Set) && colCount > 5)col = new goog.structs.Set(col);
  return goog.structs.every(this, function(value) {
    return goog.structs.contains(col, value)
  })
};
a.__iterator__ = function() {
  return this.map_.__iterator__(false)
};goog.debug.catchErrors = function(opt_logger, opt_cancel, opt_target) {
  var logger = opt_logger || goog.debug.LogManager.getRoot(), target = opt_target || goog.global, oldErrorHandler = target.onerror;
  target.onerror = function(message, url, line) {
    oldErrorHandler && oldErrorHandler(message, url, line);
    var file = String(url).split(/[\/\\]/).pop();
    goog.isFunction(logger) ? logger({message:message, fileName:file, line:line}) : logger.severe("Error: " + message + " (" + file + " @ Line: " + line + ")");
    return Boolean(opt_cancel)
  }
};
goog.debug.expose = function(obj, opt_showFn) {
  if(typeof obj == "undefined")return"undefined";
  if(obj == null)return"NULL";
  var str = [];
  for(var x in obj)if(!(!opt_showFn && goog.isFunction(obj[x]))) {
    var s = x + " = ";
    try {
      s += obj[x]
    }catch(e) {
      s += "*** " + e + " ***"
    }str.push(s)
  }return str.join("\n")
};
goog.debug.deepExpose = function(obj, opt_showFn) {
  var previous = new goog.structs.Set, str = [], helper = function(obj, space) {
    var nestspace = space + "  ", indentMultiline = function(str) {
      return str.replace(/\n/g, "\n" + space)
    };
    try {
      if(goog.isDef(obj))if(goog.isNull(obj))str.push("NULL");
      else if(goog.isString(obj))str.push('"' + indentMultiline(obj) + '"');
      else if(goog.isFunction(obj))str.push(indentMultiline(String(obj)));
      else if(goog.isObject(obj))if(previous.contains(obj))str.push("*** reference loop detected ***");
      else {
        previous.add(obj);
        str.push("{");
        for(var x in obj)if(!(!opt_showFn && goog.isFunction(obj[x]))) {
          str.push("\n");
          str.push(nestspace);
          str.push(x + " = ");
          helper(obj[x], nestspace)
        }str.push("\n" + space + "}")
      }else str.push(obj);
      else str.push("undefined")
    }catch(e) {
      str.push("*** " + e + " ***")
    }
  };
  helper(obj, "");
  return str.join("")
};
goog.debug.exposeArray = function(arr) {
  for(var str = [], i = 0;i < arr.length;i++)goog.isArray(arr[i]) ? str.push(goog.debug.exposeArray(arr[i])) : str.push(arr[i]);
  return"[ " + str.join(", ") + " ]"
};
goog.debug.exposeException = function(err, opt_fn) {
  try {
    var e = goog.debug.normalizeErrorObject(err);
    return"Message: " + goog.string.htmlEscape(e.message) + '\nUrl: <a href="view-source:' + e.fileName + '" target="_new">' + e.fileName + "</a>\nLine: " + e.lineNumber + "\n\nBrowser stack:\n" + goog.string.htmlEscape(e.stack + "-> ") + "[end]\n\nJS stack traversal:\n" + goog.string.htmlEscape(goog.debug.getStacktrace(opt_fn) + "-> ")
  }catch(e2) {
    return"Exception trying to expose exception! You win, we lose. " + e2
  }
};
goog.debug.normalizeErrorObject = function(err) {
  var href = goog.getObjectByName("window.location.href");
  return typeof err == "string" ? {message:err, name:"Unknown error", lineNumber:"Not available", fileName:href, stack:"Not available"} : !err.lineNumber || !err.fileName || !err.stack ? {message:err.message, name:err.name, lineNumber:err.lineNumber || err.line || "Not available", fileName:err.fileName || err.filename || err.sourceURL || href, stack:err.stack || "Not available"} : err
};
goog.debug.enhanceError = function(err, opt_message) {
  var error = typeof err == "string" ? Error(err) : err;
  if(!error.stack)error.stack = goog.debug.getStacktrace(arguments.callee.caller);
  if(opt_message) {
    for(var x = 0;error["message" + x];)++x;
    error["message" + x] = String(opt_message)
  }return error
};
goog.debug.getStacktraceSimple = function(opt_depth) {
  for(var sb = [], fn = arguments.callee.caller, depth = 0;fn && (!opt_depth || depth < opt_depth);) {
    sb.push(goog.debug.getFunctionName(fn));
    sb.push("()\n");
    try {
      fn = fn.caller
    }catch(e) {
      sb.push("[exception trying to get caller]\n");
      break
    }depth++;
    if(depth >= goog.debug.MAX_STACK_DEPTH) {
      sb.push("[...long stack...]");
      break
    }
  }opt_depth && depth >= opt_depth ? sb.push("[...reached max depth limit...]") : sb.push("[end]");
  return sb.join("")
};
goog.debug.MAX_STACK_DEPTH = 50;
goog.debug.getStacktrace = function(opt_fn) {
  return goog.debug.getStacktraceHelper_(opt_fn || arguments.callee.caller, [])
};
goog.debug.getStacktraceHelper_ = function(fn, visited) {
  var sb = [];
  if(goog.array.contains(visited, fn))sb.push("[...circular reference...]");
  else if(fn && visited.length < goog.debug.MAX_STACK_DEPTH) {
    sb.push(goog.debug.getFunctionName(fn) + "(");
    for(var args = fn.arguments, i = 0;i < args.length;i++) {
      i > 0 && sb.push(", ");
      var argDesc, arg = args[i];
      switch(typeof arg) {
        case "object":
          argDesc = arg ? "object" : "null";
          break;
        case "string":
          argDesc = arg;
          break;
        case "number":
          argDesc = String(arg);
          break;
        case "boolean":
          argDesc = arg ? "true" : "false";
          break;
        case "function":
          argDesc = (argDesc = goog.debug.getFunctionName(arg)) ? argDesc : "[fn]";
          break;
        case "undefined":
        ;
        default:
          argDesc = typeof arg;
          break
      }
      if(argDesc.length > 40)argDesc = argDesc.substr(0, 40) + "...";
      sb.push(argDesc)
    }visited.push(fn);
    sb.push(")\n");
    try {
      sb.push(goog.debug.getStacktraceHelper_(fn.caller, visited))
    }catch(e) {
      sb.push("[exception trying to get caller]\n")
    }
  }else fn ? sb.push("[...long stack...]") : sb.push("[end]");
  return sb.join("")
};
goog.debug.getFunctionName = function(fn) {
  var functionSource = String(fn);
  if(!goog.debug.fnNameCache_[functionSource]) {
    var matches = /function ([^\(]+)/.exec(functionSource);
    goog.debug.fnNameCache_[functionSource] = matches ? matches[1] : "[Anonymous]"
  }return goog.debug.fnNameCache_[functionSource]
};
goog.debug.getAnonFunctionName_ = function(fn, opt_obj, opt_prefix, opt_depth) {
  if(goog.getObjectByName("document.all"))return"";
  var obj = opt_obj || goog.global, prefix = opt_prefix || "", depth = opt_depth || 0;
  if(obj == fn)return prefix;
  for(var i in obj)if(!(i == "Packages" || i == "sun" || i == "netscape" || i == "java")) {
    if(obj[i] == fn)return prefix + i;
    if((typeof obj[i] == "function" || typeof obj[i] == "object") && obj[i] != goog.global && obj[i] != goog.getObjectByName("document") && obj.hasOwnProperty(i) && depth < 6) {
      var rv = goog.debug.getAnonFunctionName_(fn, obj[i], prefix + i + ".", depth + 1);
      if(rv)return rv
    }
  }return""
};
goog.debug.makeWhitespaceVisible = function(string) {
  return string.replace(/ /g, "[_]").replace(/\f/g, "[f]").replace(/\n/g, "[n]\n").replace(/\r/g, "[r]").replace(/\t/g, "[t]")
};
goog.debug.fnNameCache_ = {};goog.debug.LogRecord = function(level, msg, loggerName, opt_time, opt_sequenceNumber) {
  this.sequenceNumber_ = typeof opt_sequenceNumber == "number" ? opt_sequenceNumber : goog.debug.LogRecord.nextSequenceNumber_++;
  this.time_ = opt_time || goog.now();
  this.level_ = level;
  this.msg_ = msg;
  this.loggerName_ = loggerName
};
goog.debug.LogRecord.prototype.exception_ = null;
goog.debug.LogRecord.prototype.exceptionText_ = null;
goog.debug.LogRecord.nextSequenceNumber_ = 0;
goog.debug.LogRecord.prototype.setException = function(exception) {
  this.exception_ = exception
};
goog.debug.LogRecord.prototype.setExceptionText = function(text) {
  this.exceptionText_ = text
};
goog.debug.LogRecord.prototype.getLevel = function() {
  return this.level_
};
goog.debug.LogRecord.prototype.setLevel = function(level) {
  this.level_ = level
};goog.debug.Logger = function(name) {
  this.name_ = name;
  this.parent_ = null;
  this.children_ = {};
  this.handlers_ = []
};
goog.debug.Logger.prototype.level_ = null;
goog.debug.Logger.Level = function(name, value) {
  this.name = name;
  this.value = value
};
goog.debug.Logger.Level.prototype.toString = function() {
  return this.name
};
goog.debug.Logger.Level.OFF = new goog.debug.Logger.Level("OFF", Infinity);
goog.debug.Logger.Level.SHOUT = new goog.debug.Logger.Level("SHOUT", 1200);
goog.debug.Logger.Level.SEVERE = new goog.debug.Logger.Level("SEVERE", 1000);
goog.debug.Logger.Level.WARNING = new goog.debug.Logger.Level("WARNING", 900);
goog.debug.Logger.Level.INFO = new goog.debug.Logger.Level("INFO", 800);
goog.debug.Logger.Level.CONFIG = new goog.debug.Logger.Level("CONFIG", 700);
goog.debug.Logger.Level.FINE = new goog.debug.Logger.Level("FINE", 500);
goog.debug.Logger.Level.FINER = new goog.debug.Logger.Level("FINER", 400);
goog.debug.Logger.Level.FINEST = new goog.debug.Logger.Level("FINEST", 300);
goog.debug.Logger.Level.ALL = new goog.debug.Logger.Level("ALL", 0);
goog.debug.Logger.Level.PREDEFINED_LEVELS = [goog.debug.Logger.Level.OFF, goog.debug.Logger.Level.SHOUT, goog.debug.Logger.Level.SEVERE, goog.debug.Logger.Level.WARNING, goog.debug.Logger.Level.INFO, goog.debug.Logger.Level.CONFIG, goog.debug.Logger.Level.FINE, goog.debug.Logger.Level.FINER, goog.debug.Logger.Level.FINEST, goog.debug.Logger.Level.ALL];
goog.debug.Logger.Level.predefinedLevelsCache_ = null;
goog.debug.Logger.Level.createPredefinedLevelsCache_ = function() {
  goog.debug.Logger.Level.predefinedLevelsCache_ = {};
  for(var i = 0, level;level = goog.debug.Logger.Level.PREDEFINED_LEVELS[i];i++) {
    goog.debug.Logger.Level.predefinedLevelsCache_[level.value] = level;
    goog.debug.Logger.Level.predefinedLevelsCache_[level.name] = level
  }
};
goog.debug.Logger.Level.getPredefinedLevel = function(name) {
  goog.debug.Logger.Level.predefinedLevelsCache_ || goog.debug.Logger.Level.createPredefinedLevelsCache_();
  return goog.debug.Logger.Level.predefinedLevelsCache_[name] || null
};
goog.debug.Logger.Level.getPredefinedLevelByValue = function(value) {
  goog.debug.Logger.Level.predefinedLevelsCache_ || goog.debug.Logger.Level.createPredefinedLevelsCache_();
  if(value in goog.debug.Logger.Level.predefinedLevelsCache_)return goog.debug.Logger.Level.predefinedLevelsCache_[value];
  for(var i = 0;i < goog.debug.Logger.Level.PREDEFINED_LEVELS.length;++i) {
    var level = goog.debug.Logger.Level.PREDEFINED_LEVELS[i];
    if(level.value <= value)return level
  }return null
};
goog.debug.Logger.getLogger = function(name) {
  return goog.debug.LogManager.getLogger(name)
};
a = goog.debug.Logger.prototype;
a.getParent = function() {
  return this.parent_
};
a.setLevel = function(level) {
  this.level_ = level
};
a.getLevel = function() {
  return this.level_
};
a.isLoggable = function(level) {
  if(this.level_)return level.value >= this.level_.value;
  if(this.parent_)return this.parent_.isLoggable(level);
  return false
};
a.log = function(level, msg, opt_exception) {
  this.isLoggable(level) && this.logRecord(this.getLogRecord(level, msg, opt_exception))
};
a.getLogRecord = function(level, msg, opt_exception) {
  var logRecord = new goog.debug.LogRecord(level, String(msg), this.name_);
  if(opt_exception) {
    logRecord.setException(opt_exception);
    logRecord.setExceptionText(goog.debug.exposeException(opt_exception, arguments.callee.caller))
  }return logRecord
};
a.severe = function(msg, opt_exception) {
  this.log(goog.debug.Logger.Level.SEVERE, msg, opt_exception)
};
a.warning = function(msg, opt_exception) {
  this.log(goog.debug.Logger.Level.WARNING, msg, opt_exception)
};
a.fine = function(msg, opt_exception) {
  this.log(goog.debug.Logger.Level.FINE, msg, opt_exception)
};
a.finest = function(msg, opt_exception) {
  this.log(goog.debug.Logger.Level.FINEST, msg, opt_exception)
};
a.logRecord = function(logRecord) {
  if(this.isLoggable(logRecord.getLevel()))for(var target = this;target;) {
    target.callPublish_(logRecord);
    target = target.getParent()
  }
};
a.callPublish_ = function(logRecord) {
  for(var i = 0;i < this.handlers_.length;i++)this.handlers_[i](logRecord)
};
a.setParent_ = function(parent) {
  this.parent_ = parent
};
a.addChild_ = function(name, logger) {
  this.children_[name] = logger
};
goog.debug.LogManager = {};
goog.debug.LogManager.loggers_ = {};
goog.debug.LogManager.rootLogger_ = null;
goog.debug.LogManager.initialize = function() {
  if(!goog.debug.LogManager.rootLogger_) {
    goog.debug.LogManager.rootLogger_ = new goog.debug.Logger("");
    goog.debug.LogManager.loggers_[""] = goog.debug.LogManager.rootLogger_;
    goog.debug.LogManager.rootLogger_.setLevel(goog.debug.Logger.Level.CONFIG)
  }
};
goog.debug.LogManager.getLoggers = function() {
  return goog.debug.LogManager.loggers_
};
goog.debug.LogManager.getRoot = function() {
  goog.debug.LogManager.initialize();
  return goog.debug.LogManager.rootLogger_
};
goog.debug.LogManager.getLogger = function(name) {
  goog.debug.LogManager.initialize();
  return name in goog.debug.LogManager.loggers_ ? goog.debug.LogManager.loggers_[name] : goog.debug.LogManager.createLogger_(name)
};
goog.debug.LogManager.createLogger_ = function(name) {
  var logger = new goog.debug.Logger(name), parts = name.split("."), leafName = parts[parts.length - 1];
  parts.length -= 1;
  var parentName = parts.join("."), parentLogger = goog.debug.LogManager.getLogger(parentName);
  parentLogger.addChild_(leafName, logger);
  logger.setParent_(parentLogger);
  return goog.debug.LogManager.loggers_[name] = logger
};goog.events.EventTarget = function() {
  goog.Disposable.call(this)
};
goog.inherits(goog.events.EventTarget, goog.Disposable);
a = goog.events.EventTarget.prototype;
a.customEvent_ = true;
a.parentEventTarget_ = null;
a.getParentEventTarget = function() {
  return this.parentEventTarget_
};
a.setParentEventTarget = function(parent) {
  this.parentEventTarget_ = parent
};
a.addEventListener = function(type, handler, opt_capture, opt_handlerScope) {
  goog.events.listen(this, type, handler, opt_capture, opt_handlerScope)
};
a.removeEventListener = function(type, handler, opt_capture, opt_handlerScope) {
  goog.events.unlisten(this, type, handler, opt_capture, opt_handlerScope)
};
a.dispatchEvent = function(e) {
  return goog.events.dispatchEvent(this, e)
};
a.disposeInternal = function() {
  goog.events.EventTarget.superClass_.disposeInternal.call(this);
  goog.events.removeAll(this);
  this.parentEventTarget_ = null
};goog.json = {};
goog.json.isValid_ = function(s) {
  if(/^\s*$/.test(s))return false;
  return/^[\],:{}\s\u2028\u2029]*$/.test(s.replace(/\\["\\\/bfnrtu]/g, "@").replace(/"[^"\\\n\r\u2028\u2029\x00-\x08\x10-\x1f\x80-\x9f]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g, "]").replace(/(?:^|:|,)(?:[\s\u2028\u2029]*\[)+/g, ""))
};
goog.json.parse = function(s) {
  var o = String(s);
  if(goog.json.isValid_(o))try {
    return eval("(" + o + ")")
  }catch(ex) {
  }throw Error("Invalid JSON string: " + o);
};
goog.json.unsafeParse = function(s) {
  return eval("(" + s + ")")
};
goog.json.serialize = function(object) {
  return(new goog.json.Serializer).serialize(object)
};
goog.json.Serializer = function() {
};
goog.json.Serializer.prototype.serialize = function(object) {
  var sb = [];
  this.serialize_(object, sb);
  return sb.join("")
};
goog.json.Serializer.prototype.serialize_ = function(object, sb) {
  switch(typeof object) {
    case "string":
      this.serializeString_(object, sb);
      break;
    case "number":
      this.serializeNumber_(object, sb);
      break;
    case "boolean":
      sb.push(object);
      break;
    case "undefined":
      sb.push("null");
      break;
    case "object":
      if(object == null) {
        sb.push("null");
        break
      }if(goog.isArray(object)) {
        this.serializeArray_(object, sb);
        break
      }this.serializeObject_(object, sb);
      break;
    case "function":
      break;
    default:
      throw Error("Unknown type: " + typeof object);
  }
};
goog.json.Serializer.charToJsonCharCache_ = {'"':'\\"', "\\":"\\\\", "/":"\\/", "\u0008":"\\b", "\u000c":"\\f", "\n":"\\n", "\r":"\\r", "\t":"\\t", "\u000b":"\\u000b"};
goog.json.Serializer.charsToReplace_ = /\uffff/.test("\uffff") ? /[\\\"\x00-\x1f\x7f-\uffff]/g : /[\\\"\x00-\x1f\x7f-\xff]/g;
goog.json.Serializer.prototype.serializeString_ = function(s, sb) {
  sb.push('"', s.replace(goog.json.Serializer.charsToReplace_, function(c) {
    if(c in goog.json.Serializer.charToJsonCharCache_)return goog.json.Serializer.charToJsonCharCache_[c];
    var cc = c.charCodeAt(0), rv = "\\u";
    if(cc < 16)rv += "000";
    else if(cc < 256)rv += "00";
    else if(cc < 4096)rv += "0";
    return goog.json.Serializer.charToJsonCharCache_[c] = rv + cc.toString(16)
  }), '"')
};
goog.json.Serializer.prototype.serializeNumber_ = function(n, sb) {
  sb.push(isFinite(n) && !isNaN(n) ? n : "null")
};
goog.json.Serializer.prototype.serializeArray_ = function(arr, sb) {
  var l = arr.length;
  sb.push("[");
  for(var sep = "", i = 0;i < l;i++) {
    sb.push(sep);
    this.serialize_(arr[i], sb);
    sep = ","
  }sb.push("]")
};
goog.json.Serializer.prototype.serializeObject_ = function(obj, sb) {
  sb.push("{");
  var sep = "";
  for(var key in obj)if(obj.hasOwnProperty(key)) {
    var value = obj[key];
    if(typeof value != "function") {
      sb.push(sep);
      this.serializeString_(key, sb);
      sb.push(":");
      this.serialize_(value, sb);
      sep = ","
    }
  }sb.push("}")
};goog.Timer = function(opt_interval, opt_timerObject) {
  goog.events.EventTarget.call(this);
  this.interval_ = opt_interval || 1;
  this.timerObject_ = opt_timerObject || goog.Timer.defaultTimerObject;
  this.boundTick_ = goog.bind(this.tick_, this);
  this.last_ = goog.now()
};
goog.inherits(goog.Timer, goog.events.EventTarget);
goog.Timer.MAX_TIMEOUT_ = 2147483647;
goog.Timer.prototype.enabled = false;
goog.Timer.defaultTimerObject = goog.global.window;
goog.Timer.intervalScale = 0.8;
a = goog.Timer.prototype;
a.timer_ = null;
a.tick_ = function() {
  if(this.enabled) {
    var elapsed = goog.now() - this.last_;
    if(elapsed > 0 && elapsed < this.interval_ * goog.Timer.intervalScale)this.timer_ = this.timerObject_.setTimeout(this.boundTick_, this.interval_ - elapsed);
    else {
      this.dispatchTick_();
      if(this.enabled) {
        this.timer_ = this.timerObject_.setTimeout(this.boundTick_, this.interval_);
        this.last_ = goog.now()
      }
    }
  }
};
a.dispatchTick_ = function() {
  this.dispatchEvent(goog.Timer.TICK)
};
a.stop = function() {
  this.enabled = false;
  if(this.timer_) {
    this.timerObject_.clearTimeout(this.timer_);
    this.timer_ = null
  }
};
a.disposeInternal = function() {
  goog.Timer.superClass_.disposeInternal.call(this);
  this.stop();
  delete this.timerObject_
};
goog.Timer.TICK = "tick";
goog.Timer.callOnce = function(listener, opt_interval, opt_handler) {
  if(goog.isFunction(listener)) {
    if(opt_handler)listener = goog.bind(listener, opt_handler)
  }else if(listener && typeof listener.handleEvent == "function")listener = goog.bind(listener.handleEvent, listener);
  else throw Error("Invalid listener argument");return opt_interval > goog.Timer.MAX_TIMEOUT_ ? -1 : goog.Timer.defaultTimerObject.setTimeout(listener, opt_interval || 0)
};
goog.Timer.clear = function(timerId) {
  goog.Timer.defaultTimerObject.clearTimeout(timerId)
};goog.net = {};
goog.net.ErrorCode = {NO_ERROR:0, ACCESS_DENIED:1, FILE_NOT_FOUND:2, FF_SILENT_ERROR:3, CUSTOM_ERROR:4, EXCEPTION:5, HTTP_ERROR:6, ABORT:7, TIMEOUT:8, OFFLINE:9};
goog.net.ErrorCode.getDebugMessage = function(errorCode) {
  switch(errorCode) {
    case goog.net.ErrorCode.NO_ERROR:
      return"No Error";
    case goog.net.ErrorCode.ACCESS_DENIED:
      return"Access denied to content document";
    case goog.net.ErrorCode.FILE_NOT_FOUND:
      return"File not found";
    case goog.net.ErrorCode.FF_SILENT_ERROR:
      return"Firefox silently errored";
    case goog.net.ErrorCode.CUSTOM_ERROR:
      return"Application custom error";
    case goog.net.ErrorCode.EXCEPTION:
      return"An exception occurred";
    case goog.net.ErrorCode.HTTP_ERROR:
      return"Http response at 400 or 500 level";
    case goog.net.ErrorCode.ABORT:
      return"Request was aborted";
    case goog.net.ErrorCode.TIMEOUT:
      return"Request timed out";
    case goog.net.ErrorCode.OFFLINE:
      return"The resource is not available offline";
    default:
      return"Unrecognized error code"
  }
};goog.net.EventType = {COMPLETE:"complete", SUCCESS:"success", ERROR:"error", ABORT:"abort", READY:"ready", READY_STATE_CHANGE:"readystatechange", TIMEOUT:"timeout", INCREMENTAL_DATA:"incrementaldata"};goog.net.XhrMonitor_ = function() {
  if(goog.userAgent.GECKO) {
    this.contextsToXhr_ = {};
    this.xhrToContexts_ = {};
    this.stack_ = []
  }
};
goog.net.XhrMonitor_.getKey = function(obj) {
  return goog.isString(obj) ? obj : goog.isObject(obj) ? goog.getHashCode(obj) : ""
};
a = goog.net.XhrMonitor_.prototype;
a.logger_ = goog.debug.Logger.getLogger("goog.net.xhrMonitor");
a.pushContext = function(context) {
  if(goog.userAgent.GECKO) {
    var key = goog.net.XhrMonitor_.getKey(context);
    this.logger_.finest("Pushing context: " + context + " (" + key + ")");
    this.stack_.push(key)
  }
};
a.popContext = function() {
  if(goog.userAgent.GECKO) {
    var context = this.stack_.pop();
    this.logger_.finest("Popping context: " + context);
    this.updateDependentContexts_(context)
  }
};
a.markXhrOpen = function(xhr) {
  if(goog.userAgent.GECKO) {
    var hc = goog.getHashCode(xhr);
    this.logger_.fine("Opening XHR : " + hc);
    for(var i = 0;i < this.stack_.length;i++) {
      var context = this.stack_[i];
      this.addToMap_(this.contextsToXhr_, context, hc);
      this.addToMap_(this.xhrToContexts_, hc, context)
    }
  }
};
a.markXhrClosed = function(xhr) {
  if(goog.userAgent.GECKO) {
    var hc = goog.getHashCode(xhr);
    this.logger_.fine("Closing XHR : " + hc);
    delete this.xhrToContexts_[hc];
    for(var context in this.contextsToXhr_) {
      goog.array.remove(this.contextsToXhr_[context], hc);
      this.contextsToXhr_[context].length == 0 && delete this.contextsToXhr_[context]
    }
  }
};
a.updateDependentContexts_ = function(xhrHc) {
  var contexts = this.xhrToContexts_[xhrHc], xhrs = this.contextsToXhr_[xhrHc];
  if(contexts && xhrs) {
    this.logger_.finest("Updating dependent contexts");
    goog.array.forEach(contexts, function(context) {
      goog.array.forEach(xhrs, function(xhr) {
        this.addToMap_(this.contextsToXhr_, context, xhr);
        this.addToMap_(this.xhrToContexts_, xhr, context)
      }, this)
    }, this)
  }
};
a.addToMap_ = function(map, key, value) {
  map[key] || (map[key] = []);
  goog.array.contains(map[key], value) || map[key].push(value)
};
goog.net.xhrMonitor = new goog.net.XhrMonitor_;goog.net.XmlHttp = function() {
  return goog.net.XmlHttp.factory_()
};
goog.net.XmlHttp.getOptions = function() {
  return goog.net.XmlHttp.cachedOptions_ || (goog.net.XmlHttp.cachedOptions_ = goog.net.XmlHttp.optionsFactory_())
};
goog.net.XmlHttp.factory_ = null;
goog.net.XmlHttp.optionsFactory_ = null;
goog.net.XmlHttp.cachedOptions_ = null;
goog.net.XmlHttp.setFactory = function(factory, optionsFactory) {
  goog.net.XmlHttp.factory_ = factory;
  goog.net.XmlHttp.optionsFactory_ = optionsFactory;
  goog.net.XmlHttp.cachedOptions_ = null
};
goog.net.XmlHttp.defaultFactory_ = function() {
  var progId = goog.net.XmlHttp.getProgId_();
  return progId ? new ActiveXObject(progId) : new XMLHttpRequest
};
goog.net.XmlHttp.defaultOptionsFactory_ = function() {
  var options = {};
  if(goog.net.XmlHttp.getProgId_()) {
    options[goog.net.XmlHttp.OptionType.USE_NULL_FUNCTION] = true;
    options[goog.net.XmlHttp.OptionType.LOCAL_REQUEST_ERROR] = true
  }return options
};
goog.net.XmlHttp.setFactory(goog.net.XmlHttp.defaultFactory_, goog.net.XmlHttp.defaultOptionsFactory_);
goog.net.XmlHttp.OptionType = {USE_NULL_FUNCTION:0, LOCAL_REQUEST_ERROR:1};
goog.net.XmlHttp.ReadyState = {UNINITIALIZED:0, LOADING:1, LOADED:2, INTERACTIVE:3, COMPLETE:4};
goog.net.XmlHttp.ieProgId_ = null;
goog.net.XmlHttp.getProgId_ = function() {
  if(!goog.net.XmlHttp.ieProgId_ && typeof XMLHttpRequest == "undefined" && typeof ActiveXObject != "undefined") {
    for(var ACTIVE_X_IDENTS = ["MSXML2.XMLHTTP.6.0", "MSXML2.XMLHTTP.3.0", "MSXML2.XMLHTTP", "Microsoft.XMLHTTP"], i = 0;i < ACTIVE_X_IDENTS.length;i++) {
      var candidate = ACTIVE_X_IDENTS[i];
      try {
        new ActiveXObject(candidate);
        return goog.net.XmlHttp.ieProgId_ = candidate
      }catch(e) {
      }
    }throw Error("Could not create ActiveXObject. ActiveX might be disabled, or MSXML might not be installed");
  }return goog.net.XmlHttp.ieProgId_
};goog.net.XhrIo = function() {
  goog.events.EventTarget.call(this);
  this.headers = new goog.structs.Map
};
goog.inherits(goog.net.XhrIo, goog.events.EventTarget);
goog.net.XhrIo.prototype.logger_ = goog.debug.Logger.getLogger("goog.net.XhrIo");
goog.net.XhrIo.CONTENT_TYPE_HEADER = "Content-Type";
goog.net.XhrIo.FORM_CONTENT_TYPE = "application/x-www-form-urlencoded;charset=utf-8";
goog.net.XhrIo.sendInstances_ = [];
goog.net.XhrIo.send = function(url, opt_callback, opt_method, opt_content, opt_headers, opt_timeoutInterval) {
  var x = new goog.net.XhrIo;
  goog.net.XhrIo.sendInstances_.push(x);
  opt_callback && goog.events.listen(x, goog.net.EventType.COMPLETE, opt_callback);
  goog.events.listen(x, goog.net.EventType.READY, goog.partial(goog.net.XhrIo.cleanupSend_, x));
  opt_timeoutInterval && x.setTimeoutInterval(opt_timeoutInterval);
  x.send(url, opt_method, opt_content, opt_headers)
};
goog.net.XhrIo.cleanup = function() {
  for(var instances = goog.net.XhrIo.sendInstances_;instances.length;)instances.pop().dispose()
};
goog.net.XhrIo.protectEntryPoints = function(errorHandler, opt_tracers) {
  goog.net.XhrIo.prototype.onReadyStateChangeEntryPoint_ = errorHandler.protectEntryPoint(goog.net.XhrIo.prototype.onReadyStateChangeEntryPoint_, opt_tracers)
};
goog.net.XhrIo.cleanupSend_ = function(XhrIo) {
  XhrIo.dispose();
  goog.array.remove(goog.net.XhrIo.sendInstances_, XhrIo)
};
a = goog.net.XhrIo.prototype;
a.active_ = false;
a.xhr_ = null;
a.xhrOptions_ = null;
a.lastUri_ = "";
a.lastMethod_ = "";
a.lastErrorCode_ = goog.net.ErrorCode.NO_ERROR;
a.lastError_ = "";
a.errorDispatched_ = false;
a.inSend_ = false;
a.inOpen_ = false;
a.inAbort_ = false;
a.timeoutInterval_ = 0;
a.timeoutId_ = null;
a.setTimeoutInterval = function(ms) {
  this.timeoutInterval_ = Math.max(0, ms)
};
a.send = function(url, opt_method, opt_content, opt_headers) {
  if(this.active_)throw Error("[goog.net.XhrIo] Object is active with another request");var method = opt_method || "GET";
  this.lastUri_ = url;
  this.lastError_ = "";
  this.lastErrorCode_ = goog.net.ErrorCode.NO_ERROR;
  this.lastMethod_ = method;
  this.errorDispatched_ = false;
  this.active_ = true;
  this.xhr_ = new goog.net.XmlHttp;
  this.xhrOptions_ = goog.net.XmlHttp.getOptions();
  goog.net.xhrMonitor.markXhrOpen(this.xhr_);
  this.xhr_.onreadystatechange = goog.bind(this.onReadyStateChange_, this);
  try {
    this.logger_.fine(this.formatMsg_("Opening Xhr"));
    this.inOpen_ = true;
    this.xhr_.open(method, url, true);
    this.inOpen_ = false
  }catch(err) {
    this.logger_.fine(this.formatMsg_("Error opening Xhr: " + err.message));
    this.error_(goog.net.ErrorCode.EXCEPTION, err);
    return
  }var content = opt_content || "", headers = this.headers.clone();
  opt_headers && goog.structs.forEach(opt_headers, function(value, key) {
    headers.set(key, value)
  });
  method == "POST" && !headers.containsKey(goog.net.XhrIo.CONTENT_TYPE_HEADER) && headers.set(goog.net.XhrIo.CONTENT_TYPE_HEADER, goog.net.XhrIo.FORM_CONTENT_TYPE);
  goog.structs.forEach(headers, function(value, key) {
    this.xhr_.setRequestHeader(key, value)
  }, this);
  try {
    if(this.timeoutId_) {
      goog.Timer.defaultTimerObject.clearTimeout(this.timeoutId_);
      this.timeoutId_ = null
    }if(this.timeoutInterval_ > 0) {
      this.logger_.fine(this.formatMsg_("Will abort after " + this.timeoutInterval_ + "ms if incomplete"));
      this.timeoutId_ = goog.Timer.defaultTimerObject.setTimeout(goog.bind(this.timeout_, this), this.timeoutInterval_)
    }this.logger_.fine(this.formatMsg_("Sending request"));
    this.inSend_ = true;
    this.xhr_.send(content);
    this.inSend_ = false
  }catch(err$$5) {
    this.logger_.fine(this.formatMsg_("Send error: " + err$$5.message));
    this.error_(goog.net.ErrorCode.EXCEPTION, err$$5)
  }
};
a.dispatchEvent = function(e) {
  if(this.xhr_) {
    goog.net.xhrMonitor.pushContext(this.xhr_);
    try {
      return goog.net.XhrIo.superClass_.dispatchEvent.call(this, e)
    }finally {
      goog.net.xhrMonitor.popContext()
    }
  }else return goog.net.XhrIo.superClass_.dispatchEvent.call(this, e)
};
a.timeout_ = function() {
  if(typeof goog != "undefined")if(this.xhr_) {
    this.lastError_ = "Timed out after " + this.timeoutInterval_ + "ms, aborting";
    this.lastErrorCode_ = goog.net.ErrorCode.TIMEOUT;
    this.logger_.fine(this.formatMsg_(this.lastError_));
    this.dispatchEvent(goog.net.EventType.TIMEOUT);
    this.abort(goog.net.ErrorCode.TIMEOUT)
  }
};
a.error_ = function(errorCode, err) {
  this.active_ = false;
  if(this.xhr_) {
    this.inAbort_ = true;
    this.xhr_.abort();
    this.inAbort_ = false
  }this.lastError_ = err;
  this.lastErrorCode_ = errorCode;
  this.dispatchErrors_();
  this.cleanUpXhr_()
};
a.dispatchErrors_ = function() {
  if(!this.errorDispatched_) {
    this.errorDispatched_ = true;
    this.dispatchEvent(goog.net.EventType.COMPLETE);
    this.dispatchEvent(goog.net.EventType.ERROR)
  }
};
a.abort = function(opt_failureCode) {
  if(this.xhr_) {
    this.logger_.fine(this.formatMsg_("Aborting"));
    this.active_ = false;
    this.inAbort_ = true;
    this.xhr_.abort();
    this.inAbort_ = false;
    this.lastErrorCode_ = opt_failureCode || goog.net.ErrorCode.ABORT;
    this.dispatchEvent(goog.net.EventType.COMPLETE);
    this.dispatchEvent(goog.net.EventType.ABORT);
    this.cleanUpXhr_()
  }
};
a.disposeInternal = function() {
  if(this.xhr_) {
    if(this.active_) {
      this.active_ = false;
      this.inAbort_ = true;
      this.xhr_.abort();
      this.inAbort_ = false
    }this.cleanUpXhr_(true)
  }goog.net.XhrIo.superClass_.disposeInternal.call(this)
};
a.onReadyStateChange_ = function() {
  !this.inOpen_ && !this.inSend_ && !this.inAbort_ ? this.onReadyStateChangeEntryPoint_() : this.onReadyStateChangeHelper_()
};
a.onReadyStateChangeEntryPoint_ = function() {
  this.onReadyStateChangeHelper_()
};
a.onReadyStateChangeHelper_ = function() {
  if(this.active_)if(typeof goog != "undefined")if(this.xhrOptions_[goog.net.XmlHttp.OptionType.LOCAL_REQUEST_ERROR] && this.getReadyState() == goog.net.XmlHttp.ReadyState.COMPLETE && this.getStatus() == 2)this.logger_.fine(this.formatMsg_("Local request error detected and ignored"));
  else if(this.inSend_ && this.getReadyState() == goog.net.XmlHttp.ReadyState.COMPLETE)goog.Timer.defaultTimerObject.setTimeout(goog.bind(this.onReadyStateChange_, this), 0);
  else {
    this.dispatchEvent(goog.net.EventType.READY_STATE_CHANGE);
    if(this.isComplete()) {
      this.logger_.fine(this.formatMsg_("Request complete"));
      this.active_ = false;
      if(this.isSuccess()) {
        this.dispatchEvent(goog.net.EventType.COMPLETE);
        this.dispatchEvent(goog.net.EventType.SUCCESS)
      }else {
        this.lastErrorCode_ = goog.net.ErrorCode.HTTP_ERROR;
        this.lastError_ = this.getStatusText() + " [" + this.getStatus() + "]";
        this.dispatchErrors_()
      }this.cleanUpXhr_()
    }
  }
};
a.cleanUpXhr_ = function(opt_fromDispose) {
  if(this.xhr_) {
    this.xhr_.onreadystatechange = this.xhrOptions_[goog.net.XmlHttp.OptionType.USE_NULL_FUNCTION] ? goog.nullFunction : null;
    var xhr = this.xhr_;
    this.xhrOptions_ = this.xhr_ = null;
    if(this.timeoutId_) {
      goog.Timer.defaultTimerObject.clearTimeout(this.timeoutId_);
      this.timeoutId_ = null
    }if(!opt_fromDispose) {
      goog.net.xhrMonitor.pushContext(xhr);
      this.dispatchEvent(goog.net.EventType.READY);
      goog.net.xhrMonitor.popContext()
    }goog.net.xhrMonitor.markXhrClosed(xhr)
  }
};
a.isComplete = function() {
  return this.getReadyState() == goog.net.XmlHttp.ReadyState.COMPLETE
};
a.isSuccess = function() {
  switch(this.getStatus()) {
    case 0:
    ;
    case 200:
    ;
    case 204:
    ;
    case 304:
      return true;
    default:
      return false
  }
};
a.getReadyState = function() {
  return this.xhr_ ? this.xhr_.readyState : goog.net.XmlHttp.ReadyState.UNINITIALIZED
};
a.getStatus = function() {
  try {
    return this.getReadyState() > goog.net.XmlHttp.ReadyState.LOADED ? this.xhr_.status : -1
  }catch(e) {
    this.logger_.warning("Can not get status: " + e.message);
    return-1
  }
};
a.getStatusText = function() {
  try {
    return this.getReadyState() > goog.net.XmlHttp.ReadyState.LOADED ? this.xhr_.statusText : ""
  }catch(e) {
    this.logger_.fine("Can not get status: " + e.message);
    return""
  }
};
a.getResponseText = function() {
  return this.xhr_ ? this.xhr_.responseText : ""
};
a.formatMsg_ = function(msg) {
  return msg + " [" + this.lastMethod_ + " " + this.lastUri_ + " " + this.getStatus() + "]"
};goog.dom = {};
goog.dom.classes = {};
goog.dom.classes.set = function(element, className) {
  element.className = className
};
goog.dom.classes.get = function(element) {
  var className = element.className;
  return className && typeof className.split == "function" ? className.split(" ") : []
};
goog.dom.classes.add = function(element) {
  var classes = goog.dom.classes.get(element), args = goog.array.slice(arguments, 1), b = goog.dom.classes.add_(classes, args);
  element.className = classes.join(" ");
  return b
};
goog.dom.classes.remove = function(element) {
  var classes = goog.dom.classes.get(element), args = goog.array.slice(arguments, 1), b = goog.dom.classes.remove_(classes, args);
  element.className = classes.join(" ");
  return b
};
goog.dom.classes.add_ = function(classes, args) {
  for(var rv = 0, i = 0;i < args.length;i++)if(!goog.array.contains(classes, args[i])) {
    classes.push(args[i]);
    rv++
  }return rv == args.length
};
goog.dom.classes.remove_ = function(classes, args) {
  for(var rv = 0, i = 0;i < classes.length;i++)if(goog.array.contains(args, classes[i])) {
    goog.array.splice(classes, i--, 1);
    rv++
  }return rv == args.length
};
goog.dom.classes.swap = function(element, fromClass, toClass) {
  for(var classes = goog.dom.classes.get(element), removed = false, i = 0;i < classes.length;i++)if(classes[i] == fromClass) {
    goog.array.splice(classes, i--, 1);
    removed = true
  }if(removed) {
    classes.push(toClass);
    element.className = classes.join(" ")
  }return removed
};
goog.dom.classes.addRemove = function(element, classesToRemove, classesToAdd) {
  var classes = goog.dom.classes.get(element);
  if(goog.isString(classesToRemove))goog.array.remove(classes, classesToRemove);
  else goog.isArray(classesToRemove) && goog.dom.classes.remove_(classes, classesToRemove);
  if(goog.isString(classesToAdd) && !goog.array.contains(classes, classesToAdd))classes.push(classesToAdd);
  else goog.isArray(classesToAdd) && goog.dom.classes.add_(classes, classesToAdd);
  element.className = classes.join(" ")
};
goog.dom.classes.has = function(element, className) {
  return goog.array.contains(goog.dom.classes.get(element), className)
};
goog.dom.classes.enable = function(element, className, enabled) {
  enabled ? goog.dom.classes.add(element, className) : goog.dom.classes.remove(element, className)
};
goog.dom.classes.toggle = function(element, className) {
  var add = !goog.dom.classes.has(element, className);
  goog.dom.classes.enable(element, className, add);
  return add
};goog.math = {};
goog.math.Coordinate = function(opt_x, opt_y) {
  this.x = goog.isDef(opt_x) ? opt_x : 0;
  this.y = goog.isDef(opt_y) ? opt_y : 0
};
goog.math.Coordinate.prototype.clone = function() {
  return new goog.math.Coordinate(this.x, this.y)
};
if(goog.DEBUG)goog.math.Coordinate.prototype.toString = function() {
  return"(" + this.x + ", " + this.y + ")"
};
goog.math.Coordinate.equals = function(a, b) {
  if(a == b)return true;
  if(!a || !b)return false;
  return a.x == b.x && a.y == b.y
};
goog.math.Coordinate.distance = function(a, b) {
  var dx = a.x - b.x, dy = a.y - b.y;
  return Math.sqrt(dx * dx + dy * dy)
};
goog.math.Coordinate.squaredDistance = function(a, b) {
  var dx = a.x - b.x, dy = a.y - b.y;
  return dx * dx + dy * dy
};
goog.math.Coordinate.difference = function(a, b) {
  return new goog.math.Coordinate(a.x - b.x, a.y - b.y)
};
goog.math.Coordinate.sum = function(a, b) {
  return new goog.math.Coordinate(a.x + b.x, a.y + b.y)
};goog.math.Size = function(width, height) {
  this.width = width;
  this.height = height
};
goog.math.Size.equals = function(a, b) {
  if(a == b)return true;
  if(!a || !b)return false;
  return a.width == b.width && a.height == b.height
};
goog.math.Size.prototype.clone = function() {
  return new goog.math.Size(this.width, this.height)
};
if(goog.DEBUG)goog.math.Size.prototype.toString = function() {
  return"(" + this.width + " x " + this.height + ")"
};
goog.math.Size.prototype.area = function() {
  return this.width * this.height
};
goog.math.Size.prototype.isEmpty = function() {
  return!this.area()
};
goog.math.Size.prototype.floor = function() {
  this.width = Math.floor(this.width);
  this.height = Math.floor(this.height);
  return this
};
goog.math.Size.prototype.round = function() {
  this.width = Math.round(this.width);
  this.height = Math.round(this.height);
  return this
};goog.dom.TagName = {A:"A", ABBR:"ABBR", ACRONYM:"ACRONYM", ADDRESS:"ADDRESS", APPLET:"APPLET", AREA:"AREA", B:"B", BASE:"BASE", BASEFONT:"BASEFONT", BDO:"BDO", BIG:"BIG", BLOCKQUOTE:"BLOCKQUOTE", BODY:"BODY", BR:"BR", BUTTON:"BUTTON", CAPTION:"CAPTION", CENTER:"CENTER", CITE:"CITE", CODE:"CODE", COL:"COL", COLGROUP:"COLGROUP", DD:"DD", DEL:"DEL", DFN:"DFN", DIR:"DIR", DIV:"DIV", DL:"DL", DT:"DT", EM:"EM", FIELDSET:"FIELDSET", FONT:"FONT", FORM:"FORM", FRAME:"FRAME", FRAMESET:"FRAMESET", H1:"H1", 
H2:"H2", H3:"H3", H4:"H4", H5:"H5", H6:"H6", HEAD:"HEAD", HR:"HR", HTML:"HTML", I:"I", IFRAME:"IFRAME", IMG:"IMG", INPUT:"INPUT", INS:"INS", ISINDEX:"ISINDEX", KBD:"KBD", LABEL:"LABEL", LEGEND:"LEGEND", LI:"LI", LINK:"LINK", MAP:"MAP", MENU:"MENU", META:"META", NOFRAMES:"NOFRAMES", NOSCRIPT:"NOSCRIPT", OBJECT:"OBJECT", OL:"OL", OPTGROUP:"OPTGROUP", OPTION:"OPTION", P:"P", PARAM:"PARAM", PRE:"PRE", Q:"Q", S:"S", SAMP:"SAMP", SCRIPT:"SCRIPT", SELECT:"SELECT", SMALL:"SMALL", SPAN:"SPAN", STRIKE:"STRIKE", 
STRONG:"STRONG", STYLE:"STYLE", SUB:"SUB", SUP:"SUP", TABLE:"TABLE", TBODY:"TBODY", TD:"TD", TEXTAREA:"TEXTAREA", TFOOT:"TFOOT", TH:"TH", THEAD:"THEAD", TITLE:"TITLE", TR:"TR", TT:"TT", U:"U", UL:"UL", VAR:"VAR"};goog.dom.ASSUME_QUIRKS_MODE = false;
goog.dom.ASSUME_STANDARDS_MODE = false;
goog.dom.COMPAT_MODE_KNOWN_ = goog.dom.ASSUME_QUIRKS_MODE || goog.dom.ASSUME_STANDARDS_MODE;
goog.dom.NodeType = {ELEMENT:1, ATTRIBUTE:2, TEXT:3, CDATA_SECTION:4, ENTITY_REFERENCE:5, ENTITY:6, PROCESSING_INSTRUCTION:7, COMMENT:8, DOCUMENT:9, DOCUMENT_TYPE:10, DOCUMENT_FRAGMENT:11, NOTATION:12};
goog.dom.getDomHelper = function(opt_element) {
  return opt_element ? new goog.dom.DomHelper(goog.dom.getOwnerDocument(opt_element)) : goog.dom.defaultDomHelper_ || (goog.dom.defaultDomHelper_ = new goog.dom.DomHelper)
};
goog.dom.getDocument = function() {
  return document
};
goog.dom.getElement = function(element) {
  return goog.isString(element) ? document.getElementById(element) : element
};
goog.dom.$ = goog.dom.getElement;
goog.dom.getElementsByTagNameAndClass = function(opt_tag, opt_class, opt_el) {
  return goog.dom.getElementsByTagNameAndClass_(document, opt_tag, opt_class, opt_el)
};
goog.dom.getElementsByTagNameAndClass_ = function(doc, opt_tag, opt_class, opt_el) {
  var parent = opt_el || doc, tagName = opt_tag && opt_tag != "*" ? opt_tag.toLowerCase() : "";
  if(parent.querySelectorAll && (tagName || opt_class) && (!goog.userAgent.WEBKIT || goog.dom.isCss1CompatMode_(doc) || goog.userAgent.isVersion("528")))return parent.querySelectorAll(tagName + (opt_class ? "." + opt_class : ""));
  if(opt_class && parent.getElementsByClassName) {
    var els = parent.getElementsByClassName(opt_class);
    if(tagName) {
      for(var arrayLike = {}, len = 0, i = 0, el;el = els[i];i++)if(tagName == el.nodeName.toLowerCase())arrayLike[len++] = el;
      arrayLike.length = len;
      return arrayLike
    }else return els
  }els = parent.getElementsByTagName(tagName || "*");
  if(opt_class) {
    arrayLike = {};
    for(i = len = 0;el = els[i];i++) {
      var className = el.className;
      if(typeof className.split == "function" && goog.array.contains(className.split(" "), opt_class))arrayLike[len++] = el
    }arrayLike.length = len;
    return arrayLike
  }else return els
};
goog.dom.$$ = goog.dom.getElementsByTagNameAndClass;
goog.dom.setProperties = function(element, properties) {
  goog.object.forEach(properties, function(val, key) {
    if(key == "style")element.style.cssText = val;
    else if(key == "class")element.className = val;
    else if(key == "for")element.htmlFor = val;
    else if(key in goog.dom.DIRECT_ATTRIBUTE_MAP_)element.setAttribute(goog.dom.DIRECT_ATTRIBUTE_MAP_[key], val);
    else element[key] = val
  })
};
goog.dom.DIRECT_ATTRIBUTE_MAP_ = {cellpadding:"cellPadding", cellspacing:"cellSpacing", colspan:"colSpan", rowspan:"rowSpan", valign:"vAlign", height:"height", width:"width", usemap:"useMap", frameborder:"frameBorder", type:"type"};
goog.dom.getViewportSize = function(opt_window) {
  return goog.dom.getViewportSize_(opt_window || window)
};
goog.dom.getViewportSize_ = function(win) {
  var doc = win.document;
  if(goog.userAgent.WEBKIT && !goog.userAgent.isVersion("500") && !goog.userAgent.MOBILE) {
    if(typeof win.innerHeight == "undefined")win = window;
    var innerHeight = win.innerHeight, scrollHeight = win.document.documentElement.scrollHeight;
    if(win == win.top)if(scrollHeight < innerHeight)innerHeight -= 15;
    return new goog.math.Size(win.innerWidth, innerHeight)
  }var el = goog.dom.isCss1CompatMode_(doc) && (!goog.userAgent.OPERA || goog.userAgent.OPERA && goog.userAgent.isVersion("9.50")) ? doc.documentElement : doc.body;
  return new goog.math.Size(el.clientWidth, el.clientHeight)
};
goog.dom.getDocumentHeight = function() {
  return goog.dom.getDocumentHeight_(window)
};
goog.dom.getDocumentHeight_ = function(win) {
  var doc = win.document, height = 0;
  if(doc) {
    var vh = goog.dom.getViewportSize_(win).height, body = doc.body, docEl = doc.documentElement;
    if(goog.dom.isCss1CompatMode_(doc) && docEl.scrollHeight)height = docEl.scrollHeight != vh ? docEl.scrollHeight : docEl.offsetHeight;
    else {
      var sh = docEl.scrollHeight, oh = docEl.offsetHeight;
      if(docEl.clientHeight != oh) {
        sh = body.scrollHeight;
        oh = body.offsetHeight
      }height = sh > vh ? sh > oh ? sh : oh : sh < oh ? sh : oh
    }
  }return height
};
goog.dom.getPageScroll = function(opt_window) {
  return goog.dom.getDomHelper((opt_window || goog.global || window).document).getDocumentScroll()
};
goog.dom.getDocumentScroll = function() {
  return goog.dom.getDocumentScroll_(document)
};
goog.dom.getDocumentScroll_ = function(doc) {
  var el = goog.dom.getDocumentScrollElement_(doc);
  return new goog.math.Coordinate(el.scrollLeft, el.scrollTop)
};
goog.dom.getDocumentScrollElement = function() {
  return goog.dom.getDocumentScrollElement_(document)
};
goog.dom.getDocumentScrollElement_ = function(doc) {
  return!goog.userAgent.WEBKIT && goog.dom.isCss1CompatMode_(doc) ? doc.documentElement : doc.body
};
goog.dom.getWindow = function(opt_doc) {
  return opt_doc ? goog.dom.getWindow_(opt_doc) : window
};
goog.dom.getWindow_ = function(doc) {
  if(doc.parentWindow)return doc.parentWindow;
  if(goog.userAgent.WEBKIT && !goog.userAgent.isVersion("500") && !goog.userAgent.MOBILE) {
    var scriptElement = doc.createElement("script");
    scriptElement.innerHTML = "document.parentWindow=window";
    var parentElement = doc.documentElement;
    parentElement.appendChild(scriptElement);
    parentElement.removeChild(scriptElement);
    return doc.parentWindow
  }return doc.defaultView
};
goog.dom.createDom = function() {
  return goog.dom.createDom_(document, arguments)
};
goog.dom.createDom_ = function(doc, args) {
  var tagName = args[0], attributes = args[1];
  if(goog.userAgent.IE && attributes && (attributes.name || attributes.type)) {
    var tagNameArr = ["<", tagName];
    attributes.name && tagNameArr.push(' name="', goog.string.htmlEscape(attributes.name), '"');
    if(attributes.type) {
      tagNameArr.push(' type="', goog.string.htmlEscape(attributes.type), '"');
      attributes = goog.cloneObject(attributes);
      delete attributes.type
    }tagNameArr.push(">");
    tagName = tagNameArr.join("")
  }var element = doc.createElement(tagName);
  if(attributes)if(goog.isString(attributes))element.className = attributes;
  else goog.dom.setProperties(element, attributes);
  if(args.length > 2) {
    function childHandler(child) {
      if(child)element.appendChild(goog.isString(child) ? doc.createTextNode(child) : child)
    }
    for(var i = 2;i < args.length;i++) {
      var arg = args[i];
      goog.isArrayLike(arg) && !goog.dom.isNodeLike(arg) ? goog.array.forEach(goog.dom.isNodeList(arg) ? goog.array.clone(arg) : arg, childHandler) : childHandler(arg)
    }
  }return element
};
goog.dom.$dom = goog.dom.createDom;
goog.dom.createElement = function(name) {
  return document.createElement(name)
};
goog.dom.createTextNode = function(content) {
  return document.createTextNode(content)
};
goog.dom.htmlToDocumentFragment = function(htmlString) {
  return goog.dom.htmlToDocumentFragment_(document, htmlString)
};
goog.dom.htmlToDocumentFragment_ = function(doc, htmlString) {
  var tempDiv = doc.createElement("div");
  tempDiv.innerHTML = htmlString;
  if(tempDiv.childNodes.length == 1)return tempDiv.firstChild;
  else {
    for(var fragment = doc.createDocumentFragment();tempDiv.firstChild;)fragment.appendChild(tempDiv.firstChild);
    return fragment
  }
};
goog.dom.getCompatMode = function() {
  return goog.dom.isCss1CompatMode() ? "CSS1Compat" : "BackCompat"
};
goog.dom.isCss1CompatMode = function() {
  return goog.dom.isCss1CompatMode_(document)
};
goog.dom.isCss1CompatMode_ = function(doc) {
  if(goog.dom.COMPAT_MODE_KNOWN_)return goog.dom.ASSUME_STANDARDS_MODE;
  return doc.compatMode == "CSS1Compat"
};
goog.dom.canHaveChildren = function(node) {
  if(node.nodeType != goog.dom.NodeType.ELEMENT)return false;
  if("canHaveChildren" in node)return node.canHaveChildren;
  switch(node.tagName) {
    case goog.dom.TagName.APPLET:
    ;
    case goog.dom.TagName.AREA:
    ;
    case goog.dom.TagName.BR:
    ;
    case goog.dom.TagName.COL:
    ;
    case goog.dom.TagName.FRAME:
    ;
    case goog.dom.TagName.HR:
    ;
    case goog.dom.TagName.IMG:
    ;
    case goog.dom.TagName.INPUT:
    ;
    case goog.dom.TagName.IFRAME:
    ;
    case goog.dom.TagName.ISINDEX:
    ;
    case goog.dom.TagName.LINK:
    ;
    case goog.dom.TagName.NOFRAMES:
    ;
    case goog.dom.TagName.NOSCRIPT:
    ;
    case goog.dom.TagName.META:
    ;
    case goog.dom.TagName.OBJECT:
    ;
    case goog.dom.TagName.PARAM:
    ;
    case goog.dom.TagName.SCRIPT:
    ;
    case goog.dom.TagName.STYLE:
      return false
  }
  return true
};
goog.dom.appendChild = function(parent, child) {
  parent.appendChild(child)
};
goog.dom.removeChildren = function(node) {
  for(var child;child = node.firstChild;)node.removeChild(child)
};
goog.dom.insertSiblingBefore = function(newNode, refNode) {
  refNode.parentNode && refNode.parentNode.insertBefore(newNode, refNode)
};
goog.dom.insertSiblingAfter = function(newNode, refNode) {
  refNode.parentNode && refNode.parentNode.insertBefore(newNode, refNode.nextSibling)
};
goog.dom.removeNode = function(node) {
  return node && node.parentNode ? node.parentNode.removeChild(node) : null
};
goog.dom.replaceNode = function(newNode, oldNode) {
  var parent = oldNode.parentNode;
  parent && parent.replaceChild(newNode, oldNode)
};
goog.dom.flattenElement = function(element) {
  var child, parent = element.parentNode;
  if(parent && parent.nodeType != goog.dom.NodeType.DOCUMENT_FRAGMENT)if(element.removeNode)return element.removeNode(false);
  else {
    for(;child = element.firstChild;)parent.insertBefore(child, element);
    return goog.dom.removeNode(element)
  }
};
goog.dom.getFirstElementChild = function(node) {
  return goog.dom.getNextElementNode_(node.firstChild, true)
};
goog.dom.getLastElementChild = function(node) {
  return goog.dom.getNextElementNode_(node.lastChild, false)
};
goog.dom.getNextElementSibling = function(node) {
  return goog.dom.getNextElementNode_(node.nextSibling, true)
};
goog.dom.getPreviousElementSibling = function(node) {
  return goog.dom.getNextElementNode_(node.previousSibling, false)
};
goog.dom.getNextElementNode_ = function(node, forward) {
  for(;node && node.nodeType != goog.dom.NodeType.ELEMENT;)node = forward ? node.nextSibling : node.previousSibling;
  return node
};
goog.dom.isNodeLike = function(obj) {
  return goog.isObject(obj) && obj.nodeType > 0
};
goog.dom.BAD_CONTAINS_WEBKIT_ = goog.userAgent.WEBKIT && goog.userAgent.isVersion("522");
goog.dom.contains = function(parent, descendant) {
  if(typeof parent.contains != "undefined" && !goog.dom.BAD_CONTAINS_WEBKIT_ && descendant.nodeType == goog.dom.NodeType.ELEMENT)return parent == descendant || parent.contains(descendant);
  if(typeof parent.compareDocumentPosition != "undefined")return parent == descendant || Boolean(parent.compareDocumentPosition(descendant) & 16);
  for(;descendant && parent != descendant;)descendant = descendant.parentNode;
  return descendant == parent
};
goog.dom.compareNodeOrder = function(node1, node2) {
  if(node1 == node2)return 0;
  if(node1.compareDocumentPosition)return node1.compareDocumentPosition(node2) & 2 ? 1 : -1;
  if("sourceIndex" in node1 || node1.parentNode && "sourceIndex" in node1.parentNode) {
    var isElement1 = node1.nodeType == goog.dom.NodeType.ELEMENT, isElement2 = node2.nodeType == goog.dom.NodeType.ELEMENT;
    if(isElement1 && isElement2)return node1.sourceIndex - node2.sourceIndex;
    else {
      var parent1 = node1.parentNode, parent2 = node2.parentNode;
      if(parent1 == parent2)return goog.dom.compareSiblingOrder_(node1, node2);
      if(!isElement1 && goog.dom.contains(parent1, node2))return-1 * goog.dom.compareParentsDescendantNodeIe_(node1, node2);
      if(!isElement2 && goog.dom.contains(parent2, node1))return goog.dom.compareParentsDescendantNodeIe_(node2, node1);
      return(isElement1 ? node1.sourceIndex : parent1.sourceIndex) - (isElement2 ? node2.sourceIndex : parent2.sourceIndex)
    }
  }var doc = goog.dom.getOwnerDocument(node1), range1, range2;
  range1 = doc.createRange();
  range1.selectNode(node1);
  range1.collapse(true);
  range2 = doc.createRange();
  range2.selectNode(node2);
  range2.collapse(true);
  return range1.compareBoundaryPoints(goog.global.Range.START_TO_END, range2)
};
goog.dom.compareParentsDescendantNodeIe_ = function(textNode, node) {
  var parent = textNode.parentNode;
  if(parent == node)return-1;
  for(var sibling = node;sibling.parentNode != parent;)sibling = sibling.parentNode;
  return goog.dom.compareSiblingOrder_(sibling, textNode)
};
goog.dom.compareSiblingOrder_ = function(node1, node2) {
  for(var s = node2;s = s.previousSibling;)if(s == node1)return-1;
  return 1
};
goog.dom.findCommonAncestor = function() {
  var i, count = arguments.length;
  if(count) {
    if(count == 1)return arguments[0]
  }else return null;
  var paths = [], minLength = Infinity;
  for(i = 0;i < count;i++) {
    for(var ancestors = [], node = arguments[i];node;) {
      ancestors.unshift(node);
      node = node.parentNode
    }paths.push(ancestors);
    minLength = Math.min(minLength, ancestors.length)
  }var output = null;
  for(i = 0;i < minLength;i++) {
    for(var first = paths[0][i], j = 1;j < count;j++)if(first != paths[j][i])return output;
    output = first
  }return output
};
goog.dom.getOwnerDocument = function(node) {
  return node.nodeType == goog.dom.NodeType.DOCUMENT ? node : node.ownerDocument || node.document
};
goog.dom.getFrameContentDocument = function(frame) {
  var doc;
  return doc = goog.userAgent.WEBKIT ? frame.document || frame.contentWindow.document : frame.contentDocument || frame.contentWindow.document
};
goog.dom.getFrameContentWindow = function(frame) {
  return frame.contentWindow || goog.dom.getWindow_(goog.dom.getFrameContentDocument(frame))
};
goog.dom.setTextContent = function(element, text) {
  if("textContent" in element)element.textContent = text;
  else if(element.firstChild && element.firstChild.nodeType == goog.dom.NodeType.TEXT) {
    for(;element.lastChild != element.firstChild;)element.removeChild(element.lastChild);
    element.firstChild.data = text
  }else {
    goog.dom.removeChildren(element);
    var doc = goog.dom.getOwnerDocument(element);
    element.appendChild(doc.createTextNode(text))
  }
};
goog.dom.getOuterHtml = function(element) {
  if("outerHTML" in element)return element.outerHTML;
  else {
    var div = goog.dom.getOwnerDocument(element).createElement("div");
    div.appendChild(element.cloneNode(true));
    return div.innerHTML
  }
};
goog.dom.findNode = function(root, p) {
  var rv = [];
  return goog.dom.findNodes_(root, p, rv, true) ? rv[0] : undefined
};
goog.dom.findNodes = function(root, p) {
  var rv = [];
  goog.dom.findNodes_(root, p, rv, false);
  return rv
};
goog.dom.findNodes_ = function(root, p, rv, findOne) {
  if(root != null)for(var i = 0, child;child = root.childNodes[i];i++) {
    if(p(child)) {
      rv.push(child);
      if(findOne)return true
    }if(goog.dom.findNodes_(child, p, rv, findOne))return true
  }return false
};
goog.dom.TAGS_TO_IGNORE_ = {SCRIPT:1, STYLE:1, HEAD:1, IFRAME:1, OBJECT:1};
goog.dom.PREDEFINED_TAG_VALUES_ = {IMG:" ", BR:"\n"};
goog.dom.isFocusableTabIndex = function(element) {
  var attrNode = element.getAttributeNode("tabindex");
  if(attrNode && attrNode.specified) {
    var index = element.tabIndex;
    return goog.isNumber(index) && index >= 0
  }return false
};
goog.dom.setFocusableTabIndex = function(element, enable) {
  if(enable)element.tabIndex = 0;
  else element.removeAttribute("tabIndex")
};
goog.dom.getTextContent = function(node) {
  var textContent;
  if(goog.userAgent.IE && "innerText" in node)textContent = goog.string.canonicalizeNewlines(node.innerText);
  else {
    var buf = [];
    goog.dom.getTextContent_(node, buf, true);
    textContent = buf.join("")
  }textContent = textContent.replace(/\xAD/g, "");
  textContent = textContent.replace(/ +/g, " ");
  if(textContent != " ")textContent = textContent.replace(/^\s*/, "");
  return textContent
};
goog.dom.getRawTextContent = function(node) {
  var buf = [];
  goog.dom.getTextContent_(node, buf, false);
  return buf.join("")
};
goog.dom.getTextContent_ = function(node, buf, normalizeWhitespace) {
  if(!(node.nodeName in goog.dom.TAGS_TO_IGNORE_))if(node.nodeType == goog.dom.NodeType.TEXT)normalizeWhitespace ? buf.push(String(node.nodeValue).replace(/(\r\n|\r|\n)/g, "")) : buf.push(node.nodeValue);
  else if(node.nodeName in goog.dom.PREDEFINED_TAG_VALUES_)buf.push(goog.dom.PREDEFINED_TAG_VALUES_[node.nodeName]);
  else for(var child = node.firstChild;child;) {
    goog.dom.getTextContent_(child, buf, normalizeWhitespace);
    child = child.nextSibling
  }
};
goog.dom.getNodeTextLength = function(node) {
  return goog.dom.getTextContent(node).length
};
goog.dom.getNodeTextOffset = function(node, opt_offsetParent) {
  for(var root = opt_offsetParent || goog.dom.getOwnerDocument(node).body, buf = [];node && node != root;) {
    for(var cur = node;cur = cur.previousSibling;)buf.unshift(goog.dom.getTextContent(cur));
    node = node.parentNode
  }return goog.string.trimLeft(buf.join("")).replace(/ +/g, " ").length
};
goog.dom.getNodeAtOffset = function(parent, offset, opt_result) {
  for(var stack = [parent], pos = 0, cur;stack.length > 0 && pos < offset;) {
    cur = stack.pop();
    if(!(cur.nodeName in goog.dom.TAGS_TO_IGNORE_))if(cur.nodeType == goog.dom.NodeType.TEXT) {
      var text = cur.nodeValue.replace(/(\r\n|\r|\n)/g, "").replace(/ +/g, " ");
      pos += text.length
    }else if(cur.nodeName in goog.dom.PREDEFINED_TAG_VALUES_)pos += goog.dom.PREDEFINED_TAG_VALUES_[cur.nodeName].length;
    else for(var i = cur.childNodes.length - 1;i >= 0;i--)stack.push(cur.childNodes[i])
  }if(goog.isObject(opt_result)) {
    opt_result.remainder = cur ? cur.nodeValue.length + offset - pos - 1 : 0;
    opt_result.node = cur
  }return cur
};
goog.dom.isNodeList = function(val) {
  if(val && typeof val.length == "number")if(goog.isObject(val))return typeof val.item == "function" || typeof val.item == "string";
  else if(goog.isFunction(val))return typeof val.item == "function";
  return false
};
goog.dom.getAncestorByTagNameAndClass = function(element, opt_tag, opt_class) {
  return goog.dom.getAncestor(element, function(node) {
    return(!opt_tag || node.nodeName == opt_tag) && (!opt_class || goog.dom.classes.has(node, opt_class))
  }, true)
};
goog.dom.getAncestor = function(element, matcher, opt_includeNode, opt_maxSearchSteps) {
  if(!opt_includeNode)element = element.parentNode;
  for(var ignoreSearchSteps = opt_maxSearchSteps == null, steps = 0;element && (ignoreSearchSteps || steps <= opt_maxSearchSteps);) {
    if(matcher(element))return element;
    element = element.parentNode;
    steps++
  }return null
};
goog.dom.DomHelper = function(opt_document) {
  this.document_ = opt_document || goog.global.document || document
};
a = goog.dom.DomHelper.prototype;
a.getDomHelper = goog.dom.getDomHelper;
a.getDocument = function() {
  return this.document_
};
a.getElement = function(element) {
  return goog.isString(element) ? this.document_.getElementById(element) : element
};
a.$ = goog.dom.DomHelper.prototype.getElement;
a.getElementsByTagNameAndClass = function(opt_tag, opt_class, opt_el) {
  return goog.dom.getElementsByTagNameAndClass_(this.document_, opt_tag, opt_class, opt_el)
};
a.$$ = goog.dom.DomHelper.prototype.getElementsByTagNameAndClass;
a.setProperties = goog.dom.setProperties;
a.getViewportSize = function(opt_window) {
  return goog.dom.getViewportSize(opt_window || this.getWindow())
};
a.getDocumentHeight = function() {
  return goog.dom.getDocumentHeight_(this.getWindow())
};
a.createDom = function() {
  return goog.dom.createDom_(this.document_, arguments)
};
a.$dom = goog.dom.DomHelper.prototype.createDom;
a.createElement = function(name) {
  return this.document_.createElement(name)
};
a.createTextNode = function(content) {
  return this.document_.createTextNode(content)
};
a.htmlToDocumentFragment = function(htmlString) {
  return goog.dom.htmlToDocumentFragment_(this.document_, htmlString)
};
a.getCompatMode = function() {
  return this.isCss1CompatMode() ? "CSS1Compat" : "BackCompat"
};
a.isCss1CompatMode = function() {
  return goog.dom.isCss1CompatMode_(this.document_)
};
a.getWindow = function() {
  return goog.dom.getWindow_(this.document_)
};
a.getDocumentScrollElement = function() {
  return goog.dom.getDocumentScrollElement_(this.document_)
};
a.getDocumentScroll = function() {
  return goog.dom.getDocumentScroll_(this.document_)
};
a.appendChild = goog.dom.appendChild;
a.removeChildren = goog.dom.removeChildren;
a.insertSiblingBefore = goog.dom.insertSiblingBefore;
a.insertSiblingAfter = goog.dom.insertSiblingAfter;
a.removeNode = goog.dom.removeNode;
a.replaceNode = goog.dom.replaceNode;
a.flattenElement = goog.dom.flattenElement;
a.getFirstElementChild = goog.dom.getFirstElementChild;
a.getLastElementChild = goog.dom.getLastElementChild;
a.getNextElementSibling = goog.dom.getNextElementSibling;
a.getPreviousElementSibling = goog.dom.getPreviousElementSibling;
a.isNodeLike = goog.dom.isNodeLike;
a.contains = goog.dom.contains;
a.getOwnerDocument = goog.dom.getOwnerDocument;
a.getFrameContentDocument = goog.dom.getFrameContentDocument;
a.getFrameContentWindow = goog.dom.getFrameContentWindow;
a.setTextContent = goog.dom.setTextContent;
a.findNode = goog.dom.findNode;
a.findNodes = goog.dom.findNodes;
a.getTextContent = goog.dom.getTextContent;
a.getNodeTextLength = goog.dom.getNodeTextLength;
a.getNodeTextOffset = goog.dom.getNodeTextOffset;
a.getAncestorByTagNameAndClass = goog.dom.getAncestorByTagNameAndClass;
a.getAncestor = goog.dom.getAncestor;goog.events.EventHandler = function(opt_handler) {
  this.handler_ = opt_handler
};
goog.inherits(goog.events.EventHandler, goog.Disposable);
goog.events.EventHandler.KEY_POOL_INITIAL_COUNT = 0;
goog.events.EventHandler.KEY_POOL_MAX_COUNT = 100;
goog.events.EventHandler.keyPool_ = new goog.structs.SimplePool(goog.events.EventHandler.KEY_POOL_INITIAL_COUNT, goog.events.EventHandler.KEY_POOL_MAX_COUNT);
goog.events.EventHandler.keys_ = null;
goog.events.EventHandler.key_ = null;
a = goog.events.EventHandler.prototype;
a.listen = function(src, type, opt_fn, opt_capture, opt_handler) {
  if(goog.isArray(type))for(var i = 0;i < type.length;i++)this.listen(src, type[i], opt_fn, opt_capture, opt_handler);
  else this.recordListenerKey_(goog.events.listen(src, type, opt_fn || this, opt_capture || false, opt_handler || this.handler_ || this));
  return this
};
a.listenOnce = function(src, type, opt_fn, opt_capture, opt_handler) {
  if(goog.isArray(type))for(var i = 0;i < type.length;i++)this.listenOnce(src, type[i], opt_fn, opt_capture, opt_handler);
  else this.recordListenerKey_(goog.events.listenOnce(src, type, opt_fn || this, opt_capture || false, opt_handler || this.handler_ || this));
  return this
};
a.listenWithWrapper = function(src, wrapper, listener, opt_capt, opt_handler) {
  wrapper.listen(src, listener, opt_capt, opt_handler || this.handler_, this);
  return this
};
a.recordListenerKey_ = function(key) {
  if(this.keys_)this.keys_[key] = true;
  else if(this.key_) {
    this.keys_ = goog.events.EventHandler.keyPool_.getObject();
    this.keys_[this.key_] = true;
    this.key_ = null;
    this.keys_[key] = true
  }else this.key_ = key
};
a.unlisten = function(src, type, opt_fn, opt_capture, opt_handler) {
  if(this.key_ || this.keys_)if(goog.isArray(type))for(var i = 0;i < type.length;i++)this.unlisten(src, type[i], opt_fn, opt_capture, opt_handler);
  else {
    var listener = goog.events.getListener(src, type, opt_fn || this, opt_capture || false, opt_handler || this.handler_ || this);
    if(listener) {
      var key = listener.key;
      goog.events.unlistenByKey(key);
      if(this.keys_)goog.object.remove(this.keys_, key);
      else if(this.key_ == key)this.key_ = null
    }
  }return this
};
a.unlistenWithWrapper = function(src, wrapper, listener, opt_capt, opt_handler) {
  wrapper.unlisten(src, listener, opt_capt, opt_handler || this.handler_, this);
  return this
};
a.removeAll = function() {
  if(this.keys_) {
    for(var key in this.keys_) {
      goog.events.unlistenByKey(key);
      delete this.keys_[key]
    }goog.events.EventHandler.keyPool_.releaseObject(this.keys_);
    this.keys_ = null
  }else this.key_ && goog.events.unlistenByKey(this.key_)
};
a.disposeInternal = function() {
  goog.events.EventHandler.superClass_.disposeInternal.call(this);
  this.removeAll()
};
a.handleEvent = function() {
  throw Error("EventHandler.handleEvent not implemented");
};goog.math.Box = function(top, right, bottom, left) {
  this.top = top;
  this.right = right;
  this.bottom = bottom;
  this.left = left
};
goog.math.Box.boundingBox = function() {
  for(var box = new goog.math.Box(arguments[0].y, arguments[0].x, arguments[0].y, arguments[0].x), i = 1;i < arguments.length;i++) {
    var coord = arguments[i];
    box.top = Math.min(box.top, coord.y);
    box.right = Math.max(box.right, coord.x);
    box.bottom = Math.max(box.bottom, coord.y);
    box.left = Math.min(box.left, coord.x)
  }return box
};
goog.math.Box.prototype.clone = function() {
  return new goog.math.Box(this.top, this.right, this.bottom, this.left)
};
if(goog.DEBUG)goog.math.Box.prototype.toString = function() {
  return"(" + this.top + "t, " + this.right + "r, " + this.bottom + "b, " + this.left + "l)"
};
goog.math.Box.prototype.contains = function(other) {
  return goog.math.Box.contains(this, other)
};
goog.math.Box.equals = function(a, b) {
  if(a == b)return true;
  if(!a || !b)return false;
  return a.top == b.top && a.right == b.right && a.bottom == b.bottom && a.left == b.left
};
goog.math.Box.contains = function(box, other) {
  if(!box || !other)return false;
  if(other instanceof goog.math.Box)return other.left >= box.left && other.right <= box.right && other.top >= box.top && other.bottom <= box.bottom;
  return other.x >= box.left && other.x <= box.right && other.y >= box.top && other.y <= box.bottom
};
goog.math.Box.distance = function(box, coord) {
  if(coord.x >= box.left && coord.x <= box.right) {
    if(coord.y >= box.top && coord.y <= box.bottom)return 0;
    return coord.y < box.top ? box.top - coord.y : coord.y - box.bottom
  }if(coord.y >= box.top && coord.y <= box.bottom)return coord.x < box.left ? box.left - coord.x : coord.x - box.right;
  return goog.math.Coordinate.distance(coord, new goog.math.Coordinate(coord.x < box.left ? box.left : box.right, coord.y < box.top ? box.top : box.bottom))
};goog.math.Rect = function(x, y, w, h) {
  this.left = x;
  this.top = y;
  this.width = w;
  this.height = h
};
goog.math.Rect.prototype.clone = function() {
  return new goog.math.Rect(this.left, this.top, this.width, this.height)
};
goog.math.Rect.createFromBox = function(box) {
  return new goog.math.Rect(box.left, box.top, box.right - box.left, box.bottom - box.top)
};
if(goog.DEBUG)goog.math.Rect.prototype.toString = function() {
  return"(" + this.left + ", " + this.top + " - " + this.width + "w x " + this.height + "h)"
};
goog.math.Rect.equals = function(a, b) {
  if(a == b)return true;
  if(!a || !b)return false;
  return a.left == b.left && a.width == b.width && a.top == b.top && a.height == b.height
};
goog.math.Rect.prototype.intersection = function(rect) {
  var x0 = Math.max(this.left, rect.left), x1 = Math.min(this.left + this.width, rect.left + rect.width);
  if(x0 <= x1) {
    var y0 = Math.max(this.top, rect.top), y1 = Math.min(this.top + this.height, rect.top + rect.height);
    if(y0 <= y1) {
      this.left = x0;
      this.top = y0;
      this.width = x1 - x0;
      this.height = y1 - y0;
      return true
    }
  }return false
};
goog.math.Rect.intersection = function(a, b) {
  var x0 = Math.max(a.left, b.left), x1 = Math.min(a.left + a.width, b.left + b.width);
  if(x0 <= x1) {
    var y0 = Math.max(a.top, b.top), y1 = Math.min(a.top + a.height, b.top + b.height);
    if(y0 <= y1)return new goog.math.Rect(x0, y0, x1 - x0, y1 - y0)
  }return null
};
goog.math.Rect.intersects = function(a, b) {
  var x0 = Math.max(a.left, b.left), x1 = Math.min(a.left + a.width, b.left + b.width);
  if(x0 <= x1) {
    var y0 = Math.max(a.top, b.top), y1 = Math.min(a.top + a.height, b.top + b.height);
    if(y0 <= y1)return true
  }return false
};
goog.math.Rect.prototype.intersects = function(rect) {
  return goog.math.Rect.intersects(this, rect)
};
goog.math.Rect.difference = function(a, b) {
  var intersection = goog.math.Rect.intersection(a, b);
  if(!intersection || !intersection.height || !intersection.width)return[a.clone()];
  var result = [], top = a.top, height = a.height, ar = a.left + a.width, ab = a.top + a.height, br = b.left + b.width, bb = b.top + b.height;
  if(b.top > a.top) {
    result.push(new goog.math.Rect(a.left, a.top, a.width, b.top - a.top));
    top = b.top;
    height -= b.top - a.top
  }if(bb < ab) {
    result.push(new goog.math.Rect(a.left, bb, a.width, ab - bb));
    height = bb - top
  }b.left > a.left && result.push(new goog.math.Rect(a.left, top, b.left - a.left, height));
  br < ar && result.push(new goog.math.Rect(br, top, ar - br, height));
  return result
};
goog.math.Rect.prototype.difference = function(rect) {
  return goog.math.Rect.difference(this, rect)
};
goog.math.Rect.prototype.boundingRect = function(rect) {
  var right = Math.max(this.left + this.width, rect.left + rect.width), bottom = Math.max(this.top + this.height, rect.top + rect.height);
  this.left = Math.min(this.left, rect.left);
  this.top = Math.min(this.top, rect.top);
  this.width = right - this.left;
  this.height = bottom - this.top
};
goog.math.Rect.boundingRect = function(a, b) {
  if(!a || !b)return null;
  var clone = a.clone();
  clone.boundingRect(b);
  return clone
};
goog.math.Rect.prototype.contains = function(another) {
  return another instanceof goog.math.Rect ? this.left <= another.left && this.left + this.width >= another.left + another.width && this.top <= another.top && this.top + this.height >= another.top + another.height : another.x >= this.left && another.x <= this.left + this.width && another.y >= this.top && another.y <= this.top + this.height
};
goog.math.Rect.prototype.getSize = function() {
  return new goog.math.Size(this.width, this.height)
};goog.userAgent.product = {};
goog.userAgent.product.ASSUME_FIREFOX = false;
goog.userAgent.product.ASSUME_CAMINO = false;
goog.userAgent.product.ASSUME_IPHONE = false;
goog.userAgent.product.ASSUME_ANDROID = false;
goog.userAgent.product.ASSUME_CHROME = false;
goog.userAgent.product.ASSUME_SAFARI = false;
goog.userAgent.product.PRODUCT_KNOWN_ = goog.userAgent.ASSUME_IE || goog.userAgent.ASSUME_OPERA || goog.userAgent.product.ASSUME_FIREFOX || goog.userAgent.product.ASSUME_CAMINO || goog.userAgent.product.ASSUME_IPHONE || goog.userAgent.product.ASSUME_ANDROID || goog.userAgent.product.ASSUME_CHROME || goog.userAgent.product.ASSUME_SAFARI;
goog.userAgent.product.init_ = function() {
  goog.userAgent.product.detectedFirefox_ = false;
  goog.userAgent.product.detectedCamino_ = false;
  goog.userAgent.product.detectedIphone_ = false;
  goog.userAgent.product.detectedAndroid_ = false;
  goog.userAgent.product.detectedChrome_ = false;
  goog.userAgent.product.detectedSafari_ = false;
  var ua = goog.userAgent.getUserAgentString();
  if(ua)if(ua.indexOf("Firefox") != -1)goog.userAgent.product.detectedFirefox_ = true;
  else if(ua.indexOf("Camino") != -1)goog.userAgent.product.detectedCamino_ = true;
  else if(ua.indexOf("iPhone") != -1 || ua.indexOf("iPod") != -1)goog.userAgent.product.detectedIphone_ = true;
  else if(ua.indexOf("Android") != -1)goog.userAgent.product.detectedAndroid_ = true;
  else if(ua.indexOf("Chrome") != -1)goog.userAgent.product.detectedChrome_ = true;
  else if(ua.indexOf("Safari") != -1)goog.userAgent.product.detectedSafari_ = true
};
goog.userAgent.product.PRODUCT_KNOWN_ || goog.userAgent.product.init_();
goog.userAgent.product.OPERA = goog.userAgent.OPERA;
goog.userAgent.product.IE = goog.userAgent.IE;
goog.userAgent.product.FIREFOX = goog.userAgent.product.PRODUCT_KNOWN_ ? goog.userAgent.product.ASSUME_FIREFOX : goog.userAgent.product.detectedFirefox_;
goog.userAgent.product.CAMINO = goog.userAgent.product.PRODUCT_KNOWN_ ? goog.userAgent.product.ASSUME_CAMINO : goog.userAgent.product.detectedCamino_;
goog.userAgent.product.IPHONE = goog.userAgent.product.PRODUCT_KNOWN_ ? goog.userAgent.product.ASSUME_IPHONE : goog.userAgent.product.detectedIphone_;
goog.userAgent.product.ANDROID = goog.userAgent.product.PRODUCT_KNOWN_ ? goog.userAgent.product.ASSUME_ANDROID : goog.userAgent.product.detectedAndroid_;
goog.userAgent.product.CHROME = goog.userAgent.product.PRODUCT_KNOWN_ ? goog.userAgent.product.ASSUME_CHROME : goog.userAgent.product.detectedChrome_;
goog.userAgent.product.SAFARI = goog.userAgent.product.PRODUCT_KNOWN_ ? goog.userAgent.product.ASSUME_SAFARI : goog.userAgent.product.detectedSafari_;goog.style = {};
goog.style.setStyle = function(element, style, opt_value) {
  goog.isString(style) ? goog.style.setStyle_(element, opt_value, style) : goog.object.forEach(style, goog.partial(goog.style.setStyle_, element))
};
goog.style.setStyle_ = function(element, value, style) {
  element.style[goog.style.toCamelCase(style)] = value
};
goog.style.getStyle = function(element, style) {
  return element.style[goog.style.toCamelCase(style)]
};
goog.style.getComputedStyle = function(element, style) {
  var doc = goog.dom.getOwnerDocument(element);
  if(doc.defaultView && doc.defaultView.getComputedStyle) {
    var styles = doc.defaultView.getComputedStyle(element, "");
    if(styles)return styles[style]
  }return null
};
goog.style.getCascadedStyle = function(element, style) {
  return element.currentStyle ? element.currentStyle[style] : null
};
goog.style.getStyle_ = function(element, style) {
  return goog.style.getComputedStyle(element, style) || goog.style.getCascadedStyle(element, style) || element.style[style]
};
goog.style.getComputedPosition = function(element) {
  return goog.style.getStyle_(element, "position")
};
goog.style.getBackgroundColor = function(element) {
  return goog.style.getStyle_(element, "backgroundColor")
};
goog.style.getComputedOverflowX = function(element) {
  return goog.style.getStyle_(element, "overflowX")
};
goog.style.getComputedOverflowY = function(element) {
  return goog.style.getStyle_(element, "overflowY")
};
goog.style.getComputedZIndex = function(element) {
  return goog.style.getStyle_(element, "zIndex")
};
goog.style.getComputedTextAlign = function(element) {
  return goog.style.getStyle_(element, "textAlign")
};
goog.style.getComputedCursor = function(element) {
  return goog.style.getStyle_(element, "cursor")
};
goog.style.setPosition = function(el, arg1, opt_arg2) {
  var x, y, buggyGeckoSubPixelPos = goog.userAgent.GECKO && (goog.userAgent.MAC || goog.userAgent.X11) && goog.userAgent.isVersion("1.9");
  if(arg1 instanceof goog.math.Coordinate) {
    x = arg1.x;
    y = arg1.y
  }else {
    x = arg1;
    y = opt_arg2
  }el.style.left = typeof x == "number" ? (buggyGeckoSubPixelPos ? Math.round(x) : x) + "px" : x;
  el.style.top = typeof y == "number" ? (buggyGeckoSubPixelPos ? Math.round(y) : y) + "px" : y
};
goog.style.getPosition = function(element) {
  return new goog.math.Coordinate(element.offsetLeft, element.offsetTop)
};
goog.style.getClientViewportElement = function(opt_node) {
  var doc;
  doc = opt_node ? opt_node.nodeType == goog.dom.NodeType.DOCUMENT ? opt_node : goog.dom.getOwnerDocument(opt_node) : goog.dom.getDocument();
  if(goog.userAgent.IE && !goog.dom.getDomHelper(doc).isCss1CompatMode())return doc.body;
  return doc.documentElement
};
goog.style.getBoundingClientRect_ = function(el) {
  var rect = el.getBoundingClientRect();
  if(goog.userAgent.IE) {
    var doc = el.ownerDocument;
    rect.left -= doc.documentElement.clientLeft + doc.body.clientLeft;
    rect.top -= doc.documentElement.clientTop + doc.body.clientTop
  }return rect
};
goog.style.getOffsetParent = function(element) {
  if(goog.userAgent.IE)return element.offsetParent;
  for(var doc = goog.dom.getOwnerDocument(element), positionStyle = goog.style.getStyle_(element, "position"), skipStatic = positionStyle == "fixed" || positionStyle == "absolute", parent = element.parentNode;parent && parent != doc;parent = parent.parentNode) {
    positionStyle = goog.style.getStyle_(parent, "position");
    skipStatic = skipStatic && positionStyle == "static" && parent != doc.documentElement && parent != doc.body;
    if(!skipStatic && (parent.scrollWidth > parent.clientWidth || parent.scrollHeight > parent.clientHeight || positionStyle == "fixed" || positionStyle == "absolute"))return parent
  }return null
};
goog.style.getVisibleRectForElement = function(element) {
  for(var visibleRect = new goog.math.Box(0, Infinity, Infinity, 0), dom = goog.dom.getDomHelper(element), scrollEl = dom.getDocumentScrollElement(), inContainer, el = element;el = goog.style.getOffsetParent(el);)if((!goog.userAgent.IE || el.clientWidth != 0) && (el.scrollWidth != el.clientWidth || el.scrollHeight != el.clientHeight) && goog.style.getStyle_(el, "overflow") != "visible") {
    var pos = goog.style.getPageOffset(el), client = goog.style.getClientLeftTop(el);
    pos.x += client.x;
    pos.y += client.y;
    visibleRect.top = Math.max(visibleRect.top, pos.y);
    visibleRect.right = Math.min(visibleRect.right, pos.x + el.clientWidth);
    visibleRect.bottom = Math.min(visibleRect.bottom, pos.y + el.clientHeight);
    visibleRect.left = Math.max(visibleRect.left, pos.x);
    inContainer = inContainer || el != scrollEl
  }var scrollX = scrollEl.scrollLeft, scrollY = scrollEl.scrollTop;
  if(goog.userAgent.WEBKIT) {
    visibleRect.left += scrollX;
    visibleRect.top += scrollY
  }else {
    visibleRect.left = Math.max(visibleRect.left, scrollX);
    visibleRect.top = Math.max(visibleRect.top, scrollY)
  }if(!inContainer || goog.userAgent.WEBKIT) {
    visibleRect.right += scrollX;
    visibleRect.bottom += scrollY
  }var winSize = dom.getViewportSize();
  visibleRect.right = Math.min(visibleRect.right, scrollX + winSize.width);
  visibleRect.bottom = Math.min(visibleRect.bottom, scrollY + winSize.height);
  return visibleRect.top >= 0 && visibleRect.left >= 0 && visibleRect.bottom > visibleRect.top && visibleRect.right > visibleRect.left ? visibleRect : null
};
goog.style.scrollIntoContainerView = function(element, container, opt_center) {
  var elementPos = goog.style.getPageOffset(element), containerPos = goog.style.getPageOffset(container), containerBorder = goog.style.getBorderBox(container), relX = elementPos.x - containerPos.x - containerBorder.left, relY = elementPos.y - containerPos.y - containerBorder.top, spaceX = container.clientWidth - element.offsetWidth, spaceY = container.clientHeight - element.offsetHeight;
  if(opt_center) {
    container.scrollLeft += relX - spaceX / 2;
    container.scrollTop += relY - spaceY / 2
  }else {
    container.scrollLeft += Math.min(relX, Math.max(relX - spaceX, 0));
    container.scrollTop += Math.min(relY, Math.max(relY - spaceY, 0))
  }
};
goog.style.getClientLeftTop = function(el) {
  if(goog.userAgent.GECKO && !goog.userAgent.isVersion("1.9")) {
    var left = parseFloat(goog.style.getComputedStyle(el, "borderLeftWidth"));
    if(goog.style.isRightToLeft(el)) {
      var scrollbarWidth = el.offsetWidth - el.clientWidth - left - parseFloat(goog.style.getComputedStyle(el, "borderRightWidth"));
      left += scrollbarWidth
    }return new goog.math.Coordinate(left, parseFloat(goog.style.getComputedStyle(el, "borderTopWidth")))
  }return new goog.math.Coordinate(el.clientLeft, el.clientTop)
};
goog.style.getPageOffset = function(el) {
  var box, doc = goog.dom.getOwnerDocument(el), positionStyle = goog.style.getStyle_(el, "position"), BUGGY_GECKO_BOX_OBJECT = goog.userAgent.GECKO && doc.getBoxObjectFor && !el.getBoundingClientRect && positionStyle == "absolute" && (box = doc.getBoxObjectFor(el)) && (box.screenX < 0 || box.screenY < 0), pos = new goog.math.Coordinate(0, 0), viewportElement = goog.style.getClientViewportElement(doc);
  if(el == viewportElement)return pos;
  if(el.getBoundingClientRect) {
    box = goog.style.getBoundingClientRect_(el);
    var scrollCoord = goog.dom.getDomHelper(doc).getDocumentScroll();
    pos.x = box.left + scrollCoord.x;
    pos.y = box.top + scrollCoord.y
  }else if(doc.getBoxObjectFor && !BUGGY_GECKO_BOX_OBJECT) {
    box = doc.getBoxObjectFor(el);
    var vpBox = doc.getBoxObjectFor(viewportElement);
    pos.x = box.screenX - vpBox.screenX;
    pos.y = box.screenY - vpBox.screenY
  }else {
    var parent = el;
    do {
      pos.x += parent.offsetLeft;
      pos.y += parent.offsetTop;
      if(parent != el) {
        pos.x += parent.clientLeft || 0;
        pos.y += parent.clientTop || 0
      }if(goog.userAgent.WEBKIT && goog.style.getComputedPosition(parent) == "fixed") {
        pos.x += doc.body.scrollLeft;
        pos.y += doc.body.scrollTop;
        break
      }parent = parent.offsetParent
    }while(parent && parent != el);
    if(goog.userAgent.OPERA || goog.userAgent.WEBKIT && positionStyle == "absolute")pos.y -= doc.body.offsetTop;
    for(parent = el;(parent = goog.style.getOffsetParent(parent)) && parent != doc.body && parent != viewportElement;) {
      pos.x -= parent.scrollLeft;
      if(!goog.userAgent.OPERA || parent.tagName != "TR")pos.y -= parent.scrollTop
    }
  }return pos
};
goog.style.getPageOffsetLeft = function(el) {
  return goog.style.getPageOffset(el).x
};
goog.style.getPageOffsetTop = function(el) {
  return goog.style.getPageOffset(el).y
};
goog.style.getFramedPageOffset = function(el, relativeWin) {
  var position = new goog.math.Coordinate(0, 0), currentWin = goog.dom.getWindow(goog.dom.getOwnerDocument(el)), currentEl = el;
  do {
    var offset = currentWin == relativeWin ? goog.style.getPageOffset(currentEl) : goog.style.getClientPosition(currentEl);
    position.x += offset.x;
    position.y += offset.y
  }while(currentWin && currentWin != relativeWin && (currentEl = currentWin.frameElement) && (currentWin = currentWin.parent));
  return position
};
goog.style.translateRectForAnotherFrame = function(rect, origBase, newBase) {
  if(origBase.getDocument() != newBase.getDocument()) {
    var body = origBase.getDocument().body, pos = goog.style.getFramedPageOffset(body, newBase.getWindow());
    pos = goog.math.Coordinate.difference(pos, goog.style.getPageOffset(body));
    if(goog.userAgent.IE && !origBase.isCss1CompatMode())pos = goog.math.Coordinate.difference(pos, origBase.getDocumentScroll());
    rect.left += pos.x;
    rect.top += pos.y
  }
};
goog.style.getRelativePosition = function(a, b) {
  var ap = goog.style.getClientPosition(a), bp = goog.style.getClientPosition(b);
  return new goog.math.Coordinate(ap.x - bp.x, ap.y - bp.y)
};
goog.style.getClientPosition = function(el) {
  var pos = new goog.math.Coordinate;
  if(el.nodeType == goog.dom.NodeType.ELEMENT)if(el.getBoundingClientRect) {
    var box = goog.style.getBoundingClientRect_(el);
    pos.x = box.left;
    pos.y = box.top
  }else {
    var scrollCoord = goog.dom.getDomHelper(el).getDocumentScroll(), pageCoord = goog.style.getPageOffset(el);
    pos.x = pageCoord.x - scrollCoord.x;
    pos.y = pageCoord.y - scrollCoord.y
  }else {
    pos.x = el.clientX;
    pos.y = el.clientY
  }return pos
};
goog.style.setPageOffset = function(el, x, opt_y) {
  var cur = goog.style.getPageOffset(el);
  if(x instanceof goog.math.Coordinate) {
    opt_y = x.y;
    x = x.x
  }goog.style.setPosition(el, el.offsetLeft + (x - cur.x), el.offsetTop + (opt_y - cur.y))
};
goog.style.setSize = function(element, w, opt_h) {
  var h;
  if(w instanceof goog.math.Size) {
    h = w.height;
    w = w.width
  }else {
    if(opt_h == undefined)throw Error("missing height argument");h = opt_h
  }element.style.width = typeof w == "number" ? Math.round(w) + "px" : w;
  element.style.height = typeof h == "number" ? Math.round(h) + "px" : h
};
goog.style.getSize = function(element) {
  var hasOperaBug = goog.userAgent.OPERA && !goog.userAgent.isVersion("10");
  if(goog.style.getStyle_(element, "display") != "none")return hasOperaBug ? new goog.math.Size(element.offsetWidth || element.clientWidth, element.offsetHeight || element.clientHeight) : new goog.math.Size(element.offsetWidth, element.offsetHeight);
  var style = element.style, originalDisplay = style.display, originalVisibility = style.visibility, originalPosition = style.position;
  style.visibility = "hidden";
  style.position = "absolute";
  style.display = "inline";
  var originalWidth, originalHeight;
  if(hasOperaBug) {
    originalWidth = element.offsetWidth || element.clientWidth;
    originalHeight = element.offsetHeight || element.clientHeight
  }else {
    originalWidth = element.offsetWidth;
    originalHeight = element.offsetHeight
  }style.display = originalDisplay;
  style.position = originalPosition;
  style.visibility = originalVisibility;
  return new goog.math.Size(originalWidth, originalHeight)
};
goog.style.getBounds = function(element) {
  var o = goog.style.getPageOffset(element), s = goog.style.getSize(element);
  return new goog.math.Rect(o.x, o.y, s.width, s.height)
};
goog.style.toCamelCaseCache_ = {};
goog.style.toCamelCase = function(selector) {
  return goog.style.toCamelCaseCache_[selector] || (goog.style.toCamelCaseCache_[selector] = String(selector).replace(/\-([a-z])/g, function(all, match) {
    return match.toUpperCase()
  }))
};
goog.style.toSelectorCase = function(selector) {
  return selector.replace(/([A-Z])/g, "-$1").toLowerCase()
};
goog.style.getOpacity = function(el) {
  var style = el.style, result = "";
  if("opacity" in style)result = style.opacity;
  else if("MozOpacity" in style)result = style.MozOpacity;
  else if("filter" in style) {
    var match = style.filter.match(/alpha\(opacity=([\d.]+)\)/);
    if(match)result = String(match[1] / 100)
  }return result == "" ? result : Number(result)
};
goog.style.setOpacity = function(el, alpha) {
  var style = el.style;
  if("opacity" in style)style.opacity = alpha;
  else if("MozOpacity" in style)style.MozOpacity = alpha;
  else if("filter" in style)style.filter = alpha === "" ? "" : "alpha(opacity=" + alpha * 100 + ")"
};
goog.style.setTransparentBackgroundImage = function(el, src) {
  var style = el.style;
  if(goog.userAgent.IE && !goog.userAgent.isVersion("8"))style.filter = 'progid:DXImageTransform.Microsoft.AlphaImageLoader(src="' + src + '", sizingMethod="crop")';
  else {
    style.backgroundImage = "url(" + src + ")";
    style.backgroundPosition = "top left";
    style.backgroundRepeat = "no-repeat"
  }
};
goog.style.clearTransparentBackgroundImage = function(el) {
  var style = el.style;
  if("filter" in style)style.filter = "";
  else style.backgroundImage = "none"
};
goog.style.showElement = function(el, display) {
  el.style.display = display ? "" : "none"
};
goog.style.isElementShown = function(el) {
  return el.style.display != "none"
};
goog.style.installStyles = function(stylesString, opt_node) {
  var dh = goog.dom.getDomHelper(opt_node), styleSheet = null;
  if(goog.userAgent.IE) {
    styleSheet = dh.getDocument().createStyleSheet();
    goog.style.setStyles(styleSheet, stylesString)
  }else {
    var head = dh.getElementsByTagNameAndClass("head")[0];
    if(!head) {
      var body = dh.getElementsByTagNameAndClass("body")[0];
      head = dh.createDom("head");
      body.parentNode.insertBefore(head, body)
    }styleSheet = dh.createDom("style");
    goog.style.setStyles(styleSheet, stylesString);
    dh.appendChild(head, styleSheet)
  }return styleSheet
};
goog.style.uninstallStyles = function(styleSheet) {
  goog.dom.removeNode(styleSheet.ownerNode || styleSheet.owningElement || styleSheet)
};
goog.style.setStyles = function(element, stylesString) {
  if(goog.userAgent.IE)element.cssText = stylesString;
  else element[goog.userAgent.WEBKIT ? "innerText" : "innerHTML"] = stylesString
};
goog.style.setPreWrap = function(el) {
  var style = el.style;
  if(goog.userAgent.IE && !goog.userAgent.isVersion("8")) {
    style.whiteSpace = "pre";
    style.wordWrap = "break-word"
  }else style.whiteSpace = goog.userAgent.GECKO ? "-moz-pre-wrap" : goog.userAgent.OPERA ? "-o-pre-wrap" : "pre-wrap"
};
goog.style.setInlineBlock = function(el) {
  var style = el.style;
  style.position = "relative";
  if(goog.userAgent.IE && !goog.userAgent.isVersion("8")) {
    style.zoom = "1";
    style.display = "inline"
  }else style.display = goog.userAgent.GECKO ? goog.userAgent.isVersion("1.9a") ? "inline-block" : "-moz-inline-box" : "inline-block"
};
goog.style.isRightToLeft = function(el) {
  return"rtl" == goog.style.getStyle_(el, "direction")
};
goog.style.unselectableStyle_ = goog.userAgent.GECKO ? "MozUserSelect" : goog.userAgent.WEBKIT ? "WebkitUserSelect" : null;
goog.style.isUnselectable = function(el) {
  if(goog.style.unselectableStyle_)return el.style[goog.style.unselectableStyle_].toLowerCase() == "none";
  else if(goog.userAgent.IE || goog.userAgent.OPERA)return el.getAttribute("unselectable") == "on";
  return false
};
goog.style.setUnselectable = function(el, unselectable, opt_noRecurse) {
  var descendants = !opt_noRecurse ? el.getElementsByTagName("*") : null, name = goog.style.unselectableStyle_;
  if(name) {
    var value = unselectable ? "none" : "";
    el.style[name] = value;
    if(descendants)for(var i = 0, descendant;descendant = descendants[i];i++)descendant.style[name] = value
  }else if(goog.userAgent.IE || goog.userAgent.OPERA) {
    value = unselectable ? "on" : "";
    el.setAttribute("unselectable", value);
    if(descendants)for(i = 0;descendant = descendants[i];i++)descendant.setAttribute("unselectable", value)
  }
};
goog.style.getBorderBoxSize = function(element) {
  return new goog.math.Size(element.offsetWidth, element.offsetHeight)
};
goog.style.setBorderBoxSize = function(element, size) {
  var doc = goog.dom.getOwnerDocument(element), isCss1CompatMode = goog.dom.getDomHelper(doc).isCss1CompatMode();
  if(goog.userAgent.IE && (!isCss1CompatMode || !goog.userAgent.isVersion("8"))) {
    var style = element.style;
    if(isCss1CompatMode) {
      var paddingBox = goog.style.getPaddingBox(element), borderBox = goog.style.getBorderBox(element);
      style.pixelWidth = size.width - borderBox.left - paddingBox.left - paddingBox.right - borderBox.right;
      style.pixelHeight = size.height - borderBox.top - paddingBox.top - paddingBox.bottom - borderBox.bottom
    }else {
      style.pixelWidth = size.width;
      style.pixelHeight = size.height
    }
  }else goog.style.setBoxSizingSize_(element, size, "border-box")
};
goog.style.getContentBoxSize = function(element) {
  var doc = goog.dom.getOwnerDocument(element), ieCurrentStyle = goog.userAgent.IE && element.currentStyle;
  if(ieCurrentStyle && goog.dom.getDomHelper(doc).isCss1CompatMode() && ieCurrentStyle.width != "auto" && ieCurrentStyle.height != "auto" && !ieCurrentStyle.boxSizing) {
    var width = goog.style.getIePixelValue_(element, ieCurrentStyle.width, "width", "pixelWidth"), height = goog.style.getIePixelValue_(element, ieCurrentStyle.height, "height", "pixelHeight");
    return new goog.math.Size(width, height)
  }else {
    var borderBoxSize = goog.style.getBorderBoxSize(element), paddingBox = goog.style.getPaddingBox(element), borderBox = goog.style.getBorderBox(element);
    return new goog.math.Size(borderBoxSize.width - borderBox.left - paddingBox.left - paddingBox.right - borderBox.right, borderBoxSize.height - borderBox.top - paddingBox.top - paddingBox.bottom - borderBox.bottom)
  }
};
goog.style.setContentBoxSize = function(element, size) {
  var doc = goog.dom.getOwnerDocument(element), isCss1CompatMode = goog.dom.getDomHelper(doc).isCss1CompatMode();
  if(goog.userAgent.IE && (!isCss1CompatMode || !goog.userAgent.isVersion("8"))) {
    var style = element.style;
    if(isCss1CompatMode) {
      style.pixelWidth = size.width;
      style.pixelHeight = size.height
    }else {
      var paddingBox = goog.style.getPaddingBox(element), borderBox = goog.style.getBorderBox(element);
      style.pixelWidth = size.width + borderBox.left + paddingBox.left + paddingBox.right + borderBox.right;
      style.pixelHeight = size.height + borderBox.top + paddingBox.top + paddingBox.bottom + borderBox.bottom
    }
  }else goog.style.setBoxSizingSize_(element, size, "content-box")
};
goog.style.setBoxSizingSize_ = function(element, size, boxSizing) {
  var style = element.style;
  if(goog.userAgent.GECKO)style.MozBoxSizing = boxSizing;
  else if(goog.userAgent.WEBKIT)style.WebkitBoxSizing = boxSizing;
  else if(goog.userAgent.OPERA && !goog.userAgent.isVersion("9.50"))boxSizing ? style.setProperty("box-sizing", boxSizing) : style.removeProperty("box-sizing");
  else style.boxSizing = boxSizing;
  style.width = size.width + "px";
  style.height = size.height + "px"
};
goog.style.getIePixelValue_ = function(element, value, name, pixelName) {
  if(/^\d+px?$/.test(value))return parseInt(value, 10);
  else {
    var oldStyleValue = element.style[name], oldRuntimeValue = element.runtimeStyle[name];
    element.runtimeStyle[name] = element.currentStyle[name];
    element.style[name] = value;
    var pixelValue = element.style[pixelName];
    element.style[name] = oldStyleValue;
    element.runtimeStyle[name] = oldRuntimeValue;
    return pixelValue
  }
};
goog.style.getIePixelDistance_ = function(element, propName) {
  return goog.style.getIePixelValue_(element, goog.style.getCascadedStyle(element, propName), "left", "pixelLeft")
};
goog.style.getBox_ = function(element, stylePrefix) {
  if(goog.userAgent.IE) {
    var left = goog.style.getIePixelDistance_(element, stylePrefix + "Left"), right = goog.style.getIePixelDistance_(element, stylePrefix + "Right"), top = goog.style.getIePixelDistance_(element, stylePrefix + "Top"), bottom = goog.style.getIePixelDistance_(element, stylePrefix + "Bottom");
    return new goog.math.Box(top, right, bottom, left)
  }else {
    left = goog.style.getComputedStyle(element, stylePrefix + "Left");
    right = goog.style.getComputedStyle(element, stylePrefix + "Right");
    top = goog.style.getComputedStyle(element, stylePrefix + "Top");
    bottom = goog.style.getComputedStyle(element, stylePrefix + "Bottom");
    return new goog.math.Box(parseFloat(top), parseFloat(right), parseFloat(bottom), parseFloat(left))
  }
};
goog.style.getPaddingBox = function(element) {
  return goog.style.getBox_(element, "padding")
};
goog.style.getMarginBox = function(element) {
  return goog.style.getBox_(element, "margin")
};
goog.style.ieBorderWidthKeywords_ = {thin:2, medium:4, thick:6};
goog.style.getIePixelBorder_ = function(element, prop) {
  if(goog.style.getCascadedStyle(element, prop + "Style") == "none")return 0;
  var width = goog.style.getCascadedStyle(element, prop + "Width");
  if(width in goog.style.ieBorderWidthKeywords_)return goog.style.ieBorderWidthKeywords_[width];
  return goog.style.getIePixelValue_(element, width, "left", "pixelLeft")
};
goog.style.getBorderBox = function(element) {
  if(goog.userAgent.IE) {
    var left = goog.style.getIePixelBorder_(element, "borderLeft"), right = goog.style.getIePixelBorder_(element, "borderRight"), top = goog.style.getIePixelBorder_(element, "borderTop"), bottom = goog.style.getIePixelBorder_(element, "borderBottom");
    return new goog.math.Box(top, right, bottom, left)
  }else {
    left = goog.style.getComputedStyle(element, "borderLeftWidth");
    right = goog.style.getComputedStyle(element, "borderRightWidth");
    top = goog.style.getComputedStyle(element, "borderTopWidth");
    bottom = goog.style.getComputedStyle(element, "borderBottomWidth");
    return new goog.math.Box(parseFloat(top), parseFloat(right), parseFloat(bottom), parseFloat(left))
  }
};
goog.style.getFontFamily = function(el) {
  var doc = goog.dom.getOwnerDocument(el), font = "";
  if(doc.createTextRange) {
    var range = doc.body.createTextRange();
    range.moveToElementText(el);
    font = range.queryCommandValue("FontName")
  }if(!font) {
    font = goog.style.getStyle_(el, "fontFamily");
    if(goog.userAgent.OPERA && goog.userAgent.LINUX)font = font.replace(/ \[[^\]]*\]/, "")
  }var fontsArray = font.split(",");
  if(fontsArray.length > 1)font = fontsArray[0];
  return goog.string.stripQuotes(font, "\"'")
};
goog.style.lengthUnitRegex_ = /[^\d]+$/;
goog.style.getLengthUnits = function(value) {
  var units = value.match(goog.style.lengthUnitRegex_);
  return units && units[0] || null
};
goog.style.ABSOLUTE_CSS_LENGTH_UNITS_ = {cm:1, "in":1, mm:1, pc:1, pt:1};
goog.style.CONVERTIBLE_RELATIVE_CSS_UNITS_ = {em:1, ex:1};
goog.style.getFontSize = function(el) {
  var fontSize = goog.style.getStyle_(el, "fontSize"), sizeUnits = goog.style.getLengthUnits(fontSize);
  if(fontSize && "px" == sizeUnits)return parseInt(fontSize, 10);
  if(goog.userAgent.IE)if(sizeUnits in goog.style.ABSOLUTE_CSS_LENGTH_UNITS_)return goog.style.getIePixelValue_(el, fontSize, "left", "pixelLeft");
  else if(el.parentNode && el.parentNode.nodeType == goog.dom.NodeType.ELEMENT && sizeUnits in goog.style.CONVERTIBLE_RELATIVE_CSS_UNITS_) {
    var parentElement = el.parentNode, parentSize = goog.style.getStyle_(parentElement, "fontSize");
    return goog.style.getIePixelValue_(parentElement, fontSize == parentSize ? "1em" : fontSize, "left", "pixelLeft")
  }var sizeElement = goog.dom.createDom("span", {style:"visibility:hidden;position:absolute;line-height:0;padding:0;margin:0;border:0;height:1em;"});
  goog.dom.appendChild(el, sizeElement);
  fontSize = sizeElement.offsetHeight;
  goog.dom.removeNode(sizeElement);
  return fontSize
};
goog.style.parseStyleAttribute = function(value) {
  var result = {};
  goog.array.forEach(value.split(/\s*;\s*/), function(pair) {
    var keyValue = pair.split(/\s*:\s*/);
    if(keyValue.length == 2)result[goog.style.toCamelCase(keyValue[0].toLowerCase())] = keyValue[1]
  });
  return result
};
goog.style.toStyleAttribute = function(obj) {
  var buffer = [];
  goog.object.forEach(obj, function(value, key) {
    buffer.push(goog.style.toSelectorCase(key), ":", value, ";")
  });
  return buffer.join("")
};
goog.style.setFloat = function(el, value) {
  el.style[goog.userAgent.IE ? "styleFloat" : "cssFloat"] = value
};
goog.style.getFloat = function(el) {
  return el.style[goog.userAgent.IE ? "styleFloat" : "cssFloat"] || ""
};goog.ui = {};
goog.ui.IdGenerator = function() {
};
goog.addSingletonGetter(goog.ui.IdGenerator);
goog.ui.IdGenerator.prototype.nextId_ = 0;
goog.ui.IdGenerator.prototype.getNextUniqueId = function() {
  return":" + (this.nextId_++).toString(36)
};
goog.ui.IdGenerator.instance = goog.ui.IdGenerator.getInstance();goog.ui.Component = function(opt_domHelper) {
  goog.events.EventTarget.call(this);
  this.dom_ = opt_domHelper || goog.dom.getDomHelper();
  this.rightToLeft_ = goog.ui.Component.defaultRightToLeft_
};
goog.inherits(goog.ui.Component, goog.events.EventTarget);
goog.ui.Component.prototype.idGenerator_ = goog.ui.IdGenerator.getInstance();
goog.ui.Component.defaultRightToLeft_ = null;
goog.ui.Component.EventType = {BEFORE_SHOW:"beforeshow", SHOW:"show", HIDE:"hide", DISABLE:"disable", ENABLE:"enable", HIGHLIGHT:"highlight", UNHIGHLIGHT:"unhighlight", ACTIVATE:"activate", DEACTIVATE:"deactivate", SELECT:"select", UNSELECT:"unselect", CHECK:"check", UNCHECK:"uncheck", FOCUS:"focus", BLUR:"blur", OPEN:"open", CLOSE:"close", ENTER:"enter", LEAVE:"leave", ACTION:"action", CHANGE:"change"};
goog.ui.Component.Error = {NOT_SUPPORTED:"Method not supported", DECORATE_INVALID:"Invalid element to decorate", ALREADY_RENDERED:"Component already rendered", PARENT_UNABLE_TO_BE_SET:"Unable to set parent component", CHILD_INDEX_OUT_OF_BOUNDS:"Child component index out of bounds", NOT_OUR_CHILD:"Child is not in parent component", NOT_IN_DOCUMENT:"Operation not supported while component is not in document", STATE_INVALID:"Invalid component state"};
goog.ui.Component.State = {ALL:255, DISABLED:1, HOVER:2, ACTIVE:4, SELECTED:8, CHECKED:16, FOCUSED:32, OPENED:64};
goog.ui.Component.getStateTransitionEvent = function(state, isEntering) {
  switch(state) {
    case goog.ui.Component.State.DISABLED:
      return isEntering ? goog.ui.Component.EventType.DISABLE : goog.ui.Component.EventType.ENABLE;
    case goog.ui.Component.State.HOVER:
      return isEntering ? goog.ui.Component.EventType.HIGHLIGHT : goog.ui.Component.EventType.UNHIGHLIGHT;
    case goog.ui.Component.State.ACTIVE:
      return isEntering ? goog.ui.Component.EventType.ACTIVATE : goog.ui.Component.EventType.DEACTIVATE;
    case goog.ui.Component.State.SELECTED:
      return isEntering ? goog.ui.Component.EventType.SELECT : goog.ui.Component.EventType.UNSELECT;
    case goog.ui.Component.State.CHECKED:
      return isEntering ? goog.ui.Component.EventType.CHECK : goog.ui.Component.EventType.UNCHECK;
    case goog.ui.Component.State.FOCUSED:
      return isEntering ? goog.ui.Component.EventType.FOCUS : goog.ui.Component.EventType.BLUR;
    case goog.ui.Component.State.OPENED:
      return isEntering ? goog.ui.Component.EventType.OPEN : goog.ui.Component.EventType.CLOSE;
    default:
  }
  throw Error(goog.ui.Component.Error.STATE_INVALID);
};
goog.ui.Component.setDefaultRightToLeft = function(rightToLeft) {
  goog.ui.Component.defaultRightToLeft_ = rightToLeft
};
a = goog.ui.Component.prototype;
a.id_ = null;
a.dom_ = null;
a.inDocument_ = false;
a.element_ = null;
a.rightToLeft_ = null;
a.model_ = null;
a.parent_ = null;
a.children_ = null;
a.childIndex_ = null;
a.wasDecorated_ = false;
a.getId = function() {
  return this.id_ || (this.id_ = this.idGenerator_.getNextUniqueId())
};
a.getElement = function() {
  return this.element_
};
a.setParent = function(parent) {
  if(this == parent)throw Error(goog.ui.Component.Error.PARENT_UNABLE_TO_BE_SET);if(parent && this.parent_ && this.id_ && this.parent_.getChild(this.id_) && this.parent_ != parent)throw Error(goog.ui.Component.Error.PARENT_UNABLE_TO_BE_SET);this.parent_ = parent;
  goog.ui.Component.superClass_.setParentEventTarget.call(this, parent)
};
a.getParent = function() {
  return this.parent_
};
a.setParentEventTarget = function(parent) {
  if(this.parent_ && this.parent_ != parent)throw Error(goog.ui.Component.Error.NOT_SUPPORTED);goog.ui.Component.superClass_.setParentEventTarget.call(this, parent)
};
a.getDomHelper = function() {
  return this.dom_
};
a.isInDocument = function() {
  return this.inDocument_
};
a.createDom = function() {
  this.element_ = this.dom_.createElement("div")
};
a.decorate = function(element) {
  if(this.inDocument_)throw Error(goog.ui.Component.Error.ALREADY_RENDERED);else if(element && this.canDecorate(element)) {
    this.wasDecorated_ = true;
    if(!this.dom_ || this.dom_.getDocument() != goog.dom.getOwnerDocument(element))this.dom_ = goog.dom.getDomHelper(element);
    this.decorateInternal(element);
    this.enterDocument()
  }else throw Error(goog.ui.Component.Error.DECORATE_INVALID);
};
a.canDecorate = function() {
  return true
};
a.decorateInternal = function(element) {
  this.element_ = element
};
a.enterDocument = function() {
  this.inDocument_ = true;
  this.forEachChild(function(child) {
    !child.isInDocument() && child.getElement() && child.enterDocument()
  })
};
a.exitDocument = function() {
  this.forEachChild(function(child) {
    child.isInDocument() && child.exitDocument()
  });
  this.googUiComponentHandler_ && this.googUiComponentHandler_.removeAll();
  this.inDocument_ = false
};
a.disposeInternal = function() {
  goog.ui.Component.superClass_.disposeInternal.call(this);
  this.inDocument_ && this.exitDocument();
  if(this.googUiComponentHandler_) {
    this.googUiComponentHandler_.dispose();
    delete this.googUiComponentHandler_
  }this.forEachChild(function(child) {
    child.dispose()
  });
  !this.wasDecorated_ && this.element_ && goog.dom.removeNode(this.element_);
  this.parent_ = this.model_ = this.element_ = this.childIndex_ = this.children_ = null
};
a.isRightToLeft = function() {
  if(this.rightToLeft_ == null)this.rightToLeft_ = goog.style.isRightToLeft(this.inDocument_ ? this.element_ : this.dom_.getDocument().body);
  return this.rightToLeft_
};
a.hasChildren = function() {
  return!!this.children_ && this.children_.length != 0
};
a.getChild = function(id) {
  return this.childIndex_ && id ? goog.object.get(this.childIndex_, id) || null : null
};
a.getChildAt = function(index) {
  return this.children_ ? this.children_[index] || null : null
};
a.forEachChild = function(f, opt_obj) {
  this.children_ && goog.array.forEach(this.children_, f, opt_obj)
};
a.removeChild = function(child, opt_unrender) {
  if(child) {
    var id = goog.isString(child) ? child : child.getId();
    child = this.getChild(id);
    if(id && child) {
      goog.object.remove(this.childIndex_, id);
      goog.array.remove(this.children_, child);
      if(opt_unrender) {
        child.exitDocument();
        child.element_ && goog.dom.removeNode(child.element_)
      }child.setParent(null)
    }
  }if(!child)throw Error(goog.ui.Component.Error.NOT_OUR_CHILD);return child
};
a.removeChildAt = function(index, opt_unrender) {
  return this.removeChild(this.getChildAt(index), opt_unrender)
};
a.removeChildren = function(opt_unrender) {
  for(;this.hasChildren();)this.removeChildAt(0, opt_unrender)
};goog.ui.TableSorter = function(opt_domHelper) {
  goog.ui.Component.call(this, opt_domHelper);
  this.column_ = -1;
  this.reversed_ = false;
  this.defaultSortFunction_ = goog.ui.TableSorter.numericSort;
  this.sortFunctions_ = []
};
goog.inherits(goog.ui.TableSorter, goog.ui.Component);
goog.ui.TableSorter.EventType = {BEFORESORT:"beforesort", SORT:"sort"};
a = goog.ui.TableSorter.prototype;
a.canDecorate = function(element) {
  return element.tagName == goog.dom.TagName.TABLE
};
a.enterDocument = function() {
  goog.ui.TableSorter.superClass_.enterDocument.call(this);
  var headerRow = this.getElement().getElementsByTagName(goog.dom.TagName.TR)[0];
  goog.events.listen(headerRow, goog.events.EventType.CLICK, this.sort_, false, this)
};
a.setDefaultSortFunction = function(sortFunction) {
  this.defaultSortFunction_ = sortFunction
};
a.getSortFunction = function(column) {
  return this.sortFunctions_[column] || this.defaultSortFunction_
};
a.setSortFunction = function(column, sortFunction) {
  this.sortFunctions_[column] = sortFunction
};
a.sort_ = function(e) {
  var col = goog.dom.getAncestorByTagNameAndClass(e.target, goog.dom.TagName.TH).cellIndex, reverse = col == this.column_ ? !this.reversed_ : false;
  if(this.dispatchEvent(goog.ui.TableSorter.EventType.BEFORESORT)) {
    this.sort(col, reverse);
    this.dispatchEvent(goog.ui.TableSorter.EventType.SORT)
  }
};
a.sort = function(column, opt_reverse) {
  var table = this.getElement(), tBody = table.tBodies[0], rows = tBody.rows, headers = table.tHead.rows[0].cells;
  if(this.column_ >= 0)goog.dom.classes.remove(headers[this.column_], this.reversed_ ? "goog-tablesorter-sorted-reverse" : "goog-tablesorter-sorted");
  this.reversed_ = !!opt_reverse;
  for(var header = headers[column], values = [], i = 0, len = rows.length;i < len;i++) {
    var row = rows[i], value = goog.dom.getTextContent(row.cells[column]);
    values.push([value, row])
  }var sortFunction = this.getSortFunction(column), multiplier = this.reversed_ ? -1 : 1;
  goog.array.stableSort(values, function(a, b) {
    return sortFunction(a[0], b[0]) * multiplier
  });
  table.removeChild(tBody);
  for(i = 0;i < len;i++)tBody.appendChild(values[i][1]);
  table.insertBefore(tBody, table.tBodies[0] || null);
  this.column_ = column;
  goog.dom.classes.add(header, this.reversed_ ? "goog-tablesorter-sorted-reverse" : "goog-tablesorter-sorted")
};
goog.ui.TableSorter.numericSort = function(a, b) {
  return parseFloat(a) - parseFloat(b)
};
goog.ui.TableSorter.alphaSort = goog.array.defaultCompare;
goog.ui.TableSorter.createReverseSort = function(sortFunction) {
  return function(a, b) {
    return-1 * sortFunction(a, b)
  }
};goog.positioning = {};
goog.positioning.Corner = {TOP_LEFT:0, TOP_RIGHT:2, BOTTOM_LEFT:1, BOTTOM_RIGHT:3, TOP_START:4, TOP_END:6, BOTTOM_START:5, BOTTOM_END:7};
goog.positioning.CornerBit = {BOTTOM:1, RIGHT:2, FLIP_RTL:4};
goog.positioning.Overflow = {IGNORE:0, ADJUST_X:1, FAIL_X:2, ADJUST_Y:4, FAIL_Y:8, RESIZE_WIDTH:16, RESIZE_HEIGHT:32};
goog.positioning.OverflowStatus = {NONE:0, ADJUSTED_X:1, ADJUSTED_Y:2, WIDTH_ADJUSTED:4, HEIGHT_ADJUSTED:8, FAILED_LEFT:16, FAILED_RIGHT:32, FAILED_TOP:64, FAILED_BOTTOM:128, FAILED_OUTSIDE_VIEWPORT:256};
goog.positioning.OverflowStatus.FAILED = goog.positioning.OverflowStatus.FAILED_LEFT | goog.positioning.OverflowStatus.FAILED_RIGHT | goog.positioning.OverflowStatus.FAILED_TOP | goog.positioning.OverflowStatus.FAILED_BOTTOM | goog.positioning.OverflowStatus.FAILED_OUTSIDE_VIEWPORT;
goog.positioning.positionAtAnchor = function(anchorElement, anchorElementCorner, movableElement, movableElementCorner, opt_offset, opt_margin, opt_overflow, opt_preferredSize) {
  var moveableParentTopLeft, parent = movableElement.offsetParent;
  if(parent) {
    var isBody = parent.tagName == goog.dom.TagName.HTML || parent.tagName == goog.dom.TagName.BODY;
    if(!isBody || goog.style.getComputedPosition(parent) != "static") {
      moveableParentTopLeft = goog.style.getPageOffset(parent);
      isBody || (moveableParentTopLeft = goog.math.Coordinate.difference(moveableParentTopLeft, new goog.math.Coordinate(parent.scrollLeft, parent.scrollTop)))
    }
  }var anchorRect = goog.positioning.getVisiblePart_(anchorElement);
  goog.style.translateRectForAnotherFrame(anchorRect, goog.dom.getDomHelper(anchorElement), goog.dom.getDomHelper(movableElement));
  var corner = goog.positioning.getEffectiveCorner(anchorElement, anchorElementCorner), absolutePos = new goog.math.Coordinate(corner & goog.positioning.CornerBit.RIGHT ? anchorRect.left + anchorRect.width : anchorRect.left, corner & goog.positioning.CornerBit.BOTTOM ? anchorRect.top + anchorRect.height : anchorRect.top);
  if(moveableParentTopLeft)absolutePos = goog.math.Coordinate.difference(absolutePos, moveableParentTopLeft);
  if(opt_offset) {
    absolutePos.x += (corner & goog.positioning.CornerBit.RIGHT ? -1 : 1) * opt_offset.x;
    absolutePos.y += (corner & goog.positioning.CornerBit.BOTTOM ? -1 : 1) * opt_offset.y
  }var viewport;
  if(opt_overflow)if((viewport = goog.style.getVisibleRectForElement(movableElement)) && moveableParentTopLeft) {
    viewport.top = Math.max(0, viewport.top - moveableParentTopLeft.y);
    viewport.right -= moveableParentTopLeft.x;
    viewport.bottom -= moveableParentTopLeft.y;
    viewport.left = Math.max(0, viewport.left - moveableParentTopLeft.x)
  }return goog.positioning.positionAtCoordinate(absolutePos, movableElement, movableElementCorner, opt_margin, viewport, opt_overflow, opt_preferredSize)
};
goog.positioning.getVisiblePart_ = function(el) {
  var rect = goog.style.getBounds(el), visibleBox = goog.style.getVisibleRectForElement(el);
  visibleBox && rect.intersection(goog.math.Rect.createFromBox(visibleBox));
  return rect
};
goog.positioning.positionAtCoordinate = function(absolutePos, movableElement, movableElementCorner, opt_margin, opt_viewport, opt_overflow, opt_preferredSize) {
  absolutePos = absolutePos.clone();
  var status = goog.positioning.OverflowStatus.NONE, corner = goog.positioning.getEffectiveCorner(movableElement, movableElementCorner), elementSize = goog.style.getSize(movableElement), size = opt_preferredSize ? opt_preferredSize.clone() : elementSize;
  if(opt_margin || corner != goog.positioning.Corner.TOP_LEFT) {
    if(corner & goog.positioning.CornerBit.RIGHT)absolutePos.x -= size.width + (opt_margin ? opt_margin.right : 0);
    else if(opt_margin)absolutePos.x += opt_margin.left;
    if(corner & goog.positioning.CornerBit.BOTTOM)absolutePos.y -= size.height + (opt_margin ? opt_margin.bottom : 0);
    else if(opt_margin)absolutePos.y += opt_margin.top
  }if(opt_overflow) {
    status = opt_viewport ? goog.positioning.adjustForViewport(absolutePos, size, opt_viewport, opt_overflow) : goog.positioning.OverflowStatus.FAILED_OUTSIDE_VIEWPORT;
    if(status & goog.positioning.OverflowStatus.FAILED)return status
  }goog.style.setPosition(movableElement, absolutePos);
  goog.math.Size.equals(elementSize, size) || goog.style.setSize(movableElement, size);
  return status
};
goog.positioning.adjustForViewport = function(pos, size, viewport, overflow) {
  var status = goog.positioning.OverflowStatus.NONE;
  if(pos.x < viewport.left && overflow & goog.positioning.Overflow.ADJUST_X) {
    pos.x = viewport.left;
    status |= goog.positioning.OverflowStatus.ADJUSTED_X
  }if(pos.x < viewport.left && pos.x + size.width > viewport.right && overflow & goog.positioning.Overflow.RESIZE_WIDTH) {
    size.width -= pos.x + size.width - viewport.right;
    status |= goog.positioning.OverflowStatus.WIDTH_ADJUSTED
  }if(pos.x + size.width > viewport.right && overflow & goog.positioning.Overflow.ADJUST_X) {
    pos.x = Math.max(viewport.right - size.width, viewport.left);
    status |= goog.positioning.OverflowStatus.ADJUSTED_X
  }if(overflow & goog.positioning.Overflow.FAIL_X)status |= (pos.x < viewport.left ? goog.positioning.OverflowStatus.FAILED_LEFT : 0) | (pos.x + size.width > viewport.right ? goog.positioning.OverflowStatus.FAILED_RIGHT : 0);
  if(pos.y < viewport.top && overflow & goog.positioning.Overflow.ADJUST_Y) {
    pos.y = viewport.top;
    status |= goog.positioning.OverflowStatus.ADJUSTED_Y
  }if(pos.y >= viewport.top && pos.y + size.height > viewport.bottom && overflow & goog.positioning.Overflow.RESIZE_HEIGHT) {
    size.height -= pos.y + size.height - viewport.bottom;
    status |= goog.positioning.OverflowStatus.HEIGHT_ADJUSTED
  }if(pos.y + size.height > viewport.bottom && overflow & goog.positioning.Overflow.ADJUST_Y) {
    pos.y = Math.max(viewport.bottom - size.height, viewport.top);
    status |= goog.positioning.OverflowStatus.ADJUSTED_Y
  }if(overflow & goog.positioning.Overflow.FAIL_Y)status |= (pos.y < viewport.top ? goog.positioning.OverflowStatus.FAILED_TOP : 0) | (pos.y + size.height > viewport.bottom ? goog.positioning.OverflowStatus.FAILED_BOTTOM : 0);
  return status
};
goog.positioning.getEffectiveCorner = function(element, corner) {
  return(corner & goog.positioning.CornerBit.FLIP_RTL && goog.style.isRightToLeft(element) ? corner ^ goog.positioning.CornerBit.RIGHT : corner) & ~goog.positioning.CornerBit.FLIP_RTL
};
goog.positioning.flipCornerHorizontal = function(corner) {
  return corner ^ goog.positioning.CornerBit.RIGHT
};
goog.positioning.flipCornerVertical = function(corner) {
  return corner ^ goog.positioning.CornerBit.BOTTOM
};
goog.positioning.flipCorner = function(corner) {
  return corner ^ goog.positioning.CornerBit.BOTTOM ^ goog.positioning.CornerBit.RIGHT
};goog.positioning.AbstractPosition = function() {
};
goog.positioning.AbstractPosition.prototype.reposition = function() {
};goog.positioning.AnchoredPosition = function(anchorElement, corner) {
  this.element = anchorElement;
  this.corner = corner
};
goog.inherits(goog.positioning.AnchoredPosition, goog.positioning.AbstractPosition);
goog.positioning.AnchoredPosition.prototype.reposition = function(movableElement, movableCorner, opt_margin) {
  goog.positioning.positionAtAnchor(this.element, this.corner, movableElement, movableCorner, undefined, opt_margin)
};goog.positioning.ViewportPosition = function(arg1, opt_arg2) {
  this.coordinate = arg1 instanceof goog.math.Coordinate ? arg1 : new goog.math.Coordinate(arg1, opt_arg2)
};
goog.inherits(goog.positioning.ViewportPosition, goog.positioning.AbstractPosition);
goog.positioning.ViewportPosition.prototype.reposition = function(element, popupCorner, opt_margin, opt_preferredSize) {
  goog.positioning.positionAtAnchor(goog.style.getClientViewportElement(element), goog.positioning.Corner.TOP_LEFT, element, popupCorner, this.coordinate, opt_margin, null, opt_preferredSize)
};goog.positioning.AbsolutePosition = function(arg1, opt_arg2) {
  this.coordinate = arg1 instanceof goog.math.Coordinate ? arg1 : new goog.math.Coordinate(arg1, opt_arg2)
};
goog.inherits(goog.positioning.AbsolutePosition, goog.positioning.AbstractPosition);
goog.positioning.AbsolutePosition.prototype.reposition = function(movableElement, movableCorner, opt_margin, opt_preferredSize) {
  goog.positioning.positionAtCoordinate(this.coordinate, movableElement, movableCorner, opt_margin, null, null, opt_preferredSize)
};goog.positioning.AnchoredViewportPosition = function(anchorElement, corner, opt_adjust) {
  goog.positioning.AnchoredPosition.call(this, anchorElement, corner);
  this.adjust_ = opt_adjust
};
goog.inherits(goog.positioning.AnchoredViewportPosition, goog.positioning.AnchoredPosition);
goog.positioning.AnchoredViewportPosition.prototype.reposition = function(movableElement, movableCorner, opt_margin, opt_preferredSize) {
  var status = goog.positioning.positionAtAnchor(this.element, this.corner, movableElement, movableCorner, null, opt_margin, goog.positioning.Overflow.FAIL_X | goog.positioning.Overflow.FAIL_Y, opt_preferredSize) & goog.positioning.OverflowStatus.FAILED;
  if(status)if(status = goog.positioning.positionAtAnchor(this.element, movableCorner, movableElement, this.corner, null, opt_margin, goog.positioning.Overflow.FAIL_X | goog.positioning.Overflow.FAIL_Y, opt_preferredSize) & goog.positioning.OverflowStatus.FAILED)this.adjust_ ? goog.positioning.positionAtAnchor(this.element, this.corner, movableElement, movableCorner, null, opt_margin, goog.positioning.Overflow.ADJUST_X | goog.positioning.Overflow.ADJUST_Y, opt_preferredSize) : goog.positioning.positionAtAnchor(this.element, 
  this.corner, movableElement, movableCorner, null, opt_margin, goog.positioning.Overflow.IGNORE, opt_preferredSize)
};goog.positioning.ClientPosition = function(arg1, opt_arg2) {
  this.coordinate = arg1 instanceof goog.math.Coordinate ? arg1 : new goog.math.Coordinate(arg1, opt_arg2)
};
goog.inherits(goog.positioning.ClientPosition, goog.positioning.AbstractPosition);
goog.positioning.ClientPosition.prototype.reposition = function(element, popupCorner, opt_margin, opt_preferredSize) {
  var viewportElt = goog.style.getClientViewportElement(element), clientPos = new goog.math.Coordinate(this.coordinate.x + viewportElt.scrollLeft, this.coordinate.y + viewportElt.scrollTop);
  goog.positioning.positionAtAnchor(viewportElt, goog.positioning.Corner.TOP_LEFT, element, popupCorner, clientPos, opt_margin, null, opt_preferredSize)
};goog.positioning.ViewportClientPosition = function(arg1, opt_arg2) {
  goog.positioning.ClientPosition.call(this, arg1, opt_arg2)
};
goog.inherits(goog.positioning.ViewportClientPosition, goog.positioning.ClientPosition);
goog.positioning.ViewportClientPosition.prototype.reposition = function(element, popupCorner, opt_margin, opt_preferredSize) {
  var viewportElt = goog.style.getClientViewportElement(element), viewport = goog.style.getVisibleRectForElement(viewportElt), scrollEl = goog.dom.getDomHelper(element).getDocumentScrollElement(), clientPos = new goog.math.Coordinate(this.coordinate.x + scrollEl.scrollLeft, this.coordinate.y + scrollEl.scrollTop), failXY = goog.positioning.Overflow.FAIL_X | goog.positioning.Overflow.FAIL_Y, corner = popupCorner, status = goog.positioning.positionAtCoordinate(clientPos, element, corner, opt_margin, 
  viewport, failXY, opt_preferredSize);
  if((status & goog.positioning.OverflowStatus.FAILED) != 0) {
    if(status & goog.positioning.OverflowStatus.FAILED_LEFT || status & goog.positioning.OverflowStatus.FAILED_RIGHT)corner = goog.positioning.flipCornerHorizontal(corner);
    if(status & goog.positioning.OverflowStatus.FAILED_TOP || status & goog.positioning.OverflowStatus.FAILED_BOTTOM)corner = goog.positioning.flipCornerVertical(corner);
    status = goog.positioning.positionAtCoordinate(clientPos, element, corner, opt_margin, viewport, failXY, opt_preferredSize);
    (status & goog.positioning.OverflowStatus.FAILED) != 0 && goog.positioning.positionAtCoordinate(clientPos, element, popupCorner, opt_margin, viewport, undefined, opt_preferredSize)
  }
};goog.events.KeyCodes = {MAC_ENTER:3, BACKSPACE:8, TAB:9, NUM_CENTER:12, ENTER:13, SHIFT:16, CTRL:17, ALT:18, PAUSE:19, CAPS_LOCK:20, ESC:27, SPACE:32, PAGE_UP:33, PAGE_DOWN:34, END:35, HOME:36, LEFT:37, UP:38, RIGHT:39, DOWN:40, PRINT_SCREEN:44, INSERT:45, DELETE:46, ZERO:48, ONE:49, TWO:50, THREE:51, FOUR:52, FIVE:53, SIX:54, SEVEN:55, EIGHT:56, NINE:57, QUESTION_MARK:63, A:65, B:66, C:67, D:68, E:69, F:70, G:71, H:72, I:73, J:74, K:75, L:76, M:77, N:78, O:79, P:80, Q:81, R:82, S:83, T:84, U:85, 
V:86, W:87, X:88, Y:89, Z:90, META:91, CONTEXT_MENU:93, NUM_ZERO:96, NUM_ONE:97, NUM_TWO:98, NUM_THREE:99, NUM_FOUR:100, NUM_FIVE:101, NUM_SIX:102, NUM_SEVEN:103, NUM_EIGHT:104, NUM_NINE:105, NUM_MULTIPLY:106, NUM_PLUS:107, NUM_MINUS:109, NUM_PERIOD:110, NUM_DIVISION:111, F1:112, F2:113, F3:114, F4:115, F5:116, F6:117, F7:118, F8:119, F9:120, F10:121, F11:122, F12:123, NUMLOCK:144, SEMICOLON:186, DASH:189, EQUALS:187, COMMA:188, PERIOD:190, SLASH:191, APOSTROPHE:192, SINGLE_QUOTE:222, OPEN_SQUARE_BRACKET:219, 
BACKSLASH:220, CLOSE_SQUARE_BRACKET:221, WIN_KEY:224, MAC_FF_META:224, WIN_IME:229};
goog.events.KeyCodes.isTextModifyingKeyEvent = function(e) {
  if(e.altKey && !e.ctrlKey || e.metaKey || e.keyCode >= goog.events.KeyCodes.F1 && e.keyCode <= goog.events.KeyCodes.F12)return false;
  switch(e.keyCode) {
    case goog.events.KeyCodes.ALT:
    ;
    case goog.events.KeyCodes.SHIFT:
    ;
    case goog.events.KeyCodes.CTRL:
    ;
    case goog.events.KeyCodes.PAUSE:
    ;
    case goog.events.KeyCodes.CAPS_LOCK:
    ;
    case goog.events.KeyCodes.ESC:
    ;
    case goog.events.KeyCodes.PAGE_UP:
    ;
    case goog.events.KeyCodes.PAGE_DOWN:
    ;
    case goog.events.KeyCodes.HOME:
    ;
    case goog.events.KeyCodes.END:
    ;
    case goog.events.KeyCodes.LEFT:
    ;
    case goog.events.KeyCodes.RIGHT:
    ;
    case goog.events.KeyCodes.UP:
    ;
    case goog.events.KeyCodes.DOWN:
    ;
    case goog.events.KeyCodes.INSERT:
    ;
    case goog.events.KeyCodes.NUMLOCK:
    ;
    case goog.events.KeyCodes.CONTEXT_MENU:
    ;
    case goog.events.KeyCodes.PRINT_SCREEN:
      return false;
    default:
      return true
  }
};
goog.events.KeyCodes.firesKeyPressEvent = function(keyCode, opt_heldKeyCode, opt_shiftKey, opt_ctrlKey, opt_altKey) {
  if(!goog.userAgent.IE && !(goog.userAgent.WEBKIT && goog.userAgent.isVersion("525")))return true;
  if(goog.userAgent.MAC && opt_altKey)return goog.events.KeyCodes.isCharacterKey(keyCode);
  if(opt_altKey && !opt_ctrlKey)return false;
  if(goog.userAgent.IE && !opt_shiftKey && (opt_heldKeyCode == goog.events.KeyCodes.CTRL || opt_heldKeyCode == goog.events.KeyCodes.ALT))return false;
  if(goog.userAgent.IE && opt_ctrlKey && opt_heldKeyCode == keyCode)return false;
  switch(keyCode) {
    case goog.events.KeyCodes.ENTER:
      return true;
    case goog.events.KeyCodes.ESC:
      return!goog.userAgent.WEBKIT
  }
  return goog.events.KeyCodes.isCharacterKey(keyCode)
};
goog.events.KeyCodes.isCharacterKey = function(keyCode) {
  if(keyCode >= goog.events.KeyCodes.ZERO && keyCode <= goog.events.KeyCodes.NINE)return true;
  if(keyCode >= goog.events.KeyCodes.NUM_ZERO && keyCode <= goog.events.KeyCodes.NUM_MULTIPLY)return true;
  if(keyCode >= goog.events.KeyCodes.A && keyCode <= goog.events.KeyCodes.Z)return true;
  switch(keyCode) {
    case goog.events.KeyCodes.SPACE:
    ;
    case goog.events.KeyCodes.QUESTION_MARK:
    ;
    case goog.events.KeyCodes.NUM_PLUS:
    ;
    case goog.events.KeyCodes.NUM_MINUS:
    ;
    case goog.events.KeyCodes.NUM_PERIOD:
    ;
    case goog.events.KeyCodes.NUM_DIVISION:
    ;
    case goog.events.KeyCodes.SEMICOLON:
    ;
    case goog.events.KeyCodes.DASH:
    ;
    case goog.events.KeyCodes.EQUALS:
    ;
    case goog.events.KeyCodes.COMMA:
    ;
    case goog.events.KeyCodes.PERIOD:
    ;
    case goog.events.KeyCodes.SLASH:
    ;
    case goog.events.KeyCodes.APOSTROPHE:
    ;
    case goog.events.KeyCodes.SINGLE_QUOTE:
    ;
    case goog.events.KeyCodes.OPEN_SQUARE_BRACKET:
    ;
    case goog.events.KeyCodes.BACKSLASH:
    ;
    case goog.events.KeyCodes.CLOSE_SQUARE_BRACKET:
      return true;
    default:
      return false
  }
};goog.ui.PopupBase = function(opt_element, opt_type) {
  this.handler_ = new goog.events.EventHandler(this);
  this.setElement(opt_element || null);
  opt_type && this.setType(opt_type)
};
goog.inherits(goog.ui.PopupBase, goog.events.EventTarget);
goog.ui.PopupBase.Type = {TOGGLE_DISPLAY:"toggle_display", MOVE_OFFSCREEN:"move_offscreen"};
a = goog.ui.PopupBase.prototype;
a.element_ = null;
a.autoHide_ = true;
a.autoHideRegion_ = null;
a.isVisible_ = false;
a.shouldHideAsync_ = false;
a.lastShowTime_ = -1;
a.lastHideTime_ = -1;
a.hideOnEscape_ = false;
a.enableCrossIframeDismissal_ = true;
a.type_ = goog.ui.PopupBase.Type.TOGGLE_DISPLAY;
goog.ui.PopupBase.EventType = {BEFORE_SHOW:"beforeshow", SHOW:"show", BEFORE_HIDE:"beforehide", HIDE:"hide"};
goog.ui.PopupBase.DEBOUNCE_DELAY_MS = 150;
a = goog.ui.PopupBase.prototype;
a.getType = function() {
  return this.type_
};
a.setType = function(type) {
  this.type_ = type
};
a.getElement = function() {
  return this.element_
};
a.setElement = function(elt) {
  this.ensureNotVisible_();
  this.element_ = elt
};
a.ensureNotVisible_ = function() {
  if(this.isVisible_)throw Error("Can not change this state of the popup while showing.");
};
a.isVisible = function() {
  return this.isVisible_
};
a.setVisible = function(visible) {
  visible ? this.show_() : this.hide_()
};
a.reposition = function() {
};
a.show_ = function() {
  if(!this.isVisible_)if(this.onBeforeShow()) {
    if(!this.element_)throw Error("Caller must call setElement before trying to show the popup");this.reposition();
    var doc = goog.dom.getOwnerDocument(this.element_);
    this.hideOnEscape_ && this.handler_.listen(doc, goog.events.EventType.KEYDOWN, this.onDocumentKeyDown_, true);
    if(this.autoHide_) {
      this.handler_.listen(doc, goog.events.EventType.MOUSEDOWN, this.onDocumentMouseDown_, true);
      if(goog.userAgent.IE) {
        for(var activeElement = doc.activeElement;activeElement && activeElement.nodeName == "IFRAME";) {
          try {
            var tempDoc = goog.dom.getFrameContentDocument(activeElement)
          }catch(e) {
            break
          }doc = tempDoc;
          activeElement = doc.activeElement
        }this.handler_.listen(doc, goog.events.EventType.MOUSEDOWN, this.onDocumentMouseDown_, true);
        this.handler_.listen(doc, goog.events.EventType.DEACTIVATE, this.onDocumentBlur_)
      }else this.handler_.listen(doc, goog.events.EventType.BLUR, this.onDocumentBlur_)
    }if(this.type_ == goog.ui.PopupBase.Type.TOGGLE_DISPLAY)this.showPopupElement();
    else this.type_ == goog.ui.PopupBase.Type.MOVE_OFFSCREEN && this.reposition();
    this.isVisible_ = true;
    this.onShow_()
  }
};
a.hide_ = function(opt_target) {
  if(!this.isVisible_ || !this.onBeforeHide_(opt_target))return false;
  this.handler_ && this.handler_.removeAll();
  if(this.type_ == goog.ui.PopupBase.Type.TOGGLE_DISPLAY)this.shouldHideAsync_ ? goog.Timer.callOnce(this.hidePopupElement_, 0, this) : this.hidePopupElement_();
  else this.type_ == goog.ui.PopupBase.Type.MOVE_OFFSCREEN && this.moveOffscreen_();
  this.isVisible_ = false;
  this.onHide_(opt_target);
  return true
};
a.showPopupElement = function() {
  this.element_.style.visibility = "visible";
  goog.style.showElement(this.element_, true)
};
a.hidePopupElement_ = function() {
  this.element_.style.visibility = "hidden";
  goog.style.showElement(this.element_, false)
};
a.moveOffscreen_ = function() {
  this.element_.style.left = "-200px";
  this.element_.style.top = "-200px"
};
a.onBeforeShow = function() {
  return this.dispatchEvent(goog.ui.PopupBase.EventType.BEFORE_SHOW)
};
a.onShow_ = function() {
  this.lastShowTime_ = goog.now();
  this.lastHideTime_ = -1;
  this.dispatchEvent(goog.ui.PopupBase.EventType.SHOW)
};
a.onBeforeHide_ = function(opt_target) {
  return this.dispatchEvent({type:goog.ui.PopupBase.EventType.BEFORE_HIDE, target:opt_target})
};
a.onHide_ = function(opt_target) {
  this.lastHideTime_ = goog.now();
  this.dispatchEvent({type:goog.ui.PopupBase.EventType.HIDE, target:opt_target})
};
a.onDocumentMouseDown_ = function(e) {
  var target = e.target;
  if(!goog.dom.contains(this.element_, target) && (!this.autoHideRegion_ || goog.dom.contains(this.autoHideRegion_, target)) && !this.shouldDebounce_())this.hide_(target)
};
a.onDocumentKeyDown_ = function(e) {
  if(e.keyCode == goog.events.KeyCodes.ESC)if(this.hide_(e.target)) {
    e.preventDefault();
    e.stopPropagation()
  }
};
a.onDocumentBlur_ = function(e) {
  if(this.enableCrossIframeDismissal_) {
    var doc = goog.dom.getOwnerDocument(this.element_);
    if(goog.userAgent.IE || goog.userAgent.OPERA) {
      var activeElement = doc.activeElement;
      if(activeElement && goog.dom.contains(this.element_, activeElement))return
    }else if(e.target != doc)return;
    this.shouldDebounce_() || this.hide_()
  }
};
a.shouldDebounce_ = function() {
  return goog.now() - this.lastShowTime_ < goog.ui.PopupBase.DEBOUNCE_DELAY_MS
};
a.disposeInternal = function() {
  goog.ui.PopupBase.superClass_.disposeInternal.call(this);
  this.handler_.dispose();
  delete this.element_;
  delete this.handler_
};goog.ui.Popup = function(opt_element, opt_position) {
  this.popupCorner_ = goog.positioning.Corner.TOP_START;
  this.position_ = opt_position || undefined;
  goog.ui.PopupBase.call(this, opt_element)
};
goog.inherits(goog.ui.Popup, goog.ui.PopupBase);
goog.ui.Popup.Corner = goog.positioning.Corner;
goog.ui.Popup.Overflow = goog.positioning.Overflow;
goog.ui.Popup.prototype.getPosition = function() {
  return this.position_ || null
};
goog.ui.Popup.prototype.setPosition = function(position) {
  this.position_ = position || undefined;
  this.isVisible() && this.reposition()
};
goog.ui.Popup.prototype.reposition = function() {
  if(this.position_) {
    var hideForPositioning = !this.isVisible() && this.getType() != goog.ui.PopupBase.Type.MOVE_OFFSCREEN, el = this.getElement();
    if(hideForPositioning) {
      el.style.visibility = "hidden";
      goog.style.showElement(el, true)
    }this.position_.reposition(el, this.popupCorner_, this.margin_);
    hideForPositioning && goog.style.showElement(el, false)
  }
};
goog.ui.Popup.positionPopup = function(anchorElement, anchorElementCorner, movableElement, movableElementCorner, opt_offset, opt_margin, opt_overflow) {
  return(goog.positioning.positionAtAnchor(anchorElement, anchorElementCorner, movableElement, movableElementCorner, opt_offset, opt_margin, opt_overflow) & goog.positioning.OverflowStatus.FAILED) == 0
};
goog.ui.Popup.positionAtCoordinate = function(absolutePos, movableElement, movableElementCorner, opt_margin) {
  goog.positioning.positionAtCoordinate(absolutePos, movableElement, movableElementCorner, opt_margin);
  return true
};
goog.ui.Popup.AnchoredPosition = goog.positioning.AnchoredPosition;
goog.ui.Popup.AnchoredViewPortPosition = goog.positioning.AnchoredViewportPosition;
goog.ui.Popup.AbsolutePosition = goog.positioning.AbsolutePosition;
goog.ui.Popup.ViewPortPosition = goog.positioning.ViewportPosition;
goog.ui.Popup.ClientPosition = goog.positioning.ClientPosition;
goog.ui.Popup.ViewPortClientPosition = goog.positioning.ViewportClientPosition;goog.ui.Tooltip = function(opt_el, opt_str, opt_domHelper) {
  this.dom_ = opt_domHelper || (opt_el ? goog.dom.getDomHelper(goog.dom.getElement(opt_el)) : goog.dom.getDomHelper());
  goog.ui.Popup.call(this, this.dom_.createDom("div", {style:"position:absolute;display:none;"}));
  this.cursorPosition = new goog.math.Coordinate(1, 1);
  this.activeEl_ = null;
  this.elements_ = new goog.structs.Set;
  opt_el && this.attach(opt_el);
  opt_str != null && this.setText(opt_str)
};
goog.inherits(goog.ui.Tooltip, goog.ui.Popup);
goog.ui.Tooltip.activeInstances_ = [];
goog.ui.Tooltip.prototype.className = "goog-tooltip";
goog.ui.Tooltip.prototype.showDelayMs_ = 500;
goog.ui.Tooltip.prototype.hideDelayMs_ = 0;
goog.ui.Tooltip.State = {INACTIVE:0, WAITING_TO_SHOW:1, SHOWING:2, WAITING_TO_HIDE:3, UPDATING:4};
a = goog.ui.Tooltip.prototype;
a.getDomHelper = function() {
  return this.dom_
};
a.attach = function(el) {
  el = goog.dom.getElement(el);
  this.elements_.add(el);
  goog.events.listen(el, goog.events.EventType.MOUSEOVER, this.handleMouseOver, false, this);
  goog.events.listen(el, goog.events.EventType.MOUSEOUT, this.handleMouseOutAndBlur, false, this);
  goog.events.listen(el, goog.events.EventType.MOUSEMOVE, this.handleMouseMove, false, this);
  goog.events.listen(el, goog.events.EventType.FOCUS, this.handleFocus, false, this);
  goog.events.listen(el, goog.events.EventType.BLUR, this.handleMouseOutAndBlur, false, this)
};
a.detach = function(opt_el) {
  if(opt_el) {
    var el = goog.dom.getElement(opt_el);
    this.detachElement_(el);
    this.elements_.remove(el)
  }else {
    for(var a = this.elements_.getValues(), i = 0;el = a[i];i++)this.detachElement_(el);
    this.elements_.clear()
  }
};
a.detachElement_ = function(el) {
  goog.events.unlisten(el, goog.events.EventType.MOUSEOVER, this.handleMouseOver, false, this);
  goog.events.unlisten(el, goog.events.EventType.MOUSEOUT, this.handleMouseOutAndBlur, false, this);
  goog.events.unlisten(el, goog.events.EventType.MOUSEMOVE, this.handleMouseMove, false, this);
  goog.events.unlisten(el, goog.events.EventType.FOCUS, this.handleFocus, false, this);
  goog.events.unlisten(el, goog.events.EventType.BLUR, this.handleMouseOutAndBlur, false, this)
};
a.getHideDelayMs = function() {
  return this.hideDelayMs_
};
a.setText = function(str) {
  goog.dom.setTextContent(this.getElement(), str)
};
a.setHtml = function(str) {
  this.getElement().innerHTML = str
};
a.setElement = function(el) {
  var oldElement = this.getElement();
  oldElement && goog.dom.removeNode(oldElement);
  goog.ui.Tooltip.superClass_.setElement.call(this, el);
  if(el) {
    var body = this.dom_.getDocument().body;
    body.insertBefore(el, body.lastChild)
  }
};
a.getState = function() {
  return this.showTimer ? this.isVisible() ? goog.ui.Tooltip.State.UPDATING : goog.ui.Tooltip.State.WAITING_TO_SHOW : this.hideTimer ? goog.ui.Tooltip.State.WAITING_TO_HIDE : this.isVisible() ? goog.ui.Tooltip.State.SHOWING : goog.ui.Tooltip.State.INACTIVE
};
a.onBeforeShow = function() {
  if(!goog.ui.PopupBase.prototype.onBeforeShow.call(this))return false;
  if(this.anchor)for(var tt, i = 0;tt = goog.ui.Tooltip.activeInstances_[i];i++)goog.dom.contains(tt.getElement(), this.anchor) || tt.setVisible(false);
  goog.array.insert(goog.ui.Tooltip.activeInstances_, this);
  var element = this.getElement();
  element.className = this.className;
  this.clearHideTimer_();
  goog.events.listen(element, goog.events.EventType.MOUSEOVER, this.handleTooltipMouseOver, false, this);
  goog.events.listen(element, goog.events.EventType.MOUSEOUT, this.handleTooltipMouseOut, false, this);
  this.clearShowTimer();
  return true
};
a.onHide_ = function() {
  goog.array.remove(goog.ui.Tooltip.activeInstances_, this);
  for(var element = this.getElement(), tt, i = 0;tt = goog.ui.Tooltip.activeInstances_[i];i++)tt.anchor && goog.dom.contains(element, tt.anchor) && tt.setVisible(false);
  this.parentTooltip_ && this.parentTooltip_.startHideTimer_();
  goog.events.unlisten(element, goog.events.EventType.MOUSEOVER, this.handleTooltipMouseOver, false, this);
  goog.events.unlisten(element, goog.events.EventType.MOUSEOUT, this.handleTooltipMouseOut, false, this);
  this.anchor = undefined;
  if(this.getState() == goog.ui.Tooltip.State.INACTIVE)this.seenInteraction_ = false;
  goog.ui.PopupBase.prototype.onHide_.call(this)
};
a.maybeShow = function(el, opt_pos) {
  if(this.anchor == el)if(this.seenInteraction_ || !this.requireInteraction_) {
    this.setVisible(false);
    this.isVisible() || this.positionAndShow_(el, opt_pos)
  }else this.anchor = undefined;
  this.showTimer = undefined
};
a.positionAndShow_ = function(el, opt_pos) {
  var pos;
  if(opt_pos)pos = opt_pos;
  else {
    var coord = new goog.math.Coordinate(this.cursorPosition.x, this.cursorPosition.y);
    pos = new goog.ui.Tooltip.CursorTooltipPosition(coord)
  }this.anchor = el;
  this.setPosition(pos);
  this.setVisible(true)
};
a.maybeHide = function(el) {
  this.hideTimer = undefined;
  if(el == this.anchor)if((this.activeEl_ == null || this.activeEl_ != this.getElement() && !this.elements_.contains(this.activeEl_)) && !this.hasActiveChild())this.setVisible(false)
};
a.hasActiveChild = function() {
  return!!(this.childTooltip_ && this.childTooltip_.activeEl_)
};
a.handleMouseOver = function(event) {
  var el = this.getAnchorFromElement(event.target);
  this.activeEl_ = el;
  this.clearHideTimer_();
  if(el != this.anchor) {
    this.anchor = el;
    this.startShowTimer(el);
    this.checkForParentTooltip_()
  }
};
a.getAnchorFromElement = function(el) {
  try {
    for(;el && !this.elements_.contains(el);)el = el.parentNode;
    return el
  }catch(e) {
    return null
  }
};
a.handleMouseMove = function(event) {
  var scroll = this.dom_.getDocumentScroll();
  this.cursorPosition.x = event.clientX + scroll.x;
  this.cursorPosition.y = event.clientY + scroll.y;
  this.seenInteraction_ = true
};
a.handleFocus = function(event) {
  var el = this.getAnchorFromElement(event.target);
  this.activeEl_ = el;
  this.seenInteraction_ = true;
  if(this.anchor != el) {
    this.anchor = el;
    var pos = new goog.ui.Tooltip.ElementTooltipPosition(this.activeEl_);
    this.clearHideTimer_();
    this.startShowTimer(el, pos);
    this.checkForParentTooltip_()
  }
};
a.checkForParentTooltip_ = function() {
  if(this.anchor)for(var tt, i = 0;tt = goog.ui.Tooltip.activeInstances_[i];i++)if(goog.dom.contains(tt.getElement(), this.anchor)) {
    tt.childTooltip_ = this;
    this.parentTooltip_ = tt
  }
};
a.handleMouseOutAndBlur = function(event) {
  var el = this.getAnchorFromElement(event.target), elTo = this.getAnchorFromElement(event.relatedTarget);
  if(el != elTo) {
    if(el == this.activeEl_)this.activeEl_ = null;
    this.clearShowTimer();
    this.seenInteraction_ = false;
    if(this.isVisible() && (!event.relatedTarget || !goog.dom.contains(this.getElement(), event.relatedTarget)))this.startHideTimer_();
    else this.anchor = undefined
  }
};
a.handleTooltipMouseOver = function() {
  var element = this.getElement();
  if(this.activeEl_ != element) {
    this.clearHideTimer_();
    this.activeEl_ = element
  }
};
a.handleTooltipMouseOut = function(event) {
  var element = this.getElement();
  if(this.activeEl_ == element && (!event.relatedTarget || !goog.dom.contains(element, event.relatedTarget))) {
    this.activeEl_ = null;
    this.startHideTimer_()
  }
};
a.startShowTimer = function(el, opt_pos) {
  if(!this.showTimer)this.showTimer = goog.Timer.callOnce(goog.bind(this.maybeShow, this, el, opt_pos), this.showDelayMs_)
};
a.clearShowTimer = function() {
  if(this.showTimer) {
    goog.Timer.clear(this.showTimer);
    this.showTimer = undefined
  }
};
a.startHideTimer_ = function() {
  if(this.getState() == goog.ui.Tooltip.State.SHOWING)this.hideTimer = goog.Timer.callOnce(goog.bind(this.maybeHide, this, this.anchor), this.getHideDelayMs())
};
a.clearHideTimer_ = function() {
  if(this.hideTimer) {
    goog.Timer.clear(this.hideTimer);
    this.hideTimer = undefined
  }
};
a.disposeInternal = function() {
  this.setVisible(false);
  this.clearShowTimer();
  this.detach();
  this.getElement() && goog.dom.removeNode(this.getElement());
  this.activeEl_ = null;
  delete this.dom_;
  goog.ui.Tooltip.superClass_.disposeInternal.call(this)
};
goog.ui.Tooltip.CursorTooltipPosition = function(arg1, opt_arg2) {
  goog.positioning.ViewportPosition.call(this, arg1, opt_arg2)
};
goog.inherits(goog.ui.Tooltip.CursorTooltipPosition, goog.positioning.ViewportPosition);
goog.ui.Tooltip.CursorTooltipPosition.prototype.reposition = function(element, popupCorner, opt_margin) {
  var viewportElt = goog.style.getClientViewportElement(element), viewport = goog.style.getVisibleRectForElement(viewportElt), margin = opt_margin ? new goog.math.Box(opt_margin.top + 10, opt_margin.right, opt_margin.bottom, opt_margin.left + 10) : new goog.math.Box(10, 0, 0, 10);
  goog.positioning.positionAtCoordinate(this.coordinate, element, goog.positioning.Corner.TOP_START, margin, viewport, goog.positioning.Overflow.ADJUST_X | goog.positioning.Overflow.FAIL_Y) & goog.positioning.OverflowStatus.FAILED && goog.positioning.positionAtCoordinate(this.coordinate, element, goog.positioning.Corner.TOP_START, margin, viewport, goog.positioning.Overflow.ADJUST_X | goog.positioning.Overflow.ADJUST_Y)
};
goog.ui.Tooltip.ElementTooltipPosition = function(element) {
  goog.positioning.AnchoredPosition.call(this, element, goog.positioning.Corner.BOTTOM_RIGHT)
};
goog.inherits(goog.ui.Tooltip.ElementTooltipPosition, goog.positioning.AnchoredPosition);
goog.ui.Tooltip.ElementTooltipPosition.prototype.reposition = function(element, popupCorner, opt_margin) {
  var offset = new goog.math.Coordinate(10, 0);
  goog.positioning.positionAtAnchor(this.element, this.corner, element, popupCorner, offset, opt_margin, goog.positioning.Overflow.ADJUST_X | goog.positioning.Overflow.FAIL_Y) & goog.positioning.OverflowStatus.FAILED && goog.positioning.positionAtAnchor(this.element, goog.positioning.Corner.TOP_RIGHT, element, goog.positioning.Corner.BOTTOM_LEFT, offset, opt_margin, goog.positioning.Overflow.ADJUST_X | goog.positioning.Overflow.ADJUST_Y)
};goog.net.cookies = {};
goog.net.cookies.MAX_COOKIE_LENGTH = 3950;
goog.net.cookies.SPLIT_RE_ = /\s*;\s*/;
goog.net.cookies.TEST_COOKIE_NAME_ = "COOKIES_TEST_";
goog.net.cookies.isEnabled = function() {
  var isEnabled = goog.net.cookies.isNavigatorCookieEnabled_();
  if(isEnabled && goog.userAgent.WEBKIT) {
    var cookieName = goog.net.cookies.TEST_COOKIE_NAME_ + goog.now();
    goog.net.cookies.set(cookieName, "1");
    if(!goog.net.cookies.get(cookieName))return false;
    goog.net.cookies.remove(cookieName)
  }return isEnabled
};
goog.net.cookies.set = function(name, value, opt_maxAge, opt_path, opt_domain) {
  if(/[;=]/.test(name))throw Error('Invalid cookie name "' + name + '"');if(/;/.test(value))throw Error('Invalid cookie value "' + value + '"');goog.isDef(opt_maxAge) || (opt_maxAge = -1);
  var domainStr = opt_domain ? ";domain=" + opt_domain : "", pathStr = opt_path ? ";path=" + opt_path : "", expiresStr;
  expiresStr = opt_maxAge < 0 ? "" : opt_maxAge == 0 ? ";expires=" + (new Date(1970, 1, 1)).toUTCString() : ";expires=" + (new Date((new Date).getTime() + opt_maxAge * 1000)).toUTCString();
  document.cookie = name + "=" + value + domainStr + pathStr + expiresStr
};
goog.net.cookies.get = function(name, opt_default) {
  for(var nameEq = name + "=", parts = String(document.cookie).split(goog.net.cookies.SPLIT_RE_), i = 0, part;part = parts[i];i++)if(part.indexOf(nameEq) == 0)return part.substr(nameEq.length);
  return opt_default
};
goog.net.cookies.remove = function(name, opt_path, opt_domain) {
  var rv = goog.net.cookies.containsKey(name);
  goog.net.cookies.set(name, "", 0, opt_path, opt_domain);
  return rv
};
goog.net.cookies.isNavigatorCookieEnabled_ = function() {
  return navigator.cookieEnabled
};
goog.net.cookies.getKeyValues_ = function() {
  for(var parts = String(document.cookie).split(goog.net.cookies.SPLIT_RE_), keys = [], values = [], index, part, i = 0;part = parts[i];i++) {
    index = part.indexOf("=");
    if(index == -1) {
      keys.push("");
      values.push(part)
    }else {
      keys.push(part.substring(0, index));
      values.push(part.substring(index + 1))
    }
  }return{keys:keys, values:values}
};
goog.net.cookies.getKeys = function() {
  return goog.net.cookies.getKeyValues_().keys
};
goog.net.cookies.getValues = function() {
  return goog.net.cookies.getKeyValues_().values
};
goog.net.cookies.isEmpty = function() {
  return document.cookie == ""
};
goog.net.cookies.getCount = function() {
  var cookie = String(document.cookie);
  if(cookie == "")return 0;
  return cookie.split(goog.net.cookies.SPLIT_RE_).length
};
goog.net.cookies.containsKey = function(key) {
  return goog.isDef(goog.net.cookies.get(key))
};
goog.net.cookies.containsValue = function(value) {
  for(var values = goog.net.cookies.getKeyValues_().values, i = 0;i < values.length;i++)if(values[i] == value)return true;
  return false
};
goog.net.cookies.clear = function() {
  for(var keys = goog.net.cookies.getKeyValues_().keys, i = keys.length - 1;i >= 0;i--)goog.net.cookies.remove(keys[i])
};goog.exportSymbol("goog.provide", goog.provide);
goog.exportSymbol("goog.exportSymbol", goog.exportSymbol);
goog.exportSymbol("goog.net.XhrIo", goog.net.XhrIo);
goog.exportSymbol("goog.net.XhrIo.send", goog.net.XhrIo.send);
goog.exportSymbol("goog.net.XhrIo.prototype.getResponseText", goog.net.XhrIo.prototype.getResponseText);
goog.exportSymbol("goog.net.XhrIo.prototype.isSuccess", goog.net.XhrIo.prototype.isSuccess);
goog.exportSymbol("goog.ui.TableSorter", goog.ui.TableSorter);
goog.exportSymbol("goog.ui.TableSorter.prototype.setSortFunction", goog.ui.TableSorter.prototype.setSortFunction);
goog.exportSymbol("goog.ui.TableSorter.prototype.decorate", goog.ui.TableSorter.prototype.decorate);
goog.exportSymbol("goog.ui.TableSorter.prototype.setDefaultSortFunction", goog.ui.TableSorter.prototype.setDefaultSortFunction);
goog.exportSymbol("goog.ui.TableSorter.alphaSort", goog.ui.TableSorter.alphaSort);
goog.exportSymbol("goog.ui.TableSorter.numericSort", goog.ui.TableSorter.numericSort);
goog.exportSymbol("goog.ui.TableSorter.EventType.SORT", goog.ui.TableSorter.EventType.SORT);
goog.exportSymbol("goog.ui.TableSorter.EventType.BEFORESORT", goog.ui.TableSorter.EventType.BEFORESORT);
goog.exportSymbol("goog.ui.Tooltip", goog.ui.Tooltip);
goog.exportSymbol("goog.ui.Tooltip.prototype.setHtml", goog.ui.Tooltip.prototype.setHtml);
goog.exportSymbol("goog.userAgent.WEBKIT", goog.userAgent.WEBKIT);
goog.exportSymbol("goog.userAgent.getUserAgentString", goog.userAgent.getUserAgentString);
goog.exportSymbol("goog.net.cookies.set", goog.net.cookies.set);
goog.exportSymbol("goog.net.cookies.get", goog.net.cookies.get);
goog.exportSymbol("goog.net.cookies.remove", goog.net.cookies.remove);
goog.exportSymbol("goog.events.listen", goog.events.listen);
goog.exportSymbol("goog.events.unlisten", goog.events.unlisten);
goog.exportSymbol("goog.events.Event.prototype.preventDefault", goog.events.Event.prototype.preventDefault);
goog.exportSymbol("goog.events.Event.prototype.stopPropagation", goog.events.Event.prototype.stopPropagation);
goog.exportSymbol("goog.bind", goog.bind);
goog.exportSymbol("goog.dom.$", goog.dom.getElement);
goog.exportSymbol("goog.dom.$$", goog.dom.getElementsByTagNameAndClass);
goog.exportSymbol("goog.dom.createElement", goog.dom.createElement);
goog.exportSymbol("goog.dom.removeNode", goog.dom.removeNode);
goog.exportSymbol("goog.dom.createTextNode", goog.dom.createTextNode);
goog.exportSymbol("goog.object.containsKey", goog.object.containsKey);
