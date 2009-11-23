#!/bin/sh

../third_party/closure-library/closure/bin/calcdeps.py -i util.js  -p ../third_party/closure-library/ -o script > tmp;

java -jar ../third_party/closure-compiler/compiler.jar --js tmp --js_output_file browserscope.js --compilation_level ADVANCED_OPTIMIZATIONS
