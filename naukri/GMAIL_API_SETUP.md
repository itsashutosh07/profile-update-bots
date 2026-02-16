# Gmail API Setup Guide for OTP Auto-Reading

This guide will help you set up Gmail API to automatically read OTP codes from your email and **make your bot run indefinitely**.

**Time Required**: ~20 minutes  
**Cost**: FREE  
**Token Validity**: ⚡ **LIFETIME** (if you follow Step 2.3)

---

## 🚨 IMPORTANT: Make Your Tokens Last FOREVER

By default, Google OAuth apps in "Testing" mode have tokens that **expire after 7 days**. This guide will show you how to make them **last forever** by publishing your app. Don't worry - publishing is safe and keeps your credentials private!

**Without publishing:** Tokens expire after 7 days ❌  
**With publishing:** Tokens last forever ✅

---

## 📋 Overview

The bot needs to:
1. Access your Gmail (read-only)
2. Read emails from Naukri
3. Extract the OTP code
4. Enter it automatically
5. **Run indefinitely** without token expiration

### 🚀 Quick Summary for New Users

If you're cloning this project, here's what you'll do:

1. **Enable Gmail API** in Google Cloud Console (~5 min)
2. **Configure OAuth consent screen** (~5 min)
3. **⚡ Publish your app** to make tokens last forever (~1 min)
4. **Create OAuth credentials** (Client ID + Secret) (~2 min)
5. **Generate refresh token** using provided script (~5 min)
6. **Add 3 secrets to GitHub** (~2 min)
7. **Test and deploy** - Bot runs automatically! (~5 min)

**Total Time:** ~20-25 minutes for complete setup  
**Result:** Bot runs indefinitely, updating your Naukri profile 5x daily automatically

---

## 🔧 Step 1: Enable Gmail API

### 1.1 Go to Google Cloud Console
Visit: https://console.cloud.google.com/

### 1.2 Create a New Project
1. Click the project dropdown at the top
2. Click **"New Project"**
3. Name it: `Naukri Bot` (or any name)
4. Click **"Create"**
5. Wait for it to be created, then select it

### 1.3 Enable Gmail API
1. Go to: https://console.cloud.google.com/apis/library
2. Search for **"Gmail API"**
3. Click on it
4. Click **"Enable"**
5. Wait for it to enable (~30 seconds)

---

## 🔑 Step 2: Create OAuth2 Credentials

### 2.1 Configure OAuth Consent Screen
1. Go to: https://console.cloud.google.com/apis/credentials/consent
2. Select **"External"** user type
3. Click **"Create"**

4. Fill in required fields:
   - **App name**: `Naukri Profile Bot`
   - **User support email**: Your Gmail address
   - **Developer contact email**: Your Gmail address
5. Click **"Save and Continue"**

6. **Scopes** page: Click **"Add or Remove Scopes"**
   - Search for: `gmail.readonly`
   - Check: `https://www.googleapis.com/auth/gmail.readonly`
   - Click **"Update"**
   - Click **"Save and Continue"**

7. **Test users** page: Click **"Add Users"**
   - Enter your Gmail address (the one that receives OTP)
   - Click **"Add"**
   - Click **"Save and Continue"**

8. Review and click **"Back to Dashboard"**

### 2.2 Publish Your App (CRITICAL for Lifetime Tokens!)

🔥 **THIS STEP MAKES YOUR TOKENS LAST FOREVER!** 🔥

After configuring the OAuth consent screen, you need to publish your app to prevent token expiration.

1. On the OAuth consent screen page, you'll see your app status as **"Testing"**
2. Look for the **"PUBLISH APP"** button (usually at the top)
3. Click **"PUBLISH APP"**
4. You'll see a warning: *"Your app will be available to any user with a Google Account"*
   - **Don't panic!** This doesn't mean your app is publicly accessible
   - Only people with your Client ID + Client Secret + Refresh Token can use it
   - These credentials are safely stored in GitHub Secrets (encrypted)
5. Click **"Confirm"** to publish

**What Publishing Does:**
- ✅ Testing Mode: Tokens expire after 7 days
- ✅ Published Mode: Tokens **NEVER expire** (unless manually revoked)

**Is It Safe?**
- ✅ Your credentials remain private in GitHub Secrets
- ✅ No public website or app store listing is created
- ✅ Only YOU will use the app
- ✅ You can unpublish or revoke access anytime

**Do I Need Verification?**
- ❌ NO! Google may show a "verification required" notice
- This is only for apps distributed to 100+ users publicly
- For personal use, you can ignore it completely
- The app works perfectly without verification

**After publishing**, your app status will show **"In production"** or **"Published"**.

### 2.4 Create OAuth2 Client ID
1. Go to: https://console.cloud.google.com/apis/credentials
2. Click **"Create Credentials"** → **"OAuth client ID"**
3. Select **"Desktop app"** as application type
4. Name it: `Naukri Bot Desktop`
5. Click **"Create"**
6. A popup will show your credentials:
   - **Client ID** (looks like: `xxxxx.apps.googleusercontent.com`)
   - **Client Secret** (random string)
