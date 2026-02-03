import requests

def get_onemap_data(postal_code):
    api_url = f"https://www.onemap.gov.sg/api/common/elastic/search?searchVal={postal_code}&returnGeom=N&getAddrDetails=Y"
    res = requests.get(api_url)
    res.raise_for_status()
    return res.json()



