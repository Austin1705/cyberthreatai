# 🌐 WEBSITE SECURITY SCANNER - VISUAL REFERENCE

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  YOUR THREAT DETECTION SYSTEM                │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                     WEB INTERFACE (Port 8000)                │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  📊 Dashboard      📈 Analytics    ⚠️ Threats               │
│  🌐 Scanner ⭐NEW  🔌 API         ⚙️ Admin                 │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Website Scanner                                       │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │ Enter URL: https://www.example.com                   │  │
│  │ [🔍 SCAN WEBSITE]                                    │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │ Results:                                              │  │
│  │ ┌─────────────────────────────────────────────────┐ │  │
│  │ │ THREAT LEVEL: 🟠 MEDIUM (Score: 45/100)        │ │  │
│  │ │                                                   │ │  │
│  │ │ Vulnerabilities Found: 3                         │ │  │
│  │ │ ├─ Missing Security Headers                      │ │  │
│  │ │ ├─ Server Info Disclosure                       │ │  │
│  │ │ └─ Older Technology Stack                       │ │  │
│  │ │                                                   │ │  │
│  │ │ 💡 Recommendations:                              │ │  │
│  │ │ ✓ Enable HTTPS/SSL                              │ │  │
│  │ │ ✓ Add security headers                           │ │  │
│  │ │ ✓ Keep software updated                          │ │  │
│  │ └─────────────────────────────────────────────────┘ │  │
│  │                                                       │  │
│  │ [📜 LOAD HISTORY]                                   │  │
│  │                                                       │  │
│  │ Previous Scans:                                      │  │
│  │ • google.com      🟢 SAFE    (5/100)               │  │
│  │ • oldsite.com     🟠 MEDIUM  (45/100)  [View]      │  │
│  │ • example.com     🔴 HIGH    (82/100)  [View]      │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                               │
└──────────────────────────────────────────────────────────────┘
                           │
                           │ HTTP Requests
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                    API SERVER (Port 5000)                    │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Network Threat Detection (ML-based)                         │
│  ├─ POST   /api/analyze                                     │
│  ├─ POST   /api/batch-analyze                               │
│  └─ GET    /api/health                                      │
│                                                               │
│  Website Threat Scanning ⭐NEW                              │
│  ├─ POST   /api/scan-website         ◄─ UI sends URL       │
│  ├─ GET    /api/scan-history         ◄─ Get past scans     │
│  ├─ GET    /api/scan/<id>            ◄─ Get details        │
│  ├─ GET    /api/scan-statistics      ◄─ View stats         │
│  └─ POST   /api/scan-batch           ◄─ Scan multiple      │
│                                                               │
└──────────────────────────────────────────────────────────────┘
                           │
                           │ Scans websites
                           │ (SSL, Headers, Config)
                           ▼
┌──────────────────────────────────────────────────────────────┐
│              WEBSITE SCANNER MODULE                          │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Checks:                                                     │
│  1. SSL/TLS Certificate                                      │
│  2. Security Headers (HSTS, CSP, X-Frame, etc)              │
│  3. Server Configuration (Dir listing, version, etc)        │
│  4. Response Analysis (Status codes, content)               │
│                                                               │
│  Calculates:                                                 │
│  ├─ Threat Score (0-100)                                    │
│  ├─ Threat Level (SAFE/LOW/MEDIUM/HIGH/CRITICAL)           │
│  ├─ Vulnerabilities List                                    │
│  └─ Recommendations                                          │
│                                                               │
└──────────────────────────────────────────────────────────────┘
                           │
                           │ Stores results
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                 SQLITE DATABASE                              │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  website_scans (Main results)                               │
│  ├─ id, url, domain                                         │
│  ├─ scan_timestamp                                          │
│  ├─ ssl_valid, headers_secure                              │
│  ├─ threat_level, threat_score                             │
│  ├─ vulnerabilities_found                                   │
│  └─ recommendations                                          │
│                                                               │
│  vulnerability_history (Detailed issues)                     │
│  ├─ scan_id, vulnerability_type                            │
│  ├─ severity, description                                   │
│  └─ recommendation                                           │
│                                                               │
│  File: ./website_threats.db (SQLite3)                       │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

