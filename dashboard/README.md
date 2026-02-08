# 📊 Profile Update Bot Dashboard

A minimal, mobile-friendly dashboard to monitor GitHub Actions workflow runs with dark mode UI.

[![Live Dashboard](https://img.shields.io/badge/Live-Dashboard-667eea)](https://itsashutosh07.github.io/profile-update-bots/)

---

## 🌟 Features

- **Real-time Status**: View latest workflow runs with status badges
- **Dark Mode**: Easy on the eyes with modern dark theme
- **Mobile Responsive**: Works perfectly on all screen sizes
- **Zero Backend**: Pure client-side, fetches from GitHub API
- **Auto Stats**: Success rate, total runs, and last run status
- **Quick Actions**: Click any run card to view full logs on GitHub

---

## 🎨 What It Shows

### Top Stats
- **Total Runs**: Number of workflow runs displayed
- **Success Rate**: Percentage of successful runs
- **Last Run Status**: Status of the most recent run

### Run Cards
Each workflow run displays:
- Status badge (Success, Failure, In Progress, etc.)
- Run number
- Workflow name
- Duration
- Triggered by (user/schedule)
- Relative timestamp ("3 hours ago")
- Direct link to GitHub logs

---

## 🚀 How It Works

```
User Browser → GitHub API → Parse JSON → Render Cards
```

1. Dashboard loads in browser
2. Fetches data from GitHub's public API
3. Parses workflow run information
4. Displays as interactive cards
5. Click any card to view full logs on GitHub

**API Endpoint**: `https://api.github.com/repos/{owner}/{repo}/actions/runs`

---

## 🧪 Local Testing

Test the dashboard locally before deployment:

```bash
# Navigate to dashboard folder
cd dashboard

# Start local server (Python 3)
python3 -m http.server 8000

# Or using Python 2
python -m SimpleHTTPServer 8000

# Or using Node.js
npx http-server -p 8000
```

Then open: `http://localhost:8000`

---

## ⚙️ Configuration

To use this dashboard for your own repository:

### Update Repository Details

Edit `index.html` lines 351-352:

```javascript
const GITHUB_OWNER = 'your-github-username';
const GITHUB_REPO = 'your-repo-name';
```

### Customize Colors

Edit the CSS section (lines 13-150):

```css
/* Dark mode colors */
--bg-primary: #1a1a1a;
--bg-secondary: #2d2d2d;
--text-primary: #e0e0e0;
--success-color: #10b981;
--failure-color: #ef4444;
/* ... etc */
```

### Adjust Run Limit

Change how many runs to display (line 350):

```javascript
const API_URL = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/actions/runs?per_page=30`;
// Change ?per_page=30 to desired number (max 100)
```

---

## 📱 Responsive Design

### Mobile (<768px)
- Single column layout
- Full-width cards
- Touch-friendly buttons

### Tablet (768px-1024px)
- Two column grid
- Balanced card sizes

### Desktop (>1024px)
- Three column grid
- Maximum information density

---

## 🔒 Security & Privacy

- **No Authentication Required**: Uses GitHub's public API
- **No Data Storage**: Everything fetched live from GitHub
- **No Backend**: Pure client-side JavaScript
- **No Tracking**: No analytics or user tracking
- **Rate Limits**: 60 requests/hour (unauthenticated)

---

## 🎯 Status Badges

| Status | Color | Description |
|--------|-------|-------------|
| ✅ Success | Green (#10b981) | Run completed successfully |
| ❌ Failure | Red (#ef4444) | Run failed with errors |
| 🔄 In Progress | Blue (#3b82f6) | Currently running |
| ⏭️ Skipped | Gray (#6b7280) | Run was skipped |
| 🚫 Cancelled | Gray (#6b7280) | Run was cancelled |

---

## 🛠️ Troubleshooting

### Dashboard Shows "Failed to Load Runs"

**Possible causes:**
1. Repository is private (API requires authentication)
2. Repository name/owner is incorrect
3. Network/CORS issues
4. Rate limit exceeded (60 requests/hour)

**Solutions:**
- Verify repository is public
- Check browser console for errors
- Confirm owner/repo names in `index.html`
- Wait an hour if rate limited

### No Runs Displayed

**Possible causes:**
1. No workflows have run yet
2. Workflow file not properly configured
3. API returning empty results

**Solutions:**
- Manually trigger a workflow run
- Check GitHub Actions tab in repository
- Verify workflows exist in `.github/workflows/`

### Cards Not Clickable

**Check:**
- JavaScript is enabled in browser
- No console errors
- `html_url` field exists in API response

---

## 🎨 Customization Examples

### Change Success Color to Blue

```css
.status-success {
    background: rgba(59, 130, 246, 0.15);
    color: #3b82f6;
    border: 1px solid rgba(59, 130, 246, 0.3);
}
```

### Add Auto-Refresh

```javascript
// Add to end of script section
setInterval(loadRuns, 60000); // Refresh every 60 seconds
```

### Show More Runs

```javascript
// Change per_page parameter
const API_URL = `...actions/runs?per_page=50`; // Show 50 runs
```

---

## 📊 API Response Structure

The dashboard uses GitHub's Workflow Runs API:

```json
{
  "total_count": 123,
  "workflow_runs": [
    {
      "id": 123456,
      "name": "Update Naukri Profile",
      "status": "completed",
      "conclusion": "success",
      "html_url": "https://github.com/...",
      "run_number": 42,
      "created_at": "2026-02-08T10:00:00Z",
      "updated_at": "2026-02-08T10:02:30Z",
      "triggering_actor": {
        "login": "username"
      }
    }
  ]
}
```

---

## 🚀 Deployment

This dashboard is automatically deployed to GitHub Pages via GitHub Actions.

**Live URL**: `https://itsashutosh07.github.io/profile-update-bots/`

### Manual Deployment

1. Enable GitHub Pages in repository settings
2. Set source to "GitHub Actions"
3. Push changes to main branch
4. Workflow automatically deploys

---

## 🔮 Future Enhancements

Potential features for v2:
- [ ] Charts/graphs for trends
- [ ] Filter by date range
- [ ] Search functionality
- [ ] Export to CSV
- [ ] Dark/light mode toggle
- [ ] Notification on failures
- [ ] Historical data tracking
- [ ] Performance metrics

---

## 📝 Tech Stack

- **HTML5**: Structure
- **CSS3**: Styling (Grid, Flexbox, Animations)
- **Vanilla JavaScript**: Functionality (No frameworks!)
- **GitHub API**: Data source
- **GitHub Pages**: Hosting

**Total Size**: ~15KB (uncompressed)
**Dependencies**: None!

---

## 🤝 Contributing

Improvements welcome!

**Ideas:**
- Better mobile UX
- Additional statistics
- Performance optimizations
- Accessibility improvements

---

## 📄 License

MIT License - See [LICENSE](../LICENSE) for details.

---

## 🔗 Links

- [GitHub Repository](https://github.com/itsashutosh07/profile-update-bots)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [GitHub API Docs](https://docs.github.com/en/rest/actions/workflow-runs)

---

<div align="center">

**Dashboard for Profile Update Bot** 🤖

[⬆ Back to Main README](../README.md)

</div>

