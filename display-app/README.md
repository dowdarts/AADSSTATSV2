# AADS Display App - Standalone Package

## Overview
This is a standalone, portable version of the AADS (Atlantic Amateur Darts Series) statistics display system. It can be imported into any project to display live darts statistics and leaderboards.

## Features
- 📊 Live statistics display with auto-refresh
- 🏆 Championship standings and leaderboards
- 🎯 Event tracking and champion showcase
- 📱 Responsive design for all screen sizes
- 🎨 Professional broadcast-ready styling
- 🔄 Real-time data updates from Supabase backend

## Package Contents
```
display-app/
├── index.html              # Main statistics display page
├── embed-example.html      # Example of how to embed the display
├── assets/
│   └── logos/              # All sponsor and partner logos
│       ├── AADS.COM LOGO-2.png
│       ├── CGC official logo-1.png
│       ├── CGC Venue Logo-1 (1).png
│       ├── CGCTV logo.png
│       ├── dartstream-logo.png
│       ├── MDstudios Logo.png
│       ├── Officail AADS Logo.png
│       └── Untitled-1-CGCDARTS-COM IMPROVED LOGO.png
├── config.js               # Configuration file for API settings
└── README.md              # This file
```

## Quick Start

### Option 1: Direct Use
1. Open `index.html` in a web browser
2. The display will automatically connect to the AADS Supabase backend
3. Data refreshes automatically every 5 minutes

### Option 2: Embed in Another Project
1. Copy the entire `display-app` folder into your project
2. Reference the HTML file in an iframe or include it directly:

```html
<!-- Method 1: iFrame -->
<iframe src="path/to/display-app/index.html" 
        width="100%" 
        height="800px" 
        frameborder="0"></iframe>

<!-- Method 2: Direct inclusion (requires proper routing) -->
<div id="aads-display"></div>
<script>
  fetch('path/to/display-app/index.html')
    .then(response => response.text())
    .then(html => {
      document.getElementById('aads-display').innerHTML = html;
    });
</script>
```

### Option 3: OBS/Streaming Software
1. Add a Browser Source in OBS
2. Point it to the local file path or hosted URL
3. Set width: 1920, height: 1080 for Full HD
4. Enable "Shutdown source when not visible" for performance
5. Set refresh rate if desired (optional, page auto-refreshes)

## Configuration

### Customizing the API Endpoint
Edit `config.js` to point to your own backend:

```javascript
window.AADS_CONFIG = {
    SUPABASE_URL: 'https://your-project.supabase.co',
    SUPABASE_ANON_KEY: 'your-anon-key',
    REFRESH_INTERVAL: 300000, // 5 minutes
};
```

### Multi-Tenant Support
Add `?user_id=YOUR_USER_ID` to the URL to display stats for a specific organization:
```
index.html?user_id=abc123
```

## Browser Compatibility
- ✅ Chrome/Edge (Recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Opera
- ⚠️ IE11 (Limited support)

## Requirements
- **No build process required** - Pure HTML/CSS/JS
- **No local dependencies** - All dependencies loaded from CDN
- **Internet connection** - Required for Supabase API and CDN resources
- Modern web browser with JavaScript enabled

## Dependencies (Auto-loaded)
- Supabase JS Client v2 (via CDN)

## Features Breakdown

### Standings Tab
- Real-time player rankings
- Weighted 3-dart averages
- Total 180s, 140+, 100+ counts
- Highest finishes
- Events played

### Events Tab
- Event cards with champion info
- Match counts and player participation
- Runner-up information
- Event dates

### Champions Tab
- Latest champion showcase
- Historical champion records
- Event winners table

### Statistics Tab
- Top performers in each category
- Highest average
- Most 180s, 140+, 100+
- Highest checkout
- Most legs played

### Players Tab
- Complete player directory
- Sortable statistics
- Detailed player metrics

## Customization

### Styling
All styles are embedded in `index.html`. Look for the `<style>` tag to customize:
- Colors (CSS variables in `:root`)
- Fonts
- Layout spacing
- Animations

### Logos
Replace logo files in `assets/logos/` with your own:
- Maintain same filenames for automatic compatibility
- Or update the `<img src="">` references in `index.html`

## Troubleshooting

### Display shows "Error loading standings"
- Check internet connection
- Verify Supabase URL and API key in the HTML file
- Check browser console for specific errors

### Logos not loading
- Ensure logo files are in `assets/logos/` directory
- Check file paths in HTML match actual filenames
- Verify file permissions

### Data not refreshing
- Check browser console for JavaScript errors
- Ensure Supabase backend is operational
- Verify auto-refresh interval setting

## Support
For issues, questions, or feature requests:
- Check the main project documentation
- Review browser console for errors
- Verify all file paths are correct

## Version
- **Current Version:** 1.0.8
- **Last Updated:** December 19, 2025
- **Compatible With:** AADS Backend v1.0.x

## License
© 2025 Atlantic Amateur Darts Series. All rights reserved.

## Credits
- **Design:** MD Studios
- **Development:** AADS Development Team
- **Data:** Powered by DartConnect
- **Hosting:** Supabase
