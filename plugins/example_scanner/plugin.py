def run(target: str) -> dict:
    # Example scanner plugin returns a demo finding
    return {
        "target": target,
        "findings": [
            {
                "cve": "CVE-2021-44228",
                "title": "Log4Shell RCE",
                "cvss": 10.0,
                "service": "http",
                "port": 8080,
            }
        ],
    }
