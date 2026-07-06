import requests

def analyze_http(ip, port):

    try:
        url = f"http://{ip}:{port}"

        r = requests.get(url, timeout=3)

        headers = r.headers

        findings = []

        if "Server" in headers:
            findings.append(f"Server: {headers['Server']}")

        if "X-Frame-Options" not in headers:
            findings.append("Missing X-Frame-Options")

        if "Strict-Transport-Security" not in headers:
            findings.append("Missing HSTS")

        return findings

    except OSError:
        return []
