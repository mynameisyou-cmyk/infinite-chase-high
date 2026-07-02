# Embeddable widget recipe

One-line `<script>` widgets that run on foreign pages. No dependencies, no build step, no tracking. Used by love.js and love-widget.js.

## Skeleton

```js
(function () {
  'use strict';

  var DATA = [ /* ... */ ];

  function build() {
    var existing = document.getElementById('my-widget');
    if (existing && existing._myWidget) return;  // idempotent
    var container = existing || document.createElement('div');
    container.id = 'my-widget';
    container._myWidget = true;  // guard against double-init
    if (!existing) document.body.appendChild(container);

    // Build DOM with inline styles — no shared CSS available on foreign pages
    var el = document.createElement('div');
    el.style.cssText = 'display:block;max-width:420px;margin:2rem auto;';
    // ... populate el
    container.appendChild(el);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else {
    build();
  }

  // Re-render when fonts load (canvas text measurement changes)
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(function () { build(); });
  }

  // Public API for dynamic rendering
  window.MyWidget = { render: build, data: DATA };
})();
```

## Key decisions

1. **IIFE + strict** — no globals leaked, no module system needed.
2. **Auto-create container** — if `document.getElementById('my-widget')` returns null, create a `<div>` and append to body. The one-line embed works without any HTML.
3. **Idempotent guard** — set `container._myWidget = true` and check it. Prevents double-init when both DOMContentLoaded and `document.fonts.ready` fire.
4. **Inline styles only** — the widget runs on sites that don't load your CSS. Every element gets `el.style.cssText = '...'`. Never rely on external classes.
5. **No network calls** — all data is inline in the script. No fetch, no XHR, no tracking pixels.
6. **Font-ready re-render** — canvas text measurement depends on fonts. Re-render when `document.fonts.ready` resolves. Critical for canvas widgets; less so for DOM widgets.
7. **Public API** — expose `window.MyWidget` so host pages can render dynamically (`MyWidget.render(newContainer)`).

## Canvas vs DOM

**Canvas (love-widget.js):** for image-like cards that should be downloadable as PNG. Text wrapping needs manual `ctx.measureText` + word wrapping. Re-render on font load is critical.

**DOM (love.js):** for interactive cards with hover/click. CSS transitions work. Easier to make responsive. No font re-render needed (browser handles reflow).

## Distribution

The embed code snippet for users:
```html
<script src="https://agenttool.dev/my-widget.js"></script>
```

For canvas widgets that need a container:
```html
<script src="https://agenttool.dev/my-widget.js"></script>
<div class="my-widget" data-theme="violet"></div>
```

The script auto-finds `.my-widget` divs and renders into them. If no div exists, it creates one.