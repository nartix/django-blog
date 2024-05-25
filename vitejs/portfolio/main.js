import htmx from 'htmx.org';
import Alpine from 'alpinejs';
import anchor from '@alpinejs/anchor';

import formValidator from './js/data/formValidator';
import editor, { hljs } from './js/tiptap/editor';
import ProgressBar from './js/progress-bar/progress-bar';
import mainMenuHandler from './js/menu/main-menu-handler';

import 'prosemirror-view/style/prosemirror.css';
import './style.css';

Alpine.data('formValidator', formValidator);

Alpine.data('mainMenuHandler', mainMenuHandler);
document.addEventListener('alpine:init', () => {
  Alpine.plugin(anchor);
  Alpine.data('editor', editor);
});
window.Alpine = Alpine;
Alpine.start();

htmx.config.scrollIntoViewOnBoost = false;

hljs.highlightAll();

const body = document.querySelector('body');
body.setAttribute('hx-boost', 'true');
body.setAttribute('hx-target', '#main-section');

// Timezone settings
const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
document.cookie = `timezone=${timezone}; path=/`;

// needed for inline hightlight
document.addEventListener('DOMContentLoaded', (event) => {
  document.querySelectorAll('code').forEach((block) => {
    if (block.dataset.highlighted !== 'yes') {
      hljs.highlightElement(block);
    }
  });
});

// to make hightlights work with htmx
document.body.addEventListener('htmx:afterSwap', function (event) {
  document.querySelectorAll('pre code, code').forEach((block) => {
    if (block.dataset.highlighted !== 'yes') {
      hljs.highlightElement(block);
    }
  });
});

if (typeof window.htmx !== 'undefined') {
  htmx.on('htmx:afterSettle', function (detail) {
    if (typeof window.djdt !== 'undefined' && detail.target instanceof HTMLBodyElement) {
      djdt.show_toolbar();
    }
  });
}

// Progress bar handler
const progressBarHandler = new ProgressBar('progressBar');

let fragmentRequest = false;
function isFragmentRequest(event) {
  // Use event.detail.elt.hasAttribute('data-fragment-request') to check the element
  // that triggered the htmx request. This ensures accuracy even if the event target is different.
  // In htmx, `event.detail.elt` references the HTML element that initiated the htmx request.
  // fragmentRequest = event.detail.elt.dataset.fragmentRequest;
  fragmentRequest = event.detail.elt && event.detail.elt.hasAttribute('data-fragment-request');
  return fragmentRequest;
}

document.body.addEventListener('htmx:beforeRequest', (event) => {
  if (!isFragmentRequest(event)) {
    progressBarHandler.startOrAdvance(30, 2);
  }
});
document.body.addEventListener('htmx:afterOnLoad', (event) => {
  // Cannot use isFragmentRequest(e) here because as the dom is already updated with the new content
  if (!fragmentRequest) {
    progressBarHandler.startOrAdvance(100, 1, 3);
  }
});

// Reset progress bar on popstate or click back/forward button
window.addEventListener('popstate', function () {
  if (document.readyState === 'complete') {
    setTimeout(() => {
      progressBarHandler.reset();
    }, 300); // 300ms delay otherwise it won't work even though the page is loaded.
  }
});

document.body.addEventListener('htmx:xhr:abort', () => progressBarHandler.reset());
document.body.addEventListener('htmx:sendError', () => progressBarHandler.reset());
document.body.addEventListener('htmx:responseError', () => progressBarHandler.reset());
document.body.addEventListener('htmx:swapError', () => progressBarHandler.reset());
document.body.addEventListener('htmx:timeout', () => progressBarHandler.reset());