```
USER INTERACTION:

1. User opens http://localhost:8000
                │
                ▼
2. Navigates to Website Scanner (🌐)
                │
                ▼
3. Enters website URL
   e.g., "https://www.example.com"
                │
                ▼
4. Clicks "🔍 SCAN WEBSITE"
                │
                ├─ Show loading spinner
                │
                ▼
5. JavaScript sends POST request
   /api/scan-website with URL
                │
                ▼
6. Backend WebsiteThreatScanner processes:
                │
        ┌───────┼───────┐
        │       │       │
        ▼       ▼       ▼
     SSL/TLS  Headers  Response
     Check    Check    Analysis
        │       │       │
        └───────┼───────┘
                │
                ▼
7. Calculate threat level & recommendations
                │
                ▼
8. Save to SQLite database
                │
                ▼
9. Return JSON results to browser
                │
                ▼
10. Display results:
    ├─ Threat Level (with color)
    ├─ Threat Score (0-100)
    ├─ Vulnerabilities list
    └─ Recommendations

11. Store in browser memory for history display
```

---

## Threat Score Calculation

```
SCORING SYSTEM:

Start with: threat_score = 0

For each vulnerability found:
├─ SSL/TLS error           → +20 points
├─ Missing security header → +5 points
├─ Directory listing       → +25 points
├─ Server info disclosure  → +3 points
├─ HTTP error (500)        → +10 points
├─ HTTP error (4xx)        → +2 points
└─ Other issues            → +5 points

Examples:
─────────────────────────────────────
Google.com
├─ SSL: Valid ✓       (+0)
├─ Headers: All ✓     (+0)
├─ No issues ✓        (+0)
└─ Total: 5           → 🟢 SAFE

─────────────────────────────────────
OldSite.com
├─ SSL: Valid ✓       (+0)
├─ Headers: 2 missing (+10)
├─ Version shown      (+3)
├─ Older stack        (+12)
└─ Total: 45          → 🟠 MEDIUM

─────────────────────────────────────
BadSite.com
├─ SSL: Invalid ✗     (+20)
├─ Headers: 5 missing (+25)
├─ Dir listing ✗      (+25)
├─ Version shown      (+3)
└─ Total: 82          → 🔴 HIGH
```

---

## Threat Level Decision Tree

```
                    Start Scan
                        │
                        ▼
              Check SSL Certificate
                        │
            ┌───────────┼───────────┐
            │           │           │
          VALID       EXPIRE       INVALID
            │           │           │
            │       +10 points  +20 points
            │           │           │
            └───────────┼───────────┘
                        │
                        ▼
           Check Security Headers
                        │
            Missing HSTS?  → +5
            Missing CSP?   → +5
            Missing X-Frame? → +5
            Missing X-Type? → +5
                        │
                        ▼
           Check Server Config
                        │
            Dir listing on? → +25
            Version shown?  → +3
                        │
                        ▼
            Total Score ≥ 0
                        │
        ┌───┬───┬───┬───┴────┐
        │   │   │   │        │
        ▼   ▼   ▼   ▼        ▼
       0-20 20- 50- 80-     95+
        │   50  80  95       │
        │   │   │   │        │
        ▼   ▼   ▼   ▼        ▼
      🟢  🔵  🟠  🔴  🟣
      SAFE LOW MED HIGH CRIT
```

---

## Website Vulnerability Types