7. **Copy both values** - you'll need them in the next step
8. Optionally, click **"Download JSON"** to save them locally

---

## 🎫 Step 3: Generate Lifetime Refresh Token

Now we'll generate your refresh token using the provided script.

### 3.1 Install Required Package
```bash
pip install google-auth-oauthlib
```

### 3.2 Edit the Token Generator Script

1. **Navigate to the `naukri/` folder**:
   ```bash
   cd naukri
   ```

2. **Open `get_gmail_token.py`** in your editor

3. **Find this section** (around line 30-38):
   ```python
   client_config = {
       "installed": {
           "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
           "client_secret": "YOUR_CLIENT_SECRET",
           ...
       }
   }
   ```

4. **Replace the placeholders**:
   - Replace `YOUR_CLIENT_ID` with your actual Client ID from Step 2.4
   - Replace `YOUR_CLIENT_SECRET` with your actual Client Secret from Step 2.4

### 3.3 Run the Script

1. **Execute the script**:
   ```bash
   python3 get_gmail_token.py
   ```

2. **Read the important reminder** about publishing your app (if you haven't already)

3. **Press Enter** to continue

4. **Browser will automatically open**:
   - Select your Gmail account
   - You may see **"Google hasn't verified this app"** warning:
     - This is normal for personal projects
     - Click **"Advanced"**
     - Click **"Go to [your app name] (unsafe)"**
     - It's safe because it's YOUR app!
   - Click **"Continue"** to grant read-only Gmail access
   - Browser will show: "The authentication flow has completed"

5. **Copy the credentials from terminal**:
   ```
   ✅ SUCCESS! Your Gmail API Credentials:
   ====================================
   
   1️⃣  GMAIL_CLIENT_ID:
      xxxxx.apps.googleusercontent.com
   
   2️⃣  GMAIL_CLIENT_SECRET:
      xxxxxxxxxxxxx
   
   3️⃣  GMAIL_REFRESH_TOKEN:
      1//xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

6. **Optional**: The script will ask if you want to save to a file
   - Type `yes` only if you need a local backup
   - ⚠️ **DELETE** `gmail_credentials.txt` immediately after copying to GitHub Secrets!
   - The file is automatically gitignored for safety

**💾 SAVE THESE 3 VALUES SECURELY! You'll add them to GitHub in the next step.**

---

## 🔐 Step 4: Add Secrets to GitHub

Now we'll securely store your credentials in GitHub Secrets (encrypted storage).

### 4.1 Navigate to Repository Secrets

1. Go to your forked/cloned repository on GitHub
   - Example: `https://github.com/YOUR_USERNAME/profile-update-bot`
2. Click **"Settings"** tab (top navigation)
3. Click **"Secrets and variables"** → **"Actions"** (left sidebar)

### 4.2 Add the 3 Gmail Secrets

Click **"New repository secret"** for each of these:

#### Secret 1: GMAIL_CLIENT_ID
- **Name**: `GMAIL_CLIENT_ID` (must be exact, case-sensitive)
- **Value**: Paste your Client ID from Step 3.3
  - Format: `xxxxx.apps.googleusercontent.com`
- Click **"Add secret"**

#### Secret 2: GMAIL_CLIENT_SECRET
- **Name**: `GMAIL_CLIENT_SECRET` (must be exact, case-sensitive)
- **Value**: Paste your Client Secret from Step 3.3
  - Format: Random alphanumeric string
- Click **"Add secret"**

#### Secret 3: GMAIL_REFRESH_TOKEN
- **Name**: `GMAIL_REFRESH_TOKEN` (must be exact, case-sensitive)
- **Value**: Paste your Refresh Token from Step 3.3
  - Format: `1//xxxxxxxxxxxxxxxxxxxxx` (long string)
- Click **"Add secret"**

**🔒 Security Notes:**
- Secrets are encrypted by GitHub
- They're never visible in logs or output
- Only the workflow can access them
- You can update them anytime if compromised

---

## ✅ Step 5: Verify Setup

You should now have **5 secrets** in total:
- ✅ `NAUKRI_EMAIL` (your Naukri login email)
- ✅ `NAUKRI_PASSWORD` (your Naukri password)
- ✅ `GMAIL_CLIENT_ID` ← NEW
- ✅ `GMAIL_CLIENT_SECRET` ← NEW
- ✅ `GMAIL_REFRESH_TOKEN` ← NEW

All secret names must be **EXACTLY** as shown (case-sensitive).

---

## 🚀 Step 6: Test the Bot

1. Go to **Actions** tab in your GitHub repo
2. Click **"Update Naukri Profile"**
3. Click **"Run workflow"**
4. Wait and watch the logs

You should see:
```
[Gmail] Successfully connected to Gmail API
[OTP] OTP verification required!
[Gmail] Waiting for OTP email from naukri.com...
[Gmail] ✓ Found OTP: 123456
[OTP] OTP entered
[✓] OTP verification completed
[✓] Logged in
```

---

## 🔧 Troubleshooting

### "Missing Gmail credentials" Error
- Make sure all 3 Gmail secrets are added correctly
- Check for typos in secret names

### "Failed to get OTP from Gmail" Error
- Check that your Gmail is receiving OTP emails
- Verify the email is from `@naukri.com`
- The OTP email should arrive within 60 seconds

### "Gmail API has not been used" Error
- Make sure you enabled Gmail API in Step 1.3
- Wait a few minutes and try again

### "Access blocked: This app's request is invalid"
- Make sure you added your email as a test user in Step 2.1 (step 7)
- The OAuth consent screen must be configured correctly

### Token Expired Error

If you see `invalid_grant: Token has been expired or revoked`:

**Most Common Cause:** Your app is still in "Testing" mode
- **Solution:** Go back to Step 2.2 and publish your app
- Testing mode tokens expire after 7 days
- Published app tokens **last forever**

**Other Causes:**
- You manually revoked access at https://myaccount.google.com/permissions
- Token hasn't been used in 6+ months (rare, only for testing mode)
- Solution: Re-run Step 3 to generate a new token (after publishing!)

---

## 🔒 Security Notes

### What Access Does the Bot Have?
1. ✅ **Read-only Gmail access** - Cannot send, delete, or modify emails
2. ✅ **Scoped to specific API** - Only uses `gmail.readonly` scope
3. ✅ **GitHub Secrets are encrypted** - Never visible in logs or code
4. ✅ **No public exposure** - Publishing doesn't make your app "public"
5. ✅ **Only you control access** - Credentials stored securely in your GitHub account

### Is Publishing the App Safe?
**Yes! Here's why:**

- 🔒 **Not publicly listed**: Publishing doesn't create a public website or app store entry
- 🔒 **Private credentials**: Your Client ID + Secret + Refresh Token remain in GitHub Secrets
- 🔒 **No data sharing**: Only YOU can use these credentials
- 🔒 **Revocable anytime**: Disconnect at https://myaccount.google.com/permissions
- 🔒 **Read-only**: Bot can only read emails, not modify or delete them

**What "Published" actually means:**
- ❌ Does NOT mean: App is available to the public
- ✅ Actually means: Tokens don't expire after 7 days
- It's just Google's way of saying "production mode" vs "testing mode"

### Best Practices
1. ⚠️ **Never commit** `gmail_credentials.txt` to Git (already in `.gitignore`)
2. ⚠️ **Never share** your Client Secret or Refresh Token publicly
3. ✅ **Delete local files** after copying to GitHub Secrets
4. ✅ **Check secret names** are exact (case-sensitive)
5. ✅ **Publish your app** to avoid 7-day token expiration
6. ✅ **Monitor bot logs** regularly for any issues

### Revoking Access
If you ever want to revoke the bot's access:
1. Go to: https://myaccount.google.com/permissions
2. Find your app (e.g., "Naukri Profile Bot")
3. Click "Remove Access"
4. Delete the GitHub Secrets if you're done using the bot

---

## 🎉 You're Done!

Your bot is now fully configured and can run **indefinitely**! 🚀

✅ **Automatic OTP reading** from Gmail  
✅ **Lifetime tokens** (published app = no expiration)  
✅ **Scheduled updates** (5 times daily)  
✅ **No manual intervention** needed  
✅ **Secure credentials** in GitHub Secrets  

### What Happens Next?

The bot will automatically:
1. Run at scheduled times (5 AM, 8:30 AM, 11 AM, 2 PM, 5 PM IST)
2. Log in to Naukri
3. Request OTP
4. Read OTP from your Gmail (within 60 seconds)
5. Enter OTP and complete login
6. Update your profile headline
7. Log success/failure

**No more manual OTP entry needed!** Your profile stays active automatically.

---

## 📱 Alternative: Test Locally First

Before deploying to GitHub Actions, test locally:

1. Create `.env` file in `naukri/` folder:
```bash
NAUKRI_EMAIL=your_email@gmail.com
NAUKRI_PASSWORD=your_password
GMAIL_CLIENT_ID=your_client_id
GMAIL_CLIENT_SECRET=your_secret
GMAIL_REFRESH_TOKEN=your_refresh_token
```

2. Run locally:
```bash
cd naukri
python3 update.py
```

This way you can see if OTP reading works before pushing to GitHub!

---

## 📞 Need Help?

If you're stuck, check:
1. Gmail API is enabled
2. OAuth consent screen is configured
3. Your email is added as a test user
4. All 3 secrets are in GitHub
5. Secret names are EXACTLY as shown (case-sensitive)

Good luck! 🍀

