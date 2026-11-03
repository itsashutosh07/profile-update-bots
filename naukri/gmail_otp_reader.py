import os
import re
import time
import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

NAUKRI_OTP_SUBJECT_HINT = "otp for logging in naukri"


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
        client_id = os.environ.get("GMAIL_CLIENT_ID")
        client_secret = os.environ.get("GMAIL_CLIENT_SECRET")
        refresh_token = os.environ.get("GMAIL_REFRESH_TOKEN")

        if not all([client_id, client_secret, refresh_token]):
            raise ValueError(
                "Missing Gmail credentials! Required: "
                "GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET, GMAIL_REFRESH_TOKEN"
            )

        self.creds = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret,
            scopes=["https://www.googleapis.com/auth/gmail.readonly"],
        )

        if self.creds.expired or not self.creds.valid:
            self.creds.refresh(Request())

        self.service = build("gmail", "v1", credentials=self.creds)
        print("[Gmail] Successfully connected to Gmail API")

    def get_latest_otp(
        self,
        sender_filter="naukri.com",
        max_wait_seconds=60,
        min_received_after=None,
        exclude_message_ids=None,
    ):
        """
        Fetch the newest OTP from Gmail for the current login attempt.

        Args:
            sender_filter: Email domain to filter by (e.g. "naukri.com")
            max_wait_seconds: Maximum time to wait for OTP email
            min_received_after: Unix epoch seconds; ignore older messages
            exclude_message_ids: Message IDs already used this run

        Returns:
            dict with keys otp, message_id, subject, internal_date_ms — or None
        """
        print(f"[Gmail] Waiting for OTP email from {sender_filter}...")
        if min_received_after:
            print(
                f"[Gmail] Only considering emails after "
                f"{time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(min_received_after))}"
            )

        exclude_message_ids = set(exclude_message_ids or [])
        start_time = time.time()

        while time.time() - start_time < max_wait_seconds:
            try:
                after_clause = ""
                if min_received_after:
                    after_clause = f" after:{int(min_received_after)}"

                queries = [
                    f"from:@{sender_filter} subject:OTP{after_clause}",
                    f"from:info@naukri.com subject:OTP{after_clause}",
                    f"(from:@{sender_filter} OR from:naukri) subject:OTP{after_clause}",
                    f"from:@{sender_filter}{after_clause}",
                ]

                messages = []
                seen_ids = set()
                for query in queries:
                    results = (
                        self.service.users()
                        .messages()
                        .list(userId="me", q=query, maxResults=15)
                        .execute()
                    )
                    for item in results.get("messages", []):
                        mid = item["id"]
                        if mid in seen_ids or mid in exclude_message_ids:
                            continue
                        seen_ids.add(mid)
                        messages.append(item)

                if not messages:
                    print("[Gmail] No matching messages yet, waiting...")
                    time.sleep(5)
                    continue

                candidates = []
                for message in messages:
                    msg_id = message["id"]
                    msg = (
                        self.service.users()
                        .messages()
                        .get(
                            userId="me",
                            id=msg_id,
                            format="full",
                        )
                        .execute()
                    )

                    internal_date_ms = int(msg.get("internalDate", 0))
                    if min_received_after and internal_date_ms / 1000.0 < min_received_after - 5:
                        continue

                    subject = self._header_value(msg, "Subject")
                    body = self._get_email_body(msg)
                    snippet = msg.get("snippet", "")
                    otp = self._extract_otp(body) or self._extract_otp(snippet)
                    if not otp:
                        continue

                    subject_l = (subject or "").lower()
                    priority = 0
                    if NAUKRI_OTP_SUBJECT_HINT in subject_l:
                        priority = 2
                    elif "otp" in subject_l:
                        priority = 1

                    candidates.append(
                        {
                            "otp": otp,
                            "message_id": msg_id,
                            "subject": subject,
                            "internal_date_ms": internal_date_ms,
                            "priority": priority,
                        }
                    )

                if candidates:
                    candidates.sort(
                        key=lambda c: (c["priority"], c["internal_date_ms"]),
                        reverse=True,
                    )
                    best = candidates[0]
                    print(
                        f"[Gmail] ✓ Found OTP: {best['otp']} "
                        f"(message {best['message_id'][:8]}…, subject: {best['subject']!r})"
                    )
                    return best

                print("[Gmail] Messages found but no OTP extracted yet, waiting...")
                time.sleep(5)

            except Exception as e:
                print(f"[Gmail] Error reading emails: {str(e)}")
                time.sleep(5)

        print("[Gmail] ✗ Timeout waiting for OTP")
        return None

    @staticmethod
    def _header_value(message, name):
        headers = message.get("payload", {}).get("headers", [])
        for header in headers:
            if header.get("name", "").lower() == name.lower():
                return header.get("value", "")
        return ""

    def _get_email_body(self, message):
        """Extract plain or HTML email body from message."""
        try:
            payload = message.get("payload", {})

            def decode_part(part):
                data = part.get("body", {}).get("data")
                if not data:
                    return ""
                return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")

            if "parts" in payload:
                for part in payload["parts"]:
                    mime = part.get("mimeType", "")
                    if mime == "text/plain":
                        text = decode_part(part)
                        if text.strip():
                            return text
                for part in payload["parts"]:
                    if part.get("mimeType") == "text/html":
                        html = decode_part(part)
                        if html.strip():
                            return re.sub(r"<[^>]+>", " ", html)

            if "body" in payload and "data" in payload["body"]:
                return decode_part(payload)

            return message.get("snippet", "")

        except Exception as e:
            print(f"[Gmail] Error extracting body: {str(e)}")
            return message.get("snippet", "")

    def _extract_otp(self, text):
        """Extract OTP code from email text using various patterns."""
        if not text:
            return None

        patterns = [
            r"OTP\s*(?:is|:)?\s*(\d{4,6})",
            r"(?:verification|confirm(?:ation)?)\s*code\s*(?:is|:)?\s*(\d{4,6})",
            r"(\d{4,6})\s*is\s*your\s*(?:OTP|code)",
            r"code\s*(?:is|:)?\s*(\d{4,6})",
            r"(?:one[- ]time|temporary)\s*(?:password|code)\s*(?:is|:)?\s*(\d{4,6})",
            r"Please enter below OTP[^\d]*(\d{4,6})",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                otp = match.group(1)
                if 4 <= len(otp) <= 6 and otp.isdigit():
                    return otp

        match = re.search(r"(?<!\d)(\d{6})(?!\d)", text)
        if match:
            return match.group(1)

        return None


def get_otp_from_gmail(
    sender_filter="naukri.com",
    max_wait_seconds=60,
    min_received_after=None,
    exclude_message_ids=None,
):
    """
    Convenience function to get OTP from Gmail.

    Returns:
        dict with otp, message_id, subject, internal_date_ms — or None on failure
    """
    try:
        reader = GmailOTPReader()
        return reader.get_latest_otp(
            sender_filter=sender_filter,
            max_wait_seconds=max_wait_seconds,
            min_received_after=min_received_after,
            exclude_message_ids=exclude_message_ids,
        )
    except Exception as e:
        print(f"[Gmail] Failed to get OTP: {str(e)}")
        return None
