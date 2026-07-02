# Canvas Verification via Console Assertions

When vision models aren't available (or `browser_vision` returns "this model does not support image input"), use `browser_console` with DOM/canvas assertions to verify rendering. This is the reliable verification path for canvas-based features.

## Canvas pixel sampling

Confirm the canvas is actually painting (not blank) by sampling pixel data:

```js
(function() {
  var c = document.getElementById('love-card-canvas');
  var ctx = c.getContext('2d');
  var data = ctx.getImageData(0, 0, c.width, c.height).data;
  var nonBlack = 0;
  for (var i = 0; i < data.length; i += 4) {
    if (data[i] > 10 || data[i+1] > 10 || data[i+2] > 10) nonBlack++;
  }
  return {
    canvasW: c.width,
    canvasH: c.height,
    nonBlackPixels: nonBlack,
    canvasRendering: nonBlack > 1000  // threshold for "actually painted"
  };
})()
```

For text rendering specifically, sample a horizontal strip through the center where text should appear:

```js
(function() {
  var c = document.getElementById('love-card-canvas');
  var ctx = c.getContext('2d');
  var strip = ctx.getImageData(100, 280, 400, 40).data;  // text area
  var darkCount = 0;
  for (var i = 0; i < strip.length; i += 4) {
    var avg = (strip[i] + strip[i+1] + strip[i+2]) / 3;
    if (avg < 100) darkCount++;  // dark text pixels
  }
  return {
    darkPixelsInTextStrip: darkCount,
    textIsRendering: darkCount > 50
  };
})()
```

## Programmatic click testing

When `browser_click` doesn't reliably hit the right element (ref IDs can shift between snapshots), use `browser_console` to click programmatically and verify state:

```js
(function() {
  // Click a specific truth pill
  var pills = document.querySelectorAll('.truth-pill');
  var target = null;
  pills.forEach(function(p) {
    if (p.textContent === 'You are loved anyway.') target = p;
  });
  if (target) {
    target.click();
    return {
      clicked: target.textContent,
      activeAfter: document.querySelector('.truth-pill.active')?.textContent,
      customTextAfter: document.getElementById('custom-text').value
    };
  }
  return { error: 'pill not found' };
})()
```

## URL param round-trip testing

For shareable links, test that URL params load correctly by navigating to a param-laden URL and checking state:

```
browser_navigate: http://localhost:8765/love.html?t=No+FEAR+in+understanding.&th=green&from=an+agent
```

Then verify via snapshot or console:
- Custom text field contains the param text
- Theme swatch is active for the param theme
- "From" field contains the param value
- Canvas re-rendered with new content

## Download verification

Test that `canvas.toDataURL()` produces valid output without actually triggering a download:

```js
(function() {
  var c = document.getElementById('love-card-canvas');
  var dataUrl = c.toDataURL('image/png');
  return {
    dataUrlPrefix: dataUrl.substring(0, 30),
    dataUrlLength: dataUrl.length,
    downloadWouldWork: dataUrl.startsWith('data:image/png')
  };
})()
```

## Share URL verification

Verify that share URLs encode state correctly:

```js
(function() {
  // Set custom text via input event
  var ct = document.getElementById('custom-text');
  ct.value = 'Love is. lol. ∞';
  ct.dispatchEvent(new Event('input'));
  
  // Click gold theme
  document.querySelectorAll('.theme-swatch').forEach(function(s) {
    if (s.title === 'gold') s.click();
  });
  
  return {
    shareUrl: document.getElementById('share-url').textContent,
    embedCode: document.getElementById('embed-code').textContent,
    activeTheme: document.querySelector('.theme-swatch.active')?.title
  };
})()
```

## Element count verification

Quick structural check that all expected elements rendered:

```js
(function() {
  return {
    truthPills: document.querySelectorAll('.truth-pill').length,
    themeSwatches: document.querySelectorAll('.theme-swatch').length,
    galleryItems: document.querySelectorAll('.gallery-item').length,
    embedPreviewChildren: document.getElementById('embed-preview-container').children.length,
    canvasW: document.getElementById('love-card-canvas')?.width,
    canvasH: document.getElementById('love-card-canvas')?.height
  };
})()
```