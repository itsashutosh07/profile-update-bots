#!/usr/bin/env python3
"""
Gmail API Token Generator
==========================
This script helps you get the OAuth2 refresh token for Gmail API access.

Instructions:
1. Install: pip install google-auth-oauthlib
2. Edit the client_id and client_secret below
3. Run: python3 get_gmail_token.py
4. Follow the browser prompts
5. Copy the output tokens to GitHub Secrets
"""

from google_auth_oauthlib.flow import InstalledAppFlow

# Gmail API scope - read-only access
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_refresh_token():
    """
    Generate OAuth2 refresh token for Gmail API.
    
    Replace YOUR_CLIENT_ID and YOUR_CLIENT_SECRET with your actual values
    from Google Cloud Console.
    """
    
    # ⚠️ IMPORTANT: Replace these with YOUR credentials
    # Get them from: https://console.cloud.google.com/apis/credentials
    client_config = {
        "installed": {
            "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
            "client_secret": "YOUR_CLIENT_SECRET",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"]
        }
    }
    
    # Check if user has replaced the placeholders
    if "YOUR_CLIENT_ID" in client_config["installed"]["client_id"]:
        print("\n" + "="*70)
        print("❌ ERROR: You need to edit this script first!")
        print("="*70)
        print("\n📝 Steps:")
        print("1. Open this file: get_gmail_token.py")
        print("2. Find the client_config section")
        print("3. Replace YOUR_CLIENT_ID with your actual Client ID")
        print("4. Replace YOUR_CLIENT_SECRET with your actual Client Secret")
        print("\n💡 Get credentials from:")
        print("   https://console.cloud.google.com/apis/credentials")
        print("\n📖 Full instructions in: GMAIL_API_SETUP.md")
        print("="*70 + "\n")
        return
    
    print("\n" + "="*70)
    print("🔐 Gmail API Token Generator")
    print("="*70)
    print("\n⚠️  IMPORTANT: Publish Your App First!")
    print("="*70)
    print("To make tokens last FOREVER (not expire after 7 days):")
    print("1. Go to: https://console.cloud.google.com/")
    print("2. Navigate to: APIs & Services → OAuth consent screen")
    print("3. Click 'PUBLISH APP' button")
    print("4. Confirm the prompt")
    print("\nWithout publishing, tokens expire after 7 days!")
    print("="*70)
    print("\n📋 This script will:")
    print("   1. Open your browser")
    print("   2. Ask you to log in to Gmail")
    print("   3. Request read-only access to your Gmail")
    print("   4. Generate tokens for the bot")
    print("\n⚠️  You may see 'App not verified' warning - that's normal!")
    print("   Click 'Advanced' → 'Go to [app name] (unsafe)' → 'Continue'")
    print("\n" + "="*70)
    input("\nPress Enter to continue...")
    
    try:
        # Start OAuth flow
        flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
        creds = flow.run_local_server(port=0)
        
        # Success!
        print("\n" + "="*70)
        print("✅ SUCCESS! Authentication completed!")
        print("="*70)
        print("\n📋 Your Gmail API Credentials:")
        print("=" *70)
        
        print("\n1️⃣  GMAIL_CLIENT_ID:")
        print("   " + creds.client_id)
        
        print("\n2️⃣  GMAIL_CLIENT_SECRET:")
        print("   " + creds.client_secret)
        
        print("\n3️⃣  GMAIL_REFRESH_TOKEN:")
        print("   " + creds.refresh_token)
        
        print("\n" + "="*70)
        print("💾 NEXT STEPS:")
        print("="*70)
        print("\n1. Copy the 3 values above")
        print("2. Go to: https://github.com/YOUR_USERNAME/YOUR_REPO/settings/secrets/actions")
        print("3. Click 'New repository secret'")
        print("4. Add these 3 secrets:")
        print("   - Name: GMAIL_CLIENT_ID")
        print("     Value: (paste the Client ID)")
        print("   - Name: GMAIL_CLIENT_SECRET")
        print("     Value: (paste the Client Secret)")
        print("   - Name: GMAIL_REFRESH_TOKEN")
        print("     Value: (paste the Refresh Token)")
        print("\n⚠️  KEEP THESE SECURE! Don't share them publicly.")
        print("="*70 + "\n")
        
        # Optionally save to a file (with strong security warning)
        print("\n" + "="*70)
        print("⚠️  SECURITY WARNING")
        print("="*70)
        print("Saving credentials to a file is a SECURITY RISK!")
        print("The file will contain sensitive tokens that could compromise your account.")
        print("Only save if you will DELETE the file immediately after use.")
        print("="*70)
        save = input("\n💾 Still want to save to 'gmail_credentials.txt'? (yes/NO): ").strip().lower()
        if save == 'yes':
            with open('gmail_credentials.txt', 'w') as f:
                f.write("# ⚠️  DELETE THIS FILE AFTER COPYING TO GITHUB SECRETS!\n")
                f.write("# DO NOT COMMIT THIS FILE TO GIT!\n")
                f.write("# DO NOT SHARE THIS FILE!\n")
                f.write("="*50 + "\n\n")
                f.write(f"GMAIL_CLIENT_ID={creds.client_id}\n")
                f.write(f"GMAIL_CLIENT_SECRET={creds.client_secret}\n")
                f.write(f"GMAIL_REFRESH_TOKEN={creds.refresh_token}\n")
            print("\n✅ Saved to: gmail_credentials.txt")
            print("🚨 CRITICAL: DELETE THIS FILE IMMEDIATELY AFTER COPYING!")
            print("⚠️  Check that gmail_credentials.txt is in .gitignore")
        
    except Exception as e:
        print("\n" + "="*70)
        print("❌ ERROR!")
        print("="*70)
        print(f"\n{str(e)}")
        print("\n💡 Common issues:")
        print("   - Client ID or Secret is wrong")
        print("   - Gmail API is not enabled")
        print("   - Your email is not added as test user")
        print("\n📖 See GMAIL_API_SETUP.md for detailed instructions")
        print("="*70 + "\n")


if __name__ == '__main__':
    get_refresh_token()

