# 🚀 Advanced Port Scanner v1.0

A Python-based Advanced Port Scanner designed for network reconnaissance, service enumeration, HTTP security analysis, TLS certificate inspection, and basic risk assessment.

---

## 📌 Overview

Advanced Port Scanner is a command-line cybersecurity tool developed for educational purposes and authorized security testing. It enables users to scan a target host for open TCP ports, identify running services, perform banner grabbing, analyze HTTP security configurations, inspect TLS certificates, and generate a basic risk assessment.

The project follows a modular architecture, making it easy to maintain and extend with additional networking and security features.

---

## ✨ Features

- 🔍 Fast TCP Port Scanning
- ⚡ Multi-threaded Port Enumeration
- 🌐 Hostname Resolution
- 🖥️ Basic Operating System Detection
- 📡 Service Detection
- 🏷️ Banner Grabbing
- 🌍 HTTP Security Analysis
- 🔐 TLS Certificate Inspection
- 📊 Risk Assessment
- 📋 Scan Summary
- 📁 Modular Project Structure

---

## 📂 Project Structure

```
AdvancePortScanner/
│
├── banner.py
├── scanner.py
├── main.py
├── http_service.py
├── utils.py
│
├── services/
│   ├── __init__.py
│   ├── dns_service.py
│   ├── http_service.py
│   ├── os_detection.py
│   ├── risk_service.py
│   └── tls_service.py
│
├── reports/
├── .gitignore
└── README.md
```

---

## ⚙️ Requirements

- Python 3.10 or higher
- Linux (Recommended)
- Internet connection for scanning external hosts

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/Khushi200292/AdvancePortScanner.git
```

Navigate to the project directory:

```bash
cd AdvancePortScanner
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the scanner using:

```bash
python3 main.py
```

Follow the on-screen menu to:

- Enter the target IP address
- Specify the start port
- Specify the end port
- View the scan results and security analysis

---

## 🔧 Modules

### Port Scanner
- Performs TCP port scanning.
- Identifies open ports.

### Service Detection
- Detects commonly running network services.

### Banner Grabbing
- Retrieves service banners where available.

### HTTP Analysis
- Checks HTTP response headers.
- Identifies common security header configurations.

### TLS Analysis
- Retrieves SSL/TLS certificate information.
- Displays certificate issuer and expiration details.

### Risk Assessment
- Provides a basic security score based on scan findings.

---

## 🚀 Future Enhancements

- UDP Port Scanning
- Service Version Detection
- Advanced OS Fingerprinting
- CVE Lookup Integration
- Vulnerability Detection
- Export Reports (PDF, HTML, JSON)
- IPv6 Support
- WHOIS Lookup
- Geolocation Integration

---

## 🛠️ Technologies Used

- Python
- Socket Programming
- Multithreading
- SSL/TLS
- DNS Resolution
- Networking Concepts

---

## ⚠️ Disclaimer

This project is intended for educational purposes and authorized security testing only. Always obtain explicit permission before scanning or assessing any network or system. Unauthorized use may violate applicable laws and organizational policies.

---

## 👩‍💻 Author

**Khushi Singla**

Cybersecurity Enthusiast | Python Developer | Network Security Learner

GitHub: https://github.com/Khushi200292
