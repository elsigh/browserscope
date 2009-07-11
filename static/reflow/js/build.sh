#!/bin/sh

cat ../../util.js ../../beacon.js reflow_timer.js > reflow_timer_build.js

cat reflow_timer_build.js reflow_timer_visual_runner.js > reflow_timer_visual.js;

cat reflow_timer_build.js cssom.js reflow_timer_alltests_runner.js > reflow_timer_alltests.js;

cat reflow_timer_build.js reflow_timer_callback_runner.js > reflow_timer_callback.js;

