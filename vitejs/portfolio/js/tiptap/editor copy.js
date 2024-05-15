import { Editor } from '@tiptap/core';
import StarterKit from '@tiptap/starter-kit';
import Typography from '@tiptap/extension-typography';
import Link from '@tiptap/extension-link';
import TextAlign from '@tiptap/extension-text-align';
import Code from '@tiptap/extension-code';
import CodeBlockLowlight from '@tiptap/extension-code-block-lowlight';
import Image from '@tiptap/extension-image';

import { DynamicCharInsertionExtension } from './ext/exttest';

import CodeInlineLowlight from './extension-code-inline-lowlight/src/';
// import CodeInlineLowlight from '@nartix/tiptap-inline-code-highlight';

import 'highlight.js/styles/atom-one-dark.css';
// import 'highlight.js/styles/default.css';

// import hljs from 'highlight.js';
import hljs from 'highlight.js/lib/core';
import javascript from 'highlight.js/lib/languages/javascript';
import python from 'highlight.js/lib/languages/python';
import xml from 'highlight.js/lib/languages/xml';
import css from 'highlight.js/lib/languages/css';
import java from 'highlight.js/lib/languages/java';
import ruby from 'highlight.js/lib/languages/ruby';
import php from 'highlight.js/lib/languages/php';
import c from 'highlight.js/lib/languages/c';
import cpp from 'highlight.js/lib/languages/cpp';
import csharp from 'highlight.js/lib/languages/csharp';
import go from 'highlight.js/lib/languages/go';
import rust from 'highlight.js/lib/languages/rust';
import bash from 'highlight.js/lib/languages/bash';
import sql from 'highlight.js/lib/languages/sql';
import json from 'highlight.js/lib/languages/json';
import markdown from 'highlight.js/lib/languages/markdown';
import typescript from 'highlight.js/lib/languages/typescript';
import yaml from 'highlight.js/lib/languages/yaml';
import shell from 'highlight.js/lib/languages/shell';
import diff from 'highlight.js/lib/languages/diff';
import graphql from 'highlight.js/lib/languages/graphql';
import ini from 'highlight.js/lib/languages/ini';
import kotlin from 'highlight.js/lib/languages/kotlin';
import less from 'highlight.js/lib/languages/less';
import lua from 'highlight.js/lib/languages/lua';
import makefile from 'highlight.js/lib/languages/makefile';
import objectivec from 'highlight.js/lib/languages/objectivec';
import perl from 'highlight.js/lib/languages/perl';
import phptemplate from 'highlight.js/lib/languages/php-template';
import plaintext from 'highlight.js/lib/languages/plaintext';
import pythonrepl from 'highlight.js/lib/languages/python-repl';
import r from 'highlight.js/lib/languages/r';
import scss from 'highlight.js/lib/languages/scss';
import swift from 'highlight.js/lib/languages/swift';
import vbnet from 'highlight.js/lib/languages/vbnet';
import wasm from 'highlight.js/lib/languages/wasm';
import django from 'highlight.js/lib/languages/django';
import dockerfile from 'highlight.js/lib/languages/dockerfile';
import nginx from 'highlight.js/lib/languages/nginx';
import pgsql from 'highlight.js/lib/languages/pgsql';
import elixir from 'highlight.js/lib/languages/elixir';
import haskell from 'highlight.js/lib/languages/haskell';
import scala from 'highlight.js/lib/languages/scala';
import powershell from 'highlight.js/lib/languages/powershell';
import closure from 'highlight.js/lib/languages/clojure';
import lisp from 'highlight.js/lib/languages/lisp';

import { createLowlight } from 'lowlight';
const lowlight = createLowlight();

