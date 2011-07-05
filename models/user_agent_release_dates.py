#!/usr/bin/python2.5
#
# Copyright 2010 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License')
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Release dates for notable user agents.

TODO(slamm): Find newer release dates via browserscope data.
"""

import datetime
import csv
import logging


#http://en.wikipedia.org/wiki/Android_version_history
ANDROID_CSV = """Product,Date,Version
Android,2008-09-23,1.0
Android,2009-02-09,1.1
Android,2009-04-30,1.5
Android,2009-09-15,1.6
Android,2009-10-26,2.0
Android,2009-10-26,2.1
Android,2010-05-20,2.2
Android,2010-12-06,2.3
Android,2011-02-22,3.0
Android,2011-02-22,3.1
Android,2011-10-10,4.0
"""

IPHONE_CSV = """Product,Date,Version
iPhone,2008-07-11,2.0
iPhone,2008-09-09,2.1
iPhone,2008-11-21,2.2
iPhone,2009-06-17,3.0
iPhone,2009-09-09,3.1
iPhone,2010-02-02,3.1.3
iPhone,2010-06-21,4.0
iPhone,2010-09-08,4.1
iPhone,2010-11-22,4.2
iPhone,2011-03-09,4.3
iPhone,2011-05-04,4.3.3
iPhone,2011-10-01,5.0
"""

IPAD_CSV = """Product,Date,Version
iPad,2010-04-03,3.2
iPad,2010-07-15,3.2.1
iPad,2010-08-11,3.2.2
"""

IE_CSV = """Product,Date,Version
IE,1995-08,1.0
IE,1996-01,1.5
IE,1995-08,2.0 Beta
IE,1995-11,2.0
IE,1996-03,3.0 Alpha 1
IE,1996-05,3.0 Alpha 2
IE,1996-06,3.0 Beta 2
IE,1996-08,3.0
IE,1996-10,3.01
IE,1997-03,3.02
IE,1997,3.03
IE,1997-04,4.0 Beta 1
IE,1997-07,4.0 Beta 2
IE,1997-09,4.0
IE,1997-11,4.01
IE,1998-06,5.0 Beta 1
IE,1998-11,5.0 Beta 2
IE,1999-03,5.0
IE,1999-11,5.01
IE,1999-12,5.5 Beta 1
IE,2000-07,5.5
IE,2000-08,5.6
IE,2001-03,6.0 Beta 1
IE,2001-08-27,6.0
IE,2002-09-09,6.0 SP1
IE,2004-08-25,6.0 SV1 "SP2"
IE,2005-07-25,7.0 Beta 1
IE,2006-01-31,7.0 Beta 2 Preview
IE,2006-04-24,7.0 Beta 2
IE,2006-06-29,7.0 Beta 3
IE,2006-08-24,7.0 RC 1
IE,2006-10-18,7.0
IE,2008-03-05,8.0 Beta 1
IE,2008-08-27,8.0 Beta 2
IE,2008-12-11,8.0 Pre-RC1
IE,2009-01-26,8.0 RC1
IE,2009-03-19,8.0
IE,2011-03-14,9.0
IE Platform Preview,2010-10-28,9.0.6
IE Platform Preview,2009-11-17,9.0.7
"""

# http://en.wikipedia.org/wiki/Safari_version_history
SAFARI_CSV = """Product,Date,Version,Webkit Version,OS
Safari,2003-01-07,0.8,48,Mac OS X
Safari,2003-04-14,0.9,73,Mac OS X
Safari,2003-06-23,1.0,85,Mac OS X
Safari,2003-10-24,1.1,100,Mac OS X
Safari,2004-02-02,1.2,125,Mac OS X
Safari,2004-08-13,1.0.3,85.8.5,Mac OS X
Safari,2005-04-15,1.3,312,Mac OS X
Safari,2005-04-29,2.0,412,Mac OS X
Safari,2005-08-29,1.3.1,312.3,Mac OS X
Safari,2005-10-31,2.0.2,416.11,Mac OS X
Safari,2006-01-10,2.0.4,419.3,Mac OS X
Safari,2006-01-11,1.3.2,312.5,Mac OS X
Safari,2006-01-12,1.3.2,312.6,Mac OS X
Safari,2007-06-11,3.0,522.11,Mac OS X
Safari,2007-06-11,3.0,522.11.3,Windows
Safari,2007-06-13,3.0.1,522.12.2,Windows
Safari,2007-06-22,3.0.2,522.12,Mac OS X
Safari,2007-06-22,3.0.2,522.13.1,Windows
Safari,2007-07-31,3.0.3,522.12.1,Mac OS X
Safari,2007-08-01,3.0.3,522.15.5,Windows
Safari,2007-10-26,3.0.4,523.10,Mac OS X
Safari,2007-11-14,3.0.4,523.12.9,Windows
Safari,2007-12-17,3.0.4,523.13,Windows
Safari,2007-12-21,3.0.4,523.15,Windows
Safari,2008-03-18,3.1,525.13,Mac OS X
Safari,2008-03-18,3.1,525.13,Windows
Safari,2008-04-16,3.1.1,525.17,Mac OS X
Safari,2008-04-16,3.1.1,525.17,Windows
Safari,2008-05-28,3.1.1,525.20,Mac OS X
Safari,2008-06-11,4.0 Beta,526.11.2,Mac OS X
Safari,2008-06-11,4.0,526.12.2,Windows
Safari,2008-06-19,3.1.2,525.21,Windows
Safari,2008-06-30,3.1.2,525.21,Mac OS X
Safari,2008-08-22,4.0,528.1.1,Windows
Safari,2008-11-13,3.2,525.26,Mac OS X
Safari,2008-11-13,3.2,525.26.13,Windows
Safari,2008-11-24,3.2.1,525.27,Mac OS X
Safari,2008-11-24,3.2.1,525.27.1,Windows
Safari,2009-02-12,3.2.2,525.28.1,Windows
Safari,2009-02-24,4.0 Beta,528.16,Mac OS X
Safari,2009-02-24,4.0,528.16,Windows
Safari,2009-05-12,3.2.3,525.28,Mac OS X
Safari,2009-05-12,3.2.3,525.29.1,Windows
Safari,2009-05-12,4.0 Beta,528.17,Mac OS X
Safari,2009-05-12,4.0,528.17,Windows
Safari,2009-06-08,4.0,530.17,Mac OS X
Safari,2009-06-08,4.0.1,530.17,Windows
Safari,2009-06-17,4.0.1,530.18,Mac OS X
Safari,2009-07-08,4.0.2,530.19,Mac OS X
Safari,2009-07-08,4.0.2,530.19.1,Windows
Safari,2009-08-11,4.0.3,531.9,Mac OS X
Safari,2009-08-11,4.0.3,531.9.1,Windows
Safari,2009-11-11,4.0.4,531.21.10,Mac OS X
Safari,2009-11-11,4.0.4,531.21.10,Windows
Safari,2010-06-07,4.1,533.16,Mac OS X
Safari,2010-06-07,5.0,531.21.10,Mac OS X
Safari,2011-04-14,5.0.5,533.21.1,Mac OS X
Safari,2011-06-07,5.1,534.42,Mac OS X
"""

OPERA_CSV = """Product,Date,Version
Opera,2000-06-12,5.0
Opera,2001-06-27,5.12
Opera,2001-11-13,6.0 Beta 1
Opera,2001-12-18,6.0
Opera,2002-02-12,6.01
Opera,2002-03-18,6.06
Opera,2002-05-15,6.02
Opera,2002-05-27,6.03
Opera,2002-06-01,6.04
Opera,2002-08-13,6.05
Opera,2002-11-13,7.0 Beta 1
Opera,2002-11-22,7.0 Beta 1 v. 2
Opera,2002-12-18,7.0 Beta 2
Opera,2003-01-28,7.0
Opera,2003-02-05,7.01
Opera,2003-02-26,7.02
Opera,2003-03-13,7.03
Opera,2003-04-11,7.10
Opera,2003-05-09,7.11
Opera,2003-08-28,7.20 beta 7
Opera,2003-09-23,7.20
Opera,2003-10-14,7.21
Opera,2003-11-12,7.22
Opera,2003-11-22,7.23
Opera,2004-04-22,7.50 beta 1
Opera,2004-05-12,7.50
Opera,2004-06-03,7.51
Opera,2004-07-07,7.52
Opera,2004-07-20,7.53
Opera,2004-08-05,7.54
Opera,2004-12-10,7.54 update 1
Opera,2004-12-23,8.0 beta 1
Opera,2005-02-04,7.54 update 2
Opera,2005-02-25,8.0 beta 2
Opera,2005-03-16,8.0 beta 3
Opera,2005-04-19,8.0
Opera,2005-06-16,8.01
Opera,2005-07-28,8.02
Opera,2005-09-20,8.50
Opera,2005-11-22,8.51
Opera,2006-02-17,8.52
Opera,2006-03-02,8.53
Opera,2006-04-05,8.54
Opera,2006-04-20,9.0 beta 1
Opera,2006-05-23,9.0 beta 2
Opera,2006-06-20,9.0
Opera,2006-08-02,9.01
Opera,2006-09-21,9.02
Opera,2006-12-18,9.10
Opera,2007-03-28,9.20 beta 1
Opera,2007-04-11,9.20
Opera,2007-05-21,9.21
Opera,2007-07-19,9.22
Opera,2007-08-15,9.23
Opera,2007-10-17,9.24
Opera,2007-10-25,9.50 beta 1
Opera,2007-12-19,9.25
Opera,2008-02-20,9.26
Opera,2008-04-03,9.27
Opera,2008-04-24,9.50 beta 2
Opera,2008-06-12,9.50
Opera,2008-07-03,9.51
Opera,2008-08-20,9.52
Opera,2008-09-10,9.60 beta 1
Opera,2008-10-08,9.60
Opera,2008-10-21,9.61
Opera,2008-10-30,9.62
Opera,2008-12-16,9.63
Opera,2009-03-03,9.64
Opera,2009-06-03,10.00 beta 1
Opera,2009-07-16,10.00 beta 2
Opera,2009-08-13,10.00 beta 3
Opera,2009-09-01,10.00
Opera,2009-10-14,10.10 beta 1
Opera,2009-10-28,10.01
Opera,2009-11-23,10.10
Opera,2010-02-11,10.50 beta 1
Opera,2010-02-24,10.50 beta 2
Opera,2010-10-12,10.63
Opera,2011-05-18,11.11
"""

FIREFOX_CSV = """Product,Date,Version
Firefox,2002-09-23,0.1
Firefox,2002-10-01,0.2
Firefox,2002-10-14,0.3
Firefox,2002-10-19,0.4
Firefox,2002-12-07,0.5
Firefox,2003-05-17,0.6
Firefox,2003-07,0.6.28 1
Firefox,2003-10-15,0.7
Firefox,2003-10,0.7.26 1
Firefox,2004-02-09,0.8
Firefox,2004-06-15,0.9
Firefox,2004-06-28,0.9.1
Firefox,2004-07-08,0.9.2
Firefox,2004-08-04,0.9.3
Firefox,2004-09-14,0.10 (1.0 PR)
Firefox,2004-10-01,0.10.1
Firefox,2004-10-27,1.0 RC1
Firefox,2004-11-03,1.0 RC2
Firefox,2004-11-09,1.0
Firefox,2005-02-24,1.0.1
Firefox,2005-03-23,1.0.2
Firefox,2005-04-15,1.0.3
Firefox,2005-05-11,1.0.4
Firefox,2005-07-12,1.0.5
Firefox,2005-07-19,1.0.6
Firefox,2005-09-20,1.0.7
Firefox,2006-04-13,1.0.8
Firefox,2005-05-31,1.1a1
Firefox,2005-07-12,1.1a2
Firefox,2005-09-09,1.4
Firefox,2005-10-06,1.4.1
Firefox,2005-11-01,1.5 RC1
Firefox,2005-11-10,1.5 RC2
Firefox,2005-11-17,1.5 RC3
Firefox,2005-11-29,1.5
Firefox,2006-02-01,1.5.0.1
Firefox,2006-04-13,1.5.0.2
Firefox,2006-05-02,1.5.0.3
Firefox,2006-06-01,1.5.0.4
Firefox,2006-07-26,1.5.0.5
Firefox,2006-08-02,1.5.0.6
Firefox,2006-09-14,1.5.0.7
Firefox,2006-11-07,1.5.0.8
Firefox,2006-12-19,1.5.0.9
Firefox,2007-02-23,1.5.0.10
Firefox,2007-03-20,1.5.0.11
Firefox,2007-05-30,1.5.0.12
Firefox,2006-03-22,2.0a1
Firefox,2006-05-12,2.0a2
Firefox,2006-05-26,2.0a3
Firefox,2006-07-12,2.0b1
Firefox,2006-08-31,2.0b2
Firefox,2006-09-26,2.0 RC1
Firefox,2006-10-06,2.0 RC2
Firefox,2006-10-16,2.0 RC3
Firefox,2006-10-24,2.0
Firefox,2006-12-19,2.0.0.1
Firefox,2007-02-23,2.0.0.2
Firefox,2007-03-20,2.0.0.3
Firefox,2007-05-30,2.0.0.4
Firefox,2007-07-17,2.0.0.5
Firefox,2007-07-30,2.0.0.6
Firefox,2007-09-18,2.0.0.7
Firefox,2007-10-18,2.0.0.8
Firefox,2007-11-01,2.0.0.9
Firefox,2007-11-26,2.0.0.10
Firefox,2007-11-30,2.0.0.11
Firefox,2008-02-07,2.0.0.12
Firefox,2008-03-25,2.0.0.13
Firefox,2008-04-16,2.0.0.14
Firefox,2008-07-01,2.0.0.15
Firefox,2008-07-15,2.0.0.16
Firefox,2008-09-23,2.0.0.17
Firefox,2008-11-12,2.0.0.18
Firefox,2008-12-16,2.0.0.19
Firefox,2008-12-18,2.0.0.20
Firefox,2006-12-08,3.0a1
Firefox,2007-02-07,3.0a2
Firefox,2007-03-23,3.0a3
Firefox,2007-04-27,3.0a4
Firefox,2007-06-06,3.0a5
Firefox,2007-07-02,3.0a6
Firefox,2007-08-03,3.0a7
Firefox,2007-09-20,3.0a8
Firefox,2007-11-19,3.0b1
Firefox,2007-12-18,3.0b2
Firefox,2008-02-12,3.0b3
Firefox,2008-03-10,3.0b4
Firefox,2008-04-02,3.0b5
Firefox,2008-05-16,3.0 RC1
Firefox,2008-06-05,3.0 RC2
Firefox,2008-06-11,3.0 RC3
Firefox,2008-06-17,3.0
Firefox,2008-07-16,3.0.1
Firefox,2008-09-23,3.0.2
Firefox,2008-09-26,3.0.3
Firefox,2008-11-12,3.0.4
Firefox,2008-12-16,3.0.5
Firefox,2009-02-03,3.0.6
Firefox,2009-03-04,3.0.7
Firefox,2009-03-27,3.0.8
Firefox,2009-04-21,3.0.9
Firefox,2009-04-27,3.0.10
Firefox,2009-06-11,3.0.11
Firefox,2009-07-21,3.0.12
Firefox,2009-08-03,3.0.13
Firefox,2009-09-09,3.0.14
Firefox,2009-10-27,3.0.15
Firefox,2009-12-15,3.0.16
Firefox,2010-01-05,3.0.17
Firefox,2010-02-17,3.0.18
Firefox,2008-07-28,3.1a1
Firefox,2008-09-05,3.1a2
Firefox,2008-10-14,3.1b1
Firefox,2008-12-08,3.1b2
Firefox,2009-03-12,3.1b3
Firefox,2009-04-27,3.5b4
Firefox,2009-06-08,3.5b99
Firefox,2009-06-16,3.5 RC1
Firefox,2009-06-19,3.5 RC2
Firefox,2009-06-24,3.5 RC3
Firefox,2009-06-30,3.5
Firefox,2009-07-16,3.5.1
Firefox,2009-08-03,3.5.2
Firefox,2009-09-09,3.5.3
Firefox,2009-10-27,3.5.4
Firefox,2009-11-05,3.5.5
Firefox,2009-12-15,3.5.6
Firefox,2010-01-05,3.5.7
Firefox,2010-02-17,3.5.8
Firefox,2009-08-07,3.6a1
Firefox,2009-10-30,3.6b1
Firefox,2009-11-10,3.6b2
Firefox,2009-11-17,3.6b3
Firefox,2009-11-26,3.6b4
Firefox,2009-12-17,3.6b5
Firefox,2010-01-08,3.6 RC1
Firefox,2010-01-17,3.6 RC2
Firefox,2010-01-21,3.6
Firefox,2010-02,3.6.2
Firefox,2010-03,3.6.x
Firefox,2010-02-10,3.7a1
Firefox,2010-03,3.7a2
Firefox,2011-04-28,4.0.1
Firefox,2011-06-21,5.0
Firefox Beta,2010-09,4.0b6
Firefox Beta,2010-10,4.0b7
"""


# too much, see version below
CHROME_CSV = """Product,Date,Version,Channel
Chrome,2007-05-10,0.0.81.0,Dev
Chrome,2007-05-14,0.0.82.0,Dev
Chrome,2007-05-14,0.0.83.0,Dev
Chrome,2007-05-17,0.0.84.0,Dev
Chrome,2007-05-21,0.1.85.0,Dev
Chrome,2007-05-24,0.0.86.0,Dev
Chrome,2007-05-31,0.0.87.0,Dev
Chrome,2007-06-05,0.0.88.0,Dev
Chrome,2007-06-11,0.0.89.0,Dev
Chrome,2007-06-18,0.0.90.0,Dev
Chrome,2007-06-25,0.0.91.0,Dev
Chrome,2007-07-03,0.0.92.0,Dev
Chrome,2007-07-09,0.0.93.0,Dev
Chrome,2007-07-16,0.0.94.0,Dev
Chrome,2007-10-03,0.1.105.1,Dev
Chrome,2007-12-06,0.1.114.2,Dev
Chrome,2008-01-18,0.1.118.0,Beta
Chrome,2008-01-18,0.1.119.1,Dev
Chrome,2008-01-24,0.1.121.0,Dev
Chrome,2008-01-30,0.1.121.0,Beta
Chrome,2008-01-30,0.1.122.0,Dev
Chrome,2008-02-20,0.1.123.0,Dev
Chrome,2008-02-26,0.1.124.0,Dev
Chrome,2008-03-03,0.1.124.1,Beta
Chrome,2008-03-03,0.1.125.0,Dev
Chrome,2008-03-12,0.1.127.0,Dev
Chrome,2008-03-21,0.1.128.0,Dev
Chrome,2008-04-01,0.1.128.0,Beta
Chrome,2008-04-01,0.1.130.0,Dev
Chrome,2008-04-09,0.1.131.1,Beta
Chrome,2008-04-21,0.1.134.1,Beta
Chrome,2008-04-23,0.1.134.2,Beta
Chrome,2008-04-25,0.1.135.0,Beta
Chrome,2008-05-05,0.1.136.0,Beta
Chrome,2008-05-13,0.1.137.0,Beta
Chrome,2008-05-16,0.1.138.0,Beta
Chrome,2008-05-23,0.1.139.1,Beta
Chrome,2008-06-02,0.1.140.0,Beta
Chrome,2008-06-06,0.2.141.1,Beta
Chrome,2008-06-11,0.2.142.0,Beta
Chrome,2008-06-16,0.2.143.1,Beta
Chrome,2008-06-21,0.2.143.8,Beta
Chrome,2008-07-07,0.2.145.0,Dev
Chrome,2008-07-14,0.2.145.1,Beta
Chrome,2008-07-21,0.2.146.0,Beta
Chrome,2008-07-21,0.2.147.1,Dev
Chrome,2008-07-30,0.2.149.1,Beta
Chrome,2008-08-06,0.2.149.13,Beta
Chrome,2008-08-12,0.2.149.17,Beta
Chrome,2008-08-18,0.2.149.18,Beta
Chrome,2008-08-25,0.2.149.23,Beta
Chrome,2008-09-01,0.2.149.27,Beta
Chrome,2008-09-15,0.2.152.1,Dev
Chrome,2008-09-17,0.2.149.30,Beta
Chrome,2008-09-24,0.3.153.1,Dev
Chrome,2008-10-02,0.3.154.0,Dev
Chrome,2008-10-14,0.3.154.3,Dev
Chrome,2008-10-20,0.3.154.5,Dev
Chrome,2008-10-23,0.3.154.6,Dev
Chrome,2008-10-28,0.3.154.9,Dev
Chrome,2008-11-11,0.4.154.18,Dev
Chrome,2008-11-17,0.4.154.22,Dev
Chrome,2008-11-19,0.4.154.23,Dev
Chrome,2008-11-24,0.4.154.25,Beta
Chrome,2008-11-30,0.4.154.28,Dev
Chrome,2008-12-01,0.4.154.29,Dev
Chrome,2008-12-03,0.4.154.31,Dev
Chrome,2008-12-08,0.4.154.33,Dev
Chrome,2008-12-10,1.0.154.36,Stable
Chrome,2008-12-16,1.0.154.39,Dev
Chrome,2008-12-22,1.0.154.42,Dev
Chrome,2009-01-08,1.0.154.42,Beta
Chrome,2009-01-08,1.0.154.43,Stable
Chrome,2009-01-08,2.0.156.1,Dev
Chrome,2009-01-13,2.0.157.0,Dev
Chrome,2009-01-15,2.0.157.2,Dev
Chrome,2009-01-22,2.0.158.0,Dev
Chrome,2009-01-26,2.0.159.0,Dev
Chrome,2009-01-28,1.0.154.45,Stable
Chrome,2009-01-30,1.0.154.46,Stable
Chrome,2009-02-03,1.0.154.48,Stable
Chrome,2009-02-11,2.0.162.0,Dev
Chrome,2009-02-18,2.0.164.0,Dev
Chrome,2009-02-18,2.0.164.1,Dev
Chrome,2009-02-25,2.0.166.1,Dev
Chrome,2009-02-27,2.0.167.0,Dev
Chrome,2009-03-06,2.0.168.0,Dev
Chrome,2009-03-09,2.0.169.0,Dev
Chrome,2009-03-11,2.0.169.1,Dev
Chrome,2009-03-17,2.0.169.1,Beta
Chrome,2009-03-17,2.0.170.0,Dev
Chrome,2009-03-20,1.0.154.53,Stable
Chrome,2009-03-24,2.0.171.0,Dev
Chrome,2009-03-25,1.0.154.53,Stable
Chrome,2009-04-03,2.0.172.2,Dev
Chrome,2009-04-08,2.0.173.1,Beta
Chrome,2009-04-09,2.0.172.4,Beta
Chrome,2009-04-13,2.0.172.5,Beta
Chrome,2009-04-15,2.0.172.6,Beta
Chrome,2009-04-16,2.0.174.0,Dev
Chrome,2009-04-19,2.0.172.8,Beta
Chrome,2009-04-23,1.0.154.59,Stable
Chrome,2009-04-23,2.0.172.8,Dev
Chrome,2009-04-30,2.0.177.1,Dev
Chrome,2009-05-05,1.0.154.64,Stable
Chrome,2009-05-07,1.0.154.65,Stable
Chrome,2009-05-08,2.0.154.65,Stable
Chrome,2009-05-08,2.0.172.23,Beta
Chrome,2009-05-08,2.0.172.23,Beta
Chrome,2009-05-12,2.0.180.0,Dev
Chrome,2009-05-14,2.0.172.27,Beta
Chrome,2009-05-20,2.0.172.28,Stable
Chrome,2009-05-20,2.0.181.1,Dev
Chrome,2009-05-21,2.0.172.30,Beta
Chrome,2009-05-27,3.0.182.2,Dev
Chrome,2009-05-28,3.0.182.3,Dev
Chrome,2009-05-29,2.0.172.30,Stable
Chrome,2009-06-03,3.0.183.0,Dev
Chrome,2009-06-04,3.0.183.1,Dev
Chrome,2009-06-05,2.0.172.31,Stable
Chrome,2009-06-10,3.0.187.10,Dev
Chrome,2009-06-11,3.0.187.1,Dev
Chrome,2009-06-17,3.0.189.0,Dev
Chrome,2009-06-19,2.0.172.33,Stable
Chrome,2009-06-24,3.0.190.0,Dev
Chrome,2009-06-24,3.0.190.1,Dev
Chrome,2009-06-26,3.0.190.4,Dev
Chrome,2009-07-08,3.0.192.0,Dev
Chrome,2009-07-08,3.0.192.1,Dev
Chrome,2009-07-10,3.0.193.0,Dev
Chrome,2009-07-15,3.0.193.1,Dev
Chrome,2009-07-16,2.0.172.37,Stable
Chrome,2009-07-22,3.0.195.1,Dev
Chrome,2009-07-23,3.0.193.2,Beta
Chrome,2009-07-24,3.0.193.2,Beta
Chrome,2009-07-28,3.0.195.3,Dev
Chrome,2009-07-29,3.0.195.4,Dev
Chrome,2009-07-30,3.0.196.0,Dev
Chrome,2009-07-31,2.0.172.39,Dev
Chrome,2009-08-04,3.0.195.4,Beta
Chrome,2009-08-06,3.0.195.6,Beta
Chrome,2009-08-07,3.0.197.11,Dev
Chrome,2009-08-07,3.0.197.12,Dev
Chrome,2009-08-17,4.0.201.1,Dev
Chrome,2009-08-19,4.0.202.0,Dev
Chrome,2009-08-21,2.0.172.43,Stable
Chrome,2009-08-27,3.0.195.10,Beta
Chrome,2009-08-28,4.0.203.2,Dev
Chrome,2009-09-04,4.0.206.1,Dev
Chrome,2009-09-08,3.0.195.17,Beta
Chrome,2009-09-11,3.0.195.20,Beta
Chrome,2009-09-14,3.0.195.21,Stable
Chrome,2009-09-18,4.0.211.2,Dev
Chrome,2009-09-19,4.0.211.4,Dev
Chrome,2009-09-22,3.0.195.21,Stable
Chrome,2009-09-22,4.0.211.7,Dev
Chrome,2009-09-23,3.0.195.21,Stable
Chrome,2009-09-24,4.0.213.1,Dev
Chrome,2009-09-28,3.0.195.24,Beta
Chrome,2009-09-30,3.0.195.24,Stable
Chrome,2009-10-02,4.0.220.1,Dev
Chrome,2009-10-05,3.0.195.25,Stable
Chrome,2009-10-07,4.0.221.6,Dev
Chrome,2009-10-07,4.0.221.8,Dev
Chrome,2009-10-12,3.0.195.27,Stable
Chrome,2009-10-14,4.0.222.5,Dev
Chrome,2009-10-15,4.0.222.12,Dev
Chrome,2009-10-23,4.0.223.11,Dev
Chrome,2009-10-28,4.0.223.12,Dev
Chrome,2009-11-02,4.0.223.16,Beta
Chrome,2009-11-05,3.0.195.32,Stable
Chrome,2009-11-06,4.0.237.0,Dev
Chrome,2009-11-12,3.0.195.33,Stable
Chrome,2009-11-13,4.0.245.0,Dev
Chrome,2009-11-16,3.0.195.33,Stable
Chrome,2009-11-16,4.0.249.0,Dev
Chrome,2009-11-20,4.0.249.4,Dev
Chrome,2009-11-23,4.0.249.11,Dev
Chrome,2009-12-02,4.0.249.22,Dev
Chrome,2009-12-03,4.0.249.25,Dev
Chrome,2009-12-07,4.0.249.30,Beta
Chrome,2009-12-11,4.0.266.0,Dev
Chrome,2009-12-13,3.0.195.38,Stable
Chrome,2009-12-16,4.0.249.43,Beta
Chrome,2010-01-06,4.0.288.1,Dev
Chrome,2010-01-11,4.0.249.64,Beta
Chrome,2010-01-16,3.0.195.38,Stable
Chrome,2010-01-16,4.0.295.0,Dev
Chrome,2010-01-21,4.0.249.78,Beta
Chrome,2010-01-22,4.0.302.2,Dev
Chrome,2010-01-23,4.0.249.78,Stable
Chrome,2010-01-24,4.0.249.79,Stable
Chrome,2010-01-24,4.0.302.3,Dev
Chrome,2010-01-29,5.0.307.1,Dev
Chrome,2010-02-01,4.0.249.78,Stable
Chrome,2010-02-05,5.0.317.2,Dev
Chrome,2010-02-10,4.0.249.89,Stable
Chrome,2010-02-12,5.0.322.2,Dev
Chrome,2010-02-24,5.0.335.0,Dev
Chrome,2010-02-25,4.1.249.1017,Beta
Chrome,2010-02-25,5.0.335.1,Dev
Chrome,2010-03-01,4.1.249.1021,Beta
Chrome,2010-03-05,4.1.249.1025,Beta
Chrome,2010-03-05,5.0.342.2,Dev
"""
# NOTE - See where the list starts above a 0.2? This is a shorter
# version of this list that is useful for the default timeline.
CHROME_LIMITED_CSV ="""Product,Date,Version
Chrome,2008-09-08,0.2
Chrome,2008-12-11,1.0
Chrome,2009-05-24,2.0
Chrome,2009-10-12,3.0
Chrome,2010-01-25,4.0
Chrome,2010-05-25,5.0
Chrome,2010-09-02,6.0
Chrome,2010-10-21,7.0
Chrome,2010-11-22,8.0
Chrome,2011-02-03,9.0
Chrome,2011-03-08,10.0
Chrome,2011-04-27,11.0
Chrome,2011-06-07,12.0
Chrome,2011-06-09,13.0
"""

CHROME_TEST = """0.2.149
0.2.151
0.2.152
0.2.153
0.3.154
0.3.155
0.4.154
0.5.155
1.0.154
1.0.155
1.0.156
2.0.156
2.0.157
2.0.158
2.0.159
2.0.160
2.0.162
2.0.163
2.0.164
2.0.165
2.0.166
2.0.167
2.0.168
2.0.169
2.0.170
2.0.171
2.0.172
2.0.173
2.0.174
2.0.175
2.0.177
2.0.178
2.0.179
2.0.180
2.0.181
2.0.182
3.0.182
3.0.183
3.0.184
3.0.185
3.0.187
3.0.189
3.0.190
3.0.191
3.0.192
3.0.193
3.0.194
3.0.195
3.0.196
3.0.197
3.0.198
4.0.201
4.0.202
4.0.203
4.0.204
4.0.205
4.0.206
4.0.207
4.0.208
4.0.209
4.0.210
4.0.211
4.0.212
4.0.213
4.0.219
4.0.220
4.0.221
4.0.222
4.0.223
4.0.224
4.0.225
4.0.226
4.0.227
4.0.229
4.0.231
4.0.232
4.0.233
4.0.235
4.0.237
4.0.239
4.0.240
4.0.241
4.0.242
4.0.243
4.0.244
4.0.245
4.0.246
4.0.249
4.0.250
4.0.251
4.0.252
4.0.253
4.0.254
4.0.255
4.0.256
4.0.257
4.0.258
4.0.260
4.0.261
4.0.264
4.0.266
4.0.267
4.0.268
4.0.269
4.0.270
4.0.272
4.0.273
4.0.276
4.0.277
4.0.280
4.0.281
4.0.282
4.0.283
4.0.285
4.0.288
4.0.289
4.0.291
4.0.293
4.0.295
4.0.296
4.0.297
4.0.298
4.0.299
4.0.301
4.0.302
4.0.303
4.0.304
4.0.305
4.0.306
5.0.306
5.0.307
5.0.308
5.0.309
5.0.311
5.0.312
5.0.315
5.0.317
5.0.318
5.0.319
5.0.320
5.0.321
5.0.322
5.0.324
5.0.325
5.0.326
5.0.328
5.0.330
5.0.335
"""


def ParseReleaseCsv(csv_data):
  releases = {}
  for browser, date_str, version in csv.reader(csv_data.splitlines()):
    if browser != 'Product':
      date_params = map(int, date_str.split('-'))
      # If no month, pick January. If no day, pick 1st.
      date_params += [1] * max(0, min(2, 3 - len(date_params)))
      date = datetime.date(*date_params)
      releases[(browser, version)] = date
  return releases


def ParseChromeReleaseCsv(csv_data):
  releases = {}
  for browser, date_str, version, channel in csv.reader(csv_data.splitlines()):
    if browser != 'Product':
      date = datetime.date(*map(int, date_str.split('-')))
      major, minor, third, fourth = version.split('.')
      key = (browser, '.'.join((major, minor, third)))
      previous_date = releases.get(key, date)
      releases[key] = min(date, previous_date)
  return releases


def ParseSafariReleaseCsv(csv_data):
  """Parse Safari release data.

  Versions listed twice with get the date listed last in the csv.
  It looks like in practice, releases are only listed twice if on the
  same day.

  The Webkit version and OS fields are ignored.

  Args:
    csv_data: a string of csv_data (including newlines)
  Returns:
    { ('Safari', version): datetime_date, ... }
  """
  releases = {}
  for browser, date_str, version, webkit_version, os in csv.reader(
      csv_data.splitlines()):
    if browser != 'Product':
      date = datetime.date(*map(int, date_str.split('-')))
      releases[(browser, version)] = date
  return releases


releases = ParseReleaseCsv(IE_CSV)
releases.update(ParseReleaseCsv(FIREFOX_CSV))
releases.update(ParseReleaseCsv(OPERA_CSV))
releases.update(ParseReleaseCsv(CHROME_LIMITED_CSV))
releases.update(ParseSafariReleaseCsv(SAFARI_CSV))
releases.update(ParseChromeReleaseCsv(CHROME_CSV))
def ReleaseDate(browser, version):
  return releases.get((browser, version), None)


if __name__ == '__main__':
  for version in CHROME_TEST.splitlines():
    date = ReleaseDate('Chrome', version)
    print 'Chrome', version, date

  for version in ('6.0', '7.0', '8.0'):
    date = ReleaseDate('IE', version)
    print 'IE', version, date
