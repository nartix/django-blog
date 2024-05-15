import { Extension, findChildren } from '@tiptap/core';
import { Plugin, PluginKey, TextSelection } from 'prosemirror-state';
import { Decoration, DecorationSet } from 'prosemirror-view';
import { DOMParser } from 'prosemirror-model';
import { LowlightPlugin } from './pluginLowlight';
import Code from '@tiptap/extension-code';

import { hljs, lowlight } from '../editor';

const CursorPositionExtension = Extension.create({
  name: 'cursorPosition',

  addProseMirrorPlugins() {
    return [
      new Plugin({
        view: (view) => {
          const updateCursorPosition = () => {
            const { from, to } = view.state.selection;
            // Log the cursor position or range
            console.log(`Cursor from: ${from}, to: ${to}`);
          };

          updateCursorPosition(); // Call it initially

          return {
            update: (view, prevState) => {
              if (view.state.selection !== prevState.selection) {
                updateCursorPosition();
              }
            },
          };
        },
      }),
    ];
  },
});

// for use with unicode Emoji or to to insert any characters at cursor.
const DynamicCharInsertionExtension = Extension.create({
  name: 'dynamicCharInsertion',

  addOptions() {
    return {
      char: '', // Initial character
    };
  },

  addCommands() {
    return {
      setChar:
        (char) =>
        ({ commands }) => {
          return commands.insertContent(char);
        },
    };
  },
});

const CodeCheckExtension = Extension.create({
  name: 'codeCheck',

  addProseMirrorPlugins() {
    return [
      new Plugin({
        view: () => {
          return {
            update: (view, prevState) => {
              // Function to check the current selection
              const checkSelection = () => {
                const { state } = view;
                const { selection } = state;
                const { $anchor } = selection;

                // Check if the selection is within a 'code' node
                // and if that 'code' node is within a 'pre' node.
                const isInCode = $anchor.parent.type.name === 'codeBlock'; // Assuming 'code_block' is the name used in your schema for code blocks

                if (isInCode) {
                  // Further check if the code block is a direct child of a 'pre' tag.
                  // This requires a specific setup in your schema to differentiate between code blocks within 'pre' and other types of content.
                  // For a basic setup, this might just be checking the direct parent or a specific attribute.
                  // This example assumes a simplistic check. You might need to adjust based on your actual schema and how 'pre' tags are represented.

                  // Log the result
                  console.log('Within code block: ', isInCode); // True if within 'code_block', adjust your check as needed
                } else {
                  console.log('Within code block: ', false);
                }
              };

              // Call the check function whenever the document or selection changes
              if (view.state.doc !== prevState.doc || view.state.selection !== prevState.selection) {
                checkSelection();
              }
            },
          };
        },
      }),
    ];
  },
});

const InlineCodeCheckExtension = Extension.create({
  name: 'inlineCodeCheck',

  addProseMirrorPlugins() {
    return [
      new Plugin({
        view: () => ({
          update: (view, prevState) => {
            const { state } = view;
            const { selection } = state;
            const { $from } = selection;

            // Check for inline code mark
            const isInInlineCode = $from.marks().some((mark) => mark.type.name === 'code');

            // Check if the selection/cursor is within a code_block node
            const isInCodeBlock = $from.node($from.depth).type.name === 'codeBlock';

            // Log true if within inline code and not within a code block
            console.log('Within inline code: ', isInInlineCode && !isInCodeBlock);
          },
        }),
      }),
    ];
  },
});

