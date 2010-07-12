/**
 * @fileoverview 
 * Comparison functions used in the RTE test suite.
 *
 * TODO: license! $$$
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
function compareTestResultToSingleExpectation(expected, actual, checkSel) {
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
  return RESULT_HTML_DIFFS;
}

/**
 * Compare the current test result to the expectation string(s).
 *
 * @return {Integer} one of the RESULT_... return values
 * @see variables.js for return values
 */
function compareTestResult() {
  var checkSel = getTestParameter(PARAM_CHECK_SELECTION);
  var emitFlags = {emitAttrs:         getTestParameter(PARAM_CHECK_ATTRIBUTES),
                   emitStyle:         getTestParameter(PARAM_CHECK_STYLE),
                   emitClass:         getTestParameter(PARAM_CHECK_CLASS),
                   emitID:            getTestParameter(PARAM_CHECK_ID),
                   lowercase:         true,
                   canonicalizeUnits: true};
  var hasSelMarkers = /[\[\]\^{}\|]/;
  
  var actual = currentResultHTML;
  // Remove closing tags </hr>, </br> for comparison.
  actual = actual.replace(/<\/[hb]r>/g, '');
  // Remove text node markers for comparison.
  actual = actual.replace(/[`´]/g, '');
  // Canonicalize result.
  actual = canonicalizeElementsAndAttributes(actual, emitFlags);

  // Treat a single test expectation string as an array of 1 expectation.
  var expectedSpec = getTestParameter(PARAM_EXPECTED);
  var expectedArr;
  if (typeof expectedSpec == 'string') {
    expectedArr = [expectedSpec];
  } else {
    expectedArr = expectedSpec;
  }
  
  // Find the most favorable result among the possible expectation strings.
  var count = expectedArr.length;
  var best = RESULT_HTML_DIFFS;
  for (var idx = 0; idx < count; ++idx) {
    var expected = canonicalizeSpaces(expectedArr[idx]);
    expected = canonicalizeElementsAndAttributes(expected, emitFlags);
    // FIXME: The RegExp below is probably too simple and
    // may trigger on attribute values, etc.
    var result = compareTestResultToSingleExpectation(
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
      if (child) {
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
      } else {
        // node has no other children: insert as special attribute(s)
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

