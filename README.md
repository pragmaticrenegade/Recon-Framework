🔍 What is the Recon Framework?
Manually pivoting between modular recon utilities often results in disjointed logs and missed data correlation. This framework functions as an all-in-one execution engine that strings together passive OSINT, infrastructure auditing, and internal compliance checks into a single command-line interface.

✨ Key Features Built-In:
•	Passive Reconnaissance & OSINT: Rapid tracking utilizing target telemetry like WHOIS ownership, infrastructure mapping via Nslookup/Host, and passive subdomain aggregation using tools like Subfinder and Assetfinder.
•	Web Asset Profiling: Instant technology stack fingerprinting via inline WhatWeb extraction alongside deep CURL/Wget inline response header analysis.
•	Cryptographic & DNSSEC Auditing: Advanced DNS record validation checking for A, AAAA, MX, NS, TXT, and SOA pointers alongside a strict validation layer checking for DNSKEY, RRSIG, DS, and NSEC entries to ensure infrastructure resistance against cache poisoning.
•	Active Port & Service Enumeration: Multi-threaded target interrogation scanning across 5,000 top ports to surface exposed endpoints instantly.
•	Vulnerability Intelligence Module: A built-in automation layer leveraging optimized Nmap NSE Scripting Engine vulnerability audits (-T4 --script vuln) to instantly highlight high-severity remote code execution vectors.
•	Executive PDF Reporting: Automatically compiles the output from all disparate binaries, tracks the individual module execution statuses, sanitizes encoding anomalies, and generates an executive PDF report complete with color-coded severity metrics.

⚠️ Educational & Compliance Disclaimer
The Recon Framework is built strictly for educational purposes and authorized security assessments. It is designed to assist students accelerating their infrastructure learning curve, security researchers profiling defensive posture, and penetration testers/ethical hackers executing structured, scope-compliant vulnerability assessments. Unauthorized utilization against non-permissive infrastructure is strictly prohibited.

📜 Attribution & Trademark Notice
All integrated tools used within this framework (including Nmap, Subfinder, Assetfinder, WhatWeb, etc.) are the property of their respective owners. Original copyrights, licenses, and trademarks apply to each underlying binary and component utilized by this toolkit.
I would love to hear your feedback, feature recommendations, or code contributions on GitHub!
