/**
 * @fileoverview 
 * Functions used to handle test and expectation strings.
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
 * The selection is specified "inline", using special characters:
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
 *
 * @param suite {Object} suite that test originates in as object reference
 * @param test {Object} test to be run as object reference
 * @param container {Object} container descriptor as object reference
 */
function initContainer(suite, test, container) {
  var pad = getParameter(suite, test, PARAM_PAD);
  pad = canonicalizeSpaces(pad);
  pad = convertSelectionIndicators(pad);

  var selection = {
    anchor: null,
    focus:  null,
    range:  null
  };

  win = container.win;
  doc = container.doc;
  body = container.body;

  body.innerHTML = container.canary + container.tagOpen + pad + container.tagClose + container.canary;

  editor = container.contentEditableID ? doc.getElementById(container.contentEditableID)
                                       : body;
  container.editor = editor;

  if (!editor) {
    throw SETUP_CONTAINER;
  }

  if (getParameter(suite, test, PARAM_STYLE_WITH_CSS)) {
    try {
      doc.execCommand('styleWithCSS', false, true);
    } catch (ex) {
      // ignore exception if unsupported
    }
  }

  selection.anchor = deriveSelectionPoint(editor, '[');
  selection.focus = deriveSelectionPoint(editor, ']');
  selection.range = null;

  // sanity check
  if (!selection.anchor || !selection.focus) {
    throw SETUP_SELECTION;
  }

  if (!selection.anchor.node || !selection.focus.node) {
    if (selection.anchor.node || selection.focus.node) {
      // Broken test: only one selection point was specified
      throw SETUP_BAD_SELECTION_SPEC;
    }
    return;
  }

  if (selection.anchor.node === selection.focus.node) {
    if (selection.anchor.offs > selection.focus.offs) {
      // Both selection points are within the same node, the selection was
      // specified inline (thus the end indicator element or character was
      // removed), and the end point is before the start (reversed selection).
      // Start offset that was derived is now off by 1 and needs adjustment.
      --selection.anchor.offs;
    }

    if (selection.anchor.offs === selection.focus.offs) {
      selection.range = createCaret(
          selection.anchor.node,
          selection.anchor.offs
      );
    }
  }

  if (!selection.range) {
    selection.range = createFromNodes(
        selection.anchor.node,
        selection.anchor.offs,
        selection.focus.node,
        selection.focus.offs
    );
  }

  selection.range.select();
  sel = win.getSelection();
}

/**
 * Reset the editor element after a test is run.
 */
function resetEditorElements() {
  // Clean errant styles on body of all containers
  for (var c = 0; c < containerIDs.length; ++c) {
    var id = containerIDs[c];

    containers[id].body.setAttribute('style', '');
    containers[id].body.setAttribute('bgcolor', '');

    try {
      containers[id].doc.execCommand('styleWithCSS', false, false);
    } catch (ex) {
      // ignore exception if unsupported
    }
  }

  selection = null;
}

/**
 * Initialize the editor document.
 */
function initEditorDocs() {
  // Wrap initialization code in a try/catch so we can fail gracefully
  // on older browsers.
  try {
    for (var c = 0; c < containerIDs.length; ++c) {
      var id = containerIDs[c];

      containers[id] = {
        iframe: null,
        win:    null,
        doc:    null,
        body:   null,
        editor: null,
        tagOpen: '',
        tagClose: '',
        canary: ''
      };
      containers[id].iframe = document.getElementById('iframe-' + id);
      containers[id].win = containers[id].iframe.contentWindow;
      containers[id].doc = containers[id].win.document;
      containers[id].body = containers[id].doc.body;

      // Default styleWithCSS to false, since it's not supported by IE.
      try {
        containers[id].doc.execCommand('styleWithCSS', false, false);
      } catch (ex) {
        // Not supported by IE.
      }
    }
    
    // IMPORTANT: the tagOpen/Close and canary fields are NOT canonicalized before comparison!
    // So make sure they are correct!
    containers['div'].contentEditableID = 'editor-div';
    containers['div'].tagOpen = '<div contenteditable="true" id="' + containers['div'].contentEditableID + '">';
    containers['div'].tagClose = '</div>';
    containers['div'].canary = CANARY;
  } catch (ex) {
    writeFatalError("Exception setting up the environment: " + ex.toString());
  }
}
