#!/bin/sh

# Compiled for dev
../third_party/closure-library/closure/bin/calcdeps.py -i util.js -p ../third_party/closure-library/ -o list | grep closure | xargs cat > dev.js

# Compiled for production
../third_party/closure-library/closure/bin/calcdeps.py -i util.js -i ../third_party/uaparser/resources/user_agent_overrides.js -p ../third_party/closure-library/ -o compiled -c ../third_party/closure-compiler/compiler.jar -f "--compilation_level=ADVANCED_OPTIMIZATIONS" > browserscope.js;
