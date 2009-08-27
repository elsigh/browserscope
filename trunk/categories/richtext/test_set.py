#!/usr/bin/python2.4
#
# Copyright 2009 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License')
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Rich Text Test Definitions."""

__author__ = 'elsigh@google.com (Lindsey Simon)'


from categories import test_set_base


_CATEGORY = 'richtext'


class RichtextTest(test_set_base.TestBase):
  TESTS_URL_PATH = '/%s/test' % _CATEGORY

  def __init__(self, key, name, doc, is_hidden_stat=True, category=None):
    """Initialze a test.

    Args:
      key: key for this in dict's
      name: a human readable label for display
      url_name: the name used in the url
      score_type: 'boolean' or 'custom'
      doc: a description of the test
      value_range: (min_value, max_value) as integer values
      is_hidden_stat: whether or not the test shown in the stats table
    """
    test_set_base.TestBase.__init__(
        self,
        key=key,
        name=name,
        url=self.TESTS_URL_PATH,
        score_type='boolean',
        doc=doc,
        min_value=0,
        max_value=1,
        is_hidden_stat=is_hidden_stat)

    # This way we can assign tests to a test group, i.e. apply, unapply, etc..
    if category:
      self.category = category

  def GetScoreAndDisplayValue(self, median, tests=None):
    """Returns a tuple with display text for the cell as well as a 1-100 value.
    """
    if score == None or score == '':
      return 0, ''

    display = score
    return score, display

_TESTS = (
  # key, name, doc
  RichtextTest('apply', 'Apply Formatting', '''About this test...''', False),
  RichtextTest('unapply', 'Un-Apply Formatting', '''About this test...''', False),
  RichtextTest('change', 'Change Existing Formatting', '''About this test...''', False),
  RichtextTest('query', 'Query State and Value', '''About this test...''', False),
  # Annie, put the rest of the individual tests here, like ...
  #RichtextTest('bold', 'Bolding', None, category='apply')
  RichtextTest('backcolor', 'backcolor execCommand on plaintext', None, category='apply')
  RichtextTest('bold', 'bold execCommand on plaintext', None, category='apply')
  RichtextTest('createbookmark', 'createbookmark execCommand on plaintext', None, category='apply')
  RichtextTest('createlink', 'createlink execCommand on plaintext', None, category='apply')
  RichtextTest('decreasefontsize', 'decreasefontsize execCommand on plaintext', None, category='apply')
  RichtextTest('fontname', 'fontname execCommand on plaintext', None, category='apply')
  RichtextTest('fontsize', 'fontsize execCommand on plaintext', None, category='apply')
  RichtextTest('forecolor', 'forecolor execCommand on plaintext', None, category='apply')
  RichtextTest('formatblock', 'formatblock execCommand on plaintext', None, category='apply')
  RichtextTest('hilitecolor', 'hilitecolor execCommand on plaintext', None, category='apply')
  RichtextTest('indent', 'indent execCommand on plaintext', None, category='apply')
  RichtextTest('inserthorizontalrule', 'inserthorizontalrule execCommand on plaintext', None, category='apply')
  RichtextTest('inserthtml', 'inserthtml execCommand on plaintext', None, category='apply')
  RichtextTest('insertimage', 'insertimage execCommand on plaintext', None, category='apply')
  RichtextTest('insertorderedlist', 'insertorderedlist execCommand on plaintext', None, category='apply')
  RichtextTest('insertunorderedlist', 'insertunorderedlist execCommand on plaintext', None, category='apply')
  RichtextTest('insertparagraph', 'insertparagraph execCommand on plaintext', None, category='apply')
  RichtextTest('italic', 'italic execCommand on plaintext', None, category='apply')
  RichtextTest('justifycenter', 'justifycenter execCommand on plaintext', None, category='apply')
  RichtextTest('justifyfull', 'justifyfull execCommand on plaintext', None, category='apply')
  RichtextTest('justifyleft', 'justifyleft execCommand on plaintext', None, category='apply')
  RichtextTest('justifyright', 'justifyright execCommand on plaintext', None, category='apply')
  RichtextTest('strikethrough', 'strikethrough execCommand on plaintext', None, category='apply')
  RichtextTest('subscript', 'subscript execCommand on plaintext', None, category='apply')
  RichtextTest('superscript', 'superscript execCommand on plaintext', None, category='apply')
  RichtextTest('underline', 'underline execCommand on plaintext', None, category='apply')
  RichtextTest('bold1', 'bold execCommand on text surrounded by <b> tags', None, category='unapply')
  RichtextTest('bold2', 'bold execCommand on text surrounded by <STRONG> tags', None, category='unapply')
  RichtextTest('bold3', 'bold execCommand on text surrounded by font-weight:bold style', None, category='unapply')
  RichtextTest('italic1', 'italic execCommand on text surrounded by <i> tags', None, category='unapply')
  RichtextTest('italic2', 'italic execCommand on text surrounded by <EM> tags', None, category='unapply')
  RichtextTest('italic3', 'italic execCommand on text surrounded by font-style:italic style', None, category='unapply')
  RichtextTest('outdent1', 'outdent execCommand on blockquote generated by Firefox indent', None, category='unapply')
  RichtextTest('outdent2', 'outdent execCommand on blockquote generated by IE indent', None, category='unapply')
  RichtextTest('outdent3', 'outdent execCommand on blockquote generated by webkit indent execCommand', None, category='unapply')
  RichtextTest('outdent4', 'outdent execCommand on unordered list', None, category='unapply')
  RichtextTest('outdent5', 'outdent execCommand on ordered list', None, category='unapply')
  RichtextTest('outdent6', 'outdent execCommand on blockquote generated by Firefox indent (styleWithCSS on)', None, category='unapply')
  RichtextTest('removeformat1', 'removeformat execCommand on text surrounded by <b> tags', None, category='unapply')
  RichtextTest('removeformat2', 'removeformat execCommand on text surrounded by <a> tags', None, category='unapply')
  RichtextTest('removeformat3', 'removeformat execCommand on text in table', None, category='unapply')
  RichtextTest('strikethrough1', 'strikethrough execCommand on text surrounded by <strike> tag', None, category='unapply')
  RichtextTest('strikethrough2', 'strikethrough execCommand on text surrounded by <s> tag', None, category='unapply')
  RichtextTest('strikethrough3', 'strikethrough execCommand on text surrounded by <del> tag', None, category='unapply')
  RichtextTest('strikethrough4', 'strikethrough execCommand on text surrounded by text-decoration:linethrough style', None, category='unapply')
  RichtextTest('subscript1', 'subscript execCommand on text surrounded by <sub> tag', None, category='unapply')
  RichtextTest('subscript2', 'subscript execCommand on text surrounded by vertical-align:sub style', None, category='unapply')
  RichtextTest('superscript1', 'superscript execCommand on text surrounded by <sup> tag', None, category='unapply')
  RichtextTest('superscript2', 'superscript execCommand on text surrounded by vertical-align:super style', None, category='unapply')
  RichtextTest('unbookmark', 'unbookmark execCommand on a bookmark created with createbookmark in IE', None, category='unapply')
  RichtextTest('underline1', 'underline execCommand on text surrounded by <u> tags', None, category='unapply')
  RichtextTest('underline2', 'underline execCommand on text surrounded by text-decoration:underline style', None, category='unapply')
  RichtextTest('backcolor1', 'queryCommandValue for backcolor on <font> tag with background-color style', None, category='query')
  RichtextTest('backcolor2', 'queryCommandValue for backcolor on <span> tag with background-color style generated by webkit', None, category='query')
  RichtextTest('backcolor3', 'queryCommandValue for backcolor on <span> tag with background-color style', None, category='query')
  RichtextTest('bold1', 'queryCommandState for bold on plain text', None, category='query')
  RichtextTest('bold2', 'queryCommandState for bold on text surrounded by <b> tags', None, category='query')
  RichtextTest('bold3', 'queryCommandState for bold on text surrounded by <STRONG> tags', None, category='query')
  RichtextTest('bold4', 'queryCommandState for bold on text surrounded by font-weight:bold style', None, category='query')
  RichtextTest('bold5', 'queryCommandState for bold on text surrounded by font-weight:normal style', None, category='query')
  RichtextTest('bold6', 'queryCommandState for bold on text surrounded by b tag with font-weight:bold style', None, category='query')
  RichtextTest('fontname1', 'queryCommandValue for fontname on <font> tag face attribute', None, category='query')
  RichtextTest('fontname2', 'queryCommandValue for fontname on font-family style', None, category='query')
  RichtextTest('fontname3', 'queryCommandValue for fontname on <font> tag with face attribute AND font-family style', None, category='query')
  RichtextTest('fontname4', 'queryCommandValue for fontname on nested <font> tags with different face attributes', None, category='query')
  RichtextTest('fontname5', 'queryCommandValue for fontname on <font> tag with face attribute surrounded by font-family style', None, category='query')
  RichtextTest('fontsize1', 'queryCommandValue for fontsize on <font> tag size attribute', None, category='query')
  RichtextTest('fontsize2', 'queryCommandValue for fontsize on font-size style', None, category='query')
  RichtextTest('fontsize3', 'queryCommandValue for fontsize on <font> tag with size attribute AND font-size style', None, category='query')
  RichtextTest('forecolor1', 'queryCommandValue for forecolor on <font> tag color attribute', None, category='query')
  RichtextTest('forecolor2', 'queryCommandValue for forecolor on color style', None, category='query')
  RichtextTest('forecolor3', 'queryCommandValue for forecolor on <font> tag with color attribute AND color style', None, category='query')
  RichtextTest('hilitecolor1', 'queryCommandValue for hilitecolor on <font> tag with background-color style', None, category='query')
  RichtextTest('hilitecolor2', 'queryCommandValue for hilitecolor on <span> tag with background-color style generated by webkit', None, category='query')
  RichtextTest('hilitecolor3', 'queryCommandValue for hilitecolor on <span> tag with background-color style', None, category='query')
  RichtextTest('insertorderedlist1', 'queryCommandState for insertorderedlist on plain text', None, category='query')
  RichtextTest('insertorderedlist2', 'queryCommandState for insertorderedlist on ordered list', None, category='query')
  RichtextTest('insertorderedlist3', 'queryCommandState for insertorderedlist on undordered list', None, category='query')
  RichtextTest('insertunorderedlist1', 'queryCommandState for insertunorderedlist on plain text', None, category='query')
  RichtextTest('insertunorderedlist2', 'queryCommandState for insertunorderedlist on ordered list', None, category='query')
  RichtextTest('insertunorderedlist3', 'queryCommandState for insertunorderedlist on undordered list', None, category='query')
  RichtextTest('italic1', 'queryCommandState for italic on plain text', None, category='query')
  RichtextTest('italic2', 'queryCommandState for italic on text surrounded by <i> tags', None, category='query')
  RichtextTest('italic3', 'queryCommandState for italic on text surrounded by <EM> tags', None, category='query')
  RichtextTest('italic4', 'queryCommandState for italic on text surrounded by font-style:italic style', None, category='query')
  RichtextTest('italic5', 'queryCommandState for italic on text surrounded by font-style:normal style italic tag', None, category='query')
  RichtextTest('justifycenter1', 'queryCommandState for justifycenter on plain text', None, category='query')
  RichtextTest('justifycenter2', 'queryCommandState for justifycenter on text centered by Firefox', None, category='query')
  RichtextTest('justifycenter3', 'queryCommandState for justifycenter on text centered by IE', None, category='query')
  RichtextTest('justifycenter4', 'queryCommandState for justifycenter on text centered by webkit', None, category='query')
  RichtextTest('justifyfull1', 'queryCommandState for justifyfull on plain text', None, category='query')
  RichtextTest('justifyfull2', 'queryCommandState for justifyfull on text justified by Firefox', None, category='query')
  RichtextTest('justifyfull3', 'queryCommandState for justifyfull on text justified by IE', None, category='query')
  RichtextTest('justifyfull4', 'queryCommandState for justifyfull on text justified by webkit', None, category='query')
  RichtextTest('justifyleft1', 'queryCommandState for justifyleft on plain text', None, category='query')
  RichtextTest('justifyleft2', 'queryCommandState for justifyleft on text left-aligned by Firefox', None, category='query')
  RichtextTest('justifyleft3', 'queryCommandState for justifyleft on text left-aligned by IE', None, category='query')
  RichtextTest('justifyleft4', 'queryCommandState for justifyleft on text left-aligned by webkit', None, category='query')
  RichtextTest('justifyright1', 'queryCommandState for justifyright on plain text', None, category='query')
  RichtextTest('justifyright2', 'queryCommandState for justifyright on text right-aligned by Firefox', None, category='query')
  RichtextTest('justifyright3', 'queryCommandState for justifyright on text right-aligned by IE', None, category='query')
  RichtextTest('justifyright4', 'queryCommandState for justifyright on text right-aligned by webkit', None, category='query')
  RichtextTest('strikethrough1', 'queryCommandState for strikethrough on plain text', None, category='query')
  RichtextTest('strikethrough2', 'queryCommandState for strikethrough on text surrounded by <strike> tag', None, category='query')
  RichtextTest('strikethrough3', 'queryCommandState for strikethrough on text surrounded by <strike> tag with text-decoration:none style', None, category='query')
  RichtextTest('strikethrough4', 'queryCommandState for strikethrough on text surrounded by <s> tag', None, category='query')
  RichtextTest('strikethrough5', 'queryCommandState for strikethrough on text surrounded by <del> tag', None, category='query')
  RichtextTest('strikethrough6', 'queryCommandState for strikethrough on text surrounded by b tag with text-decoration:line-through style', None, category='query')
  RichtextTest('subscript1', 'queryCommandState for subscript on plain text', None, category='query')
  RichtextTest('subscript2', 'queryCommandState for subscript on text surrounded by <sub> tag', None, category='query')
  RichtextTest('superscript1', 'queryCommandState for superscript on plain text', None, category='query')
  RichtextTest('superscript2', 'queryCommandState for superscript on text surrounded by <sup> tag', None, category='query')
  RichtextTest('underline1', 'queryCommandState for underline on plain text', None, category='query')
  RichtextTest('underline1', 'queryCommandState for underline on text surrounded by <u> tag', None, category='query')
  RichtextTest('underline3', 'queryCommandState for underline on text surrounded by <a> tag', None, category='query')
  RichtextTest('underline4', 'queryCommandState for underline on text surrounded by text-deocoration:undeline style', None, category='query')
  RichtextTest('underline5', 'queryCommandState for underline on text surrounded by <u> tag with text-decoration:none style', None, category='query')
  RichtextTest('underline6', 'queryCommandState for underline on text surrounded by <a> tag with text-decoration:none style', None, category='query')
  RichtextTest('backcolor1', 'backcolor execCommand on text surrounded by <font> tag with background-color style', None, category='change')
  RichtextTest('backcolor2', 'backcolor execCommand on text with background-color style generated by webkit', None, category='change')
  RichtextTest('backcolor3', 'backcolor execCommand on text with background-color style', None, category='change')
  RichtextTest('fontname1', 'fontname execCommand on text surrounded by <font> tag with face attribute', None, category='change')
  RichtextTest('fontname2', 'fontname execCommand on text with font-family style', None, category='change')
  RichtextTest('fontname3', 'fontname execCommand on text surrounded by <font> tag with face attribute AND font-family style', None, category='change')
  RichtextTest('fontname4', 'fontname execCommand on text surrounded by nested <font> tags with face attributes', None, category='change')
  RichtextTest('fontname5', 'fontname execCommand on text surrounded by <font> tag with face attribute inside font-family style', None, category='change')
  RichtextTest('fontsize1', 'fontsize execCommand on text surrounded by <font> tag with size attribute', None, category='change')
  RichtextTest('fontsize2', 'fontsize execCommand on text with font-size style', None, category='change')
  RichtextTest('fontsize3', 'fontsize execCommand on text surrounded by <font> tag with size attribute AND font-size style', None, category='change')
  RichtextTest('forecolor1', 'forecolor execCommand on text surrounded by <font> tag with color attribute', None, category='change')
  RichtextTest('forecolor2', 'forecolor execCommand on text with color style', None, category='change')
  RichtextTest('forecolor3', 'forecolor execCommand on text surrounded by <font> tag with color attribute AND color style', None, category='change')
  RichtextTest('hilitecolor1', 'hilitecolor execCommand on text surrounded by <font> tag with background-color style', None, category='change')
  RichtextTest('hilitecolor2', 'hilitecolor execCommand on text with background-color style generated by webkit', None, category='change')
  RichtextTest('hilitecolor3', 'hilitecolor execCommand on text with background-color style', None, category='change')
)


TEST_SET = test_set_base.TestSet(
    category=_CATEGORY,
    category_name='Rich Text',
    tests=_TESTS,
    subnav={
      'Test': '/%s/test' % _CATEGORY,
      'About': '/%s/about' % _CATEGORY
    },
    home_intro='These are the Rich Text tests...'
)
