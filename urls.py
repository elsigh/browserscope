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
  (r'^alltests', 'base.util.AllTests'),
  (r'^beacon.*', 'base.util.Beacon'),
  (r'^get_csrf',  'base.util.GetCsrf'),
  (r'^resource',  'third_party.resource-cgi.resource.Handler'),

  # Admin functionality
  (r'^update_datastore', 'base.util.UpdateDatastore'),
  (r'^seed_datastore$', 'base.util.SeedDatastore'),
  (r'^clear_datastore$', 'base.util.ClearDatastore'),
  (r'^clear_memcache',  'base.util.ClearMemcache'),
  (r'^show_memcache',  'base.util.ShowMemcache'),
  (r'^admin$', 'base.admin.Admin'),
  (r'^admin/confirm-ua', 'base.admin.ConfirmUa'),
  (r'^admin/stats', 'base.admin.Stats'),
  (r'^admin/rankers/all', 'base.admin_rankers.AllRankers'),
  (r'^admin/rankers/rebuild', 'base.admin_rankers.RebuildRankers'),
  (r'^admin/rankers/release_next', 'base.admin_rankers.ReleaseNextRankers'),
  (r'^admin/rankers/reset_next', 'base.admin_rankers.ResetNextRankers'),
  (r'^admin/update_result_parents?', 'base.admin_rankers.UpdateResultParents'),
  (r'^admin/update_dirty$', 'base.manage_dirty.UpdateDirty'),
  (r'^admin/unpause_dirty$', 'base.manage_dirty.UnPauseUpdateDirty'),
  (r'^admin/release_lock$', 'base.manage_dirty.ReleaseLock'),
  (r'^admin/make_dirty$', 'base.manage_dirty.MakeDirty'),
  (r'^admin/user_agents.csv$', 'base.util.UserAgents'),
  (r'^admin/ua_groups', 'base.admin.GetUserAgentGroupStrings'),
  (r'^admin/wtf$', 'base.admin.WTF'),
  (r'^admin/ua/rebuild$', 'base.admin_rankers.RebuildUserAgents'),
  (r'^admin/ua/release$', 'base.admin_rankers.ReleaseUserAgentGroups'),
  (r'^admin/ua/reset$', 'base.admin_rankers.ResetUserAgentGroups'),
  (r'^admin/data_dump', 'base.admin.DataDump'),

  # Cron admin scripts
  (r'^cron/user_agent_group$', 'base.cron.UserAgentGroup'),
  (r'^cron/update_recent_tests$', 'base.cron.UpdateRecentTests'),

  (r'^_ah/queue/update-dirty', 'base.manage_dirty.UpdateDirty'),
  (r'^_ah/queue/user-agent-group$', 'base.cron.UserAgentGroup'),
  (r'^_ah/queue/recent-tests$', 'base.cron.UpdateRecentTests'),

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
  (r'^network/tests/scripts-block', 'categories.network.handlers.ScriptsBlock'),
  (r'^network/tests/stylesheets-block', 'categories.network.handlers.StylesheetsBlock'),
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

  # Security urls
  (r'^security/about$', 'categories.security.handlers.About'),
  (r'^security/test_tpl$', 'categories.security.handlers.Test'),

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

)
