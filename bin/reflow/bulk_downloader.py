
import sys
sys.path.append('/tmp')
sys.path.append('/home/elsigh/src/google_appengine/')
sys.path.append('/home/elsigh/src/google_appengine/lib')
sys.path.append('/home/elsigh/src/google_appengine/lib/webob')
sys.path.append('/home/elsigh/src/browserscope')

from google.appengine.tools import bulkloader
from controllers.reflows import ReflowTime

class ReflowTimeExporter(bulkloader.Exporter):
  def __init__(self):
    bulkloader.Exporter.__init__(self, 'ReflowTime',
                         [('location', str, None),
                          ('time', str, None),
                          ('test', str, None),
                          ('user_agent_string', str, None),
                          ('created', str, None)
                          ])

exporters = [ReflowTimeExporter]

