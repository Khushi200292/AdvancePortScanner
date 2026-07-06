import socket
import time

from banner import show_banner
from scanner import scan_port

from rich import print
from rich.console import Console
from rich.progress import Progress
from rich.table import Table
from rich.panel import Panel
from rich import box

from threading import Thread, Lock

from services.http_service import analyze_http
from services.dns_service import dns_lookup
from services.tls_service import get_tls_info
from services.risk_service import calculate_risk
from services.os_detection import detect_os

console = Console()


# ----------------------------------
# Banner Grabbing
# ----------------------------------

def get_service_banner(ip, port):
    try:
        s = socket.socket()
        s.settimeout(1)

        s.connect((ip, port))

        s.send(b"HEAD / HTTP/1.0\r\n\r\n")

        banner = s.recv(1024).decode(errors="ignore")

        s.close()

        if "Server:" in banner:
            for line in banner.splitlines():
                if "Server:" in line:
                    return line.replace(
                        "Server:",
                        ""
                    ).strip()

        return banner.split("\n")[0][:50]

    except OSError:
        return "No Banner"


# ----------------------------------
# Worker Thread
# ----------------------------------

def worker(port):
    global open_ports
    global closed_ports
    global scanned

    result = scan_port(target, port)

    try:
        service = socket.getservbyport(port)
    except OSError:
        service = "Unknown"

    with lock:
        scanned += 1

    if result:

        banner = get_service_banner(
            target,
            port
        )

        with lock:
            open_ports.append(
                (port, service, banner)
            )

    else:
        with lock:
            closed_ports += 1


# ----------------------------------
# Main Menu
# ----------------------------------

print("[cyan]1.[/cyan] Scan Target")
print("[cyan]2.[/cyan] Exit")

choice = input("\nSelect Option: ")

if choice == "1":

    target = input("Target IP: ")

    hostname = dns_lookup(target)
    os_name, confidence = detect_os(target)

    start_port = int(
        input("Start Port: ")
    )

    end_port = int(
        input("End Port: ")
    )

    start_time = time.time()

    open_ports = []
    closed_ports = 0
    scanned = 0

    lock = Lock()

    threads = []

    total_ports = (
        end_port - start_port + 1
    )

    print("\n[cyan]Scanning...[/cyan]\n")

    with Progress() as progress:

        task = progress.add_task(
            "[cyan]Scanning Ports...",
            total=total_ports
        )

        for port in range(
            start_port,
            end_port + 1
        ):
            t = Thread(
                target=worker,
                args=(port,)
            )

            t.start()

            threads.append(t)

        while any(
            t.is_alive()
            for t in threads
        ):

            progress.update(
                task,
                completed=scanned
            )

            time.sleep(0.1)

        for t in threads:
            t.join()

        progress.update(
            task,
            completed=scanned
        )

    end_time = time.time()

    # ----------------------------------
    # Target Information
    # ----------------------------------

    console.print(
    Panel.fit(
        f"""Target      : {target}
Hostname    : {hostname}
OS          : {os_name}
Confidence  : {confidence}""",
        title="[bold green]TARGET INFORMATION[/bold green]",
        border_style="green"
    )
  )

    # ----------------------------------
    # Open Ports Table
    # ----------------------------------

    ports_table = Table(
        title="OPEN PORTS",
        box=box.ROUNDED
    )

    ports_table.add_column(
        "Port",
        style="cyan"
    )

    ports_table.add_column(
        "Service",
        style="green"
    )

    ports_table.add_column(
        "Banner",
        style="yellow"
    )

    for port, service, banner in sorted(open_ports):

        ports_table.add_row(
            str(port),
            service.upper(),
            banner[:40]
        )

    console.print(ports_table)

    # ----------------------------------
    # HTTP Analysis
    # ----------------------------------

    console.print(
        Panel.fit(
            "HTTP Security Checks",
            title="[bold yellow]HTTP ANALYSIS[/bold yellow]",
            border_style="yellow"
        )
    )

    for port, service, banner in open_ports:

        if port in [80, 8080]:

            findings = analyze_http(
                target,
                port
            )

            if findings:

                for item in findings:
                    print(
                        f"[yellow][HTTP][/yellow] {item}"
                    )

    # ----------------------------------
    # TLS Analysis
    # ----------------------------------

    console.print(
        Panel.fit(
            "TLS Certificate Inspection",
            title="[bold blue]TLS ANALYSIS[/bold blue]",
            border_style="blue"
        )
    )

    for port, service, banner in open_ports:

        if port == 443:

            cert = get_tls_info(
                target,
                port
            )

            if cert:

                print(
                    "[green][TLS][/green] Certificate Found"
                )

                print(
                    f"[green][TLS][/green] Expires : "
                    f"{cert.get('notAfter', 'Unknown')}"
                )

                issuer = cert.get(
                    "issuer",
                    "Unknown"
                )

                issuer = str(issuer)

                print(
                    f"[green][TLS][/green] Issuer : "
                    f"{issuer[:80]}"
                )

            else:

                print(
                    "[red][TLS][/red] Unable to retrieve certificate"
                )

    # ----------------------------------
    # Risk Assessment
    # ----------------------------------

    risk_score, risk_level = calculate_risk(
        open_ports
    )

    risk_color = {
        "LOW": "green",
        "MEDIUM": "yellow",
        "HIGH": "red"
    }.get(
        risk_level.upper(),
        "white"
    )

    console.print(
        Panel.fit(
            f"""
Risk Score : {risk_score}

Risk Level : {risk_level}
""",
            title="[bold red]RISK ASSESSMENT[/bold red]",
            border_style=risk_color
        )
    )

    # ----------------------------------
    # Summary
    # ----------------------------------

    summary = Table(
        title="SCAN SUMMARY",
        box=box.ROUNDED
    )

    summary.add_column("Metric")
    summary.add_column("Value")

    summary.add_row(
        "Target",
        target
    )

    summary.add_row(
        "Hostname",
        hostname
    )

    summary.add_row(
        "Open Ports",
        str(len(open_ports))
    )

    summary.add_row(
        "Closed Ports",
        str(closed_ports)
    )

    summary.add_row(
        "Scan Time",
        f"{end_time - start_time:.2f}s"
    )

    summary.add_row(
        "Risk Level",
        risk_level
    )

    console.print(summary)

elif choice == "2":

    print("[yellow]Exiting...[/yellow]")

else:

    print("[red]Invalid Option[/red]")
           
