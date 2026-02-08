# Dashboard Setup Guide

## 📋 Quick Setup (5 minutes)

### Step 1: Enable GitHub Pages

1. Go to your repository on GitHub:
   ```
   https://github.com/itsashutosh07/profile-update-bots
   ```

2. Click **Settings** tab

3. In the left sidebar, click **Pages**

4. Under "Build and deployment":
   - **Source**: Select **GitHub Actions**
   - (Not "Deploy from a branch")

5. Click **Save**

6. You should see a message: "Your site is ready to be published at..."

### Step 2: Deploy the Dashboard

The dashboard will automatically deploy when you push the dashboard files to the main branch.

**Option A: Already pushed** (recommended)
- The workflow should trigger automatically
- Go to **Actions** tab to see deployment progress
- Wait 2-3 minutes for deployment

**Option B: Manual trigger**
1. Go to **Actions** tab
2. Click "Deploy Dashboard to GitHub Pages" workflow
3. Click **Run workflow** button
4. Click **Run workflow** to confirm

### Step 3: Verify Deployment

1. Go to **Actions** tab
2. Click on the latest "Deploy Dashboard" workflow run
3. Wait for it to complete (green checkmark)
4. Visit your dashboard:
   ```
   https://itsashutosh07.github.io/profile-update-bots/
   ```

---

## ✅ Verification Checklist

After setup, verify these:

- [ ] GitHub Pages is enabled with "GitHub Actions" source
- [ ] Deployment workflow completed successfully
- [ ] Dashboard URL loads without errors
- [ ] Stats show correct run count
- [ ] Run cards are clickable
- [ ] "View Logs" links work
- [ ] Mobile view works (test on phone or dev tools)

---

## 🔧 Troubleshooting

### "Pages" option not in Settings

**Solution**: Make sure you have admin access to the repository.

### "GitHub Actions" not available as source

**Solution**: 
1. Make sure repository is public (or you have GitHub Pro/Team)
2. Refresh the page
3. Try selecting "Deploy from a branch" then switching back

### Dashboard shows 404 error

**Possible causes**:
1. Workflow hasn't run yet → Check Actions tab
2. Deployment failed → Check workflow logs
3. Wrong URL → Should be: `https://USERNAME.github.io/REPO-NAME/`

### Dashboard loads but shows "Failed to Load Runs"

**Possible causes**:
1. Repository is private → Make it public or add authentication
2. Owner/repo name mismatch → Update in `dashboard/index.html`
3. Rate limit exceeded → Wait an hour

**Check**: Open browser console (F12) to see error messages

### Workflow fails with "permissions" error

**Solution**: 
1. Go to Settings → Actions → General
2. Scroll to "Workflow permissions"
3. Select "Read and write permissions"
4. Check "Allow GitHub Actions to create and approve pull requests"
5. Click **Save**

### Changes not reflected on live site

**Solution**:
1. Clear browser cache (Ctrl+F5 or Cmd+Shift+R)
2. Wait 2-3 minutes for deployment
3. Check if workflow completed successfully
4. Try incognito/private browsing mode

---

## 🎨 Customization

### Update Repository Info

Edit `dashboard/index.html` lines 351-352:

```javascript
const GITHUB_OWNER = 'your-username';  // Change this
const GITHUB_REPO = 'your-repo-name';   // Change this
```

### Change Colors

Edit the CSS variables in `dashboard/index.html`:

```css
/* Find these in the <style> section */
background-color: #1a1a1a;  /* Main background */
background: #2d2d2d;        /* Card background */
color: #e0e0e0;             /* Text color */
```

### Show More/Fewer Runs

Edit line 350 in `dashboard/index.html`:

```javascript
const API_URL = `...?per_page=30`;  // Change 30 to desired number (max 100)
```

---

## 🔄 Update Process

When you make changes to the dashboard:

1. Edit files in `dashboard/` folder
2. Commit and push to main branch:
   ```bash
   git add dashboard/
   git commit -m "Update dashboard"
   git push
   ```
3. Workflow automatically deploys (2-3 minutes)
4. Refresh dashboard URL to see changes

---

## 📱 Mobile Testing

Test responsiveness:

1. Open dashboard URL
2. Open browser developer tools (F12)
3. Click device toolbar icon (Ctrl+Shift+M)
4. Test different screen sizes:
   - Mobile: 375px
   - Tablet: 768px
   - Desktop: 1440px

Or simply open on your phone!

---

## 🔐 Security Notes

- Dashboard uses **public** GitHub API (no authentication needed)
- **Rate limit**: 60 requests/hour per IP address
- **No data storage**: Everything fetched live from GitHub
- **No secrets required**: Dashboard doesn't need repository secrets

---

## 🆘 Still Having Issues?

1. **Check workflow logs**: Actions tab → Latest run → View logs
2. **Verify repository settings**: Settings → Pages
3. **Test locally first**: Run `python3 -m http.server 8000` in dashboard/
4. **Check browser console**: F12 → Console tab for errors
5. **Repository visibility**: Must be public for free GitHub Pages

---

## 📞 Support

If you're stuck:
- Check [GitHub Pages documentation](https://docs.github.com/en/pages)
- Check [GitHub Actions documentation](https://docs.github.com/en/actions)
- Review workflow logs for specific errors
- Test locally to isolate issues

---

<div align="center">

**Dashboard should be live at:**

`https://itsashutosh07.github.io/profile-update-bots/`

🎉 **Enjoy your dashboard!**

[⬆ Back to Dashboard README](README.md)

</div>