const InlineCodeTransformExtension = Extension.create({
  name: 'inlineCodeTransform',

  addGlobalAttributes() {
    return [
      {
        types: ['textStyle'],
        attributes: {
          inlineCodeTransform: {
            default: null,
            parseHTML: (element) => {
              return {
                inlineCodeTransform: element.getAttribute('data-inline-code-transform'),
              };
            },
            renderHTML: (attributes) => {
              if (!attributes.inlineCodeTransform) {
                return {};
              }

              return {
                'data-inline-code-transform': attributes.inlineCodeTransform,
              };
            },
          },
        },
      },
    ];
  },

  addCommands() {
    return {
      transformInlineCode:
        () =>
        ({ state, dispatch, commands }) => {
          const { tr } = state;
          let modified = false;

          state.doc.descendants((node, pos) => {
            if (node.isText && node.marks.some((mark) => mark.type.name === 'code')) {
              // Check for text nodes that have the "code" mark.
              // const newText = hljs.highlightAuto(node.text).value; // Append "123" to the node's text.
              // const result = lowlight.highlightAuto(newText);
              // const renderedText = result.value.map((item) => item.value).join('');

              // console.log('test: ', hljs.highlightAuto(newText).value);
              // tr.insertText(newText, pos, pos + node.nodeSize); // Replace the text directly with tr.insertText

              const newText = hljs.highlightAuto(node.text).value;
              const newNode = state.schema.text(newText, [state.schema.marks.code.create()]);
              console.log('new content: ', newText);
              // tr.insertText(newText, pos, pos + node.nodeSize);

              // Set the selection to the node's position and replace the text
              // tr.setSelection(new TextSelection(tr.doc.resolve(pos), tr.doc.resolve(pos + node.nodeSize)));
              // tr.setSelection(TextSelection.create(newNode, pos, tr.doc.resolve(pos + newNode.nodeSize)));
              // commands.setContent(`sdfsdfsdfsdf`);
              // tr.replaceWith(pos, pos + node.nodeSize, newNode);
              const from = tr.doc.resolve(pos);
              const to = tr.doc.resolve(pos + node.nodeSize);
              tr.setSelection(new TextSelection(from, to));
              tr.replaceWith(from.pos, to.pos, newNode);

              modified = true;
            }
          });

          if (modified) {
            dispatch(tr); // Apply the transaction if changes have been made
            return true;
          }

          return false;
        },
    };
  },
});

const HighlightCodeExtension = Extension.create({
  name: 'highlightCode',

  addDecorations() {
    return ({ doc, tr }) => {
      const decorations = [];
      const highlightDecoration = (node, pos) => {
        if (node.isText && node.marks.some((mark) => mark.type.name === 'code')) {
          const html = hljs.highlightAuto(node.text).value;
          const decoration = document.createElement('span');
          console.log('decoration: ', html);
          decoration.innerHTML = html;
          decorations.push(tr.doc.type.schema.marks.code.create({}, decoration));
        }
      };

      doc.descendants(highlightDecoration);
      return decorations;
    };
  },
});

// changes the background to yellow at current cursor -- working
const testProseMirrorPluggin2 = Extension.create({
  name: 'testPluggin',

  addProseMirrorPlugins() {
    const pluginKey = new PluginKey('testPluggin');
    return [
      new Plugin({
        key: pluginKey,
        state: {
          init(_, { doc }) {
            return DecorationSet.empty;
          },
          apply: (tr, set) => {
            // If the transaction changes the selection, update the decoration
            if (tr.selectionSet) {
              const { selection } = tr;
              const { $head } = selection;
              const paragraphPos = $head.before($head.depth);
              const paragraphNode = $head.node($head.depth);

              if (paragraphNode.type.name === 'paragraph') {
                const decoration = Decoration.node(paragraphPos, paragraphPos + paragraphNode.nodeSize, {
                  style: 'background: yellow',
                });
                set = DecorationSet.create(tr.doc, [decoration]);
              } else {
                set = DecorationSet.empty;
              }
            } else {
              // If the transaction doesn't change the selection, just map the decoration
              set = set.map(tr.mapping, tr.doc);
            }

            return set;
          },
        },
        props: {
          decorations(state) {
            return pluginKey.getState(state);
          },
        },
      }),
    ];
  },
});

// changes all paragraph to yellow
// apply(tr, set) {
//   // Map the old decorations to the new state
//   set = set.map(tr.mapping, tr.doc);
//   // Create new decorations for paragraph nodes
//   const decorations = [];
//   tr.doc.descendants((node, pos) => {
//     if (node.type.name === 'paragraph') {
//       decorations.push(Decoration.node(pos, pos + node.nodeSize, { style: 'background: yellow' }));
//     }
//   });
//   // Add the new decorations to the set
//   set = set.add(tr.doc, decorations);
//   return set;
// },

