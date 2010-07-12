/**
 * @fileoverview 
 * Functions used to handle test and expectation strings.
 *
 * TODO: license! $$$
 *
 * @version 0.1
 * @author rolandsteiner@google.com
 */

/**
 * Normalize text selection indicators and convert inter-element selection
 * indicators to comments.
 *
 * Note that this function relies on the spaces of the input string already
 * having been normalized by canonicalizeSpaces!
 *
 * @param pad {String} HTML string that includes selection marker characters
 * @return {String} the HTML string with the selection markers converted
 */
function convertSelectionIndicators(pad) {
  // Sanity check: Markers { } | only directly before or after an element,
  // or just before a closing > (i.e., not within a text node).
  // Note that intra-tag selection markers have already been converted to the
  // special selection attribute(s) above.
  if (/[^>][{}\|][^<>]/.test(pad) ||
      /^[{}\|][^<]/.test(pad) ||
      /[^>][{}\|]$/.test(pad) ||
      /^[{}\|]*$/.test(pad)) {
    throw SETUP_BAD_SELECTION_SPEC;
  }

  // Convert intra-tag selection markers to special attributes.
  pad = pad.replace(/\{\>/g, ATTRNAME_SEL_START + '="1">');  
  pad = pad.replace(/\}\>/g, ATTRNAME_SEL_END + '="1">');  
  pad = pad.replace(/\|\>/g, ATTRNAME_SEL_START + '="1" ' + 
                             ATTRNAME_SEL_END + '="1">'); 

  // Convert remaining {, }, | to comments with '[' and ']' data.
  pad = pad.replace('{', '<!--[-->');
  pad = pad.replace('}', '<!--]-->');
  pad = pad.replace('|', '<!--[--><!--]-->');

  // Convert caret indicator ^ to empty selection indicator []
  // (this simplifies further processing).
  pad = pad.replace(/\^/, '[]');

  return pad;
}

/**
 * Derives one point of the selection from the indicators with the HTML tree:
 * '[' or ']' within a text or comment node, or the special selection
 * attributes within an element node.
 *
 * @param root {DOMNode} root node of the recursive search
 * @param marker {String} which marker to look for: '[' or ']'
 * @return {Object} a pair object: {node: {DOMNode}/null, offset: {Integer}}
 */
function deriveSelectionPoint(root, marker) {
  switch (root.nodeType) {
    case DOM_NODE_TYPE_ELEMENT:
      if (root.attributes) {
        // Note: getAttribute() is necessary for this to work on all browsers!
        if (marker == '[' && root.getAttribute(ATTRNAME_SEL_START)) {
          root.removeAttribute(ATTRNAME_SEL_START);
          return {node: root, offs: 0};
        }
        if (marker == ']' && root.getAttribute(ATTRNAME_SEL_END)) {
          root.removeAttribute(ATTRNAME_SEL_END);
          return {node: root, offs: 0};
        }
      }
      for (var i = 0; i < root.childNodes.length; ++i) {
        var pair = deriveSelectionPoint(root.childNodes[i], marker);
        if (pair.node) {
          return pair;
        }
      }
      break;
      
    case DOM_NODE_TYPE_TEXT:
      var pos = root.data.indexOf(marker);
      if (pos != -1) {
        // Remove selection marker from text.
        var nodeText = root.data;
        root.data = nodeText.substr(0, pos) + nodeText.substr(pos + 1);
        return {node: root, offs: pos };
      }
      break;

    case DOM_NODE_TYPE_COMMENT:
      var pos = root.data.indexOf(marker);
      if (pos != -1) {
        // Remove comment node from parent.
        var helper = root.previousSibling;

        for (pos = 0; helper; ++pos ) {
          helper = helper.previousSibling;
        }
        helper = root;
        root = root.parentNode;
        root.removeChild(helper);
        return {node: root, offs: pos };
      }
      break;
  }

  return {node: null, offs: 0 };
}

