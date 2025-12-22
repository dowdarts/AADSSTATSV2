# AADS Display App - Quick Start Guide

## 🚀 Get Started in 60 Seconds

### For Immediate Use (No Setup)
```bash
# Just open the file!
1. Navigate to the display-app folder
2. Double-click index.html
3. Done! 🎯
```

### For Local Development Server
```bash
# Option 1: Python (usually pre-installed)
python -m http.server 8080
# Then open: http://localhost:8080

# Option 2: Node.js
npx http-server -p 8080 -o
# Opens automatically in browser
```

### For OBS/Streaming Software
```
1. Add Browser Source
2. Set URL: file:///path/to/display-app/index.html
3. Width: 1920, Height: 1080
4. Done!
```

## 📁 What's Included?

```
display-app/
├── index.html              ← Main display (open this!)
├── embed-example.html      ← Embedding examples
├── config.js               ← Customize settings here
├── package.json            ← Project metadata
├── assets/
│   └── logos/              ← All sponsor logos (7 files)
└── README.md               ← Full documentation
```

## ⚙️ Quick Configuration

### Change API Endpoint
Edit `config.js`:
```javascript
window.AADS_CONFIG = {
    SUPABASE_URL: 'https://your-project.supabase.co',
    SUPABASE_ANON_KEY: 'your-key-here',
    // ... other settings
};
```

### Multi-Tenant Mode
Add to URL:
```
index.html?user_id=abc123
```

## 🎨 Customization

### Update Logos
1. Replace files in `assets/logos/`
2. Keep same filenames OR
3. Update `config.js` PARTNER_LOGOS array

### Change Colors
Edit CSS variables in `index.html` or override in `config.js`:
```javascript
CUSTOM_STYLES: {
    PRIMARY_COLOR: '#FF6B00',
    DARK_BG: '#0a0a0a',
    // ...
}
```

## 📋 Checklist for Importing to Another Project

- [ ] Copy entire `display-app` folder
- [ ] Verify `assets/logos/` contains all PNG files
- [ ] Update `config.js` with your API settings
- [ ] Test by opening `index.html` in browser
- [ ] Check browser console for errors
- [ ] Verify logos load correctly
- [ ] Test data refresh (wait 5 minutes or refresh manually)

## 🔧 Troubleshooting

### Logos Not Showing
- ✅ Check file paths in `index.html`
- ✅ Ensure files are in `assets/logos/`
- ✅ Check browser console for 404 errors

### Data Not Loading
- ✅ Check internet connection
- ✅ Verify Supabase URL in config
- ✅ Open browser dev tools (F12) → Console
- ✅ Look for API errors

### CORS Issues
- ✅ Use local server (not file://)
- ✅ Use Python or Node server (see above)

## 📞 Support

See full `README.md` for detailed documentation.

## 📦 Dependencies

**Runtime:**
- Supabase JS v2 (loaded from CDN)
- Modern web browser

**No build tools required!**
**No npm install needed!**
**No compilation step!**

## ✅ Browser Compatibility

- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ⚠️ IE11 (limited)

---

**Ready to go?** Just open `index.html`! 🎯
