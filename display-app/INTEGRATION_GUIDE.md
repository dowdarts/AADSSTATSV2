# AADS Display App - Integration Guide for Developers

## Overview
This guide shows how to integrate the AADS Display App into various project types.

## Integration Methods

### 1. Static HTML/Website Integration

#### Direct Embed (iFrame)
```html
<!DOCTYPE html>
<html>
<head>
    <title>My Darts Website</title>
</head>
<body>
    <h1>Live Statistics</h1>
    
    <!-- Embedded AADS Display -->
    <iframe 
        src="display-app/index.html" 
        width="100%" 
        height="900px"
        frameborder="0"
        style="border: 2px solid #FF6B00; border-radius: 10px;">
    </iframe>
</body>
</html>
```

#### Responsive iFrame
```html
<style>
.aads-container {
    position: relative;
    width: 100%;
    padding-bottom: 56.25%; /* 16:9 aspect ratio */
    height: 0;
    overflow: hidden;
}
.aads-container iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}
</style>

<div class="aads-container">
    <iframe src="display-app/index.html" frameborder="0"></iframe>
</div>
```

### 2. React Integration

#### Component Wrapper
```jsx
// components/AADSDisplay.jsx
import React from 'react';

export default function AADSDisplay({ userId = null, height = '900px' }) {
    const baseUrl = '/display-app/index.html';
    const url = userId ? `${baseUrl}?user_id=${userId}` : baseUrl;
    
    return (
        <div className="aads-display-wrapper">
            <iframe
                src={url}
                width="100%"
                height={height}
                frameBorder="0"
                title="AADS Statistics Display"
                style={{ border: '2px solid #FF6B00', borderRadius: '10px' }}
            />
        </div>
    );
}

// Usage in your app:
// <AADSDisplay userId="abc123" />
```

### 3. Vue.js Integration

```vue
<!-- components/AADSDisplay.vue -->
<template>
  <div class="aads-display-wrapper">
    <iframe
      :src="displayUrl"
      width="100%"
      :height="height"
      frameborder="0"
      title="AADS Statistics Display"
    ></iframe>
  </div>
</template>

<script>
export default {
  name: 'AADSDisplay',
  props: {
    userId: {
      type: String,
      default: null
    },
    height: {
      type: String,
      default: '900px'
    }
  },
  computed: {
    displayUrl() {
      const base = '/display-app/index.html';
      return this.userId ? `${base}?user_id=${this.userId}` : base;
    }
  }
}
</script>

<style scoped>
.aads-display-wrapper iframe {
  border: 2px solid #FF6B00;
  border-radius: 10px;
}
</style>
```

### 4. Next.js Integration

```jsx
// pages/stats.js or app/stats/page.js
'use client'; // If using App Router

import { useSearchParams } from 'next/navigation';

export default function StatsPage() {
    const searchParams = useSearchParams();
    const userId = searchParams.get('user_id');
    
    const displayUrl = userId 
        ? `/display-app/index.html?user_id=${userId}`
        : '/display-app/index.html';
    
    return (
        <div style={{ padding: '20px' }}>
            <h1>Live Statistics</h1>
            <iframe
                src={displayUrl}
                width="100%"
                height="900px"
                frameBorder="0"
                style={{ 
                    border: '2px solid #FF6B00', 
                    borderRadius: '10px' 
                }}
            />
        </div>
    );
}
```

### 5. WordPress Integration

#### Method A: HTML Block
1. Add HTML block to page
2. Paste this code:
```html
<iframe 
    src="/wp-content/uploads/display-app/index.html"
    width="100%" 
    height="900px"
    frameborder="0"
    style="border: 2px solid #FF6B00; border-radius: 10px;">
</iframe>
```

#### Method B: Custom Shortcode
Add to `functions.php`:
```php
function aads_display_shortcode($atts) {
    $atts = shortcode_atts(array(
        'user_id' => '',
        'height' => '900px'
    ), $atts);
    
    $url = '/wp-content/uploads/display-app/index.html';
    if (!empty($atts['user_id'])) {
        $url .= '?user_id=' . esc_attr($atts['user_id']);
    }
    
    return '<iframe src="' . $url . '" width="100%" height="' . 
           esc_attr($atts['height']) . '" frameborder="0" 
           style="border: 2px solid #FF6B00; border-radius: 10px;"></iframe>';
}
add_shortcode('aads_display', 'aads_display_shortcode');

// Usage in posts/pages:
// [aads_display]
// [aads_display user_id="abc123" height="1000px"]
```

