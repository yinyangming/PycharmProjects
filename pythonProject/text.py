import requests
from bs4 import BeautifulSoup
url = "https://www.amazon.com/Daily-Ritual-Standard-Fit-Sleeveless-Empire-Waist/dp/B08P7DCNNT/ref=sr_1_1?pf_rd_r=019ZSSHW8ZJ755459WJF&qid=1693400113&refinements=p_89%3ADaily+Ritual&rnid=2528832011l&s=apparel&sr=1-1"
res = requests.get(
  url=url,
  headers={
            "User - Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit/537.36(KHTML,likeGecko) Chrome / 116.0.0.0Safari/537.36",
            "pragma": "no_cache",
            "Accept - Language": "zh - CN, zh;q = 0.9, en - US;q = 0.8, en;q = 0.7",
            "upgrade-insecure-requests": "1",
            "cache-control": "no-cache",
            "accept-encoding": "gzip,deflate,br",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
        }
    )
if res.status_code == 200:
    print(res.status_code)