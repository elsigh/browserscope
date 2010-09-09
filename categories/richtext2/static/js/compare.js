/**
 * @fileoverview 
 * Comparison functions used in the RTE test suite.
 *
 * Copyright 2010 Google Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the 'License')
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an 'AS IS' BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * @version 0.1
 * @author rolandsteiner@google.com
 */

/**
 * Compare a test result to a single expectation string.
 *
 * FIXME: add support for optional elements/attributes.
 *
 * @param expected {String} the already canonicalized (with the exception of selection marks) expectation string
 * @param actual {String} the already canonicalized (with the exception of selection marks) actual result
 * @param checkSel {Bool} whether the correctness of the resulst selection should be checked for
 * @return {Integer} one of the RESULT_... return values
 * @see variables.js for return values
 */
function compareHTMLTestResultToSingleHTMLExpectation(expected, actual, checkSel) {
  // If the test checks the selection, then the actual string must match the
  // expectation exactly.
  if (checkSel && expected == actual) {
    return RESULT_EQUAL;
  }

  // Remove selection markers and see if strings match then.
  expected = expected.replace(/ [{}\|]>/g, '>');     // intra-tag
  expected = expected.replace(/[\[\]\^{}\|]/g, '');  // outside tag
  actual = actual.replace(/ [{}\|]>/g, '>');         // intra-tag
  actual = actual.replace(/[\[\]\^{}\|]/g, '');      // outside tag
  if (expected == actual) {
    // If the test doesn't care about selection then we can treat the result
    // as fully conformant. Flag selection differences otherwise.
    return checkSel ? RESULT_SELECTION_DIFFS : RESULT_EQUAL;
  }
  return RESULT_DIFFS;
}

/**
 * Gets the test expectations as an array from the passed-in field.
 *
 * @param {Array|String} the test expectation(s) as string or array.
 * @return {Array} test expectations as an array.
 */
function getExpectationArray(expected) {
  // Treat a single test expectation string or bool as an array of 1 expectation.
  switch (typeof expected) {
    case 'string':
    case 'boolean':
      return [expected];
  }
  return expected;
}

/**
 * Compare the current HTMLtest result to the expectation string(s).
 *
 * @param {String/Boolean} actual value
 * @param {String/Array} expectation(s)
 * @param {Object} flags to use for canonicalization
 * @param {Boolean} whether to check the result selection
 * @return {Integer} one of the RESULT_... return values
 * @see variables.js for return values
 */
function compareHTMLTestResultWith(actual, expected, emitFlags, checkSel) {
  // Find the most favorable result among the possible expectation strings.
  var expectedArr  = getExpectationArray(expected);
  var count = expectedArr.length;
  var best = RESULT_DIFFS;
  for (var idx = 0; idx < count; ++idx) {
    var expected = canonicalizeSpaces(expectedArr[idx]);
    expected = canonicalizeElementsAndAttributes(expected, emitFlags);
    // FIXME: The RegExp below is probably too simple and
    // may trigger on attribute values, etc.
    var result = compareHTMLTestResultToSingleHTMLExpectation(
                     expected,
                     actual,
                     checkSel != false &&
                         (checkSel || hasSelMarkers.test(expected)));
    if (result == RESULT_EQUAL) {
      // Shortcut: it doesn't get any better.
      return RESULT_EQUAL;
    }
    if (result > best) {
      best = result;
    }
  }
  return best;
}

/**
 * Compare the current HTMLtest result to the expectation string(s).
 *
 * @return {Integer} one of the RESULT_... return values
 * @see variables.js for return values
 */
function compareHTMLTestResult() {
  var checkSel = getTestParameter(PARAM_CHECK_SELECTION);
  var emitFlags = {emitAttrs:         getTestParameter(PARAM_CHECK_ATTRIBUTES),
                   emitStyle:         getTestParameter(PARAM_CHECK_STYLE),
                   emitClass:         getTestParameter(PARAM_CHECK_CLASS),
                   emitID:            getTestParameter(PARAM_CHECK_ID),
                   lowercase:         true,
                   canonicalizeUnits: true};
  
  var actual = currentResultHTML;
  // Remove closing tags </hr>, </br> for comparison.
  actual = actual.replace(/<\/[hb]r>/g, '');
  // Remove text node markers for comparison.
  actual = actual.replace(/[\x60\xb4]/g, '');
  // Canonicalize result.
  actual = canonicalizeElementsAndAttributes(actual, emitFlags);

  var expected = getTestParameter(PARAM_EXPECTED);
  var bestExpected = compareHTMLTestResultWith(actual, expected, emitFlags, checkSel);
  if (bestExpected == RESULT_EQUAL) {
    return RESULT_EQUAL;
  }
  var accepted = getTestParameter(PARAM_ACCEPT);
  if (!accepted) {
    return bestExpected;
  }
  var bestAccepted = compareHTMLTestResultWith(actual, accepted, emitFlags, checkSel);
  if (bestAccepted == RESULT_EQUAL) {
    return RESULT_ACCEPT;
  }
  return bestExpected > bestAccepted ? bestExpected : bestAccepted;
}

