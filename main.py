from bs4 import BeautifulSoup
import requests
import csv
import tkinter as tk

# https://www.ebay.com/usr/macgyversqualityconnections
# https://www.ebay.com/str/tangibleinvestmentsinc/Coins-Paper-Money/_i.html?_sacat=11116&rt=nc
# https://www.ebay.com/str/mintstategoldbystupplerandco/Best-Sellers/_i.html?store_cat=22969624015&_trksid=p4429486.m3561.l161211
# https://www.ebay.com/str/tangibleinvestmentsinc/Coins-Paper-Money/_i.html?_sacat=11116&rt=nc


name_list = []
price_list = []
image_list = []


def on_button_click():
    link = text_entry.get()
    text_entry.delete(0, tk.END)
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, "lxml")
    store_name = ""
    pages = soup.find_all("a", class_="pagination__item")
    for page in pages:
        link = page.get("href")
        html_text = requests.get(link).text
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
        html_text = requests.get(link).text
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


root = tk.Tk()
root.title("Ebay Profile Scraper")

window_width = 800
window_height = 400

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

text_entry = tk.Entry(root, width=56)
text_entry.config(font=("Arial", 12))
text_entry.place(x=100, y=200)

button = tk.Button(root, text="Save CSV", command=on_button_click)
button.place(x=610, y=197)

label = tk.Label(root, font=("Arial", 17), text="Paste The Link Of An Ebay Profile")
label.place(x=200, y=100)

root.mainloop()