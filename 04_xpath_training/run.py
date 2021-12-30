from lxml.html import fromstring
import requests


page = requests.get("https://eldorado.ua/uk/notebooks/c1039096/")
tree = fromstring(page.text)

hrefs = []
phones = tree.xpath('//div[@class="goods-list row"]//div[@class="image-place"]//a')
print(phones)
hrefs.extend([p.href for p in phones])

print(hrefs[:2])