/**
 * Compare a text test result to the expectation string(s).
 *
 * @param {String/Boolean} actual value
 * @param {String/Array} expectation(s)
 * @return {Boolean} whether we found a match
 */
function compareTextTestResultWith(actual, expected) {
  var expectedArr = getExpectationArray(expected);
  // Find the most favorable result among the possible expectation strings.
  var count = expectedArr.length;
  
  // We only need to look at Color and Size units if the originating test
  // was for queryCommandValue. If queryCommandValue is not for a color/size
  // specific state, or it it wasn't a queryCommandValue test at all, then
  // just compare directly.
  //
  // TODO(rolandsteiner): This is ugly! Refactor!
  switch (getTestParameter(PARAM_QUERYCOMMANDVALUE)) {
    case 'backcolor':
    case 'forecolor':
    case 'hilitecolor':
      for (var idx = 0; idx < count; ++idx) {
        if (new Color(actual).compare(new Color(expectedArr[idx]))) {
          return true;
        }
      }
      return false;
    
    case 'fontsize':
      for (var idx = 0; idx < count; ++idx) {
        if (new Size(actual).compare(new Size(expectedArr[idx]))) {
          return true;
        }
      }
      return false;
    
    default:
      for (var idx = 0; idx < count; ++idx) {
        if (actual === expectedArr[idx]) {
          return true;
        }
      }
  }
  
  return false;
}

/**
 * Compare the passed-in text test result to the expectation string(s).
 *
 * @param {String/Boolean} actual value
 * @return {Integer} one of the RESULT_... return values
 * @see variables.js for return values
 */
function compareTextTestResult(actual) {
  var expected = getTestParameter(PARAM_EXPECTED);
  if (compareTextTestResultWith(actual, expected)) {
    return RESULT_EQUAL;
  }
  var accepted = getTestParameter(PARAM_ACCEPT);
  if (accepted && compareTextTestResultWith(actual, accepted)) {
    return RESULT_ACCEPT;
  }
  return RESULT_DIFFS;
}

/**
 * Insert a selection position indicator.
 *
 * @param node {DOMNode} the node where to insert the selection indicator
 * @param offs {Integer} the offset of the selection indicator
 * @param textInd {String}  the indicator to use if the node is a text node
 * @param elemInd {String}  the indicator to use if the node is an element node
 */
function insertSelectionIndicator(node, offs, textInd, elemInd) {
  switch (node.nodeType) {
    case DOM_NODE_TYPE_TEXT:
      // Insert selection marker for text node into text content.
      var text = node.data;
      node.data = text.substring(0, offs) + textInd + text.substring(offs);
      break;
      
    case DOM_NODE_TYPE_ELEMENT:
      var child = node.firstChild;
      try {
        // node has other children: insert marker as comment node
        var comment = document.createComment(elemInd);
        while (child && offs) {
          --offs;
          child = child.nextSibling;
        }
        if (child) {
          node.insertBefore(comment, child);
        } else {
          node.appendChild(comment);
        }
      } catch (ex) {
        // can't append child comment -> insert as special attribute(s)
        switch (elemInd) {
          case '|':
            node.setAttribute(ATTRNAME_SEL_START, '1');
            node.setAttribute(ATTRNAME_SEL_END, '1');
            break;

          case '{':
            node.setAttribute(ATTRNAME_SEL_START, '1');
            break;

          case '}':
            node.setAttribute(ATTRNAME_SEL_END, '1');
            break;
        }
      }
      break;
  }
}

/**
 * Retrieve the result of a test run and do some preliminary canonicalization.
 */
function prepareTestResult() {
  // 1.) insert selection markers
  var selRange = createFromWindow(editorWin);
  if (selRange) {
    // save values, since range object gets auto-modified
    var node1 = selRange.getAnchorNode();
    var offs1 = selRange.getAnchorOffset();
    var node2 = selRange.getFocusNode();
    var offs2 = selRange.getFocusOffset();
    if (node1 && node1 == node2 && offs1 == offs2) {
      // collapsed selection
      insertSelectionIndicator(node1, offs1, '^', '|');
    } else {
      // Start point and end point are different
      if (node1) {
        insertSelectionIndicator(node1, offs1, '[', '{');
      }

      if (node2) {
        if (node1 == node2 && offs1 < offs2) {
          // Anchor indicator was inserted under the same node, so we need
          // to shift the offset by 1
          ++offs2;
        }
        insertSelectionIndicator(node2, offs2, ']', '}');
      }
    }
  }

  // 2.) insert markers for text node boundaries;
  encloseTextNodesWithQuotes(contentEditableElem);
  
  // 3.) retrieve innerHTML, canonicalize spacing
  currentResultHTML = canonicalizeSpaces(contentEditableElem.innerHTML);

  // 4a.) remove comment start and end comment tags, retain only {, } and |
  currentResultHTML = currentResultHTML.replace(/ ?<!-- ?/g, '');
  currentResultHTML = currentResultHTML.replace(/ ?--> ?/g, '');
}

