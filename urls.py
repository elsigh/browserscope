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
  (r'^$', 'controllers.shared.util.Home'),
  (r'^faq', 'controllers.shared.util.Faq'),
  (r'^alltests', 'controllers.shared.util.AllTests'),
  (r'^beacon.*', 'controllers.shared.util.Beacon'),
  (r'^get_csrf',  'controllers.shared.util.GetCsrf'),

  # Admin functionality
  (r'^update_datastore', 'controllers.shared.util.UpdateDatastore'),
  (r'^seed_datastore$', 'controllers.shared.util.SeedDatastore'),
  (r'^clear_datastore$', 'controllers.shared.util.ClearDatastore'),
  (r'^clear_memcache',  'controllers.shared.util.ClearMemcache'),
  (r'^admin$', 'controllers.admin.Admin'),
  (r'^admin/confirm-ua', 'controllers.admin.ConfirmUa'),
  (r'^admin/stats', 'controllers.admin.Stats'),

  # Cron admin scripts
  (r'^cron/update_dirty$', 'controllers.shared.cron.UpdateDirty'),
  (r'^cron/more_dirty$', 'controllers.shared.cron.MoreDirty'),
  (r'^cron/user_agent_group$', 'controllers.shared.cron.UserAgentGroup'),
  (r'^cron/update_recent_tests$', 'controllers.shared.cron.UpdateRecentTests'),

  (r'^_ah/queue/update-dirty$', 'controllers.shared.cron.UpdateDirty'),
  (r'^_ah/queue/more-dirty$', 'controllers.shared.cron.MoreDirty'),
  (r'^_ah/queue/user-agent-group$', 'controllers.shared.cron.UserAgentGroup'),
  (r'^_ah/queue/recent-tests$', 'controllers.shared.cron.UpdateRecentTests'),

  # GAEBar
  (r'^gaebar/', include('gaebar.urls')),

  # UNIT TEST URLs
  # TODO(elsigh): try to do a custom urls.py for unit tests?
  (r'^fake_check_csrf',  'controllers.shared.util.FakeCheckCsrf'),


  #############################################################################
  ## CATEGORY URLS BELOW
  #############################################################################

  # Reflow Timer URLs
  (r'^reflows?/?$', 'controllers.reflow.About'),
  (r'^reflow/about$', 'controllers.reflow.About'),
  (r'^reflow/test$', 'controllers.reflow.Test'),
  (r'^reflow/test/nested_tables$', 'controllers.reflow.NestedTables'),
  (r'^reflow/test/nested_divs$', 'controllers.reflow.NestedDivs'),
  (r'^reflow/test/nested_anchors$', 'controllers.reflow.NestedAnchors'),
  (r'^reflow/stats_chart$', 'controllers.reflow.StatsChart'),
  (r'^reflow/stats_table$', 'controllers.reflow.StatsTable'),
  (r'^reflow/locations', 'controllers.reflow.Locations'),

  # Network Performance main URLs
  (r'^network/?$', 'controllers.network.About'),
  (r'^network/about$', 'controllers.network.About'),
  (r'^network/test$', 'controllers.network.Test'),
  (r'^network/testdriver', 'controllers.network.TestDriver'),
  (r'^network/stats_table$', 'controllers.network.StatsTable'),

  # Network Performance test URLs
  (r'^network/tests/cache-expires2', 'controllers.network.CacheExpires2'),
  (r'^network/tests/cache-expires', 'controllers.network.CacheExpires'),
  (r'^network/tests/cache-redirects2', 'controllers.network.CacheRedirects2'),
  (r'^network/tests/cache-redirects', 'controllers.network.CacheRedirects'),
  (r'^network/tests/cache-resource-redirects2', 'controllers.network.CacheResourceRedirects2'),
  (r'^network/tests/cache-resource-redirects', 'controllers.network.CacheResourceRedirects'),
  (r'^network/tests/connections-per-hostname', 'controllers.network.ConnectionsPerHostname'),
  (r'^network/tests/data-urls', 'controllers.network.DataUrls'),
  (r'^network/tests/gzip', 'controllers.network.Gzip'),
  (r'^network/tests/inline-script-after-stylesheet', 'controllers.network.InlineScriptAfterStylesheet'),
  (r'^network/tests/latency', 'controllers.network.Latency'),
  (r'^network/tests/link-prefetch2', 'controllers.network.LinkPrefetch2'),
  (r'^network/tests/link-prefetch', 'controllers.network.LinkPrefetch'),
  (r'^network/tests/max-connections', 'controllers.network.MaxConnections'),
  (r'^network/tests/scripts-block', 'controllers.network.ScriptsBlock'),
  (r'^network/tests/stylesheets-block', 'controllers.network.StylesheetsBlock'),
  # Network Performance admin URLs
  (r'^network/admin', 'controllers.network.Admin'),
  (r'^network/confirm-ua', 'controllers.network.ConfirmUa'),
  (r'^network/stats', 'controllers.network.Stats'),
  (r'^network/loader', 'controllers.network_loader.ResultLoader'),

  # Rich text urls
  (r'^richtext/tests', 'controllers.richtext.RunTests'),
  (r'^richtext/editable', 'controllers.richtext.EditableIframe'),
)
