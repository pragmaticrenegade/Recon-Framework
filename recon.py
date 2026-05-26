#!/usr/bin/env -S python3 -u
import subprocess
import argparse
import sys
import os
import re
import ipaddress
from datetime import datetime
from fpdf import FPDF, XPos, YPos
import urllib.request
import urllib.parse
import urllib.error
import json
import time

# Store results for PDF generation
recon_results = {}

# Store vulnerability findings from Nmap NSE
vuln_results = {}          
extracted_keywords = []    # Software/service/version strings parsed from scan output

def print_banner():
    """Displays the Recon Framework banner in italics and Cyan/Teal."""
    cyan_teal = "\033[3;1;36m"
    yellow = "\033[1;33m"
    green = "\033[1;32m"
    reset = "\033[0m"

    banner = r"""
  ____                            _____                                             _ 
 |  _ \ ___  ___ ___  _ __        |  ___| __ __ _ _ __ ___   _____      _____  _ __| | __
 | |_) / _ \/ __/ _ \| '_ \       | |_ | '__/ _` | '_ ` _ \ / _ \ \ /\ / / _ \| '__| |/ /
 |  _ <  __/ (_| (_) | | | |      |  _|| | | (_| | | | | | |  __/\\ V  V / (_) | |  |   < 
 |_| \_\___|\___\___/|_| |_|      |_|  |_|  \__,_|_| |_| |_|\___/ \_/\_/ \___/|_|  |_|\_\ 
    """
    
    print(cyan_teal + banner + reset)
    print(yellow + "            Recon Framework By Arpan Bhattacharya" + reset)
    print(green + "          Perform Active And Passive Reconnaissance" + reset)
    print("-" * 85)

def run_command(name, command):
    """Executes a command and ensures 'Not Found' is recorded for empty results."""
    print(f"\033[1;34m[*] Running {name}...\033[0m")
    try:
        # Execute and capture output
        result = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, text=True)
        
        # Check if output is empty
        if not result.strip():
            recon_results[name] = "No records found (Not Enabled/Supported)"
        else:
            print(result)
            recon_results[name] = result

    except subprocess.CalledProcessError as e:
        # Distinguish between system errors and missing DNS data
        output = e.output if e.output else ""
        if "connection timed out" in output.lower():
            recon_results[name] = "FAILED: Connection Timeout"
        elif "command not found" in output.lower():
            recon_results[name] = f"FAILED: {name} tool is not installed on this system."
        else:
            # For most recon tools, a non-zero exit with some output usually means no data
            recon_results[name] = "No records found (Not Enabled/Supported)"
            
    except Exception as e:
        recon_results[name] = f"FAILED: System Error: {str(e)}"

