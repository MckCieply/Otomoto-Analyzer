#Choose scirocco / lancer x
#Scrape it
#make it look nice
#store it in DB
import requests
from bs4 import BeautifulSoup
import time
import sqlite3 as sql
conn = sql.connect("C:/Users/mwppl/Desktop/Code/Full-Stack-Project/otofeature/deals.db")
c = conn.cursor()
try:    
    c.execute(f"""CREATE TABLE cars(id INT PRIMARY KEY, brand TEXT, model TEXT, price INT, currency TEXT, year INT, mileage INT, add_date TEXT, url TEXT)""")
except:
    pass

brand = "Mitsubishi"    #Mitsubishi Volkswagen
model = "Lancer"  #Lancer Scirocco
min_year = "2007" #2007 2008
fuel_type = "petrol"#petrol
min_capacity = "1700"#1900 1500-1700
chasis = "sedan" #sedan coupe
def finding_last_page(brand, model, min_year, fuel_type, min_capacity):
    URL = f"https://www.otomoto.pl/osobowe/{brand}/{model}/seg-{chasis}/od-{min_year}?search%5Bfilter_enum_fuel_type%5D={fuel_type}&search%5Bfilter_float_engine_capacity%3Afrom%5D={min_capacity}?page=1"
    request = requests.get(URL)
    soup = BeautifulSoup(request.content, 'html5lib')
    try:
        div = soup.find('div', {'class':'ooa-1oll9pn e19uumca7'})
        ul = div.find('ul', {'data-testid': 'pagination-list'})
        for li in ul.find_all('li', {'data-testid': 'pagination-list-item'}):
            global last_page
            last_page = int(li.a.span.text)
    except:
        last_page = 1
        
def all_deals(brand, model, min_year, fuel_type, min_capacity, last_page):        
    counter = 1
    for page in range(1, last_page+1):
        URL = f'https://www.otomoto.pl/osobowe/{brand}/{model}/seg-{chasis}/od-{min_year}?search%5Bfilter_enum_fuel_type%5D={fuel_type}&search%5Bfilter_float_engine_capacity%3Afrom%5D={min_capacity}%3Fpage%3D1"&page={page}'
        request = requests.get(URL)
        soup = BeautifulSoup(request.content, 'html5lib')
        for div in soup.find_all('div',attrs={'class' : "ooa-le0vtj e1b25f6f14"}):
            deal_url = div.a["href"]
            #print(counter,".",deal_url)
            single_deal(deal_url)

            counter +=1
        print(f"Total of {counter} deals")
def single_deal(deal_url):                      #extract id/ deal add date/ price/ production year/ mileage
    request = requests.get(deal_url)
    soup = BeautifulSoup(request.content, 'html5lib')
    span = soup.find('span', {"class":"offer-price__number"})
    price = span.contents[0].replace(" ", "")
    currency = span.contents[1].text

    span = soup.find_all('span', {'class':'offer-main-params__item'})
    year = span[0].text.strip()
    mileage = span[1].text.strip().replace(" ", "").strip("km")

    span = soup.find('span',{'class':'offer-meta__value'})
    add_date = span.contents[0]

    span = soup.find('span',{'id':'ad_id'})
    id = span.text

    #print(f"{id}, {brand}, {model}, {price}, {currency}, {year}, {mileage}, {add_date}")
    try:
        c.execute("""INSERT INTO  cars VALUES (?,?,?,?,?,?,?,?,?)""",(id, brand, model, price, currency, year, mileage, add_date, deal_url))
    except:
        pass
    
if __name__ == "__main__":
    finding_last_page(brand, model, min_year, fuel_type, min_capacity)
    all_deals(brand, model, min_year, fuel_type, min_capacity, last_page)

conn.commit()

print(f"Finishing... ")
    
conn.close()