// highlights all inline code to yellow
// apply(tr, set) {
//   // Map the old decorations to the new state
//   set = set.map(tr.mapping, tr.doc);
//   // Create new decorations for inline code
//   const decorations = [];
//   tr.doc.descendants((node, pos) => {
//     node.marks.forEach((mark) => {
//       if (mark.type.name === 'code') {
//         decorations.push(Decoration.inline(pos, pos + node.nodeSize, { style: 'background: yellow' }));
//       }
//     });
//   });
//   // Add the new decorations to the set
//   set = set.add(tr.doc, decorations);
//   return set;
// },

function getHighlightNodes(result) {
  // `.value` for lowlight v1, `.children` for lowlight v2
  return result.value || result.children || [];
}

function parseNodes(nodes, className = []) {
  return nodes
    .map((node) => {
      const classes = [...className, ...(node.properties ? node.properties.className : [])];

      if (node.children) {
        return parseNodes(node.children, classes);
      }

      return {
        text: node.value,
        classes,
      };
    })
    .flat();
}

function getDecorations({ doc, lowlight, defaultLanguage }) {
  const decorations = [];

  findInlineCode(doc, 'code').forEach((block) => {
    let from = block.from;
    const to = block.to;
    const language = block.node.attrs.language || defaultLanguage;
    const languages = lowlight.listLanguages();

    const nodes = getHighlightNodes(lowlight.highlightAuto(block.text));
    console.log('----text', block.text, nodes);

    console.log('-----------------', nodes.length, nodes);

    parseNodes(nodes).forEach((node) => {
      console.log('------node-----', node, node.classes);
      if (node.classes.length) {
        const decoration = Decoration.inline(from, from + node.text.length, {
          class: node.classes.join(' '),
        });

        decorations.push(decoration);
      }

      from += node.text.length;
    });
  });

  return DecorationSet.create(doc, decorations);
}

function findInlineCode(doc, markType) {
  const inlineCodeSpans = [];
  doc.descendants((node, pos) => {
    if (!node.isText) return true; // Continue traversing if not a text node
    node.marks.forEach((mark) => {
      if (mark.type.name === markType) {
        // Found an inline code mark, store this node's position and content
        inlineCodeSpans.push({
          from: pos,
          to: pos + node.nodeSize,
          text: node.text,
          node: mark,
        });
      }
    });
  });
  return inlineCodeSpans;
}

const testProseMirrorPluggin = Extension.create({
  name: 'testPluggin',

  addProseMirrorPlugins() {
    const pluginKey = new PluginKey('testPluggin');
    return [
      new Plugin({
        key: pluginKey,
        state: {
          init(_, { doc }) {
            return DecorationSet.empty;
          },
          apply(tr, set, oldState, newState) {
            const oldNodeName = oldState.selection.$head.parent.type.name;
            const newNodeName = newState.selection.$head.parent.type.name;
            const oldNodes = findInlineCode(oldState.doc, 'code');
            const newNodes = findInlineCode(newState.doc, 'code');

            console.log('oldNodes', oldNodes);
            console.log('newNodes', newNodes);
            console.log('include', newNodes.length !== oldNodes.length);

            if (
              tr.docChanged &&
              (newNodes.length !== oldNodes.length ||
                tr.steps.some((step) => {
                  console.log('changed');
                  return (
                    step.from !== undefined &&
                    step.to !== undefined &&
                    oldNodes.some((mark) => {
                      return step.from >= mark.from && step.to <= mark.to;
                    })
                  );
                }))
            ) {
              console.log('return decoration');
              return getDecorations({
                doc: tr.doc,
                name: 'code',
                lowlight: lowlight,
                defaultLanguage: '',
              });
            }

            return set.map(tr.mapping, tr.doc);
          },
        },
        props: {
          decorations(state) {
            return pluginKey.getState(state);
          },
        },
      }),
    ];
  },
});

export {
  CursorPositionExtension,
  DynamicCharInsertionExtension,
  CodeCheckExtension,
  InlineCodeCheckExtension,
  InlineCodeTransformExtension,
  HighlightCodeExtension,
  testProseMirrorPluggin,
};