// Register languages for lowlight
lowlight.register('javascript', javascript);
lowlight.register('css', css);
lowlight.register('typescript', typescript);
lowlight.register('python', python);
lowlight.register('xml', xml); // xml is an alias for html
lowlight.register('java', java);
lowlight.register('ruby', ruby);
lowlight.register('php', php);
lowlight.register('c', c);
lowlight.register('cpp', cpp);
lowlight.register('csharp', csharp);
lowlight.register('go', go);
lowlight.register('rust', rust);
lowlight.register('bash', bash);
lowlight.register('sql', sql);
lowlight.register('json', json);
lowlight.register('markdown', markdown);
lowlight.register('yaml', yaml);
lowlight.register('shell', shell);
lowlight.register('diff', diff);
lowlight.register('graphql', graphql);
lowlight.register('ini', ini);
lowlight.register('kotlin', kotlin);
lowlight.register('less', less);
lowlight.register('lua', lua);
lowlight.register('makefile', makefile);
lowlight.register('objectivec', objectivec);
lowlight.register('perl', perl);
lowlight.register('phptemplate', phptemplate);
lowlight.register('plaintext', plaintext);
lowlight.register('pythonrepl', pythonrepl);
lowlight.register('r', r);
lowlight.register('scss', scss);
lowlight.register('swift', swift);
lowlight.register('vbnet', vbnet);
lowlight.register('wasm', wasm);
lowlight.register('django', django);
lowlight.register('dockerfile', dockerfile);
lowlight.register('nginx', nginx);
lowlight.register('pgsql', pgsql);
lowlight.register('elixir', elixir);
lowlight.register('haskell', haskell);
lowlight.register('scala', scala);
lowlight.register('powershell', powershell);
lowlight.register('closure', closure);
lowlight.register('lisp', lisp);

hljs.registerLanguage('javascript', javascript);
hljs.registerLanguage('python', python);
hljs.registerLanguage('xml', xml);
hljs.registerLanguage('css', css);
hljs.registerLanguage('java', java);
hljs.registerLanguage('ruby', ruby);
hljs.registerLanguage('php', php);
hljs.registerLanguage('c', c);
hljs.registerLanguage('cpp', cpp);
hljs.registerLanguage('csharp', csharp);
hljs.registerLanguage('go', go);
hljs.registerLanguage('rust', rust);
hljs.registerLanguage('bash', bash);
hljs.registerLanguage('sql', sql);
hljs.registerLanguage('json', json);
hljs.registerLanguage('markdown', markdown);
hljs.registerLanguage('typescript', typescript);
hljs.registerLanguage('yaml', yaml);
hljs.registerLanguage('shell', shell);
hljs.registerLanguage('diff', diff);
hljs.registerLanguage('graphql', graphql);
hljs.registerLanguage('ini', ini);
hljs.registerLanguage('kotlin', kotlin);
hljs.registerLanguage('less', less);
hljs.registerLanguage('lua', lua);
hljs.registerLanguage('makefile', makefile);
hljs.registerLanguage('objectivec', objectivec);
hljs.registerLanguage('perl', perl);
hljs.registerLanguage('phptemplate', phptemplate);
hljs.registerLanguage('plaintext', plaintext);
hljs.registerLanguage('pythonrepl', pythonrepl);
hljs.registerLanguage('r', r);
hljs.registerLanguage('scss', scss);
hljs.registerLanguage('swift', swift);
hljs.registerLanguage('vbnet', vbnet);
hljs.registerLanguage('wasm', wasm);
hljs.registerLanguage('django', django);
hljs.registerLanguage('dockerfile', dockerfile);
hljs.registerLanguage('nginx', nginx);
hljs.registerLanguage('pgsql', pgsql);
hljs.registerLanguage('elixir', elixir);
hljs.registerLanguage('haskell', haskell);
hljs.registerLanguage('scala', scala);
hljs.registerLanguage('closure', closure);
hljs.registerLanguage('lisp', lisp);

hljs.configure({ ignoreUnescapedHTML: true });

export { hljs, lowlight };

