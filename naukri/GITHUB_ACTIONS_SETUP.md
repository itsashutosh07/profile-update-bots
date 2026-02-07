# 🆓 GitHub Actions Setup - NO Credit Card Required!

**Perfect if you don't have a credit card!** ✅

GitHub Actions is **completely FREE** and requires **NO CREDIT CARD** - just a GitHub account (which is also free)!

## ✅ What You Get FREE:

- **2,000 minutes/month** of automation time (plenty for this bot!)
- **Runs every 2 hours automatically**
- **500MB storage** for artifacts (screenshots)
- **NO credit card needed** ✅
- **Forever FREE** for public repositories

## 📊 Is 2,000 Minutes Enough?

**YES!** Here's the math:
- Each update takes ~2-3 minutes
- Running every 2 hours = 12 updates/day
- 12 updates × 3 minutes = 36 minutes/day
- 36 minutes × 30 days = **1,080 minutes/month**
- You get 2,000 minutes = **Plenty of buffer!** ✅

---

## 🚀 Complete Setup Guide (10 Minutes)

### Step 1: Create GitHub Account (if you don't have one)

1. Go to [github.com](https://github.com)
2. Click **"Sign up"**
3. Enter:
   - Email address
   - Password
   - Username
4. Verify email
5. **Done! No credit card needed!** ✅

---

### Step 2: Create a New Repository

**Option A: Using GitHub Website (Easier)**

1. Go to [github.com/new](https://github.com/new)
2. Fill in:
   - **Repository name**: `naukri-profile-bot`
   - **Description**: "Automatically updates my Naukri profile every 2 hours"
   - **Visibility**: 
     - ✅ **Public** (to get free Actions minutes)
     - ⚠️ Don't worry - we'll secure your credentials!
   - ✅ Check "Add a README file"
3. Click **"Create repository"**

---

### Step 3: Upload Your Project Files

#### Option A: Using GitHub Web Interface (No Git knowledge needed!)

1. In your new repository, click **"Add file"** → **"Upload files"**

2. **From your laptop**, drag and drop these files:
   ```
   update.py
   scheduler.py (not needed for GitHub Actions, but good to have)
   requirements.txt
   .github/workflows/update-profile.yml
   README.md
   ```

3. **IMPORTANT**: Do NOT upload `.env` file (contains your password!)

4. Click **"Commit changes"**

#### Option B: Using Git Command Line

```bash
# Navigate to your project
cd /Users/ashutoshmac/Work/Projects/profile-update-bot/naukri

# Initialize git (if not already done)
git init

# Add GitHub as remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/naukri-profile-bot.git

# Add all files except .env
git add update.py requirements.txt README.md .github/ deployment/ *.md

# Commit
git commit -m "Initial commit - Naukri profile update bot"

# Push to GitHub
git branch -M main
git push -u origin main
```

---

### Step 4: Add Your Credentials as Secrets (SECURE!)

This is how you store your email and password **securely** without exposing them:

1. In your GitHub repository, click **"Settings"** tab

2. In left sidebar, click **"Secrets and variables"** → **"Actions"**

3. Click **"New repository secret"**

4. **Add First Secret**:
   - Name: `NAUKRI_EMAIL`
   - Secret: `7.ashutoshj@gmail.com`
   - Click **"Add secret"**

5. Click **"New repository secret"** again

6. **Add Second Secret**:
   - Name: `NAUKRI_PASSWORD`
   - Secret: `Qwer!yu7890`
   - Click **"Add secret"**

✅ **Your credentials are now secure!** They're encrypted and never visible in your code.

---

### Step 5: Enable GitHub Actions

1. In your repository, click **"Actions"** tab

2. If you see a message about workflows:
   - Click **"I understand my workflows, go ahead and enable them"**

3. You should see the workflow: **"Update Naukri Profile"**

4. Click on it to see details

---

### Step 6: Test Run (Manual Trigger)

1. Click **"Actions"** tab

2. Click on **"Update Naukri Profile"** workflow (left sidebar)

3. Click **"Run workflow"** button (on the right)

4. Click **"Run workflow"** in the popup

5. Wait ~2-3 minutes

6. Click on the running workflow to see live logs

7. ✅ Should show:
   ```
   ✓ Logged in
   ✓ Navigated to profile page
   ✓ Resume Headline updated
   ```

---

### Step 7: View Screenshots

After the workflow completes:

1. Scroll down on the workflow run page

2. Under **"Artifacts"**, you'll see:
   - `screenshots-1` (or similar name)

3. Click to download the screenshots ZIP file

4. Extract and view screenshots to verify update worked!

---

### Step 8: Automated Schedule (Already Configured!)

✅ **You're done!** The workflow is already configured to run **every 2 hours automatically**.

The schedule is defined in `.github/workflows/update-profile.yml`:
```yaml
schedule:
  - cron: '0 */2 * * *'  # Runs every 2 hours
```

---

## 📊 How to Monitor Your Bot

### View Workflow Runs

1. Go to **"Actions"** tab in your repository
2. See all past and current runs
3. Click on any run to see detailed logs
4. Download screenshots from "Artifacts" section

### Check Schedule

Your bot runs automatically at:
- 12:00 AM, 2:00 AM, 4:00 AM, 6:00 AM, 8:00 AM, 10:00 AM
- 12:00 PM, 2:00 PM, 4:00 PM, 6:00 PM, 8:00 PM, 10:00 PM
- (All times in UTC - GitHub Actions uses UTC timezone)

### Manual Trigger Anytime

1. Go to **Actions** → **Update Naukri Profile**
2. Click **"Run workflow"**
3. Select branch: `main`
4. Click **"Run workflow"** button

---

## 🎛️ Management

### Pause the Bot

1. Go to **"Actions"** tab
2. Click **"Update Naukri Profile"** (left sidebar)
3. Click "..." menu (top right)
4. Click **"Disable workflow"**

### Resume the Bot

1. Same steps as above
2. Click **"Enable workflow"**

### Change Schedule

1. Edit `.github/workflows/update-profile.yml`
2. Change the cron expression:
   ```yaml
   # Every 3 hours
   - cron: '0 */3 * * *'
   
   # Every 4 hours
   - cron: '0 */4 * * *'
   
   # Every 6 hours
   - cron: '0 */6 * * *'
   ```

---

## 🔧 Troubleshooting

### Workflow Fails with "Missing Credentials"

**Solution**: Check your secrets:
1. Settings → Secrets and variables → Actions
2. Make sure you have:
   - `NAUKRI_EMAIL`
   - `NAUKRI_PASSWORD`
3. Re-add them if missing

### Workflow Fails with Chrome Error

**Solution**: The workflow already installs Chrome. If it fails:
1. Check the error logs
2. Try re-running the workflow (sometimes transient issues)

### Cannot Find Workflow File

**Solution**: Make sure `.github/workflows/update-profile.yml` exists:
1. In your repo, navigate to `.github/workflows/`
2. Should see `update-profile.yml`
3. If missing, upload it again

### Screenshots Not Saved

**Solution**: 
1. The workflow saves screenshots as "Artifacts"
2. Check at the bottom of the workflow run page
3. Download the ZIP file
4. Artifacts are kept for 7 days by default

---

## 💡 Advantages of GitHub Actions

### ✅ Pros:
- **NO credit card required** ✅
- **Completely FREE** (2,000 minutes/month)
- **Easy to monitor** (web interface with logs)
- **Secure credential storage** (GitHub Secrets)
- **Automatic screenshots** (saved as artifacts)
- **No server maintenance** needed
- **Reliable** (GitHub's infrastructure)

### ⚠️ Limitations:
- **Public repository required** (for free tier)
  - Your code is public, but credentials are secure
- **2,000 minutes/month limit** (but that's plenty!)
- **Artifacts kept only 7 days** (screenshots)
- **Might be detected as bot** (less common than VPS though)
- **Cannot view live browser** (headless only)

---

## 🆚 GitHub Actions vs VPS

| Feature | GitHub Actions | VPS (Oracle/AWS) |
|---------|----------------|------------------|
| **Credit Card** | ❌ NOT Required | ✅ Required |
| **Cost** | FREE | FREE (with trials) |
| **Setup Time** | 10 min | 15-20 min |
| **Maintenance** | None | Need to manage server |
| **Reliability** | Very High | Very High |
| **Flexibility** | Medium | High |
| **Best For** | No credit card | Full control |

---

## 📈 Usage Tracking

### Check Your Minutes Used

1. Go to [github.com/settings/billing](https://github.com/settings/billing)
2. Click **"Plans and usage"**
3. Scroll to **"Actions"**
4. See minutes used vs. limit (2,000/month)

### Typical Usage for This Bot

- **Per run**: 2-3 minutes
- **Per day**: ~36 minutes (12 runs)
- **Per month**: ~1,080 minutes
- **Remaining**: ~920 minutes buffer ✅

---

## 🔒 Security Notes

### Your Credentials are Safe

1. ✅ **Secrets are encrypted** by GitHub
2. ✅ **Never visible** in logs or code
3. ✅ **Only accessible** to your workflows
4. ✅ **Cannot be read** by others (even if repo is public)

### What's Public vs Private

**Public (Safe):**
- ✅ Your code (`update.py`, etc.)
- ✅ Workflow configuration
- ✅ Documentation

**Private (Secure):**
- ✅ Your email (stored as secret)
- ✅ Your password (stored as secret)
- ✅ Secrets are NEVER exposed

---

## 🎉 You're All Set!

Your Naukri profile will now update automatically every 2 hours via GitHub Actions!

### What Happens Now:

- ✅ Runs every 2 hours automatically
- ✅ Updates your Naukri profile
- ✅ Saves screenshots (available for 7 days)
- ✅ Shows logs for each run
- ✅ Emails you if workflow fails (optional)
- ✅ Uses only ~1,000 of your 2,000 free minutes

### Next Steps:

1. ✅ Wait for first scheduled run (within 2 hours)
2. ✅ Check "Actions" tab to see results
3. ✅ Download and verify screenshots
4. ✅ Relax - it runs automatically! 😊

---

## 💡 Pro Tips

### Get Email Notifications

1. GitHub → Settings → Notifications
2. Enable "Email" for workflow failures
3. Get notified if something goes wrong

### Change Update Interval

Edit `.github/workflows/update-profile.yml`:

```yaml
# Current: Every 2 hours
- cron: '0 */2 * * *'

# Every 3 hours
- cron: '0 */3 * * *'

# Every 4 hours  
- cron: '0 */4 * * *'

# Every 6 hours
- cron: '0 */6 * * *'

# Daily at 9 AM and 6 PM UTC
- cron: '0 9,18 * * *'
```

### Keep Artifacts Longer

Edit `.github/workflows/update-profile.yml`:

```yaml
- name: Upload screenshots as artifacts
  uses: actions/upload-artifact@v3
  with:
    name: screenshots-${{ github.run_number }}
    path: Logs Screenshot/
    retention-days: 30  # Change from 7 to 30 days
```

---

## ❓ FAQ

**Q: Is GitHub Actions really free?**  
A: Yes! 2,000 minutes/month for public repos. No credit card needed.

**Q: Will my email/password be visible?**  
A: No! They're stored as encrypted secrets, never visible anywhere.

**Q: Can others see my profile updates?**  
A: They can see your code, but NOT your credentials or personal data.

**Q: What if I run out of minutes?**  
A: Very unlikely (~1,000/2,000 used). But you can reduce update frequency.

**Q: How reliable is it?**  
A: Very! GitHub has 99.9%+ uptime. Much more reliable than personal laptop.

**Q: Can I make the repository private?**  
A: Yes, but free Actions minutes are reduced. You'd need GitHub Pro ($4/month).

**Q: Can I use this for other automation?**  
A: Yes! GitHub Actions can run any script within the 2,000 minute limit.

---

## 🎊 Congratulations!

You're now running automated profile updates **24/7** without:
- ❌ NO credit card needed
- ❌ NO server management
- ❌ NO laptop running
- ❌ NO monthly costs

Just **completely FREE** automation! 🎉

**Happy job hunting!** 🚀