/**
 * Initialize the test HTML with the starting state specified in the test.
 *
 * The selection can be specified explicitly, as one of:
 *   selFrom: <posStart>,
 *   selTo:   <posEnd>
 * OR
 *   selCaret: <posCaret>
 * OR
 *   selWord: "word"
 *
 * where <posCaret>, <posStart>, <posEnd> can be specified as:
 *   [node, offset]
 *   ["id", offset]
 *
 * "word" specifies a single consecutive piece of text content that should be
 * fully selected.
 *
 * The selection can be also be specified "inline", using special characters:
 *     ^   a collapsed text caret selection (same as [])
 *     [   the selection start within a text node
 *     ]   the selection end within a text node
 *     |   collapsed selection between elements (same as {})
 *     {   selection starting with the following element
 *     }   selection ending with the preceding element
 * {, } and | can also be used within an element tag, just before the closing
 * angle bracket > to specify a selection [element, 0] where the element
 * doesn't otherwise have any children. Ex.: <hr {>foobarbaz<hr }>
 *
 * Explicit and implicit specification can also be mixed between the 2 points.
 * 
 * A pad string must only contain at most ONE of the above that is suitable for
 * that start or end point, respectively, and must contain either both or none.
 */
function initEditorElement() {
  var pad = getTestParameter(PARAM_PAD);

  pad = canonicalizeSpaces(pad);
  pad = convertSelectionIndicators(pad);

  if (getTestParameter(PARAM_STYLE_WITH_CSS)) {
    try {
      editorDoc.execCommand('styleWithCSS', false, true);
    } catch (ex) {
    }
  }
  try {
    contentEditableElem.innerHTML = pad;
  } catch (ex) {
    return SETUP_HTML_EXCEPTION;
  }

  var pair1 = deriveSelectionPoint(contentEditableElem, '[');
  var pair2 = deriveSelectionPoint(contentEditableElem, ']');

  if (!pair1.node || !pair2.node) {
    if (pair1.node || pair2.node) {
      // Broken test: only one selection point was specified
      throw SETUP_BAD_SELECTION_SPEC;
    }
    return;
  }

  if (pair1.node === pair2.node) {
    if (pair1.offs > pair2.offs && !currentTest.selFrom && !currentTest.selTo) {
      // Both selection points are within the same node, the selection was
      // specified inline (thus the end indicator element or character was
      // removed), and the end point is before the start (reversed selection).
      // Start offset that was derived is now off by 1 and needs adjustment.
      --pair1.offs;
    }

    if (pair1.offs == pair2.offs) {
      var caret = createCaret(pair1.node, pair1.offs);
      caret.select();
      return;
    }
  }

  var range = createFromNodes(pair1.node, pair1.offs, pair2.node, pair2.offs);
  range.select();
}

/**
 * Reset the editor element after a test is run.
 */
function resetEditorElement() {
  // These attributes can get set on the iframe by some errant execCommands
  contentEditableElem.setAttribute('style', '');
  contentEditableElem.setAttribute('bgcolor', '');

  if (getTestParameter(PARAM_STYLE_WITH_CSS)) {
    try {
      editorDoc.execCommand('styleWithCSS', false, false);
    } catch (ex) {
    }
  }
}

/**
 * Initialize the editor document.
 */
function initEditorDoc() {
  // Wrap initialization code in a try/catch so we can fail gracefully
  // on older browsers.
  try {
 
    // version using IFRAME
    editorElem = document.getElementById('editor');
    editorWin = editorElem.contentWindow;
    editorDoc = editorWin.document;
    contentEditableElem = editorDoc.body;
/*
    // version using a simple DIV
    editorElem = document.getElementById('editor');
    editorWin = window;
    editorDoc = document;
    contentEditableElem = editorElem;
*/
    // Default styleWithCSS to false, since it's not supported by IE.
    try {
      editorDoc.execCommand('styleWithCSS', false, false);
    } catch (ex) {
      // Not supported by IE.
    }
    
    // FF "ice breaker": execCommand('delete') silently fails in FF when run
    // on a document within an IFRAME, unless an insert command has run
    // before it.
    try {
      contentEditableElem.innerHTML = 'foobar';
      var caret = createCaret(contentEditableElem.firstChild, 3);
      caret.select();
      editorDoc.execCommand('insertHorizontalRule', false, null);
    } catch (ex) {
      // Ignore, perhaps unsupported command by other browser
    }
  } catch (ex) {
    alert("Exception setting up the environment: " + ex.toString());
  }
}
