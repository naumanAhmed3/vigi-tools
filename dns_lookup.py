import dns.resolver
import json

def dns_lookup(domain: str) -> str:
    """
    Performs DNS lookup for A, CNAME, MX, and NS records of the given domain.
    Returns detailed information (record type, TTL, target/value) as JSON.

    Requires: pip install dnspython
    """
    record_types = ["A", "CNAME", "MX", "NS"]
    results = {
        "domain": domain,
        "status": "success",
        "records": []
    }

    try:
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                for rdata in answers:
                    record = {
                        "type": record_type,
                        "ttl": answers.rrset.ttl,
                        "host": domain
                    }
                    if record_type == "A":
                        record["value"] = rdata.address
                    elif record_type == "CNAME":
                        record["value"] = rdata.target.to_text()
                    elif record_type == "MX":
                        record["priority"] = rdata.preference
                        record["value"] = rdata.exchange.to_text()
                    elif record_type == "NS":
                        record["value"] = rdata.target.to_text()
                    results["records"].append(record)
            except dns.resolver.NoAnswer:
                results["records"].append({
                    "type": record_type,
                    "host": domain,
                    "value": None,
                    "message": f"No {record_type} record found."
                })
            except dns.resolver.NXDOMAIN:
                return json.dumps({
                    "domain": domain,
                    "status": "error",
                    "message": "Domain does not exist."
                }, indent=2)
            except dns.exception.DNSException as e:
                results["records"].append({
                    "type": record_type,
                    "host": domain,
                    "value": None,
                    "error": str(e)
                })
    except Exception as e:
        return json.dumps({
            "domain": domain,
            "status": "error",
            "message": str(e)
        }, indent=2)

    return json.dumps(results, indent=2)

# Example usage:
if __name__ == "__main__":
    print(dns_lookup("example.com"))
