# Gmail API Setup Guide for OTP Auto-Reading

This guide will help you set up Gmail API to automatically read OTP codes from your email.

**Time Required**: ~15 minutes  
**Cost**: FREE

---

## 📋 Overview

The bot needs to:
1. Access your Gmail
2. Read emails from Naukri
3. Extract the OTP code
4. Enter it automatically

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

### 2.2 Create OAuth2 Client ID
1. Go to: https://console.cloud.google.com/apis/credentials
2. Click **"Create Credentials"** → **"OAuth client ID"**
3. Select **"Desktop app"** as application type
4. Name it: `Naukri Bot Desktop`
5. Click **"Create"**
6. **IMPORTANT**: Download the JSON file (click "Download JSON")
7. Note down:
   - **Client ID** (looks like: `xxxxx.apps.googleusercontent.com`)
   - **Client Secret** (random string)

---

## 🎫 Step 3: Get Refresh Token

We'll use a Python script to get your refresh token.

### 3.1 Install Required Package
```bash
pip install google-auth-oauthlib
```

### 3.2 Create Token Generator Script

Create a file `get_gmail_token.py`:

```python
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_refresh_token():
    # Replace these with YOUR credentials from Step 2
    client_config = {
        "installed": {
            "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
            "client_secret": "YOUR_CLIENT_SECRET",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"]
        }
    }
    
    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    creds = flow.run_local_server(port=0)
    
    print("\n" + "="*50)
    print("✅ SUCCESS! Your Gmail API credentials:")
    print("="*50)
    print(f"\nRefresh Token:\n{creds.refresh_token}")
    print(f"\nClient ID:\n{creds.client_id}")
    print(f"\nClient Secret:\n{creds.client_secret}")
    print("\n" + "="*50)
    print("\n💾 SAVE THESE! You'll need them for GitHub Secrets")
    print("="*50 + "\n")

if __name__ == '__main__':
    get_refresh_token()
```

### 3.3 Edit and Run the Script

1. **Open `get_gmail_token.py`**
2. **Replace** `YOUR_CLIENT_ID` and `YOUR_CLIENT_SECRET` with values from Step 2.2
3. **Run**:
   ```bash
   python3 get_gmail_token.py
   ```

4. **Browser will open**:
   - Select your Gmail account
   - Click **"Continue"** (ignore the "not verified" warning - it's your own app!)
   - Click **"Continue"** again to grant permissions
   - Browser will show "The authentication flow has completed"

5. **Copy the output** - you'll see:
   - ✅ Refresh Token (long string)
   - ✅ Client ID
   - ✅ Client Secret

**SAVE THESE SECURELY!**

---

## 🔐 Step 4: Add Secrets to GitHub

1. Go to your GitHub repository: https://github.com/itsashutosh07/profile-update-bots

2. Click **"Settings"** → **"Secrets and variables"** → **"Actions"**

3. Click **"New repository secret"** and add these **3 secrets**:

### Secret 1: GMAIL_CLIENT_ID
- **Name**: `GMAIL_CLIENT_ID`
- **Value**: `xxxxx.apps.googleusercontent.com` (from Step 3.3)
- Click **"Add secret"**

### Secret 2: GMAIL_CLIENT_SECRET
- **Name**: `GMAIL_CLIENT_SECRET`
- **Value**: Your client secret (from Step 3.3)
- Click **"Add secret"**

### Secret 3: GMAIL_REFRESH_TOKEN
- **Name**: `GMAIL_REFRESH_TOKEN`
- **Value**: Your refresh token (from Step 3.3)
- Click **"Add secret"**

---

## ✅ Step 5: Verify Setup

You should now have **5 secrets** in total:
- ✅ `NAUKRI_EMAIL`
- ✅ `NAUKRI_PASSWORD`
- ✅ `GMAIL_CLIENT_ID` (NEW)
- ✅ `GMAIL_CLIENT_SECRET` (NEW)
- ✅ `GMAIL_REFRESH_TOKEN` (NEW)

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

### Token Expired
- Refresh tokens don't expire unless:
  - You revoke access
  - You don't use it for 6 months
- If it expires, just re-run Step 3 to get a new one

---

## 🔒 Security Notes

1. ✅ **Refresh tokens are secure** - They only give read-only access to Gmail
2. ✅ **GitHub Secrets are encrypted** - They're never visible in logs
3. ✅ **Only you can access** - The app is in "Testing" mode with only your email as test user
4. ⚠️ **Never share** your Client Secret or Refresh Token
5. ⚠️ **Revoke access anytime** at: https://myaccount.google.com/permissions

---

## 🎉 You're Done!

Your bot can now:
- ✅ Automatically read OTP from Gmail
- ✅ Enter it on Naukri
- ✅ Update your profile every 2 hours

No more manual OTP entry needed! 🚀

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

