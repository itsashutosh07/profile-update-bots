import os
import re
import time
import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

class GmailOTPReader:
    """
    Reads OTP from Gmail using Gmail API.
    Requires OAuth2 credentials stored as environment variables.
    """
    
    def __init__(self):
        self.creds = None
        self.service = None
        self._setup_credentials()
    
    def _setup_credentials(self):
        """Setup Gmail API credentials from environment variables."""
        # Get credentials from environment
        client_id = os.environ.get('GMAIL_CLIENT_ID')
        client_secret = os.environ.get('GMAIL_CLIENT_SECRET')
        refresh_token = os.environ.get('GMAIL_REFRESH_TOKEN')
        
        if not all([client_id, client_secret, refresh_token]):
            raise ValueError(
                "Missing Gmail credentials! Required: "
                "GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET, GMAIL_REFRESH_TOKEN"
            )
        
        # Create credentials object
        self.creds = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=client_id,
            client_secret=client_secret,
            scopes=['https://www.googleapis.com/auth/gmail.readonly']
        )
        
        # Refresh the token if needed
        if self.creds.expired or not self.creds.valid:
            self.creds.refresh(Request())
        
        # Build the Gmail service
        self.service = build('gmail', 'v1', credentials=self.creds)
        print("[Gmail] Successfully connected to Gmail API")
    
    def get_latest_otp(self, sender_filter="naukri.com", max_wait_seconds=60):
        """
        Fetch the latest OTP from Gmail.
        
        Args:
            sender_filter: Email domain to filter by (e.g., "naukri.com")
            max_wait_seconds: Maximum time to wait for OTP email
        
        Returns:
            str: The OTP code, or None if not found
        """
        print(f"[Gmail] Waiting for OTP email from {sender_filter}...")
        
        start_time = time.time()
        
        while time.time() - start_time < max_wait_seconds:
            try:
                # Search for recent emails from Naukri
                query = f'from:@{sender_filter} newer_than:2m'
                results = self.service.users().messages().list(
                    userId='me',
                    q=query,
                    maxResults=5
                ).execute()
                
                messages = results.get('messages', [])
                
                if not messages:
                    print("[Gmail] No new messages yet, waiting...")
                    time.sleep(5)
                    continue
                
                # Check each message for OTP
                for message in messages:
                    msg_id = message['id']
                    msg = self.service.users().messages().get(
                        userId='me',
                        id=msg_id,
                        format='full'
                    ).execute()
                    
                    # Get email body
                    body = self._get_email_body(msg)
                    
                    # Extract OTP using regex patterns
                    otp = self._extract_otp(body)
                    
                    if otp:
                        print(f"[Gmail] ✓ Found OTP: {otp}")
                        return otp
                
                print("[Gmail] OTP not found in recent emails, waiting...")
                time.sleep(5)
                
            except Exception as e:
                print(f"[Gmail] Error reading emails: {str(e)}")
                time.sleep(5)
        
        print("[Gmail] ✗ Timeout waiting for OTP")
        return None
    
    def _get_email_body(self, message):
        """Extract email body from message."""
        try:
            # Try to get the plain text body
            if 'parts' in message['payload']:
                parts = message['payload']['parts']
                for part in parts:
                    if part['mimeType'] == 'text/plain':
                        data = part['body'].get('data')
                        if data:
                            return base64.urlsafe_b64decode(data).decode('utf-8')
            
            # If no parts, try direct body
            if 'body' in message['payload'] and 'data' in message['payload']['body']:
                data = message['payload']['body']['data']
                return base64.urlsafe_b64decode(data).decode('utf-8')
            
            # Try snippet as fallback
            return message.get('snippet', '')
            
        except Exception as e:
            print(f"[Gmail] Error extracting body: {str(e)}")
            return message.get('snippet', '')
    
    def _extract_otp(self, text):
        """
        Extract OTP code from email text using various patterns.
        
        Common patterns:
        - "OTP is 123456"
        - "Your OTP: 123456"
        - "verification code is 123456"
        - "123456 is your OTP"
        """
        if not text:
            return None
        
        # List of regex patterns to try
        patterns = [
            r'OTP\s*(?:is|:)?\s*(\d{4,6})',  # OTP is 123456
            r'(?:verification|confirm(?:ation)?)\s*code\s*(?:is|:)?\s*(\d{4,6})',  # verification code is 123456
            r'(\d{4,6})\s*is\s*your\s*(?:OTP|code)',  # 123456 is your OTP
            r'code\s*(?:is|:)?\s*(\d{4,6})',  # code: 123456
            r'(?:one[- ]time|temporary)\s*(?:password|code)\s*(?:is|:)?\s*(\d{4,6})',  # one-time password is 123456
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        # Last resort: find any 6-digit number (be careful with this)
        match = re.search(r'\b(\d{6})\b', text)
        if match:
            return match.group(1)
        
        return None


# Convenience function for easy import
def get_otp_from_gmail(sender_filter="naukri.com", max_wait_seconds=60):
    """
    Convenience function to get OTP from Gmail.
    
    Usage:
        otp = get_otp_from_gmail()
    """
    try:
        reader = GmailOTPReader()
        return reader.get_latest_otp(sender_filter, max_wait_seconds)
    except Exception as e:
        print(f"[Gmail] Failed to get OTP: {str(e)}")
        return None

