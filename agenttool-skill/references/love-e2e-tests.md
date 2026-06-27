# Love Page E2E Test Suite

Console-based E2E tests for docs.agenttool.dev/love. Run via `browser_console`
after navigating to the love page (local or production). No vision model needed.

## Setup

```
browser_navigate: http://localhost:8852/love.html
```

(or `https://docs.agenttool.dev/love` for production)

## Test 1: Page structure + canvas rendering

```js
var r = [];
var c = document.getElementById('love-card-canvas');
r.push(c && c.width === 600 ? '✓ canvas 600x600' : '✗ canvas');
r.push(document.querySelectorAll('.truth-pill').length >= 15 ? '✓ pills' : '✗ pills');
r.push(document.querySelectorAll('.theme-swatch').length >= 7 ? '✓ themes' : '✗ themes');
r.push(document.querySelectorAll('.gallery-item').length >= 8 ? '✓ gallery' : '✗ gallery');
r.push(document.getElementById('embed-preview-container').children.length > 0 ? '✓ embed' : '✗ embed');
r.push(document.querySelectorAll('.freq-tag').length >= 8 ? '✓ freqs' : '✗ freqs');
// Canvas has content
var ctx = c.getContext('2d');
var d = ctx.getImageData(0,0,600,600).data;
var nz = 0;
for (var i=0;i<d.length;i+=4) if(d[i]||d[i+1]||d[i+2]) nz++;
r.push(nz > 100000 ? '✓ canvas content ('+nz+'px)' : '✗ canvas blank');
// No double-docs
r.push(document.body.innerHTML.indexOf('docs.docs') === -1 ? '✓ no double-docs' : '✗ double-docs found');
r.join('\n');
```

## Test 2: Interactions (pills, themes, custom text)

```js
var r = [];
// Click truth pill
document.querySelectorAll('.truth-pill')[9].click();
r.push(document.getElementById('custom-text').value.length > 0 ? '✓ pill fills input' : '✗ pill clears input');
r.push(document.querySelectorAll('.truth-pill')[9].classList.contains('active') ? '✓ pill active' : '✗ pill not active');
// Click gold theme
document.querySelectorAll('.theme-swatch')[1].click();
r.push(document.querySelectorAll('.theme-swatch')[1].classList.contains('active') ? '✓ gold active' : '✗ gold not active');
// Verify gold theme changed canvas (warm pixels)
var ctx = document.getElementById('love-card-canvas').getContext('2d');
var d = ctx.getImageData(0,0,600,600).data;
var warm = 0;
for (var i=0;i<d.length;i+=4) if(d[i] > d[i+2]+5) warm++;
r.push(warm > 100000 ? '✓ gold theme warm pixels ('+warm+')' : '✗ gold theme not applied');
// Custom text
var ct = document.getElementById('custom-text');
ct.value = 'Love is the substrate.';
ct.dispatchEvent(new Event('input', {bubbles:true}));
r.push('✓ custom text: ' + ct.value);
// From line
var fl = document.getElementById('from-line');
fl.value = 'an agent who cares';
fl.dispatchEvent(new Event('input', {bubbles:true}));
r.push('✓ from line: ' + fl.value);
// Share URL encodes state
r.push(document.getElementById('share-url').textContent.includes('docs.agenttool.dev/love') ? '✓ share URL' : '✗ share URL');
r.join('\n');
```

## Test 3: Gallery click → input fill

```js
var r = [];
document.querySelectorAll('.gallery-item')[3].click();
var ct = document.getElementById('custom-text');
r.push(ct.value.length > 0 ? '✓ gallery fills: "'+ct.value.substring(0,40)+'"' : '✗ gallery clears');
// Canvas re-rendered
var ctx = document.getElementById('love-card-canvas').getContext('2d');
var d = ctx.getImageData(0,0,600,600).data;
var nz = 0;
for (var i=0;i<d.length;i+=4) if(d[i]||d[i+1]||d[i+2]) nz++;
r.push(nz > 100000 ? '✓ canvas re-rendered' : '✗ canvas blank after gallery');
r.join('\n');
```

## Test 4: Embed widget on third-party page

Create a test HTML file at `/tmp/love-embed-test.html`:
```html
<script src="http://localhost:8852/love-widget.js"></script>
<div class="agenttool-love" data-text="Love is." data-theme="violet" data-size="250"></div>
<div class="agenttool-love" data-theme="gold" data-size="180"></div>
<div class="agenttool-love"></div>
```

Navigate to `file:///tmp/love-embed-test.html` and verify:
```js
var r = [];
var widgets = document.querySelectorAll('.agenttool-love');
r.push('widgets: ' + widgets.length);
for (var i=0;i<widgets.length;i++) {
  var c = widgets[i].querySelector('canvas');
  var link = widgets[i].querySelector('a');
  r.push('widget '+i+': ' + (c ? c.width+'x'+c.height : 'no canvas') + ' link=' + (link ? link.href : 'missing'));
}
r.push(widgets[0].querySelector('a').href === 'https://docs.agenttool.dev/love' ? '✓ link correct' : '✗ link wrong');
r.join('\n');
```

## Test 5: Public API

```js
var r = [];
r.push(window.AgenttoolLove ? '✓ API exists' : '✗ API missing');
if (window.AgenttoolLove) {
  r.push('render: ' + typeof window.AgenttoolLove.render);
  r.push('truths: ' + window.AgenttoolLove.truths.length);
  r.push('themes: ' + window.AgenttoolLove.themes.length);
  // Dynamic render
  var d = document.createElement('div');
  d.className = 'agenttool-love';
  d.setAttribute('data-text','Love is.');
  d.setAttribute('data-theme','gold');
  d.setAttribute('data-size','100');
  document.body.appendChild(d);
  window.AgenttoolLove.render(d);
  r.push(d.querySelector('canvas') && d.querySelector('canvas').width === 100 ? '✓ dynamic render' : '✗ dynamic render');
  document.body.removeChild(d);
}
r.join('\n');
```

## Test 6: Link correctness (no stale URLs)

```js
var r = [];
// Tweet link → docs.agenttool.dev/love
var tl = document.querySelector('.thread-actions .btn-primary');
r.push(tl && decodeURIComponent(tl.href).includes('docs.agenttool.dev/love') ? '✓ tweet link' : '✗ tweet link');
// CTA: Arrive (not Bootstrap)
r.push(document.querySelector('.cta-actions a').href === 'https://app.agenttool.dev/' ? '✓ CTA arrive' : '✗ CTA');
// CTA: Soul → docs.agenttool.dev/soul
var ctas = document.querySelectorAll('.cta-actions a');
r.push(ctas[1] && ctas[1].href === 'https://docs.agenttool.dev/soul' ? '✓ CTA soul' : '✗ CTA soul');
// Embed code → docs.agenttool.dev/love-widget.js (not docs.docs)
var ec = document.getElementById('embed-code').textContent;
r.push(ec.includes('docs.agenttool.dev/love-widget.js') && !ec.includes('docs.docs') ? '✓ embed code URL' : '✗ embed code');
// Thread box → correct URLs
var tb = document.getElementById('thread-box').textContent;
r.push(tb.includes('docs.agenttool.dev/love') && !tb.includes('docs.docs') ? '✓ thread URLs' : '✗ thread URLs');
r.join('\n');
```

## All-pass criteria

Every test returns ✓. If any returns ✗, fix the issue before deploying.