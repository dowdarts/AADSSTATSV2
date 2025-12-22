# AADS Stats - Public Display

This is the public-facing statistics display for the Atlantic Amateur Darts Series.

## 🎯 Live Site

**View Live Stats**: [https://dowdarts.github.io/AADSSTATSV2/](https://dowdarts.github.io/AADSSTATSV2/)

## 📊 Features

- 🏆 Series Leaderboard - Overall rankings across all events
- 📋 Event Standings - Round Robin group standings
- 🎯 Player Search - Find players and view detailed stats
- 🏅 Knockout Brackets - Quarterfinals, Semifinals, Finals visualization
- 🎨 AADS Branding - Professional green/gold styling

## 🌐 Embedding on Your Website

### Full Page Embed

```html
<iframe 
    src="https://dowdarts.github.io/AADSSTATSV2/" 
    width="100%" 
    height="800px"
    frameborder="0"
    allowfullscreen>
</iframe>
```

### Responsive Embed

```html
<div style="position: relative; padding-bottom: 75%; height: 0; overflow: hidden;">
    <iframe 
        src="https://dowdarts.github.io/AADSSTATSV2/" 
        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
        frameborder="0">
    </iframe>
</div>
```

## 🔄 Data Source

All data is powered by **Supabase** and updated in real-time:
- Admins review and approve all data via localhost admin panel
- Approved data instantly appears on this public display
- Automatic ranking calculations based on AADS tournament rules

## 🎨 Customization

The display uses AADS official colors:
- **Primary Green**: #1a472a
- **Secondary Green**: #2d7a4f  
- **Gold Accent**: #ffd700

## 📞 Contact

- **Organization**: Atlantic Amateur Darts Series (AADS)
- **Website**: [aadsdarts.com](https://aadsdarts.com)

---

*This is a read-only public display. Admin functions are available separately via localhost.*