```
VULNERABILITY CATEGORIES:

1. SSL/TLS Issues
   ├─ Certificate expired
   ├─ Invalid certificate
   ├─ Weak cipher suite
   └─ SSL version too old
   Risk: ⚠️ VERY HIGH

2. Missing Security Headers
   ├─ No HSTS (Strict-Transport-Security)
   ├─ No CSP (Content-Security-Policy)
   ├─ No X-Frame-Options
   ├─ No X-Content-Type-Options
   └─ No X-XSS-Protection
   Risk: ⚠️ MEDIUM-HIGH

3. Information Disclosure
   ├─ Server version shown
   ├─ Technology stack visible
   ├─ Directory listing enabled
   └─ Error messages verbose
   Risk: ⚠️ MEDIUM

4. Server Configuration
   ├─ Outdated software
   ├─ Default configurations
   ├─ HTTP endpoints available
   └─ Unnecessary services running
   Risk: ⚠️ LOW-MEDIUM

5. Response Issues
   ├─ Server errors (500)
   ├─ Not found errors (404)
   ├─ Timeout issues
   └─ Redirect chains
   Risk: ⚠️ LOW
```

---

## Safe Usage Recommendations

```
Based on Threat Score:

🟢 SAFE (0-20)
│
├─ Can browse normally
├─ Can enter passwords
├─ Can make purchases
├─ Can submit forms
└─ No special precautions needed

🔵 LOW (20-50)
│
├─ Use with caution
├─ Use strong password (unique)
├─ Don't reuse passwords
├─ Monitor account activity
└─ Consider 2FA

🟠 MEDIUM (50-80)
│
├─ Avoid if possible
├─ Don't enter passwords
├─ Don't make purchases
├─ Use temp email for signup
├─ Enable 2FA if available
└─ Use password manager

🔴 HIGH (80-95)
│
├─ STRONGLY avoid
├─ No personal data
├─ No passwords
├─ No payment info
├─ Use VPN if must visit
└─ Monitor for fraud

🟣 CRITICAL (95+)
│
├─ DO NOT USE
├─ Report to authorities
├─ Warn others
├─ Use alternative sites
└─ Block in firewall
```

---

## Scanner Features Overview

```
FEATURE                    WHAT IT DOES              RESULT
────────────────────────────────────────────────────────────

SSL Check                  Verify HTTPS cert         ✓/✗
                          Check expiry              Date
                          Validate chain            Status

Header Analysis           Look for security        List of
                         headers                   missing

Dir Listing              Check if browseable       ✓/✗
                        directories               Risk level

Server Info              Check version            Software
                        disclosure               name/version

Response Code            HTTP status              Code
                                                 (200,404,500)

Response Time            Speed check              milliseconds

Tech Stack               Identify tools           Framework
                                                 language, CMS

Threat Scoring           Calculate risk           0-100 score

Threat Level            Assign category          SAFE/LOW/MED/
                                                HIGH/CRIT

Recommendations         Safety advice            Action items

History Storage         Save results             Database
```

---

## Quick Decision Chart

```
WEBSITE SECURITY AT A GLANCE:

Visit Site? → Check Threat Level → Take Action
             │
        ┌────┼────┬────┬─────┐
        │    │    │    │     │
       🟢   🔵   🟠   🔴    🟣
      SAFE  LOW  MED  HIGH CRIT
       │    │    │    │     │
       ▼    ▼    ▼    ▼     ▼
       ✅  ⚠️  ⚠️  ❌   ❌
      YES  YES  NO  NO   NO
       
      Use  Use  Use AVOID BLOCK
      freely care avoid always
             &   with
             use cautions
             2FA
```

---

## System Files Overview

