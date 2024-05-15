import { Node, Plugin, PluginKey, DecorationSet, Decoration } from 'tiptap';
import { Extension } from 'tiptap';
import { lowlight } from 'lowlight';
import { hljs } from 'highlight.js';

export default class CodeInlineLowlight extends Extension {
  get schema() {
    return {
      group: 'inline',
      content: 'text*',
      marks: '',
      parseDOM: [{ tag: 'code' }],
      toDOM: (node) => {
        return ['code', { class: `language-${this.options.language}` }, 0];
      },
    };
  }

  commands({ type }) {
    return (attrs) => {
      return (state, dispatch) => {
        const { selection } = state;
        const position = selection.$cursor ? selection.$cursor.pos : selection.$to.pos;
        const node = type.create(attrs);
        const transaction = state.tr.insert(position, node);
        dispatch(transaction);
        console.log('transaction', transaction);
        return transaction;
      };
    };
  }

  get plugins() {
    return [
      new Plugin({
        key: new PluginKey('code_inline_lowlight'),
        state: {
          init: () => {
            return DecorationSet.empty;
          },
          apply(tr, set) {
            return set.map(tr.mapping, tr.doc);
          },
        },
        props: {
          decorations(state) {
            const decorations = [];
            const { doc } = state;
            doc.descendants((node, pos) => {
              if (!node.isText) return true;
              node.marks.forEach((mark) => {
                if (mark.type.name === 'code_inline_lowlight') {
                  const from = pos;
                  const to = pos + node.nodeSize;
                  const language = mark.attrs.language || this.options.language;
                  const nodes = getHighlightNodes(lowlight.highlightAuto(node.text));
                  parseNodes(nodes).forEach((node) => {
                    if (node.classes.length === 0) return;
                    const decoration = Decoration.inline(from, from + node.text.length, {
                      class: node.classes.join(' '),
                    });
                    decorations.push(decoration);
                  });
                }
              });
            });
            return DecorationSet.create(doc, decorations);
          },
        },
      }),
    ];
  }
}
