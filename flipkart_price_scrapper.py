from bs4 import BeautifulSoup
import requests
import smtplib

AUTH_EMAIL = "sender's email id"
AUTH_PASSWORD = "sender's account password"
FROM = AUTH_EMAIL
TO = "receiver's email id"
UPPER_PRICE = {enter your price here}

URL = "enter url of a flipkart product here"

headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
    }

def check_price():
    page = requests.get(URL, headers = headers)
    soup = BeautifulSoup(page.content, features="html.parser")
    get_title = soup.find("span", {"class" : "_35KyD6"}).get_text()
    print(get_title)
    get_price = soup.find("div", {"class" : "_1vC4OE _3qQ9m1"}).get_text()
    price_ = [s for s in get_price if (s.isdigit() or s == ".")] 
    converted_price = "".join(price_)
    price = float(converted_price)
    print(price)
    if price < UPPER_PRICE:
        send_mail(get_title, price, URL)

def send_mail(get_title, price, URL):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(AUTH_EMAIL, AUTH_PASSWORD)
    subject = "PRICE FELL DOWN"
    body_temp = f"The price of product - {get_title} fell down to {price} \n CHECK THE LINK -\n {URL}"    # having non-ascii characters
    body = body_temp.encode("ascii", "ignore").decode("utf8")    # first coverted into ascii format and removing all non-ascii characters and then coverting back to utf8 fromat
    msg = f"Subject : {subject}\n\n{body}"
    server.sendmail(FROM, TO, msg)
    print("EMAIL HAS BEEN SENT")
    server.quit()

check_price()
