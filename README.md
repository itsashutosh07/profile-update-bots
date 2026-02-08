# 🤖 Profile Update Bot

**Automated profile management for job portals** - Keep your profile active and visible to recruiters 24/7 without manual intervention.

[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue)](https://github.com/features/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Live Dashboard](https://img.shields.io/badge/📊_Live-Dashboard-667eea?style=for-the-badge)](https://itsashutosh07.github.io/profile-update-bots/)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Dashboard](#dashboard)
- [Currently Supported Platforms](#currently-supported-platforms)
- [Key Features](#key-features)
- [How It Works](#how-it-works)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Future Roadmap](#future-roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

Profile Update Bot is an intelligent automation solution that keeps your job portal profiles fresh and active. By automatically updating your profile at regular intervals, you increase visibility to recruiters and stay at the top of search results.

### Why This Matters

- **Algorithmic Priority**: Job portals prioritize recently active profiles in recruiter searches
- **Increased Visibility**: Regular updates keep your profile appearing in "recently updated" sections
- **Time-Saving**: Set it once, forget about it - runs automatically
- **Professional Presence**: Maintains an active, engaged profile without manual effort

---

## 📊 Dashboard

**Monitor your automation in real-time!**

A beautiful, minimal dashboard to track workflow runs, success rates, and execution history.

[![View Live Dashboard](https://img.shields.io/badge/📊_View-Live_Dashboard-667eea?style=for-the-badge)](https://itsashutosh07.github.io/profile-update-bots/)

### Features
- ✅ Real-time workflow status with detailed error messages
- 📈 Success rate statistics
- 🕐 Run history with flip-card UI
- 📱 Mobile-friendly responsive design
- 🌙 Dark mode with Naukri branding
- 🔄 Manual refresh with API rate limit tracking
- 🔗 Direct links to specific job logs
- 🎨 Satoshi font • Professional UI

**Tech**: Pure HTML/CSS/JS • No backend • GitHub API • GitHub Pages

📚 **Setup Guide**: See [`dashboard/SETUP.md`](dashboard/SETUP.md) for deployment instructions

---

## 🌐 Currently Supported Platforms

### ✅ Naukri.com (Production Ready)

Full automation support with:
- ✅ Automatic login with credentials
- ✅ OTP handling via Gmail API
- ✅ Profile headline updates
- ✅ Rate limit detection and handling
- ✅ Scheduled runs (once daily at 6:00 AM IST)
- ✅ Screenshot logging for debugging
- ✅ Error handling and recovery

**Status**: ⭐ Fully Operational

📚 **Documentation**: See [`naukri/README.md`](naukri/README.md) for detailed setup

---

## ✨ Key Features

### 🔐 Security First
- Credentials stored as encrypted GitHub Secrets
- OAuth2 authentication for Gmail API
- No plain-text passwords in code
- Read-only Gmail access

### 🤖 Fully Automated
- Runs on GitHub Actions (100% free)
- No server or hosting costs
- Scheduled execution (every 6 hours)
- Manual trigger option available

### 🛡️ Robust & Reliable
- Anti-bot detection measures
- Rate limit handling
- Automatic OTP reading from email
- Comprehensive error logging
- Screenshot artifacts for debugging

### 📊 Monitoring & Logging
- Detailed execution logs
- Screenshot captures at each step
- Error tracking with stack traces
- Success/failure notifications

---

## 🔄 How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Actions Workflow                  │
│                (Runs Daily at 6:00 AM IST)                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 1: Launch Headless Browser (Chrome)                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 2: Navigate to Job Portal & Login                     │
│  • Enter credentials from GitHub Secrets                     │
│  • Handle anti-bot detection                                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 3: OTP Verification (if required)                     │
│  • Detect OTP page                                           │
│  • Connect to Gmail API                                      │
│  • Read OTP from email                                       │
│  • Enter OTP automatically                                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 4: Update Profile                                     │
│  • Navigate to profile section                               │
│  • Modify profile fields                                     │
│  • Save changes                                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 5: Cleanup & Logging                                  │
│  • Save screenshots as artifacts                             │
│  • Close browser                                             │
│  • Report success/failure                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- GitHub account (free)
- Gmail account (for OTP reading)
- Account on target job portal (e.g., Naukri.com)

### Setup Time: ~20 minutes

1. **Clone this repository**
   ```bash
   git clone https://github.com/yourusername/profile-update-bot.git
   cd profile-update-bot
   ```

2. **Choose your platform**
   ```bash
   cd naukri  # Currently the only supported platform
   ```

3. **Follow platform-specific setup**
   - For Naukri: See [`naukri/QUICK_START_OTP.md`](naukri/QUICK_START_OTP.md)
   - Detailed guide: [`naukri/GMAIL_API_SETUP.md`](naukri/GMAIL_API_SETUP.md)

4. **Configure GitHub Actions**
   - Add secrets to your repository
   - Enable GitHub Actions
   - Workflow runs automatically!

### Run Schedule

- **Frequency**: Once daily
- **Time**: 6:00 AM IST (12:30 AM UTC)
- **Manual trigger**: Available anytime via Actions tab
- **Why once daily?**: Prevents rate limiting and account restrictions

---

## 📁 Project Structure

```
profile-update-bot/
├── README.md                          # This file
├── LICENSE                            # MIT License
│
├── naukri/                            # Naukri.com automation
│   ├── README.md                      # Naukri-specific documentation
│   ├── update.py                      # Main bot script
│   ├── gmail_otp_reader.py           # Gmail API OTP reader
│   ├── requirements.txt               # Python dependencies
│   │
│   ├── GET_STARTED.md                 # Quick start guide
│   ├── GMAIL_API_SETUP.md            # Gmail API setup tutorial
│   ├── QUICK_START_OTP.md            # OTP setup quick reference
│   ├── GITHUB_ACTIONS_SETUP.md       # GitHub Actions configuration
│   │
│   └── get_gmail_token.py            # OAuth token generator
│
├── .github/
│   └── workflows/
│       └── update-profile.yml         # GitHub Actions workflow
│
└── instahyre/                         # 🚧 Coming Soon
    └── README.md                      # Instahyre automation (planned)
```

---

## 🗺️ Future Roadmap

### 🚧 Planned Platforms

| Platform | Status | Priority | ETA |
|----------|--------|----------|-----|
| **Naukri.com** | ✅ Complete | - | Live |
| **Instahire** | 📋 Planned | High | Q2 2026 |
| **LinkedIn** | 💡 Exploring | Medium | Q3 2026 |
| **Indeed** | 💡 Exploring | Medium | Q3 2026 |
| **Monster** | 📋 Planned | Low | Q4 2026 |
| **Glassdoor** | 💡 Exploring | Low | TBD |

### 🔮 Upcoming Features

#### v2.0 - Multi-Platform Support
- [ ] Instahyre.com integration
- [ ] Unified configuration system
- [ ] Cross-platform scheduling
- [ ] Consolidated reporting

#### v2.1 - Enhanced Automation
- [ ] Multiple profile update strategies
- [ ] A/B testing different headlines
- [ ] Smart scheduling based on recruiter activity
- [ ] Profile analytics and insights

#### v2.2 - Intelligence Layer
- [ ] AI-generated profile updates
- [ ] Keyword optimization based on job trends
- [ ] Automatic skill section updates
- [ ] Resume parsing and suggestions

#### v3.0 - Enterprise Features
- [ ] Multi-user support
- [ ] Team dashboards
- [ ] Custom scheduling rules
- [ ] Webhook notifications
- [ ] Slack/Discord integration

### 🎯 Why Instahyre Next?

1. **High ROI**: Instahyre targets experienced professionals (higher value roles)
2. **Cleaner Interface**: Easier automation compared to other platforms
3. **Active User Base**: Growing platform with engaged recruiters
4. **Similar Architecture**: Profile update mechanisms similar to Naukri

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Ways to Contribute

1. **Add New Platforms**
   - Create a new folder (e.g., `instahyre/`)
   - Follow the structure from `naukri/`
   - Submit a pull request

2. **Improve Existing Bots**
   - Enhance error handling
   - Add new features
   - Fix bugs
   - Improve documentation

3. **Documentation**
   - Write tutorials
   - Create video guides
   - Translate to other languages

4. **Testing**
   - Test on different accounts
   - Report bugs and issues
   - Suggest improvements

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/profile-update-bot.git
cd profile-update-bot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd naukri
pip install -r requirements.txt

# Run locally
python3 update.py
```

### Contribution Guidelines

- Follow existing code style
- Add tests for new features
- Update documentation
- One feature per pull request
- Add your name to CONTRIBUTORS.md

---

## 📊 Statistics

### Naukri Bot (Current)

- **Active Users**: Growing community
- **Success Rate**: ~95% (with proper setup)
- **Average Runtime**: 1-2 minutes per execution
- **GitHub Actions Minutes Used**: ~30-40 min/month (out of 2000 free)

### Why GitHub Actions?

- ✅ **100% Free** (2000 minutes/month)
- ✅ **No Server Needed** (runs in the cloud)
- ✅ **Reliable** (99.9% uptime)
- ✅ **Secure** (encrypted secrets)
- ✅ **Logs & Artifacts** (debugging made easy)

---

## 🔒 Security & Privacy

### What We Do

✅ Store credentials as encrypted GitHub Secrets  
✅ Use OAuth2 for Gmail (no password storage)  
✅ Read-only Gmail access  
✅ All code is open source (audit anytime)  
✅ No data collection or tracking  

### What We Don't Do

❌ Store passwords in code  
❌ Send data to third parties  
❌ Track user behavior  
❌ Access more than necessary  

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/profile-update-bot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/profile-update-bot/discussions)
- **Email**: your.email@example.com

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Selenium WebDriver community
- Google Gmail API team
- GitHub Actions platform
- All contributors and testers

---

## ⚠️ Disclaimer

This bot is for educational and personal use only. Make sure you:
- Comply with the Terms of Service of job portals
- Use responsibly and ethically
- Don't spam or abuse the automation
- Are aware of rate limits and restrictions

**Use at your own risk.** The authors are not responsible for any account restrictions or bans.

---

## 🌟 Star History

If this project helped you, please consider giving it a ⭐!

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/profile-update-bot&type=Date)](https://star-history.com/#yourusername/profile-update-bot&Date)

---

<div align="center">

**Made with ❤️ by developers, for developers**

[⬆ Back to Top](#-profile-update-bot)

</div>

