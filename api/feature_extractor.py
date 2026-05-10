# api/feature_extractor.py
import re
from urllib.parse import urlparse
import ipaddress


def extract_features(url: str) -> list[int]:
    """
    Takes a raw URL and returns a 30-element list mapping to the UCI dataset features.
    Values are typically 1 (Legitimate), 0 (Suspicious), or -1 (Phishing).
    """
    # Ensure URL has a scheme for parsing
    if not re.match(r'^https?://', url):
        url = 'http://' + url

    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path

    # Initialize a 30-element array with default "Legitimate" (1) values
    # We will flag the suspicious ones (-1) based on our checks.
    features = [1] * 30

    # 1. having_IP_Address (If domain is an IP, it's highly suspicious -> -1)
    try:
        ipaddress.ip_address(domain)
        features[0] = -1
    except ValueError:
        features[0] = 1

    # 2. URL_Length (Long URLs hide the true domain)
    if len(url) < 54:
        features[1] = 1
    elif 54 <= len(url) <= 75:
        features[1] = 0
    else:
        features[1] = -1

    # 3. Shortining_Service (TinyURL, Bitly, etc.)
    shorteners = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs"
    if re.search(shorteners, domain):
        features[2] = -1

    # 4. having_At_Symbol (Browser ignores everything before @)
    if '@' in url:
        features[3] = -1

    # 5. double_slash_redirecting (// after the protocol)
    if url.rfind('//') > 7:
        features[4] = -1

    # 6. Prefix_Suffix (Dashes in domain are common in phishing)
    if '-' in domain:
        features[5] = -1

    # 7. having_Sub_Domain (Too many subdomains is suspicious)
    dot_count = domain.count('.')
    if dot_count == 1:
        features[6] = 1
    elif dot_count == 2:
        features[6] = 0
    else:
        features[6] = -1

    # 11. port (Non-standard ports)
    if parsed_url.port and parsed_url.port not in [80, 443]:
        features[10] = -1

    # 12. HTTPS_token (Attackers add "https" to the domain string itself)
    if 'https' in domain:
        features[11] = -1

    # Note for a production system:
    # Features 8, 9, 13-30 (like SSL certificate validation, WHOIS domain age,
    # page rank, and HTML iframe checks) require heavy external API calls
    # (e.g., python-whois, requests to download HTML).
    # For this academic implementation, we extract the structural features above
    # and default the network-heavy features to neutral/safe to allow the model to run fast.

    return features