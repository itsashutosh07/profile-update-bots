#!/usr/bin/env python3
"""Smoke-test Gmail OTP listing (requires GMAIL_* vars in naukri/.env)."""
import os
import sys
import time
from datetime import datetime, timezone

from dotenv import load_dotenv

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(SCRIPT_DIR, ".env"))

from gmail_otp_reader import GmailOTPReader  # noqa: E402


def main():
    if not all(os.environ.get(k) for k in ("GMAIL_CLIENT_ID", "GMAIL_CLIENT_SECRET", "GMAIL_REFRESH_TOKEN")):
        print("Missing GMAIL_CLIENT_ID / GMAIL_CLIENT_SECRET / GMAIL_REFRESH_TOKEN in naukri/.env")
        sys.exit(1)

    reader = GmailOTPReader()
    since = time.time() - 24 * 3600
    result = reader.get_latest_otp(max_wait_seconds=20, min_received_after=since - 30)
    if not result:
        print("No Naukri OTP email found in the last 24 hours.")
        sys.exit(1)

    ts = datetime.fromtimestamp(result["internal_date_ms"] / 1000, tz=timezone.utc)
    print(f"Latest OTP: {result['otp']}")
    print(f"Message id: {result['message_id']}")
    print(f"Subject: {result['subject']}")
    print(f"Internal date (UTC): {ts.isoformat()}")


if __name__ == "__main__":
    main()
