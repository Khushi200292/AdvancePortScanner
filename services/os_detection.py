import subprocess
import platform
import re


def detect_os(ip):
    try:

        if platform.system().lower() == "windows":

            output = subprocess.check_output(
                f"ping -n 1 {ip}",
                shell=True,
                text=True
            )

        else:

            output = subprocess.check_output(
                f"ping -c 1 {ip}",
                shell=True,
                text=True
            )

        match = re.search(
            r"ttl[=\s](\d+)",
            output,
            re.IGNORECASE
        )

        if not match:
            return "Unknown", "0%"

        ttl = int(match.group(1))

        if ttl <= 64:
            return "Linux / Unix", "80%"

        elif ttl <= 128:
            return "Windows", "80%"

        elif ttl <= 255:
            return "Network Device / Router", "70%"

        return "Unknown", "0%"

    except Exception:
        return "Unknown", "0%"