### 6. OBS Studio Integration

1. **Add Browser Source:**
   - Sources → Add → Browser Source
   - Name it "AADS Statistics"

2. **Configure:**
   ```
   URL: file:///C:/path/to/display-app/index.html
   Width: 1920
   Height: 1080
   FPS: 30
   ☑ Shutdown source when not visible
   ☐ Refresh browser when scene becomes active
   ```

3. **Chroma Key (Optional):**
   - Right-click source → Filters → Add → Chroma Key
   - Select key color (if using transparent background)

### 7. Electron App Integration

```javascript
// main.js
const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
    const win = new BrowserWindow({
        width: 1920,
        height: 1080,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true
        }
    });
    
    // Load the display app
    win.loadFile(path.join(__dirname, 'display-app', 'index.html'));
}

app.whenReady().then(createWindow);
```

### 8. Node.js/Express Backend

```javascript
// server.js
const express = require('express');
const path = require('path');

const app = express();

// Serve static files from display-app
app.use('/display', express.static(path.join(__dirname, 'display-app')));

// Route for stats page
app.get('/stats', (req, res) => {
    res.sendFile(path.join(__dirname, 'display-app', 'index.html'));
});

app.listen(3000, () => {
    console.log('Server running on http://localhost:3000/stats');
});
```

### 9. Python Flask Backend

```python
from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/stats')
@app.route('/stats/<path:filename>')
def serve_display(filename='index.html'):
    return send_from_directory('display-app', filename)

if __name__ == '__main__':
    app.run(port=5000)
```

## Advanced Integration

### Custom API Backend
If you want to use your own API instead of Supabase:

1. **Edit config.js:**
```javascript
window.AADS_CONFIG = {
    // Point to your API
    API_BASE: 'https://your-api.com',
    
    // Disable Supabase
    USE_SUPABASE: false,
    
    // Your API endpoints
    ENDPOINTS: {
        STATS: '/api/stats',
        EVENTS: '/api/events',
        PLAYERS: '/api/players'
    }
};
```

2. **Update API calls in index.html:**
Find the fetch calls and update URLs:
```javascript
// Original:
const response = await fetch(`${API_BASE}/aads-api/stats`);

// Your API:
const response = await fetch(`${window.AADS_CONFIG.API_BASE}/api/stats`);
```

### Dynamic Theme Switching
```javascript
// Add to config.js or your application
window.setAADSTheme = function(theme) {
    const iframe = document.querySelector('iframe');
    iframe.contentWindow.postMessage({
        type: 'theme',
        data: theme
    }, '*');
};

// Usage:
window.setAADSTheme({
    PRIMARY_COLOR: '#00FF00',
    DARK_BG: '#000000'
});
```

## Security Considerations

### Content Security Policy (CSP)
If using CSP headers, add:
```
Content-Security-Policy: 
    default-src 'self';
    script-src 'self' 'unsafe-inline' https://unpkg.com;
    img-src 'self' data:;
    connect-src 'self' https://*.supabase.co;
    frame-src 'self';
```

### iFrame Sandbox
For restricted environments:
```html
<iframe 
    src="display-app/index.html"
    sandbox="allow-scripts allow-same-origin"
    allow="accelerometer; gyroscope">
</iframe>
```

## Testing Your Integration

```bash
# Test checklist:
✅ Display loads without errors
✅ Logos render correctly
✅ Data fetches successfully
✅ Auto-refresh works (5 min)
✅ Responsive on different sizes
✅ Multi-tenant parameter works (?user_id=)
✅ Console shows no errors
```

## Performance Tips

1. **Lazy Loading:**
```javascript
// Load iframe only when visible
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const iframe = entry.target;
            iframe.src = iframe.dataset.src;
            observer.unobserve(iframe);
        }
    });
});

const iframe = document.querySelector('iframe');
iframe.dataset.src = 'display-app/index.html';
observer.observe(iframe);
```

2. **Preloading:**
```html
<link rel="prefetch" href="display-app/index.html">
<link rel="preload" href="display-app/assets/logos/Officail AADS Logo.png" as="image">
```

## Support

For integration issues:
1. Check browser console for errors
2. Verify file paths are correct
3. Ensure CORS is configured properly
4. Test with local server (not file://)

## Examples Repository

See `embed-example.html` for working examples of:
- Basic embed
- Responsive embed
- Custom styling
- Multi-tenant usage
