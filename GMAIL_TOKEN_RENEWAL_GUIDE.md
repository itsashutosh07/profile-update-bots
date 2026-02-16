# Gmail Token Renewal Guide 🔄

## Problem: Token Expired Error

```
[Gmail] Failed to get OTP: ('invalid_grant: Token has been expired or revoked.')
```

This happens when your Gmail API refresh token expires. In Google Cloud Projects set to **"Testing"** mode, refresh tokens expire after **7 days**.

---

## Solution: Publish Your App (Make Tokens Last Forever)

### Step 1: Move App from Testing to Production

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project (the one with Gmail API enabled)
3. Navigate to: **APIs & Services** → **OAuth consent screen**
4. You'll see your app status as "Testing" with a warning about 7-day token expiry
5. Click **"PUBLISH APP"** button
6. Confirm the prompt

**Important Notes:**
- You'll see a warning saying "Your app will be available to any user with a Google Account"
- **This is safe** because:
  - Your app doesn't have a public website
  - Only YOU will use the credentials
  - No one else can access your app without your Client ID/Secret
- Google may show a "verification required" notice, but you can ignore it for personal use
- Verification is only needed if you plan to distribute the app publicly

### Step 2: Regenerate Your Refresh Token

After publishing, you need to get a NEW refresh token:

#### Option A: Using the Helper Script (Recommended)

1. **Edit the script:**
   ```bash
   cd /Users/ashutoshmac/Work/Projects/profile-update-bot/naukri
   nano get_gmail_token.py  # or open in your editor
   ```

2. **Replace placeholders** with your actual credentials:
   ```python
   client_config = {
       "installed": {
           "client_id": "YOUR_ACTUAL_CLIENT_ID.apps.googleusercontent.com",
           "client_secret": "YOUR_ACTUAL_CLIENT_SECRET",
           # ... rest stays the same
       }
   }
   ```

   Get these from: [Google Cloud Credentials](https://console.cloud.google.com/apis/credentials)

3. **Install required package:**
   ```bash
   pip install google-auth-oauthlib
   ```

4. **Run the script:**
   ```bash
   python3 get_gmail_token.py
   ```

5. **Follow the prompts:**
   - Browser will open automatically
   - Log in to your Gmail account
   - You may see "App not verified" warning:
     - Click **"Advanced"**
     - Click **"Go to [app name] (unsafe)"**
     - Click **"Continue"**
   - Grant read-only Gmail access
   - Script will display your new tokens

#### Option B: Manual OAuth Flow

If the script doesn't work, use the [OAuth Playground](https://developers.google.com/oauthplayground/):

1. Go to: https://developers.google.com/oauthplayground/
2. Click the gear icon (⚙️) in top-right
3. Check "Use your own OAuth credentials"
4. Enter your Client ID and Client Secret
5. In Step 1, find and select: `https://www.googleapis.com/auth/gmail.readonly`
6. Click "Authorize APIs"
7. Log in and grant permissions
8. In Step 2, click "Exchange authorization code for tokens"
9. Copy the `refresh_token` value

### Step 3: Update GitHub Secrets

1. Go to your repository:
   ```
   https://github.com/itsashutosh07/profile-update-bots/settings/secrets/actions
   ```

2. Click on **GMAIL_REFRESH_TOKEN** secret
3. Click **"Update secret"**
4. Paste the new refresh token value
5. Click **"Update secret"** to save

**Optional:** If you regenerated Client ID/Secret, also update:
- `GMAIL_CLIENT_ID`
- `GMAIL_CLIENT_SECRET`

### Step 4: Test the Fix

Trigger a manual workflow run:

1. Go to: https://github.com/itsashutosh07/profile-update-bots/actions
2. Click "Update Naukri Profile" workflow
3. Click "Run workflow" button
4. Select branch: `main`
5. Click "Run workflow"
6. Wait 1-2 minutes and check the logs

---

## Verification Checklist ✅

- [ ] App status changed from "Testing" to "In Production" or "Published"
- [ ] New refresh token generated
- [ ] GitHub Secret `GMAIL_REFRESH_TOKEN` updated
- [ ] Test workflow run completed successfully
- [ ] Bot logs show: `[Gmail] Successfully connected to Gmail API`

---

## Why This Makes Tokens Last Forever

**Testing Mode:**
- Refresh tokens expire after **7 days**
- Need to regenerate tokens weekly
- Designed for development/testing

**Production Mode (Published):**
- Refresh tokens **never expire** (unless manually revoked)
- Token automatically refreshes on each use
- Designed for production applications

**Security:**
- Your credentials remain private in GitHub Secrets
- No one can access your Gmail without your specific Client ID + Secret + Refresh Token
- Publishing the app doesn't make it "public" - it just removes the 7-day token limit

---

## Troubleshooting

### Token Still Expiring?

- Make sure you clicked "PUBLISH APP" (not just "Make Public")
- Wait 5-10 minutes after publishing for changes to take effect
- Generate a NEW refresh token AFTER publishing

### "App not verified" Warning?

- This is normal for personal projects
- Click "Advanced" → "Go to [app name] (unsafe)"
- Google shows this because your app isn't formally verified (costs money)
- Safe to proceed since you're the only user

### Can't Find "Publish App" Button?

- Make sure you're on the OAuth consent screen page
- If you see "Verification required", you can ignore it for personal use
- The "Publish" button is usually at the top of the page

---

## Quick Reference: Token Regeneration (Future)

If you ever need to regenerate tokens again:

```bash
cd /Users/ashutoshmac/Work/Projects/profile-update-bot/naukri
python3 get_gmail_token.py
# Copy new GMAIL_REFRESH_TOKEN to GitHub Secrets
```

---

## Need Help?

- [Gmail API Documentation](https://developers.google.com/gmail/api/guides)
- [OAuth 2.0 Overview](https://developers.google.com/identity/protocols/oauth2)
- Check your bot logs: https://github.com/itsashutosh07/profile-update-bots/actions
