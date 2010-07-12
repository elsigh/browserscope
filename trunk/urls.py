# Copyright 2009 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.conf.urls.defaults import *

urlpatterns = patterns('',
  # General URL handlers in shared/util.py
  (r'^$', 'base.util.Home'),
  (r'^faq', 'base.util.Faq'),
  (r'^news', 'base.util.News'),
  (r'^alltests', 'base.util.AllTests'),
  (r'^beacon.*', 'base.util.Beacon'),
  (r'^ua', 'base.util.UaParser'),
  (r'^get_csrf',  'base.util.GetCsrf'),
  (r'^resource',  'third_party.resource-cgi.resource.Handler'),
  (r'^set_cookie',  'base.util.SetCookieAndRedirect'),
  (r'^timeline$', 'base.util.BrowserTimeLine'),  # beta
  (r'^user/settings$', 'base.user_tests.Settings'),  # beta
  (r'^user/tests/update_schema$', 'base.user_tests.UpdateSchema'),
  (r'^user/tests/create$', 'base.user_tests.TestCreate'),  # beta
  (r'^user/beacon/(.+)$', 'base.user_tests.BeaconJs'),  # beta
  (r'^user/tests/edit/(.+)$', 'base.user_tests.TestEdit'),  # beta
  (r'^user/tests/view/(.+)$', 'base.user_tests.TestView'),  # beta
  (r'^user/tests/table/(.+)$', 'base.user_tests.TestStatsTable'),  # beta
  (r'^user/tests/howto$', 'base.user_tests.TestHowto'),  # beta
  (r'^user/tests/raw/(.+)$', 'base.user_tests.RawTestData'),  # beta
  (r'^user/tests/(.+)$', 'base.user_tests.Test'),  # beta

  # Admin functionality
  (r'^update_datastore', 'base.util.UpdateDatastore'),
  (r'^seed_datastore$', 'base.util.SeedDatastore'),
  (r'^clear_datastore$', 'base.util.ClearDatastore'),
  (r'^clear_memcache',  'base.util.ClearMemcache'),
  (r'^show_memcache',  'base.util.ShowMemcache'),
  (r'^admin$', 'base.admin.Admin'),
  (r'^admin/confirm-ua', 'base.admin.ConfirmUa'),
  (r'^admin/stats', 'base.admin.Stats'),
  (r'^admin/rankers/upload', 'base.admin_rankers.UploadRankers'),
  (r'^admin/upload_category_browsers', 'base.admin.UploadCategoryBrowsers'),
  (r'^admin/update_category', 'base.admin.UpdateCategory'),
  (r'^admin/update_summary_browsers', 'base.admin.UpdateSummaryBrowsers'),
  (r'^admin/update_stats_cache', 'base.admin.UpdateStatsCache'),
  (r'^admin/update_all_stats_cache', 'base.admin.UpdateAllStatsCache'),
  (r'^admin/update_dirty', 'base.manage_dirty.UpdateDirty'),
  (r'^admin/pause_dirty$', 'base.manage_dirty.PauseUpdateDirty'),
  (r'^admin/unpause_dirty$', 'base.manage_dirty.UnPauseUpdateDirty'),
  (r'^admin/release_lock$', 'base.manage_dirty.ReleaseLock'),
  (r'^admin/make_dirty$', 'base.manage_dirty.MakeDirty'),
  (r'^admin/user_agents.csv$', 'base.util.UserAgents'),
  (r'^admin/ua_groups', 'base.admin.GetUserAgentGroupStrings'),
  (r'^admin/ua/rebuild$', 'base.admin_rankers.RebuildUserAgents'),
  (r'^admin/ua/release$', 'base.admin_rankers.ReleaseUserAgentGroups'),
  (r'^admin/ua/reset$', 'base.admin_rankers.ResetUserAgentGroups'),
  (r'^admin/data_dump_keys', 'base.admin.DataDumpKeys'),
  (r'^admin/data_dump', 'base.admin.DataDump'),
  (r'^admin/serialization_test', 'base.serialization_test.GraphIt'),
  (r'^admin/ua_test', 'base.ua.ParseTest'),
  (r'^admin/test_task_queue', 'gaeunit_test.TaskHandler'),
  (r'^admin/getdirty', 'base.admin.GetDirty'),
  (r'^admin/schedule-dirty-update', 'base.admin.ScheduleDirtyUpdate'),


  # Cron admin scripts
  (r'^cron/update_recent_tests$', 'base.cron.UpdateRecentTests'),

  (r'^_ah/queue/update-dirty', 'base.manage_dirty.UpdateDirty'),
  (r'^_ah/queue/update-category', 'base.admin.UpdateCategory'),
  (r'^_ah/queue/recent-tests$', 'base.cron.UpdateRecentTests'),
  (r'^_ah/queue/update-stats-cache$', 'base.admin.UpdateStatsCache'),

  # GViz Data source
  #(r'^gviz$', 'base.util.Gviz'),

  # GAEBar
  (r'^gaebar/', include('third_party.gaebar.urls')),

  # UNIT TEST URLs
  # TODO(elsigh): try to do a custom urls.py for unit tests?
  (r'^fake_check_csrf', 'base.util.FakeCheckCsrf'),

  # Category Test Handlers, i.e. /network/test
  (r'^[^\/]+/test$', 'base.util.CategoryTest'),
  (r'^category_test_driver$', 'base.util.CategoryTestDriver'),
  (r'^multi_test_frameset$', 'base.util.MultiTestFrameset'),
  (r'^multi_test_driver$', 'base.util.MultiTestDriver'),

  #############################################################################
  ## CATEGORY URLS BELOW
  #############################################################################

  # Reflow Timer URLs
  (r'^reflow/about$', 'categories.reflow.handlers.About'),
  (r'^reflow/home$', 'categories.reflow.handlers.OldHome'),
  (r'^reflow/test_acid1$', 'categories.reflow.handlers.TestAcid1'),
  (r'^reflow/test_selectors$', 'categories.reflow.handlers.TestSelectors'),
  (r'^reflow/test_gen_css$', 'categories.reflow.handlers.TestGenCss'),
  (r'^reflow/test/nested_tables$', 'categories.reflow.handlers.NestedTables'),
  (r'^reflow/test/nested_divs$', 'categories.reflow.handlers.NestedDivs'),
  (r'^reflow/test/nested_anchors$', 'categories.reflow.handlers.NestedAnchors'),
  (r'^reflow/stats_chart$', 'categories.reflow.handlers.StatsChart'),
  (r'^reflow/stats_table$', 'categories.reflow.handlers.StatsTable'),
  (r'^reflow/locations', 'categories.reflow.handlers.Locations'),

  # Network Performance main URLs
  (r'^network/about$', 'categories.network.handlers.About'),
  (r'^network/stats_table$', 'categories.network.handlers.StatsTable'),

  # Network Performance test URLs
  (r'^network/tests/cache-expires2', 'categories.network.handlers.CacheExpires2'),
  (r'^network/tests/cache-expires', 'categories.network.handlers.CacheExpires'),
  (r'^network/tests/cache-redirects2', 'categories.network.handlers.CacheRedirects2'),
  (r'^network/tests/cache-redirects', 'categories.network.handlers.CacheRedirects'),
  (r'^network/tests/cache-resource-redirects2', 'categories.network.handlers.CacheResourceRedirects2'),
  (r'^network/tests/cache-resource-redirects', 'categories.network.handlers.CacheResourceRedirects'),
  (r'^network/tests/connections-per-hostname', 'categories.network.handlers.ConnectionsPerHostname'),
  (r'^network/tests/data-urls', 'categories.network.handlers.DataUrls'),
  (r'^network/tests/gzip', 'categories.network.handlers.Gzip'),
  (r'^network/tests/inline-script-after-stylesheet', 'categories.network.handlers.InlineScriptAfterStylesheet'),
  (r'^network/tests/latency', 'categories.network.handlers.Latency'),
  (r'^network/tests/link-prefetch2', 'categories.network.handlers.LinkPrefetch2'),
  (r'^network/tests/link-prefetch', 'categories.network.handlers.LinkPrefetch'),
  (r'^network/tests/max-connections', 'categories.network.handlers.MaxConnections'),
  (r'^network/tests/scripts-block-scripts', 'categories.network.handlers.ScriptsBlockScripts'),
  (r'^network/tests/scripts-block-stylesheets', 'categories.network.handlers.ScriptsBlockStylesheets'),
  (r'^network/tests/scripts-block-images', 'categories.network.handlers.ScriptsBlockImages'),
  (r'^network/tests/scripts-block-iframes', 'categories.network.handlers.ScriptsBlockIframes'),
  (r'^network/tests/scripts-block$', 'categories.network.handlers.ScriptsBlock'),
  (r'^network/tests/scripts-async', 'categories.network.handlers.ScriptsAsync'),
  (r'^network/tests/stylesheets-block', 'categories.network.handlers.StylesheetsBlock'),
  (r'^network/tests/trailer', 'categories.network.handlers.Trailer'),
  # Network Performance admin URLs
  (r'^network/admin', 'categories.network.handlers.Admin'),
  (r'^network/confirm-ua', 'categories.network.handlers.ConfirmUa'),
  (r'^network/stats', 'categories.network.handlers.Stats'),
  (r'^network/loader', 'categories.network.bulkloader.ResultLoader'),

  # Acid3 Test URLs
  (r'acid3/about$', 'categories.acid3.handlers.About'),
  (r'acid3/support-a.png$', 'categories.acid3.handlers.SupportAPng'),

  # Selectors API Test URLs
  (r'selectors/about$', 'categories.selectors.handlers.About'),

  # v8 Benchmark Suite URLs
  (r'v8/about$', 'categories.v8.handlers.About'),

  # SunSpider Benchmark Suite URLs
  (r'sunspider/about$', 'categories.sunspider.handlers.About'),

  # Rich text urls
  (r'^richtext/about$', 'categories.richtext.handlers.About'),

  # Rich text 2 urls
  (r'^richtext2/about$', 'categories.richtext2.handlers.About'),

  # Security urls
  (r'^security/about$', 'categories.security.handlers.About'),
  (r'^security/test_tpl$', 'categories.security.handlers.Test'),
  (r'^security/test/xframe$', 'categories.security.handlers.XFrameOptionsTest'),
  (r'^security/test/xcontenttype$', 'categories.security.handlers.XContentTypeOptionsTest'),
  (r'^security/test/originheader$', 'categories.security.handlers.OriginHeaderTest'),
  (r'^security/test/set-sts$', 'categories.security.handlers.SetSts'),
  (r'^security/test/test-sts$', 'categories.security.handlers.TestSts'),
  (r'^security/test/xss-frame-victim$', 'categories.security.handlers.ReflectedXSSVictim'),

  # HTML5 urls
  (r'^html5/about$', 'categories.html5.handlers.About'),

  # Cookies URLs
 (r'^cookies/about$', 'categories.cookies.handlers.About'),
 (r'^cookies/tests/clear-cookies$', 'categories.cookies.handlers.ClearCookies'),
 (r'^cookies/tests/expires$', 'categories.cookies.handlers.Expires'),
 (r'^cookies/tests/expires2$', 'categories.cookies.handlers.Expires2'),
 (r'^cookies/tests/max-per-host$', 'categories.cookies.handlers.MaxPerHost'),
 (r'^cookies/tests/max-name-size$', 'categories.cookies.handlers.MaxNameSize'),
 (r'^cookies/tests/max-value-size$', 'categories.cookies.handlers.MaxValueSize'),
 (r'^cookies/tests/max-total-size$', 'categories.cookies.handlers.MaxTotalSize'),

 # JSKB URLs
 (r'^jskb/about$', 'categories.jskb.handlers.About'),
 (r'^jskb/json$', 'categories.jskb.handlers.Json'),
 (r'^jskb/environment-checks$', 'categories.jskb.handlers.EnvironmentChecks'),


)
