# 🤖 Naukri.com Profile Update Bot

Automatically updates your Naukri.com profile daily at 6:00 AM IST using **GitHub Actions** - completely FREE and NO credit card required!

[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)]()
[![Platform](https://img.shields.io/badge/Platform-Naukri.com-blue)]()
[![Automation](https://img.shields.io/badge/Automation-100%25-success)]()
[![Dashboard](https://img.shields.io/badge/📊-View_Dashboard-667eea)](https://itsashutosh07.github.io/profile-update-bots/)

---

## ✨ Features

### 🤖 Full Automation
- ✅ **Automatic updates** once daily at 6:00 AM IST
- ✅ **OTP handling** via Gmail API (no manual intervention!)
- ✅ **Anti-bot detection** measures built-in
- ✅ **Rate limit handling** with graceful exits

### 💰 Free Forever
- ✅ **No credit card** required
- ✅ **GitHub Actions** (2000 free minutes/month)
- ✅ Uses only ~30-40 minutes/month
- ✅ **Zero hosting costs**

### 🔒 Secure & Private
- ✅ **Encrypted credentials** via GitHub Secrets
- ✅ **OAuth2** for Gmail (no password storage)
- ✅ **Read-only** Gmail access
- ✅ **No data collection**

### 📸 Monitoring & Debugging
- ✅ **Live Dashboard** - Real-time run status and history
- ✅ **Screenshots** at every step
- ✅ **Detailed logs** with timestamps
- ✅ **Error tracking** with full stack traces
- ✅ **Artifact storage** for 7 days

**🎯 [View Live Dashboard](https://itsashutosh07.github.io/profile-update-bots/)** - Monitor success rates, run history, and execution status

---

## 🚀 Quick Setup

### Prerequisites
- GitHub account (free)
- Gmail account (for OTP)
- Naukri.com account
- 20 minutes setup time

### Setup Guides (Choose One)

| Guide | Best For | Time | Difficulty |
|-------|----------|------|------------|
| [**QUICK_START_OTP.md**](QUICK_START_OTP.md) | Quick reference | 5 min | ⭐ |
| [**GMAIL_API_SETUP.md**](GMAIL_API_SETUP.md) | First-time setup | 20 min | ⭐⭐ |
| [**GITHUB_ACTIONS_SETUP.md**](GITHUB_ACTIONS_SETUP.md) | Detailed walkthrough | 30 min | ⭐⭐⭐ |

### 3-Step Setup

1. **Clone & Configure**
   ```bash
   git clone <your-repo-url>
   cd profile-update-bot/naukri
   ```

2. **Setup Gmail API** (for OTP)
   - Follow [GMAIL_API_SETUP.md](GMAIL_API_SETUP.md)
   - Get OAuth credentials
   - Run `get_gmail_token.py`

3. **Add GitHub Secrets**
   - `NAUKRI_EMAIL`
   - `NAUKRI_PASSWORD`
   - `NAUKRI_HEADLINE`
   - `GMAIL_CLIENT_ID`
   - `GMAIL_CLIENT_SECRET`
   - `GMAIL_REFRESH_TOKEN`

✅ **Done!** Your profile updates automatically!

---

## 📁 Project Structure

```
naukri/
├── update.py                      # Main automation script
├── gmail_otp_reader.py           # Gmail API OTP reader
├── get_gmail_token.py            # OAuth token generator
├── requirements.txt               # Python dependencies
│
├── README.md                      # This file
├── QUICK_START_OTP.md            # Quick reference guide
├── GMAIL_API_SETUP.md            # Gmail API setup tutorial
├── GITHUB_ACTIONS_SETUP.md       # Detailed GitHub Actions guide
├── GET_STARTED.md                # General getting started
│
└── .gitignore                     # Protected files
```

---

## 🎯 How It Works

### Execution Flow

```
┌─────────────────────────────────┐
│  GitHub Actions (Daily 6 AM IST)│
└─────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│  Launch Headless Chrome Browser │
└─────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│  Navigate to Naukri Login Page  │
│  • Enter email & password       │
│  • Anti-bot measures active     │
└─────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│  OTP Detection & Handling       │
│  • Detect OTP page              │
│  • Connect to Gmail API         │
│  • Read OTP from email          │
│  • Enter OTP automatically      │
└─────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│  Profile Update                 │
│  • Navigate to profile page     │
│  • Find Resume Headline section │
│  • Update with keywords         │
│  • Save changes                 │
└─────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│  Cleanup & Logging              │
│  • Save screenshots             │
│  • Upload artifacts             │
│  • Report success/failure       │
└─────────────────────────────────┘
```

### Schedule

**Runs once daily:**
- 00:30 UTC (06:00 AM IST)

**Why once daily?**
- Prevents OTP rate limiting
- Avoids account restrictions
- Still keeps profile active
- Manual trigger available anytime

---

## 🔒 Security Features

### Credential Protection
- All credentials stored as GitHub Secrets (encrypted)
- OAuth2 for Gmail (no password storage)
- No plain-text passwords in code or logs
- Credentials never visible in workflow logs

### Gmail API Permissions
- **Read-only** access to Gmail
- Cannot send emails
- Cannot delete emails
- Only reads OTP from Naukri

### Anti-Detection Measures
- Custom User-Agent strings
- Disables automation detection flags
- Removes webdriver property
- Natural timing and delays

---

## 📊 Cost & Usage

| Resource | Free Tier | Our Usage | Remaining |
|----------|-----------|-----------|-----------|
| **GitHub Actions** | 2000 min/month | ~30-40 min/month | ~1960 min |
| **Storage** | 500 MB | ~50 MB | ~450 MB |
| **Gmail API** | Free | Free forever | ∞ |
| **Total Cost** | $0 | $0 | **FREE** |

**Why This Works:**
- Each run: ~1.5 minutes
- 1 run/day × 30 days = 30 runs
- 30 runs × 1.5 min = 45 minutes/month
- **Well within free tier!** 🎉

---

## 🎛️ Management

### View Runs
```
GitHub Repo → Actions Tab → Update Naukri Profile
```

### Manual Trigger
```
Actions → Update Naukri Profile → Run workflow → Run workflow
```

### Check Screenshots
```
Click on run → Scroll to Artifacts → Download screenshots-*.zip
```

### Pause/Resume
```
Actions → Update Naukri Profile → ⋯ → Disable/Enable workflow
```

---

## 🧪 Local Testing

Test before deploying to GitHub Actions:

```bash
# Install dependencies
cd naukri
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
NAUKRI_EMAIL=your_email@gmail.com
NAUKRI_PASSWORD=your_password
NAUKRI_HEADLINE=your_resume_headline
GMAIL_CLIENT_ID=your_client_id
GMAIL_CLIENT_SECRET=your_secret
GMAIL_REFRESH_TOKEN=your_token
EOF

# Run locally
python3 update.py
```

Screenshots saved in: `Logs Screenshot/DD-MM-YY_HH-MM_AM/`

---

## 🔧 Configuration

### Change Update Frequency

Edit `.github/workflows/update-profile.yml`:

```yaml
schedule:
  # Current: Every 6 hours (4x daily)
  - cron: '0 */6 * * *'
  
  # Every 8 hours (3x daily)
  - cron: '0 */8 * * *'
  
  # Every 12 hours (2x daily)
  - cron: '0 */12 * * *'
  
  # Daily at 9 AM UTC
  - cron: '0 9 * * *'
```

⚠️ **Warning**: More frequent updates may trigger rate limits!

### Customize Profile Text

Edit `update.py` around line 342:

```python
updated_text = (
    "Your custom resume headline with keywords"
)
```

**Tips:**
- Include relevant keywords
- Keep it under 250 characters
- Update periodically for freshness

---

## 🔍 Troubleshooting

### Common Issues

#### 1. OTP Not Detected
**Symptoms**: Logs show "No OTP required" but OTP was sent

**Solution**:
- Check Gmail API credentials
- Verify all 3 Gmail secrets are added
- Ensure test user is configured in Google Cloud
- Check screenshots for actual page state

#### 2. Rate Limited
**Symptoms**: "Require OTP to login, but you have reached max limit"

**Solution**:
- **This is normal!** Bot handles it gracefully
- Wait 24 hours
- Reduce update frequency
- Don't manually test too often

#### 3. Login Fails
**Symptoms**: Still on login page after OTP

**Solution**:
- Verify `NAUKRI_EMAIL` and `NAUKRI_PASSWORD`
- Check if password has special characters (may need escaping)
- Review screenshot artifacts
- Try manual login to verify credentials

#### 4. Gmail API Errors
**Symptoms**: "Failed to retrieve OTP from Gmail"

**Solutions**:
- Refresh token expired → Regenerate using `get_gmail_token.py`
- Check Gmail API is enabled in Google Cloud Console
- Verify email is added as test user
- Check credential names match exactly

### Debug Steps

1. **Check workflow logs**
   ```
   Actions → Failed Run → Click on "update" job
   ```

2. **Download screenshots**
   ```
   Scroll to Artifacts → Download screenshots-*.zip
   ```

3. **Verify secrets**
   ```
   Settings → Secrets and variables → Actions
   Should have 6 secrets total
   ```

4. **Test locally**
   ```bash
   python3 update.py
   ```

---

## 📖 Documentation Index

| Document | Purpose | When to Read |
|----------|---------|--------------|
| [README.md](README.md) | Overview & reference | Always |
| [QUICK_START_OTP.md](QUICK_START_OTP.md) | Fast setup guide | After first setup |
| [GMAIL_API_SETUP.md](GMAIL_API_SETUP.md) | Gmail API tutorial | First time setup |
| [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) | Complete walkthrough | Beginners |
| [GET_STARTED.md](GET_STARTED.md) | General guide | Optional |

---

## 🎯 Success Metrics

Once properly configured, you should see:

- ✅ **95%+ success rate** on workflow runs
- ✅ **Profile last updated** within 6 hours on Naukri
- ✅ **OTP handled automatically** (no manual intervention)
- ✅ **Screenshots** showing successful profile updates
- ✅ **Zero failures** due to rate limiting (handles gracefully)

---

## 💡 Pro Tips

1. **Don't Over-Test**: Manual testing triggers OTP limits
2. **Check Weekly**: Review Actions tab once a week
3. **Monitor Gmail**: Ensure OTP emails are coming through
4. **Update Keywords**: Refresh resume text monthly
5. **Download Logs**: Save artifacts before they expire (7 days)

---

## 🚨 Known Limitations

- **OTP Rate Limit**: Naukri limits OTP requests (handled gracefully)
- **Manual OTP**: Can't handle SMS OTP (only email)
- **Session Duration**: Must re-login each time (no session storage)
- **Single Account**: One bot per GitHub repo/account

---

## 🔄 What Gets Updated

Currently updates:
- ✅ **Resume Headline**: Main profile summary

**Future Plans**:
- 📋 Profile summary
- 📋 Skills section
- 📋 Last active timestamp
- 📋 Resume file (re-upload)

---

## 📞 Support

### Get Help

1. **Read Documentation**: Check guides above
2. **Review Logs**: Actions tab has detailed logs
3. **Check Screenshots**: Download artifacts to see visual state
4. **GitHub Issues**: Report bugs or request features

### Useful Links

- 📖 [Parent Project README](../README.md)
- 🐛 [Report Issue](../../issues)
- 💬 [Discussions](../../discussions)
- 📧 Email: your.email@example.com

---

## 🎉 Success Stories

Once deployed successfully:
- Increases profile visibility
- Appears in "recently active" searches
- Higher recruiter engagement
- Zero manual effort required

---

## 📝 Changelog

### v2.0 (Current)
- ✅ Gmail API OTP automation
- ✅ Rate limit handling
- ✅ Improved error logging
- ✅ Reduced frequency (6 hours)

### v1.0
- ✅ Basic automation
- ✅ GitHub Actions integration
- ✅ Screenshot logging

---

## ⚖️ License

MIT License - See [LICENSE](../LICENSE) for details.

---

## 🙏 Credits

- Selenium WebDriver
- Google Gmail API
- GitHub Actions
- All contributors

---

## ⚠️ Disclaimer

**For educational and personal use only.**

- ✅ Use responsibly
- ✅ Follow Naukri's Terms of Service
- ✅ Don't spam or abuse
- ⚠️ Use at your own risk

**Authors not responsible for account restrictions.**

---

<div align="center">

**Ready to automate your profile?**

Start with: [QUICK_START_OTP.md](QUICK_START_OTP.md)

---

[⬆ Back to Top](#-naukricom-profile-update-bot) | [🏠 Main README](../README.md)

</div>
