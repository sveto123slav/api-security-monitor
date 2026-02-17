import requests

targets = [
    "https://www.creditkarma.ca",
    "https://cms.creditkarma.ca",
    "https://help.creditkarma.ca",
    "https://api.creditkarma.com"
]

sensitive_paths = [
    "/.env", 
    "/.git/config", 
    "/wp-config.php.bak", 
    "/.aws/credentials",
    "/.well-known/security.txt",
    "/robots.txt"
]

def run_security_audit():
    session = requests.Session()
    session.headers.update({'User-Agent': 'BugBounty-Researcher-Teti-Audit-v1'})

    for target in targets:
        for path in sensitive_paths:
            url = f"{target}{path}"
            try:
                response = session.get(url, timeout=10, allow_redirects=False)
                if response.status_code == 200:
                    print(f"[!!] EXPOSED: {url}")
                else:
                    print(f"[-] Checked: {url} ({response.status_code})")
            except:
                continue

if __name__ == "__main__":
    run_security_audit()
