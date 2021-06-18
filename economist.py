import requests
from lxml import html


url = "https://www.920.im/the-economist-ebook-audio-weekly-update/"
header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}
payload = {
            "e_secret_key": "920.im"
        }
response = requests.post(url, data=payload, headers=header)
tree = html.fromstring(response.text)
link = tree.xpath("/html/body/section/div[2]/div/article/div[3]/p/a[1]/@href")
print(link)