```
PROJECT STRUCTURE:

myproject/
├── 🌐 WEB PAGES (Port 8000)
│   ├── index.html              Dashboard with charts
│   ├── analytics.html          Analytics & reports
│   ├── threats.html            Threat history
│   ├── scanner.html  ⭐NEW     Website scanner
│   ├── api.html                API testing
│   └── admin.html              Admin controls
│
├── ⚙️ BACKEND (Port 5000)
│   ├── app/
│   │   └── app.py              Flask API server
│   │       └── New endpoints:
│   │           • /api/scan-website
│   │           • /api/scan-history
│   │           • /api/scan/<id>
│   │           • /api/scan-statistics
│   │           • /api/scan-batch
│   │
│   ├── 🔬 SCANNER ⭐NEW
│   │   └── website_scanner.py   (250+ lines)
│   │       • WebsiteThreatScanner class
│   │       • SSL/TLS checking
│   │       • Header analysis
│   │       • Threat calculation
│   │       • Database operations
│   │
│   ├── 🧠 ML MODEL
│   │   └── models/
│   │       ├── train_model.py   Train ML model
│   │       ├── threat_detector.joblib
│   │       └── scaler.joblib
│   │
│   ├── 📊 DATA
│   │   └── data/
│   │       ├── generate_data.py Generate training data
│   │       └── network_traffic.csv
│   │
│   └── 🗄️ DATABASE ⭐NEW
│       └── website_threats.db   SQLite database
│           ├── website_scans (main results)
│           └── vulnerability_history (details)
│
├── 📚 DOCUMENTATION
│   ├── README.md                Main guide
│   ├── SCANNER_QUICKSTART.md ⭐NEW Quick start (5 min)
│   ├── WEBSITE_SECURITY_GUIDE.md ⭐NEW Safety guide
│   ├── SCANNER_UPGRADE_COMPLETE.md ⭐NEW Implementation
│   ├── HOW_THREAT_DETECTION_WORKS.md ML explanation
│   └── MULTI_PAGE_GUIDE.md     App overview
│
├── 🧪 TESTING
│   ├── test_api.py             API test script
│   └── check_websites.py       Website checker
│
└── 📋 CONFIGURATION
    ├── requirements.txt        Python packages
    └── config/                 Configuration files
```

---

## Quick Reference Commands

```bash
# Start the system
python app/app.py                    # API server (port 5000)
python server.py                     # Dashboard (port 8000)

# Test the API
curl http://127.0.0.1:5000/api/health

# Scan a website
curl -X POST http://127.0.0.1:5000/api/scan-website \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.example.com"}'

# Get scan history
curl http://127.0.0.1:5000/api/scan-history

# Get scan details
curl http://127.0.0.1:5000/api/scan/1

# Get statistics
curl http://127.0.0.1:5000/api/scan-statistics

# Query database
sqlite3 website_threats.db "SELECT * FROM website_scans;"
```

---

## Your System in One Picture

```
    ┌─────────────────────────────────────────┐
    │   👨‍💻 YOU                                 │
    │   Open: http://localhost:8000           │
    └────────┬────────────────────────────────┘
             │
             ▼
    ┌─────────────────────────────────────────┐
    │   🌐 WEB INTERFACE                       │
    │   • Dashboard, Analytics, Threats       │
    │   • 📱 Website Scanner ⭐NEW            │
    │   • API Console, Admin Panel            │
    └────────┬────────────────────────────────┘
             │ JavaScript
             │ HTTP POST
             ▼
    ┌─────────────────────────────────────────┐
    │   🔌 API SERVER (Port 5000)             │
    │   Flask + CORS                          │
    │   Network threat detection (ML)         │
    │   Website scanning ⭐NEW                │
    └────────┬────────────────────────────────┘
             │
             ├──────────────────┬──────────────┐
             │                  │              │
             ▼                  ▼              ▼
    ┌──────────────┐  ┌───────────────┐ ┌──────────┐
    │ 🧠 ML Model  │  │ 🔬 Scanner    │ │📝 Logger │
    │ Random       │  │ SSL, Headers, │ │ Results  │
    │ Forest       │  │ Config, etc.  │ │ stored   │
    └──────────────┘  └───────────────┘ └──────────┘
                             │
                             ▼
                      ┌─────────────────┐
                      │ 🗄️ Database    │
                      │ SQLite          │
                      │ Results + Vulns │
                      └─────────────────┘
```

---

**This is your complete Website Security Scanner System!** 🛡️
