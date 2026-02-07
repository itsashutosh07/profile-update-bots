# 🤖 Naukri Profile Update Bot

Automatically updates your Naukri.com profile every 2 hours using **GitHub Actions** - completely FREE and NO credit card required!

## ✨ Features

- ✅ **Automatic updates** every 2 hours
- ✅ **Free forever** (GitHub Actions)
- ✅ **No credit card** required
- ✅ **Screenshots** saved for verification
- ✅ **Secure** credential storage
- ✅ **Easy setup** (10 minutes)

---

## 🚀 Quick Setup (10 Minutes)

### Step 1: Prerequisites

You need:
- Free GitHub account (no credit card!)
- Your Naukri.com credentials
- 10 minutes

### Step 2: Follow the Setup Guide

📖 **Open**: [`GITHUB_ACTIONS_SETUP.md`](./GITHUB_ACTIONS_SETUP.md)

This guide includes:
- Step-by-step instructions with screenshots
- How to secure your credentials
- How to monitor your bot
- Troubleshooting tips
- FAQ

### Step 3: Done! ✅

Your profile will update automatically every 2 hours!

---

## 📁 Project Files

```
naukri/
├── update.py                      # Main automation script
├── requirements.txt               # Python dependencies
├── .env                          # Your credentials (DON'T upload to GitHub!)
├── .env.example                  # Template for credentials
├── .gitignore                    # Protects sensitive files
├── .github/
│   └── workflows/
│       └── update-profile.yml    # GitHub Actions workflow
├── README.md                     # This file
└── GITHUB_ACTIONS_SETUP.md       # Complete setup guide
```

---

## 🎯 How It Works

1. **GitHub Actions** runs on a schedule (every 2 hours)
2. **Chrome browser** logs into your Naukri account
3. **Script updates** your resume headline with keywords
4. **Screenshots** are saved for verification
5. **Repeat** automatically!

---

## 🔒 Security

Your credentials are stored as **GitHub Secrets**:
- ✅ Encrypted by GitHub
- ✅ Never visible in logs or code
- ✅ Only accessible to your workflows
- ✅ Cannot be read by anyone else

---

## 📊 Cost & Limits

| Resource | Limit | Usage | Status |
|----------|-------|-------|--------|
| **GitHub Actions** | 2,000 min/month | ~1,000 min/month | ✅ Plenty |
| **Storage** | 500MB | ~50MB | ✅ Plenty |
| **Cost** | $0 | $0 | ✅ FREE! |

---

## 🎛️ Management

### View Workflow Runs
1. Go to your repository on GitHub
2. Click "Actions" tab
3. See all runs with logs and screenshots

### Run Manually
1. Actions → Update Naukri Profile
2. Click "Run workflow"
3. Done!

### Pause Automation
1. Actions → Update Naukri Profile
2. Click "..." → Disable workflow

### Resume Automation
1. Actions → Update Naukri Profile
2. Click "..." → Enable workflow

---

## 🧪 Local Testing (Optional)

Want to test locally before deploying?

```bash
# Install dependencies
pip3 install -r requirements.txt

# Create .env file with your credentials
cp .env.example .env
nano .env  # Add your email and password

# Run once
python3 update.py
```

Screenshots will be saved in `Logs Screenshot/` folder.

---

## 📖 Documentation

| File | Purpose |
|------|---------|
| **GITHUB_ACTIONS_SETUP.md** | Complete setup guide (START HERE!) |
| **README.md** | This file - project overview |
| **.env.example** | Template for credentials |

---

## 🔧 Troubleshooting

### Workflow Fails

**Check the logs:**
1. Go to Actions tab
2. Click on failed workflow run
3. Review error messages

**Common issues:**
- Missing secrets (add `NAUKRI_EMAIL` and `NAUKRI_PASSWORD` in Settings → Secrets)
- Incorrect credentials (update secrets)
- Naukri website changes (check screenshots to see what happened)

### Can't Find Secrets

1. Go to your repository on GitHub
2. Click "Settings" tab
3. Secrets and variables → Actions
4. Add/update secrets here

### Workflow Not Running

- Make sure Actions are enabled (Actions tab)
- Check if workflow is disabled (re-enable it)
- Verify cron schedule is correct

---

## 💡 Tips

1. **Check weekly**: Review Actions tab to ensure updates are working
2. **Download screenshots**: Available for 7 days in Artifacts
3. **Monitor usage**: Check GitHub Actions usage in settings
4. **Update resume text**: Edit `update.py` line 100-102 to customize

---

## ⚙️ Configuration

### Change Update Interval

Edit `.github/workflows/update-profile.yml`:

```yaml
schedule:
  # Current: Every 2 hours
  - cron: '0 */2 * * *'
  
  # Every 3 hours
  - cron: '0 */3 * * *'
  
  # Every 4 hours
  - cron: '0 */4 * * *'
```

### Change Resume Headline Text

Edit `update.py` around line 100-102:

```python
updated_text = (
    "Your custom resume headline with keywords here"
)
```

---

## 📞 Need Help?

1. Read [`GITHUB_ACTIONS_SETUP.md`](./GITHUB_ACTIONS_SETUP.md) - detailed guide
2. Check troubleshooting section above
3. Review GitHub Actions logs for errors
4. Check screenshots to see what's happening

---

## 🎉 What You Get

Once deployed:
- ✅ Profile updates every 2 hours automatically
- ✅ Runs 24/7 without your laptop
- ✅ Screenshots saved with timestamps
- ✅ Detailed logs of each run
- ✅ Email notifications on failures
- ✅ Completely FREE forever
- ✅ NO credit card required

---

## 📝 License

MIT License - Feel free to use and modify!

---

## 🚀 Ready to Start?

**Open the setup guide and follow along:**

📖 **[GITHUB_ACTIONS_SETUP.md](./GITHUB_ACTIONS_SETUP.md)**

Takes only 10 minutes! 🎊

---

**Happy job hunting! 🤖**
