# Frontend - AI Mock Interview Coach

Modern, responsive frontend for the AI Mock Interview Coach application.

## Features

- 🎨 **Modern Design**: Dark theme with glassmorphism effects
- 📊 **Real-time Scoring**: Visual feedback on 5 dimensions
- 🔄 **Adaptive UI**: Responds to interview progress
- 📱 **Responsive**: Works on desktop, tablet, and mobile
- ⚡ **Fast**: No build step, pure HTML/CSS/JS

## Files

- `index.html` - Landing page with features and CTA
- `interview.html` - Main interview application (3 states)
- `app.js` - JavaScript logic and API integration
- `styles.css` - Shared styles and animations
- `guide.md` - Detailed build guide
- `spec.json` - Component specifications

## Quick Start

### 1. Start the API Server

From the project root:
```bash
python api_server.py
```

### 2. Serve the Frontend

From this directory:
```bash
python -m http.server 3000
```

### 3. Open in Browser

Navigate to: `http://localhost:3000/index.html`

## Configuration

### API Base URL

The default API URL is `http://localhost:8000/api/v1`.

To change it:
1. Open `interview.html`
2. Find the "API URL" input in the header
3. Update the default value

Or change it in the UI using the "API URL" field.

### API Key

You can provide your Google API key in two ways:

1. **Environment Variable** (Recommended):
   - Set `GOOGLE_API_KEY` in `.env` file
   - The API server will use it automatically

2. **UI Input**:
   - Enter it in the "API Key" field in the top navigation
   - It will be stored in localStorage

## Application States

The interview app has 3 states:

### 1. Setup View
- Resume input (LaTeX format)
- Job description input (plain text)
- Settings configuration
- Preview parsed data

### 2. Interview View
- Progress bar
- Conversation history
- Current question display
- Answer input
- Real-time evaluation scores
- Outcome prediction (after turn 3)

### 3. Results View
- Readiness level and percentile
- Full coaching report (markdown)
- Strengths and skill gaps
- Answer patterns analysis
- Session statistics

## Styling

### Color Palette

- Background: `#09090b` (near black)
- Cards: `#0e0e11` (dark gray)
- Borders: `rgba(255,255,255,0.05)` (subtle white)
- Text: `#e4e4e7` (light gray)
- Accent: `#a1a1aa` (zinc)

### Typography

- Primary: Inter (sans-serif)
- Headings: Geist (display font)

### Components

- **Panel**: Card with backdrop blur and subtle border
- **Glass Card**: Glassmorphism effect with gradient highlight
- **Input Field**: Dark background with focus states
- **Buttons**: Animated hover effects with gradient overlays
- **Score Bars**: Color-coded progress bars (1-5 scale)

## API Integration

All API calls are handled in `app.js`:

```javascript
// State management
const state = {
    apiKey: localStorage.getItem('interviewai_apikey') || '',
    baseUrl: 'http://localhost:8000/api/v1',
    sessionId: null,
    // ...
};

// API helper
async function apiCall(method, path, body = null) {
    // Makes authenticated requests to the API
}

// Key functions
handleStart()      // Initialize interview
fetchQuestion()    // Get next question
handleSubmit()     // Submit answer
handleComplete()   // Generate report
```

## Customization

### Changing Colors

Edit `styles.css`:

```css
/* Background */
body { background: #09090b; }

/* Cards */
.panel { background: rgba(14, 14, 17, 0.8); }

/* Accent color */
.btn-primary { background: linear-gradient(135deg, #18181b, #27272a); }
```

### Adding Features

1. Add UI elements to `interview.html`
2. Add event listeners in `app.js`
3. Make API calls using the `apiCall()` helper
4. Update state and UI accordingly

### Modifying Layout

The layout uses CSS Grid and Flexbox:

```html
<!-- Two-column layout -->
<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div>Column 1</div>
    <div>Column 2</div>
</div>
```

## Browser Support

- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support
- Mobile browsers: ✅ Responsive design

## Performance

- No build step required
- Minimal dependencies (Tailwind CDN, Iconify, Lucide)
- Lazy loading for icons
- Efficient state management

## Development

### Hot Reload

Use a development server with hot reload:

```bash
# Python
python -m http.server 3000

# Node.js
npx http-server -p 3000

# VS Code Live Server extension
# Right-click index.html → Open with Live Server
```

### Debugging

1. Open browser DevTools (F12)
2. Check Console for errors
3. Check Network tab for API calls
4. Use `console.log()` in `app.js`

## Deployment

### Static Hosting

Deploy to any static hosting service:

- **Netlify**: Drag and drop the `Frontend` folder
- **Vercel**: Connect your Git repository
- **GitHub Pages**: Push to `gh-pages` branch
- **AWS S3**: Upload files and enable static hosting
- **Cloudflare Pages**: Connect repository

### Configuration for Production

1. Update `baseUrl` in `app.js` to your production API URL
2. Remove or secure the API key input (use backend authentication)
3. Enable HTTPS
4. Add analytics if needed

## Security

- Never expose API keys in frontend code
- Use environment variables for sensitive data
- Validate all user inputs
- Sanitize HTML output
- Use HTTPS in production

## Troubleshooting

### CORS Errors
- Ensure the API server has CORS enabled
- Check that `flask-cors` is installed

### API Key Issues
- Verify the key is correct
- Check that it's set in `.env` or entered in UI
- Ensure the API server can access it

### Styling Issues
- Clear browser cache
- Check that Tailwind CDN is loading
- Verify CSS file is linked correctly

### JavaScript Errors
- Check browser console for errors
- Ensure `app.js` is loaded
- Verify API responses match expected format

## Resources

- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Iconify Icons](https://icon-sets.iconify.design/)
- [Lucide Icons](https://lucide.dev/)
- [MDN Web Docs](https://developer.mozilla.org/)

## Contributing

To contribute to the frontend:

1. Make changes to HTML/CSS/JS files
2. Test in multiple browsers
3. Ensure responsive design works
4. Update this README if needed
5. Submit a pull request

---

**Built with ❤️ using vanilla HTML, CSS, and JavaScript**
