/**
 * AADS Display App Configuration
 * 
 * This file contains all configuration settings for the AADS statistics display.
 * You can customize these settings to point to your own backend or adjust behavior.
 */

window.AADS_CONFIG = {
    /**
     * Supabase Configuration
     * Replace these with your own Supabase project credentials
     */
    SUPABASE_URL: 'https://kswwbqumgsdissnwuiab.supabase.co',
    SUPABASE_ANON_KEY: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtzd3dicXVtZ3NkaXNzbnZ1aWFiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQ0ODMwNTIsImV4cCI6MjA4MDA1OTA1Mn0.b-z8JqL1dBYJcrrzSt7u6VAaFAtTOl1vqqtFFgHkJ50',
    
    /**
     * API Configuration
     * Constructed from Supabase settings
     */
    get API_BASE() {
        return `${this.SUPABASE_URL}/functions/v1`;
    },
    
    /**
     * Display Settings
     */
    REFRESH_INTERVAL: 300000, // 5 minutes in milliseconds
    AUTO_REFRESH: true,        // Enable/disable auto-refresh
    
    /**
     * Multi-Tenant Support
     * Set to null for default tenant, or provide user_id
     */
    DEFAULT_USER_ID: null,
    
    /**
     * Feature Flags
     */
    FEATURES: {
        SHOW_EVENTS: true,
        SHOW_CHAMPIONS: true,
        SHOW_STATISTICS: true,
        SHOW_PLAYERS: true,
        SHOW_FOOTER: true,
        SHOW_PARTNER_LOGOS: true
    },
    
    /**
     * Branding
     */
    BRANDING: {
        TITLE: 'Atlantic Amateur Darts Series',
        SUBTITLE: '2025 Championship Standings',
        MAIN_LOGO: 'assets/logos/Officail AADS Logo.png',
        FAVICON: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y="0.9em" font-size="90">🎯</text></svg>'
    },
    
    /**
     * Partner Logos Configuration
     * Add or remove logos as needed
     */
    PARTNER_LOGOS: [
        {
            src: 'assets/logos/AADS.COM LOGO-2.png',
            alt: 'AADS.com',
            title: 'Visit AADS.com',
            link: 'https://www.aadsdarts.com/'
        },
        {
            src: 'assets/logos/CGC official logo-1.png',
            alt: 'CGC',
            title: 'Visit CGC Facebook Group',
            link: 'https://www.facebook.com/share/g/1AKwm6pdvE/'
        },
        {
            src: 'assets/logos/CGC Venue Logo-1 (1).png',
            alt: 'CGC Venue',
            title: 'View CGC Venue Location',
            link: 'https://maps.app.goo.gl/5keVvEccA7nTrvXa6'
        },
        {
            src: 'assets/logos/CGCTV logo.png',
            alt: 'CGC TV',
            title: 'CGC TV',
            link: null
        },
        {
            src: 'assets/logos/Untitled-1-CGCDARTS-COM IMPROVED LOGO.png',
            alt: 'CGC Darts',
            title: 'Visit CGCDarts.com',
            link: 'https://cgcdarts.com'
        },
        {
            src: 'assets/logos/MDstudios Logo.png',
            alt: 'MD Studios',
            title: 'MD Studios',
            link: null
        }
    ],
    
    /**
     * Styling Options
     * These can override the default CSS variables
     */
    CUSTOM_STYLES: {
        PRIMARY_COLOR: '#FF6B00',
        DARK_BG: '#0a0a0a',
        CARD_BG: '#1a1a1a',
        TEXT_PRIMARY: '#ffffff',
        TEXT_SECONDARY: '#b0b0b0'
    },
    
    /**
     * Debug Settings
     */
    DEBUG: false,
    CONSOLE_LOGS: true
};

/**
 * Helper Functions
 */
window.AADS_HELPERS = {
    /**
     * Get current user ID from URL parameter or config
     */
    getUserId() {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('user') || 
               urlParams.get('user_id') || 
               window.AADS_CONFIG.DEFAULT_USER_ID;
    },
    
    /**
     * Build API URL with optional user_id parameter
     */
    buildApiUrl(endpoint) {
        const userId = this.getUserId();
        const baseUrl = `${window.AADS_CONFIG.API_BASE}/${endpoint}`;
        return userId ? `${baseUrl}?user_id=${userId}` : baseUrl;
    },
    
    /**
     * Log message if debug enabled
     */
    log(...args) {
        if (window.AADS_CONFIG.DEBUG && window.AADS_CONFIG.CONSOLE_LOGS) {
            console.log('[AADS Display]', ...args);
        }
    },
    
    /**
     * Handle errors
     */
    error(...args) {
        console.error('[AADS Display Error]', ...args);
    }
};

// Initialize notification
if (window.AADS_CONFIG.DEBUG) {
    console.log('AADS Configuration loaded successfully', window.AADS_CONFIG);
}
