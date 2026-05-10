import re
from urllib.parse import urlparse
import ipaddress

def extract_features(url: str) -> list[int]:
    if not re.match(r'^https?://', url):
        url = 'http://' + url

    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    features = [0] * 30

    try:
        ipaddress.ip_address(domain)
        features[0] = -1
    except ValueError:
        features[0] = 1

    # 2. URL_Length
    if len(url) < 54:
        features[1] = 1
    elif 54 <= len(url) <= 75:
        features[1] = 0
    else:
        features[1] = -1

    shorteners = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs"
    if re.search(shorteners, domain):
        features[2] = -1

    if '@' in url:
        features[3] = -1

    if url.rfind('//') > 7:
        features[4] = -1

    if '-' in domain:
        features[5] = -1

    dot_count = domain.count('.')
    if dot_count == 1:
        features[6] = 1
    elif dot_count == 2:
        features[6] = 0
    else:
        features[6] = -1

    if parsed_url.scheme == 'https':
        features[7] = 1
    else:
        features[7] = -1

    if parsed_url.port and parsed_url.port not in [80, 443]:
        features[10] = -1

    if 'https' in domain:
        features[11] = -1

    return features