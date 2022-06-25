#%%
from curses.panel import top_panel
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import sys
import re
import pandas
import seaborn
chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.reddit.com/r/TokyoRevengers/?f=flair_name%3A%22New%20Chapter%22")

time.sleep(2)  
scroll_pause_time = 5
last_height = driver.execute_script("return document.body.scrollHeight;")  
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    new_height = driver.execute_script("return document.body.scrollHeight")
    time.sleep(scroll_pause_time)    

    if new_height == last_height:
        break
    last_height = new_height
    


soup = BeautifulSoup(driver.page_source, "html.parser")
redditFluff = soup.find_all("div", class_="_1rZYMD_4xY3gRcSS3p8ODO _3a2ZHWaih05DgAOtvu6cIo")

upvotes = []
for post in reversed(redditFluff):
    if post.text[-1]=='k':
        upvotes.append(float((post.text)[:-1])*1000)
    else:
        upvotes.append(int(post.text))


chapters = []
for i in range(213,257):
    chapters.append(i)
sys.stdout = open("output.txt", "w")


df = pandas.DataFrame({'Upvotes': upvotes, 'Chapters' :chapters})
print(df)
seaborn.lineplot(x='Chapters', y='Upvotes',  data=df)
driver.quit()















# %%
