# ⚡ Quick Start: Gmail OTP Setup

Your bot can now automatically read OTP from Gmail! Follow these steps:

---

## 📝 What You Need to Do

### Step 1: Get Gmail API Credentials (15 minutes)

Follow the detailed guide: **[GMAIL_API_SETUP.md](GMAIL_API_SETUP.md)**

**Quick summary:**
1. Enable Gmail API in Google Cloud Console
2. Create OAuth2 credentials
3. Run `get_gmail_token.py` to get your tokens
4. Add 3 secrets to GitHub

---

### Step 2: Add GitHub Secrets

Go to: https://github.com/itsashutosh07/profile-update-bots/settings/secrets/actions

Add these **3 NEW secrets**:

| Secret Name | Where to Get It |
|------------|-----------------|
| `GMAIL_CLIENT_ID` | From `get_gmail_token.py` output |
| `GMAIL_CLIENT_SECRET` | From `get_gmail_token.py` output |
| `GMAIL_REFRESH_TOKEN` | From `get_gmail_token.py` output |

You should have **5 total secrets**:
- ✅ NAUKRI_EMAIL (existing)
- ✅ NAUKRI_PASSWORD (existing)
- 🆕 GMAIL_CLIENT_ID (new)
- 🆕 GMAIL_CLIENT_SECRET (new)
- 🆕 GMAIL_REFRESH_TOKEN (new)

---

### Step 3: Test the Bot

1. Go to **Actions** tab: https://github.com/itsashutosh07/profile-update-bots/actions
2. Click **"Update Naukri Profile"**
3. Click **"Run workflow"**
4. Watch the logs - you should see:
   ```
   [Gmail] Successfully connected to Gmail API
   [OTP] OTP verification required!
   [Gmail] ✓ Found OTP: 123456
   [✓] OTP verification completed
   ```

---

## 🔧 Test Locally First (Recommended)

Before using GitHub Actions, test on your laptop:

### 1. Install dependencies:
```bash
cd naukri
pip install -r requirements.txt
```

### 2. Create `.env` file:
```bash
NAUKRI_EMAIL=7.ashutoshj@gmail.com
NAUKRI_PASSWORD=Qwer!yu7890
GMAIL_CLIENT_ID=your_client_id_here
GMAIL_CLIENT_SECRET=your_secret_here
GMAIL_REFRESH_TOKEN=your_refresh_token_here
```

### 3. Run the bot:
```bash
python3 update.py
```

---

## 📚 Files Added

| File | Purpose |
|------|---------|
| `gmail_otp_reader.py` | Module to read OTP from Gmail |
| `get_gmail_token.py` | Helper script to get OAuth tokens |
| `GMAIL_API_SETUP.md` | Detailed setup instructions |
| `QUICK_START_OTP.md` | This file - quick reference |

---

## 🎯 How It Works

```
1. Bot logs in to Naukri
   ↓
2. Naukri asks for OTP
   ↓
3. Bot connects to Gmail API
   ↓
4. Bot reads latest email from naukri.com
   ↓
5. Bot extracts OTP code
   ↓
6. Bot enters OTP automatically
   ↓
7. Bot updates your profile
   ✅ Done!
```

---

## ⏱️ Time Estimates

- ✅ Read this file: **2 minutes**
- ✅ Gmail API setup: **15 minutes** ([GMAIL_API_SETUP.md](GMAIL_API_SETUP.md))
- ✅ Add secrets to GitHub: **2 minutes**
- ✅ Test run: **2 minutes**

**Total: ~20 minutes** for full automation! 🚀

---

## 🆘 Need Help?

1. **Setup Issues**: See [GMAIL_API_SETUP.md](GMAIL_API_SETUP.md) Troubleshooting section
2. **Can't get token**: Make sure you added your email as a test user
3. **OTP not detected**: Check logs for `[OTP]` messages
4. **Gmail connection fails**: Verify all 3 secrets are in GitHub

---

## 🔒 Is This Safe?

✅ **YES!**
- Refresh token only gives **read-only** access to Gmail
- It can't send emails or delete anything
- GitHub Secrets are encrypted
- You can revoke access anytime at: https://myaccount.google.com/permissions

---

## 🎉 Ready?

**Start here**: [GMAIL_API_SETUP.md](GMAIL_API_SETUP.md)

Good luck! 🍀