def generate_pdf(target, filename):
    """Generates a structured PDF report with clear status indicators."""
    print(f"\n\033[1;32m[+] Generating PDF report: {filename}\033[0m")
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Header
    pdf.set_font("Courier", "B", 16)
    pdf.cell(0, 10, "Network Reconnaissance Report", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.set_font("Courier", "I", 10)
    pdf.cell(0, 10, f"Target: {target} | Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(10)

    # Status Summary Table
    pdf.set_font("Courier", "B", 12)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(0, 10, " Module Execution Status Summary ", new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
    pdf.ln(2)
    
    pdf.set_font("Courier", "B", 10)
    pdf.cell(100, 8, "Tool / Module Name", border=1)
    pdf.cell(80, 8, "Execution Status", border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_font("Courier", size=10)
    for tool, output in recon_results.items():
        if "FAILED:" in output:
            status = "ERROR/MISSING TOOL"
        elif "No records found" in output:
            status = "NOT FOUND / DISABLED"
        else:
            status = "SUCCESS"
            
        pdf.cell(100, 8, tool, border=1)
        pdf.cell(80, 8, status, border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.add_page() 

    # Detailed Module Output Section
    for tool, output in recon_results.items():
        pdf.set_font("Courier", "B", 12)
        pdf.set_fill_color(200, 220, 255)
        pdf.cell(0, 10, f" Module: {tool} ", new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
        pdf.ln(2)
        pdf.set_font("Courier", size=9)
        
        # Sanitize for PDF encoding
        clean_output = re.sub(r'[^\x00-\x7F]+', ' ', output)
        pdf.multi_cell(0, 5, clean_output)
        pdf.ln(5)
        
    # Vulnerability Intelligence Section (appended after recon output)
    generate_vuln_pdf_section(pdf)

    pdf.output(filename)
    print(f"\033[1;32m[+] PDF Report saved successfully!\033[0m")

# =============================================================================
# VULNERABILITY INTELLIGENCE MODULE
# Integrates: Nmap NSE Vulnerability Scripts
# =============================================================================

def run_vulnerability_scan(target, use_nmap_nse=False):
    """
    Master vulnerability intelligence runner.
    Selectively triggers Nmap vulnerability checks if requested.
    """
    print("\n\033[1;33m" + "=" * 85 + "\033[0m")
    print("\033[1;33m[+] VULNERABILITY INTELLIGENCE MODULE ACTIVATED\033[0m")
    print("\033[1;33m" + "=" * 85 + "\033[0m")

    # Local Nmap NSE Scan Logic
    if use_nmap_nse:
        run_command("Nmap NSE Vulnerability Scan", f"nmap -sV -T4 --script vuln {target}")

    print(f"\n\033[1;32m[+] Vulnerability scan complete.\033[0m")


def print_vuln_results():
    """Prints vulnerability summary information notice if populated."""
    if not recon_results.get("Nmap NSE Vulnerability Scan"):
        return

    reset = "\033[0m"
    cyan  = "\033[1;36m"

    print("\n" + "=" * 85)
    print(f"{cyan}  VULNERABILITY INTELLIGENCE REPORT{reset}")
    print("=" * 85)
    print("  Nmap NSE Vulnerability Scan execution completed.")
    print("  Please review the detailed 'Nmap NSE Vulnerability Scan' module output above.")
    print("\n" + "=" * 85 + "\n")


def generate_vuln_pdf_section(pdf):
    """
    Appends vulnerability intelligence pages to an existing FPDF object.
    Called from generate_pdf() after the standard recon sections.
    """
    if "Nmap NSE Vulnerability Scan" not in recon_results:
        return

    PW  = 190   # printable width  (mm)
    LM  =  10   # left margin      (mm)

    # ------------------------------------------------------------------ header
    pdf.add_page()
    pdf.set_font("Courier", "B", 14)
    pdf.set_fill_color(255, 80, 80)
    pdf.set_text_color(255, 255, 255)
    pdf.set_x(LM)
    pdf.cell(PW, 12, " VULNERABILITY INTELLIGENCE REPORT ",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True, align="C")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)

    # Source legend
    pdf.set_font("Courier", "I", 9)
    pdf.set_fill_color(245, 245, 245)
    pdf.set_x(LM)
    pdf.multi_cell(PW, 6, "Sources: Nmap NSE Scripting Engine")
    pdf.ln(4)

    pdf.set_font("Courier", size=10)
    pdf.set_x(LM)
    pdf.multi_cell(PW, 6, "Nmap NSE Vulnerability Scan results have been recorded in the main module section of this document.")


def main():
    parser = argparse.ArgumentParser(description="Recon Framework - Full Toolset", add_help=False)
    
    group_options = parser.add_argument_group("options")
    group_options.add_argument("-h", "--help", action="help", help="show this help message and exit")
    group_options.add_argument("-w", "--whois", action="store_true", help="WHOIS: Domain ownership info")
    group_options.add_argument("-ns", "--nslookup", action="store_true", help="Nslookup: Standard DNS query")
    group_options.add_argument("-c", "--curl", action="store_true", help="CURL: HTTP response headers")
    group_options.add_argument("-sf", "--subfinder", action="store_true", help="Subfinder: Subdomain discovery")
    group_options.add_argument("-as", "--assetfinder", action="store_true", help="Assetfinder: Find related assets")
    group_options.add_argument("-ww", "--whatweb", action="store_true", help="WhatWeb: Identify tech stack")
    group_options.add_argument("-nm", "--nmap", action="store_true", help="Nmap: Deep scan (Top 5,000 ports)")
    group_options.add_argument("-ht", "--host", action="store_true", help="Host: Quick DNS/IP mapping")
    group_options.add_argument("-wg", "--wget", action="store_true", help="Wget: Header analysis fallback")
    group_options.add_argument("-a", "--all", action="store_true", help="Run ALL tools and Generate PDF Report")
    group_options.add_argument("-o", "--output", help="Custom PDF name (default: report.pdf)")
    
    # --- Vulnerability Intelligence Module flags ---
    vuln_group = parser.add_argument_group("Vulnerability Intelligence :")
    vuln_group.add_argument("-nse", "--nmapvuln", action="store_true",
                            help="Nmap NSE: Run targeted script vulnerability scanning")
    vuln_group.add_argument("-vs", "--vulnscan", action="store_true",
                            help="VulnScan: Run vuln sources (Nmap NSE)")
    
    parser.add_argument("target", nargs='?', help="Target Domain or IP Address")

    dns_group = parser.add_argument_group("DNS Dig Options")
    dns_group.add_argument("-A", action="store_true", help="Dig A record")
    dns_group.add_argument("-AAAA", action="store_true", help="Dig AAAA record")
    dns_group.add_argument("-MX", action="store_true", help="Dig MX record")
    dns_group.add_argument("-NS", action="store_true", help="Dig NS record")
    dns_group.add_argument("-TXT", action="store_true", help="Dig TXT record")
    dns_group.add_argument("-SOA", action="store_true", help="Dig SOA record")
    dns_group.add_argument("-PTR", action="store_true", help="Dig PTR record")
    dns_group.add_argument("-ds", "--dnssec", action="store_true", help="DNSSEC: Comprehensive security check")
    dns_group.add_argument("-RRSIG", action="store_true", help="Dig RRSIG: Resource Record Signatures")
    dns_group.add_argument("-DNSKEY", action="store_true", help="Dig DNSKEY: Public Keys")
    dns_group.add_argument("-DS", action="store_true", help="Dig DS: Delegation Signer")
    dns_group.add_argument("-NSEC", action="store_true", help="Dig NSEC: Next Secure records")

    if len(sys.argv) == 1:
        print_banner()
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()
    print_banner()
    target = args.target

    if not target:
        print("\033[31m[!] Error: No target specified.\033[0m")
        sys.exit(1)

    # Passive & Active Modules
    if args.whois or args.all: run_command("WHOIS", f"whois {target}")
    if args.subfinder or args.all: run_command("Subfinder", f"subfinder -d {target} -silent")
    if args.assetfinder or args.all: run_command("Assetfinder", f"assetfinder --subs-only {target}")
    
    # DNS Module
    dns_records = ["A", "AAAA", "MX", "NS", "TXT", "SOA", "PTR", "RRSIG", "DNSKEY", "DS", "NSEC"]
    for r in dns_records:
        if getattr(args, r) or args.all:
            query = target
            if r == "PTR":
                try: query = ipaddress.ip_address(target).reverse_pointer
                except: pass
            
            dnssec_flag = " +dnssec" if (args.dnssec or r in ["RRSIG", "DNSKEY", "DS", "NSEC"]) else ""
            run_command(f"Dig {r}", f"dig {query} {r} +short{dnssec_flag}")

    if args.dnssec or args.all:
        run_command("DNSSEC Interrogation", f"dig {target} ANY +dnssec +multi")

    if args.nslookup or args.all: run_command("Nslookup", f"nslookup {target}")
    if args.host or args.all: run_command("Host Info", f"host {target}")
    if args.whatweb or args.all: run_command("WhatWeb", f"whatweb {target} --color=never")
    if args.curl or args.all: run_command("CURL Headers", f"curl -I -s -L {target}")
    if args.wget or args.all: run_command("Wget Headers", f"wget --server-response --spider {target} 2>&1 | grep -E 'HTTP/|Server:|Content-Type:'")

    # Scanning Module (Deep Scan)
    if args.nmap or args.all: 
        run_command("Nmap Deep Scan", f"nmap --top-ports 5000 -T4 --open {target}")

    # -------------------------------------------------------------------------
    # Vulnerability Intelligence Module
    # -------------------------------------------------------------------------
    run_vuln = args.vulnscan or args.all
    use_nse  = args.nmapvuln or run_vuln

    if use_nse:
        run_vulnerability_scan(
            target           = target,
            use_nmap_nse     = use_nse
        )
        print_vuln_results()

    # Report Generation
    if args.all:
        output_name = args.output if args.output else "report.pdf"
        generate_pdf(target, output_name)

if __name__ == "__main__":
    main()
