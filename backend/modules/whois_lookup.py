import whois

def get_whois(domain):
    try:
        return whois.whois(domain)
    except Exception as e:
        return str(e)
