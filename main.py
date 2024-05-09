from bs4 import BeautifulSoup
import requests
import csv


# LINK = "https://www.ebay.com/usr/macgyversqualityconnections"
# LINK = "https://www.ebay.com/str/tangibleinvestmentsinc/Coins-Paper-Money/_i.html?_sacat=11116&rt=nc"
# LINK = "https://www.ebay.com/str/mintstategoldbystupplerandco/Best-Sellers/_i.html?store_cat=22969624015&_trksid=p4429486.m3561.l161211"
LINK = "https://www.ebay.com/str/tangibleinvestmentsinc/Coins-Paper-Money/_i.html?_sacat=11116"
PAGES = 4


name_list = []
price_list = []
image_list = []
store_name = ""

LINK = LINK + "&_pgn="

html_text = requests.get(f"{LINK}{1}").text
soup = BeautifulSoup(html_text, "lxml")
try:
    store_name = soup.find("div", class_="str-seller-card__store-name").text
except AttributeError:
    LINK = LINK.replace("&_pgn=", "?_pgn=")


for i in range(1, PAGES+1):
    html_text = requests.get(f"{LINK}{i}").text
    soup = BeautifulSoup(html_text, "lxml")
    store_name = soup.find("div", class_="str-seller-card__store-name").text
    items = soup.find_all("article")

    for item in items:
        name = item.find("span", class_="str-text-span").text
        price = item.find("span", class_="str-text-span str-item-card__property-displayPrice").text
        image = item.find("img").get("src")
        if name in name_list and price in price_list and image in image_list:
            continue
        else:
            name_list.append(name)
            price_list.append(price)
            image_list.append(image)

if len(name_list) == 0:
    for i in range(1, PAGES + 1):
        html_text = requests.get(f"{LINK}{i}").text
        soup = BeautifulSoup(html_text, "lxml")
        items = soup.find_all("li", class_="s-item s-item__pl-on-bottom")
        for item in items:
            name = item.find("div", class_="s-item__title").text
            price = item.find("span", class_="s-item__price").text
            image = item.find("img").get("src")
            if name in name_list and price in price_list and image in image_list:
                continue
            else:
                name_list.append(name)
                price_list.append(price)
                image_list.append(image)

print(store_name)
print(name_list)
print(price_list)
print(image_list)
print(f"{len(name_list)}, {len(price_list)}, {len(image_list)}")

with open(f"{store_name}.csv", "w", newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["NAME", "PRICE", "WATCHERS"])

    for name, price, image in zip(name_list, price_list, image_list):
        writer.writerow([name, price, image])

