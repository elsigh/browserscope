#!/bin/sh

cat ../../util.js ../../beacon.js reflow_timer.js > reflow_timer_build.js

cat reflow_timer_build.js cssom.js reflow_timer_ui_runner.js > reflow_timer_ui.js;

cat reflow_timer_build.js reflow_timer_callback_runner.js > reflow_timer_callback.js;

