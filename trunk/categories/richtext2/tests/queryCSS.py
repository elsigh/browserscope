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

"""Query with CSS tests"""

__author__ = 'rolandsteiner@google.com (Roland Steiner)'

QUERY_TESTS_CSS = {
  'id':            'QC',
  'caption':       'Query Tests, using styleWithCSS',
  'checkAttrs':    False,
  'checkStyle':    False,
  'checkSel':      False,
  'styleWithCSS':  True,

  'Proposed': [
    ### queryCommandSupported
    { 'id':          'SUPP-BOLD-TEXT',
      'desc':        'check whether the "bold" command is supported',
      'qcsupported': 'bold',
      'pad':         'foo[bar]baz',
      'expected':    True },

    { 'id':          'SUPP-BOLD-B',
      'desc':        'check whether the "bold" command is supported',
      'qcsupported': 'bold',
      'pad':         '<b>foo[bar]baz</b>',
      'expected':    True },

    { 'id':          'SUPP-ITALIC-TEXT',
      'desc':        'check whether the "italic" command is supported',
      'qcsupported': 'italic',
      'pad':         'foo[bar]baz',
      'expected':    True },

    { 'id':          'SUPP-ITALIC-I',
      'desc':        'check whether the "italic" command is supported',
      'qcsupported': 'italic',
      'pad':         '<i>foo[bar]baz</i>',
      'expected':    True },

    { 'id':          'SUPP-SUBSCRIPT',
      'desc':        'check whether the "subscript" command is supported',
      'qcsupported': 'subscript',
      'pad':         'foo[bar]baz',
      'expected':    True },

    { 'id':          'SUPP-SUPERSCRIPT',
      'desc':        'check whether the "superscript" command is supported',
      'qcsupported': 'superscript',
      'pad':         'foo[bar]baz',
      'expected':    True },

    { 'id':          'SUPP-STRIKETHROUGH',
      'desc':        'check whether the "strikethrough" command is supported',
      'qcsupported': 'strikethrough',
      'pad':         'foo[bar]baz',
      'expected':    True },

    { 'id':          'SUPP-UNDERLINE',
      'desc':        'check whether the "underline" command is supported',
      'qcsupported': 'underline',
      'pad':         'foo[bar]baz',
      'expected':    True },

    { 'id':          'SUPP-CREATELINK',
      'desc':        'check whether the "createlink" command is supported',
      'qcsupported': 'createlink',
      'pad':         'foo[bar]baz',
      'expected':    True },

    { 'id':          'SUPP-UNLINK',
      'desc':        'check whether the "unlink" command is supported',
      'qcsupported': 'unlink',
      'pad':         'foo[bar]baz',
      'expected':    True },

    { 'id':          'SUPP-DELETE',
      'desc':        'check whether the "delete" command is supported',
      'qcsupported': 'delete',
      'pad':         'foo[bar]baz',
      'expected':    True },

    { 'id':          'SUPP-FORWARDDELETE',
      'desc':        'check whether the "forwarddelete" command is supported',
      'qcsupported': 'forwarddelete',
      'pad':         'foo[bar]baz',
      'expected':    True },

    { 'id':          'SUPP-FORMATBLOCK',
      'desc':        'check whether the "formatblock" command is supported',
      'qcsupported': 'formatblock',
      'pad':         'foo[bar]baz',
      'expected':    True },

    { 'id':          'SUPP-INSERTHTML',
      'desc':        'check whether the "inserthtml" command is supported',
      'qcsupported': 'inserthtml',
      'pad':         'foo[bar]baz',
      'expected':    True },

    { 'id':          'SUPP-INSERTIMAGE',
      'desc':        'check whether the "insertimage" command is supported',
      'qcsupported': 'insertimage',
      'pad':         'foo[bar]baz',
      'expected':    True },

    { 'id':          'SUPP-INSERTLINEBREAK',
      'desc':        'check whether the "insertlinebreak" command is supported',
      'qcsupported': 'insertlinebreak',
      'pad':         'foo[bar]baz',
      'expected':    True },

    { 'id':          'SUPP-INSERTORDEREDLIST',
      'desc':        'check whether the "insertorderedlist" command is supported',
      'qcsupported': 'insertorderedlist',
      'pad':         'foo[bar]baz',
      'expected':    True },

    { 'id':          'SUPP-INSERTUNORDEREDLIST',
      'desc':        'check whether the "insertunorderedlist" command is supported',
      'qcsupported': 'insertunorderedlist',
      'pad':         'foo[bar]baz',
      'expected':    True },

    { 'id':          'SUPP-INSERTPARAGRAPH',
      'desc':        'check whether the "insertparagraph" command is supported',
      'qcsupported': 'insertparagraph',
      'pad':         'foo[bar]baz',
      'expected':    True },

    { 'id':          'SUPP-INSERTTEXT',
      'desc':        'check whether the "inserttext" command is supported',
      'qcsupported': 'inserttext',
      'pad':         'foo[bar]baz',
      'expected':    True },

    { 'id':          'SUPP-UNDO',
      'desc':        'check whether the "undo" command is supported',
      'qcsupported': 'undo',
      'pad':         'foo[bar]baz',
      'expected':    True },

    { 'id':          'SUPP-REDO',
      'desc':        'check whether the "redo" command is supported',
      'qcsupported': 'redo',
      'pad':         'foo[bar]baz',
      'expected':    True },

    { 'id':          'SUPP-SELECTALL',
      'desc':        'check whether the "selectall" command is supported',
      'qcsupported': 'selectall',
      'pad':         'foo[bar]baz',
      'expected':    True },

    { 'id':          'SUPP-UNSELECT',
      'desc':        'check whether the "unselect" command is supported',
      'qcsupported': 'unselect',
      'pad':         'foo[bar]baz',
      'expected':    True },

    ### queryCommandEnabled
    { 'id':          'EN-BOLD-TEXT',
      'desc':        'check whether the "bold" command is enabled',
      'qcenabled':   'bold',
      'pad':         'foo[bar]baz',
      'expected':    True },

    { 'id':          'EN-BOLD-B',
      'desc':        'check whether the "bold" command is enabled',
      'qcenabled':   'bold',
      'pad':         '<b>foo[bar]baz</b>',
      'expected':    True },

    { 'id':          'EN-ITALIC-TEXT',
      'desc':        'check whether the "bold" command is enabled',
      'qcenabled':   'italic',
      'pad':         'foo[bar]baz',
      'expected':    True },

    { 'id':          'EN-ITALIC-I',
      'desc':        'check whether the "bold" command is enabled',
      'qcenabled':   'italic',
      'pad':         '<i>foo[bar]baz</i>',
      'expected':    True },

    ### queryCommandIndeterm
    { 'id':          'IND-BOLD-TEXT',
      'desc':        'check whether the "bold" command is indeterminate',
      'qcindeterm':  'bold',
      'pad':         'foo[bar]baz',
      'expected':    False },

    { 'id':          'IND-BOLD-B',
      'desc':        'check whether the "bold" command is indeterminate',
      'qcindeterm':  'bold',
      'pad':         '<b>foo[bar]baz</b>',
      'expected':    False },

    { 'id':          'IND-ITALIC-TEXT',
      'desc':        'check whether the "bold" command is indeterminate',
      'qcindeterm':  'italic',
      'pad':         'foo[bar]baz',
      'expected':    False },

    { 'id':          'IND-BITALIC-I',
      'desc':        'check whether the "bold" command is indeterminate',
      'qcindeterm':  'italic',
      'pad':         '<i>foo[bar]baz</i>',
      'expected':    False },

    ### queryCommandState
    { 'id':          'STATE-BOLD-TEXT',
      'desc':        'query the state of the "bold" command',
      'qcstate':     'bold',
      'pad':         'foo[bar]baz',
      'expected':    False },

    { 'id':          'STATE-BOLD-B',
      'desc':        'query the state of the "bold" command',
      'qcstate':     'bold',
      'pad':         '<b>foo[bar]baz</b>',
      'expected':    True },

    { 'id':          'STATE-BOLD-STRONG',
      'desc':        'query the state of the "bold" command',
      'qcstate':     'bold',
      'pad':         '<strong>foo[bar]baz</strong>',
      'expected':    True },

    { 'id':          'STATE-BOLD-STYLE-FW-bold',
      'desc':        'query the state of the "bold" command',
      'qcstate':     'bold',
      'pad':         '<span style="font-weight: bold">foo[bar]baz</span>',
      'expected':    True },

    { 'id':          'STATE-BOLD-STYLE-FW-normal',
      'desc':        'query the state of the "bold" command',
      'qcstate':     'bold',
      'pad':         '<span style="font-weight: normal">foo[bar]baz</span>',
      'expected':    False },

    { 'id':          'STATE-BOLD-B-STYLE-FW-normal',
      'desc':        'query the state of the "bold" command',
      'qcstate':     'bold',
      'pad':         '<b><span style="font-weight: normal">foo[bar]baz</span></b>',
      'expected':    False },

    { 'id':          'STATE-ITALIC-TEXT',
      'desc':        'query the state of the "bold" command',
      'qcstate':     'italic',
      'pad':         'foo[bar]baz',
      'expected':    False },

    { 'id':          'STATE-ITALIC-I',
      'desc':        'query the state of the "bold" command',
      'qcstate':     'italic',
      'pad':         '<i>foo[bar]baz</i>',
      'expected':    True },

    { 'id':          'STATE-ITALIC-EM',
      'desc':        'query the state of the "bold" command',
      'qcstate':     'italic',
      'pad':         '<em>foo[bar]baz</em>',
      'expected':    True },

    { 'id':          'STATE-ITALIC-STYLE-FS-italic',
      'desc':        'query the state of the "bold" command',
      'qcstate':     'italic',
      'pad':         '<span style="font-style: italic">foo[bar]baz</span>',
      'expected':    True },

    { 'id':          'STATE-ITALIC-STYLE-FS-normal',
      'desc':        'query the state of the "bold" command',
      'qcstate':     'italic',
      'pad':         '<span style="font-style: normal">foo[bar]baz</span>',
      'expected':    False },

    { 'id':          'STATE-ITALIC-I-STYLE-FS-normal',
      'desc':        'query the state of the "bold" command',
      'qcstate':     'italic',
      'pad':         '<i><span style="font-style: normal">foo[bar]baz</span></i>',
      'expected':    False },

    { 'id':          'STATE-IOL-TEXT',
      'desc':        'query the state of the "insertorderedlist" command',
      'qcstate':     'insertorderedlist',
      'pad':         'foo[bar]baz',
      'expected':    False },

    { 'id':          'STATE-IOL-OL',
      'desc':        'query the state of the "insertorderedlist" command',
      'qcstate':     'insertorderedlist',
      'pad':         '<ol><li>foo[bar]baz</li></ol>',
      'expected':    True },

    { 'id':          'STATE-IOL-UL',
      'desc':        'query the state of the "insertorderedlist" command',
      'qcstate':     'insertorderedlist',
      'pad':         '<ul><li>foo[bar]baz</li></ul>',
      'expected':    False },

    { 'id':          'STATE-IUL-TEXT',
      'desc':        'query the state of the "insertunorderedlist" command',
      'qcstate':     'insertunorderedlist',
      'pad':         'foo[bar]baz',
      'expected':    False },

    { 'id':          'STATE-IUL-OL',
      'desc':        'query the state of the "insertunorderedlist" command',
      'qcstate':     'insertunorderedlist',
      'pad':         '<ol><li>foo[bar]baz</li></ol>',
      'expected':    False },

    { 'id':          'STATE-IUL-UL',
      'desc':        'query the state of the "insertunorderedlist" command',
      'qcstate':     'insertunorderedlist',
      'pad':         '<ul><li>foo[bar]baz</li></ul>',
      'expected':    True },

    { 'id':          'STATE-JC-TEXT',
      'desc':        'query the state of the "justifycenter" command',
      'qcstate':     'justifycenter',
      'pad':         'foo[bar]baz',
      'expected':    False },

    { 'id':          'STATE-JC-DIV-ALIGN-center',
      'desc':        'query the state of the "justifycenter" command',
      'qcstate':     'justifycenter',
      'pad':         '<div align="center">foo[bar]baz</div>',
      'expected':    True },

    { 'id':          'STATE-JC-P-ALIGN-center',
      'desc':        'query the state of the "justifycenter" command',
      'qcstate':     'justifycenter',
      'pad':         '<p align="center">foo[bar]baz</p>',
      'expected':    True },

    { 'id':          'STATE-JC-STYLE-TA-center',
      'desc':        'query the state of the "justifycenter" command',
      'qcstate':     'justifycenter',
      'pad':         '<span style="text-align: center">foo[bar]baz</span>',
      'expected':    True },

    { 'id':          'STATE-JF-TEXT',
      'desc':        'query the state of the "justifyfull" command',
      'qcstate':     'justifyfull',
      'pad':         'foo[bar]baz',
      'expected':    False },

    { 'id':          'STATE-JF-DIV-ALIGN-justify',
      'desc':        'query the state of the "justifyfull" command',
      'qcstate':     'justifyfull',
      'pad':         '<div align="justify">foo[bar]baz</div>',
      'expected':    True },

    { 'id':          'STATE-JF-P-ALIGN-justify',
      'desc':        'query the state of the "justifyfull" command',
      'qcstate':     'justifyfull',
      'pad':         '<p align="justify">foo[bar]baz</p>',
      'expected':    True },

    { 'id':          'STATE-JF-STYLE-TA-justify',
      'desc':        'query the state of the "justifyfull" command',
      'qcstate':     'justifyfull',
      'pad':         '<span style="text-align: justify">foo[bar]baz</span>',
      'expected':    True },

    { 'id':          'STATE-JL-TEXT',
      'desc':        'query the state of the "justifyleft" command',
      'qcstate':     'justifyleft',
      'pad':         'foo[bar]baz',
      'expected':    False },

    { 'id':          'STATE-JL-DIV-ALIGN-left',
      'desc':        'query the state of the "justifyleft" command',
      'qcstate':     'justifyleft',
      'pad':         '<div align="left">foo[bar]baz</div>',
      'expected':    True },

    { 'id':          'STATE-JL-P-ALIGN-left',
      'desc':        'query the state of the "justifyleft" command',
      'qcstate':     'justifyleft',
      'pad':         '<p align="left">foo[bar]baz</p>',
      'expected':    True },

    { 'id':          'STATE-JL-STYLE-TA-left',
      'desc':        'query the state of the "justifyleft" command',
      'qcstate':     'justifyleft',
      'pad':         '<span style="text-align: left">foo[bar]baz</span>',
      'expected':    True },

    { 'id':          'STATE-JR-TEXT',
      'desc':        'query the state of the "justifyright" command',
      'qcstate':     'justifyright',
      'pad':         'foo[bar]baz',
      'expected':    False },

    { 'id':          'STATE-JR-DIV-ALIGN-right',
      'desc':        'query the state of the "justifyright" command',
      'qcstate':     'justifyright',
      'pad':         '<div align="right">foo[bar]baz</div>',
      'expected':    True },

    { 'id':          'STATE-JR-P-ALIGN-right',
      'desc':        'query the state of the "justifyright" command',
      'qcstate':     'justifyright',
      'pad':         '<p align="right">foo[bar]baz</p>',
      'expected':    True },

    { 'id':          'STATE-JR-STYLE-TA-right',
      'desc':        'query the state of the "justifyright" command',
      'qcstate':     'justifyright',
      'pad':         '<span style="text-align: right">foo[bar]baz</span>',
      'expected':    True },

    { 'id':          'STATE-S-TEXT',
      'desc':        'query the state of the "strikethrough" command',
      'qcstate':     'strikethrough',
      'pad':         'foo[bar]baz',
      'expected':    False },

    { 'id':          'STATE-S-S',
      'desc':        'query the state of the "strikethrough" command',
      'qcstate':     'strikethrough',
      'pad':         '<s>foo[bar]baz</s>',
      'expected':    True },

    { 'id':          'STATE-S-STRIKE',
      'desc':        'query the state of the "strikethrough" command',
      'qcstate':     'strikethrough',
      'pad':         '<strike>foo[bar]baz</strike>',
      'expected':    True },

    { 'id':          'STATE-S-STRIKE-STYLE-TD-none',
      'desc':        'query the state of the "strikethrough" command',
      'qcstate':     'strikethrough',
      'pad':         '<strike style="text-decoration: none">foo[bar]baz</strike>',
      'expected':    False },

    { 'id':          'STATE-S-DEL',
      'desc':        'query the state of the "strikethrough" command',
      'qcstate':     'strikethrough',
      'pad':         '<del>foo[bar]baz</del>',
      'expected':    True },

    { 'id':          'STATE-S-STYLE-TD-LT',
      'desc':        'query the state of the "strikethrough" command',
      'qcstate':     'strikethrough',
      'pad':         '<span style="text-decoration: line-through">foo[bar]baz</span>',
      'expected':    True },

    { 'id':          'STATE-SUB-TEXT',
      'desc':        'query the state of the "subscript" command',
      'qcstate':     'subscript',
      'pad':         'foo[bar]baz',
      'expected':    False },

    { 'id':          'STATE-SUB-SUB',
      'desc':        'query the state of the "subscript" command',
      'qcstate':     'subscript',
      'pad':         '<sub>foo[bar]baz</sub>',
      'expected':    True },

    { 'id':          'STATE-SUP-TEXT',
      'desc':        'query the state of the "superscript" command',
      'qcstate':     'superscript',
      'pad':         'foo[bar]baz',
      'expected':    False },

    { 'id':          'STATE-SUP-SUP',
      'desc':        'query the state of the "superscript" command',
      'qcstate':     'superscript',
      'pad':         '<sup>foo[bar]baz</sup>',
      'expected':    True },

    { 'id':          'STATE-U-TEXT',
      'desc':        'query the state of the "underline" command',
      'qcstate':     'underline',
      'pad':         'foo[bar]baz',
      'expected':    False },

    { 'id':          'STATE-U-U',
      'desc':        'query the state of the "underline" command',
      'qcstate':     'underline',
      'pad':         '<u>foo[bar]baz</u>',
      'expected':    True },

    { 'id':          'STATE-U-U-STYLE-TD-none',
      'desc':        'query the state of the "underline" command',
      'qcstate':     'underline',
      'pad':         '<u style="text-decoration: none">foo[bar]baz</u>',
      'expected':    False },

    { 'id':          'STATE-U-A',
      'desc':        'query the state of the "underline" command',
      'qcstate':     'underline',
      'pad':         '<a href="http://www.foo.com">foo[bar]baz</a>',
      'expected':    True },

    { 'id':          'STATE-U-A-STYLE-TD-none',
      'desc':        'query the state of the "underline" command',
      'qcstate':     'underline',
      'pad':         '<a href="http://www.foo.com" style="text-decoration: none">foo[bar]baz</a>',
      'expected':    False },

    { 'id':          'STATE-U-STYLE-TD-UL',
      'desc':        'query the state of the "underline" command',
      'qcstate':     'underline',
      'pad':         '<span style="text-decoration: underline">foo[bar]baz</span>',
      'expected':    True },

    ### queryCommandValue
    { 'id':          'VALUE-BOLD-TEXT',
      'desc':        'query the value of the "bold" command',
      'qcvalue':     'bold',
      'pad':         'foo[bar]baz',
      'expected':    'false' },

    { 'id':          'VALUE-BOLD-B',
      'desc':        'query the value of the "bold" command',
      'qcvalue':     'bold',
      'pad':         '<b>foo[bar]baz</b>',
      'expected':    'true' },

    { 'id':          'VALUE-BOLD-STRONG',
      'desc':        'query the value of the "bold" command',
      'qcvalue':     'bold',
      'pad':         '<strong>foo[bar]baz</strong>',
      'expected':    'true' },

    { 'id':          'VALUE-BOLD-STYLE-FW-bold',
      'desc':        'query the value of the "bold" command',
      'qcvalue':     'bold',
      'pad':         '<span style="font-weight: bold">foo[bar]baz</span>',
      'expected':    'true' },

    { 'id':          'VALUE-BOLD-STYLE-FW-normal',
      'desc':        'query the value of the "bold" command',
      'qcvalue':     'bold',
      'pad':         '<span style="font-weight: normal">foo[bar]baz</span>',
      'expected':    'false' },

    { 'id':          'VALUE-BOLD-B-STYLE-FW-normal',
      'desc':        'query the value of the "bold" command',
      'qcvalue':     'bold',
      'pad':         '<b><span style="font-weight: normal">foo[bar]baz</span></b>',
      'expected':    'false' },

    { 'id':          'VALUE-ITALIC-TEXT',
      'desc':        'query the value of the "bold" command',
      'qcvalue':     'italic',
      'pad':         'foo[bar]baz',
      'expected':    'false' },

    { 'id':          'VALUE-ITALIC-I',
      'desc':        'query the value of the "bold" command',
      'qcvalue':     'italic',
      'pad':         '<i>foo[bar]baz</i>',
      'expected':    'true' },

    { 'id':          'VALUE-ITALIC-EM',
      'desc':        'query the value of the "bold" command',
      'qcvalue':     'italic',
      'pad':         '<em>foo[bar]baz</em>',
      'expected':    'true' },

    { 'id':          'VALUE-ITALIC-STYLE-FS-italic',
      'desc':        'query the value of the "bold" command',
      'qcvalue':     'italic',
      'pad':         '<span style="font-style: italic">foo[bar]baz</span>',
      'expected':    'true' },

    { 'id':          'VALUE-ITALIC-STYLE-FS-normal',
      'desc':        'query the value of the "bold" command',
      'qcvalue':     'italic',
      'pad':         '<span style="font-style: normal">foo[bar]baz</span>',
      'expected':    'false' },

    { 'id':          'VALUE-ITALIC-I-STYLE-FS-normal',
      'desc':        'query the value of the "bold" command',
      'qcvalue':     'italic',
      'pad':         '<i><span style="font-style: normal">foo[bar]baz</span></i>',
      'expected':    'false' },

    { 'id':          'VALUE-BC-FONT-STYLE-BC',
      'desc':        'query the value of the "backcolor" command',
      'qcvalue':     'backcolor',
      'pad':         '<font style="background-color: #ffccaa">foo[bar]baz</font>',
      'expected':    '#ffccaa' },

    { 'id':          'VALUE-BC-SPAN-STYLE-BC',
      'desc':        'query the value of the "backcolor" command',
      'qcvalue':     'backcolor',
      'pad':         '<span style="background-color: #aabbcc">foo[bar]baz</span>',
      'expected':    '#aabbcc' },

    { 'id':          'VALUE-BC-FONT-STYLE-BC-SPAN',
      'desc':        'query the value of the "backcolor" command, where the color was set on an ancestor',
      'qcvalue':     'backcolor',
      'pad':         '<font style="background-color: #008844"><span>foo[bar]baz</span></font>',
      'expected':    '#008844' },

    { 'id':          'VALUE-BC-SPAN-STYLE-BC-SPAN',
      'desc':        'query the value of the "backcolor" command, where the color was set on an ancestor',
      'qcvalue':     'backcolor',
      'pad':         '<span style="background-color: #ccddee"><span>foo[bar]baz</span></span>',
      'expected':    '#ccddee' },

    { 'id':          'VALUE-FN-FONT-FACE-Arial',
      'desc':        'query the value of the "fontname" command',
      'qcvalue':     'fontname',
      'pad':         '<font face="Arial">foo[bar]baz</font>',
      'expected':    'Arial' },

    { 'id':          'VALUE-FN-STYLE-FF-Arial',
      'desc':        'query the value of the "fontname" command',
      'qcvalue':     'fontname',
      'pad':         '<span style="font-family: Arial">foo[bar]baz</span>',
      'expected':    'Arial' },

    { 'id':          'VALUE-FN-FONT-FACE-Arial-STYLE-FF-Courier',
      'desc':        'query the value of the "fontname" command',
      'qcvalue':     'fontname',
      'pad':         '<font face="Arial" style="font-family: Courier">foo[bar]baz</font>',
      'expected':    'Courier' },

    { 'id':          'VALUE-FN-FONT-FACE-Arial-FONT-FACE-Courier',
      'desc':        'query the value of the "fontname" command',
      'qcvalue':     'fontname',
      'pad':         '<font face="Arial"><font face="Courier">foo[bar]baz</font></font>',
      'expected':    'Courier' },

    { 'id':          'VALUE-FN-STYLE-FF-Courier-FONT-FACE-Arial',
      'desc':        'query the value of the "fontname" command',
      'qcvalue':     'fontname',
      'pad':         '<span style="font-family: Courier"><font face="Arial">foo[bar]baz</font></span>',
      'expected':    'Arial' },

    { 'id':          'VALUE-FS-FONT-SIZE-4',
      'desc':        'query the value of the "fontsize" command',
      'qcvalue':     'fontsize',
      'pad':         '<font size=4>foo[bar]baz</font>',
      'expected':    '18px' },

    { 'id':          'VALUE-FS-FONT-STYLE-FS-large',
      'desc':        'query the value of the "fontsize" command',
      'qcvalue':     'fontsize',
      'pad':         '<font style="font-size: large">foo[bar]baz</font>',
      'expected':    '18px' },

    { 'id':          'VALUE-FS-FONT-SIZE-1-STYLE-FS-x-large',
      'desc':        'query the value of the "fontsize" command',
      'qcvalue':     'fontsize',
      'pad':         '<font size=1 style="font-size: x-large">foo[bar]baz</font>',
      'expected':    '24px' },

    { 'id':          'VALUE-FC-FONT-C',
      'desc':        'query the value of the "forecolor" command',
      'qcvalue':     'forecolor',
      'pad':         '<font color="#ff0000">foo[bar]baz</font>',
      'expected':    '#ff0000' },

    { 'id':          'VALUE-FC-STYLE-C',
      'desc':        'query the value of the "forecolor" command',
      'qcvalue':     'forecolor',
      'pad':         '<span style="color: #00ff00">foo[bar]baz</span>',
      'expected':    '#00ff00' },

    { 'id':          'VALUE-FC-FONT-C-STYLE-C',
      'desc':        'query the value of the "forecolor" command',
      'qcvalue':     'forecolor',
      'pad':         '<font color="#333333" style="color: #999999">foo[bar]baz</font>',
      'expected':    '#999999' },

    { 'id':          'VALUE-FC-FONT-C-SPAN',
      'desc':        'query the value of the "forecolor" command, where the color was set on an ancestor',
      'qcvalue':     'forecolor',
      'pad':         '<font color="#664411"><span>foo[bar]baz</span></font>',
      'expected':    '#664411' },

    { 'id':          'VALUE-FC-STYLE-C-SPAN',
      'desc':        'query the value of the "forecolor" command, where the color was set on an ancestor',
      'qcvalue':     'forecolor',
      'pad':         '<span style="color: #dd9955"><span>foo[bar]baz</span></span>',
      'expected':    '#dd9955' },

    { 'id':          'VALUE-HC-FONT-STYLE-BC',
      'desc':        'query the value of the "hilitecolor" command',
      'qcvalue':     'hilitecolor',
      'pad':         '<font style="background-color: #ffcc00">foo[bar]baz</font>',
      'expected':    '#ffcc00' },

    { 'id':          'VALUE-HC-SPAN-STYLE-BC',
      'desc':        'query the value of the "hilitecolor" command',
      'qcvalue':     'hilitecolor',
      'pad':         '<span style="background-color: #aa00cc">foo[bar]baz</span>',
      'expected':    '#aa00cc' },

    { 'id':          'VALUE-HC-FONT-STYLE-BC-SPAN',
      'desc':        'query the value of the "hilitecolor" command, where the color was set on an ancestor',
      'qcvalue':     'hilitecolor',
      'pad':         '<font style="background-color: #8833ee"><span>foo[bar]baz</span></font>',
      'expected':    '#8833ee' },

    { 'id':          'VALUE-HC-SPAN-STYLE-BC-SPAN',
      'desc':        'query the value of the "hilitecolor" command, where the color was set on an ancestor',
      'qcvalue':     'hilitecolor',
      'pad':         '<span style="background-color: #bb1122"><span>foo[bar]baz</span></span>',
      'expected':    '#bb1122' }
  ]
};


