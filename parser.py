from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd


option = Options()
option.add_argument("--disable-infobars") 


### LOCAL PATH TO chromedriver !!!!
browser = webdriver.Chrome(executable_path = r'/Users/beknazarkhamituly/Documents/chromedriver', chrome_options=option)
path = 'data/krysha_astana_2-3room_longterm.csv'

link = f'https://krisha.kz/arenda/kvartiry/astana/?das[live.rooms][]=2&das[live.rooms][]=3&das[rent.period]=2&das[who]=1'
# browser.get(link)
# elems = browser.find_elements(By.XPATH, "//div[@class= 'a-card__header']")
browser.get(link)
elems = browser.find_elements(By.XPATH,"//a[@class = 'paginator__btn ']")
max_page_size = elems[-1].text

new_df = pd.DataFrame(columns=['krysha_id','title','room','address','price','link'])

for i in range(1,int(max_page_size)+1):
    link = f'https://krisha.kz/arenda/kvartiry/astana/?das[live.rooms][]=2&das[live.rooms][]=3&das[rent.period]=2&das[who]=1&page={i}'
    browser.get(link)
    elems = browser.find_elements(By.XPATH, "//div[@class= 'a-card__header']")

    for i in range(len(elems)):
        temp = elems[i].find_element(By.CLASS_NAME, 'a-card__title ')
        name = temp.text
        price = elems[i].find_element(By.CLASS_NAME, 'a-card__price').text
        address = elems[i].find_element(By.CLASS_NAME, 'a-card__subtitle ').text
        room = name.split(',')[0]
        link = temp.get_attribute('href')
        id = link.split('/')[-1]
        row = pd.Series(data=[id,name,room,address,price,link],index = new_df.columns)
        
        new_df = new_df.append(row, ignore_index=True)

root_df = pd.read_csv(path)
new_df['krysha_id'] = new_df.krysha_id.astype(int)
root_df['krysha_id'] = root_df.krysha_id.astype(int)

list_id = root_df.krysha_id.tolist()

def is_new_ad(id):
    if id in list_id:
        return None
    return True

new_advertisments = new_df.copy()

new_advertisments['is_new'] = new_advertisments.apply(lambda row: is_new_ad(row.krysha_id), axis=1)
new_advertisments = new_advertisments.dropna(subset=['is_new'])

# new_advertisments - is dataframe of new ads 
# new_df - all new parsed ads that will be rewrited over previous csv 

new_df.to_csv(path)