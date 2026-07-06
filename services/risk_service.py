def calculate_risk(open_ports):

    score = 0

    high_risk_ports = [
        21,
        23,
        25,
        53,
        139,
        445,
        3306,
        5432
    ]

    for port, service, banner in open_ports:

        if port in high_risk_ports:
            score += 10

    if score >= 40:
        level = "HIGH"
    elif score >= 20:
        level = "MEDIUM"
    else:
        level = "LOW"

    return score, level