export default (content) => {
  // Alpine's reactive engine automatically wraps component properties in proxy objects.
  // Attempting to use a proxied editor instance to apply a transaction will cause
  // a "Range Error: Applying a mismatched transaction", so be sure to unwrap it using Alpine.raw(),
  // or simply avoid storing your editor as a component property, as shown in this example.
  let editor;
  return {
    updatedAt: Date.now(), // force Alpine to rerender on selection change
    init() {
      // otherwise, clicking back/forward in the browser will create multiple duplicate editors
      document.body.addEventListener('htmx:beforeSwap', () => {
        if (editor) {
          editor.destroy();
          editor = null;
          console.log('Editor destroyed');
        }
      });
      const _this = this;

      editor = new Editor({
        element: this.$refs.elementEditor,
        extensions: [
          StarterKit.configure({
            codeBlock: false,
            code: false,
          }),
          Typography,
          Link.configure({
            HTMLAttributes: {
              class: '',
            },
          }),
          TextAlign.configure({
            types: ['heading', 'paragraph'],
            alignments: ['left', 'center', 'right', 'justify'],
          }),
          Code.configure({
            HTMLAttributes: {
              class: 'hljs',
            },
          }),
          CodeBlockLowlight.configure({
            lowlight,
            HTMLAttributes: {
              class: 'hljs',
            },
          }),
          CodeInlineLowlight.configure({
            lowlight,
          }),
          Image,
          DynamicCharInsertionExtension,
        ],
        editorProps: {
          attributes: {
            class: '',
          },
        },
        content: content,
        onCreate({ editor }) {
          _this.updatedAt = Date.now();
        },
        onUpdate({ editor }) {
          console.log(editor.getHTML());
          document.getElementById('editorContent').value = editor.getHTML();
          _this.updatedAt = Date.now();
        },
        onSelectionUpdate({ editor }) {
          _this.updatedAt = Date.now();
        },
        // new recenetly added by feroz
        onTransaction: () => {
          _this.updatedAt = Date.now();
        },
      });
    },
    cleanup() {
      if (editor) {
        editor.destroy();
        editor = null;
      }
    },
    isLoaded() {
      return editor;
    },
    isActive(type, opts = {}) {
      return editor.isActive(type, opts);
    },
    toggleHeading(opts) {
      editor.chain().toggleHeading(opts).focus().run();
      this.updatedAt = Date.now();
    },
    toggleBold() {
      editor.chain().toggleBold().focus().run();
      this.updatedAt = Date.now();
    },
    toggleItalic() {
      editor.chain().toggleItalic().focus().run();
      this.updatedAt = Date.now();
    },
    undo() {
      if (editor.can().undo()) {
        editor.chain().undo().run();
        this.updatedAt = Date.now();
      } else {
        console.log('No undo history available');
      }
    },
    redo() {
      if (editor.can().redo()) {
        editor.chain().redo().run();
        this.updatedAt = Date.now();
      } else {
        console.log('No redo history available');
      }
    },
    toggleCode() {
      editor.chain().toggleCode().focus().run();
      this.updatedAt = Date.now();
    },
    toggleCodeBlock() {
      editor.chain().toggleCodeBlock().focus().run();
      this.updatedAt = Date.now();
    },
    toggleBlockquote() {
      editor.chain().toggleBlockquote().focus().run();
      this.updatedAt = Date.now();
    },
    setLink(url) {
      editor.chain().focus().extendMarkRange('link').setLink({ href: url }).run();
      this.updatedAt = Date.now();
    },
    setTextAlign(alignment) {
      editor.chain().focus().setTextAlign(alignment).run();
      this.updatedAt = Date.now();
    },
    toggleBulletList() {
      editor.chain().toggleBulletList().focus().run();
      this.updatedAt = Date.now();
    },
    toggleOrderedList() {
      editor.chain().toggleOrderedList().focus().run();
      this.updatedAt = Date.now();
    },
    setImage(url) {
      if (url) {
        isImage(url).then((isValid) => {
          if (isValid) {
            editor.chain().focus().setImage({ src: url }).run();
            this.updatedAt = Date.now();
          } else {
            console.error('Invalid image URL');
          }
        });
      }
    },
    setChar(char) {
      editor.chain().focus().setChar(char).run();
    },
    transformInlineCode() {
      editor.chain().focus().transformInlineCode().run();
    },
  };
};

async function isImage(url) {
  const response = await fetch(url, {
    method: 'HEAD', // make a HEAD request to get the headers
    mode: 'cors', // use CORS to avoid cross-origin issues
  });
  const contentType = response.headers.get('Content-Type');
  return contentType && contentType.startsWith('image/');
}
