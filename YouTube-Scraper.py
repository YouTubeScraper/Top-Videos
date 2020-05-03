"""
This code was written by Viraj Shetty and Arjun Praveen!
"""
import pandas as pd
import time
import operator
import bs4 as bs
import datetime
from bs4 import BeautifulSoup # For Extracting tags from YouTube video's HTML
from urllib.request import urlopen # Opening the YouTube Video Link
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC # Will extract data when it finds certain conditions
from selenium.webdriver.support.ui import WebDriverWait # Adding Waits to the webpage for it to load
from selenium.webdriver.common.keys import Keys # For Scrolling the Page
from selenium.webdriver.firefox.options import Options # For Headless mode
from datetime import date # For Date
from textblob import TextBlob # For Tokenizer

"""
This little piece of code is added to make the webdriver run silently
Generally when you use WebDriver in Selenium it opens a new window
If you have automated some functions you can also see those functions happening live
To avoid it use this option called "headless" which does all this in the background

You will also have to remove the browser.maximize() for the Browser window to not open

Web Driver object creation
Note: Before importing Selenium Webdriver
    Make sure you have a webdriver application installed in the same directory
    
    For Mozzilla
    >https://github.com/mozilla/geckodriver/releases
    
    For Chrome
    >https://chromedriver.chromium.org/downloads
"""
options = Options()
options.headless = True
browser = webdriver.Firefox(options = options)


# This function tokenizes the entered keywords

def tokenizer(l_t, l_d):
    v = TextBlob(l_t)
    w = TextBlob(l_d)
    a = v.noun_phrases
    b = w.noun_phrases
    c = a + b
    d = ""
    for i in c:
        d = d + i + " "
    print(d)
    return d

# Function for extracting number of days since the video has been uploaded

def number_of_days(v_date):
    today = date.today()
    month = {
             "Jan" : 1,
             "Feb" : 2,
             "Mar" : 3,
             "Apr" : 4,
             "May" : 5,
             "Jun" : 6,
             "Jul" : 7,
             "Aug" : 8,
             "Sep" : 9,
             "Oct" : 10,
             "Nov" : 11,
             "Dec" : 12
            }
    v=v_date.split(" ")
    v_year = int(v[2])
    v_month = int(month[v[0]])
    v_day = int(v[1])
    v_date = date(v_year,v_month,v_day)
    time = abs(today - v_date)
    return time.days

def search():
    
    keyword = input("Enter title: ")
    
    description = input("Enter description: ")  
    
    keysearch = tokenizer(keyword, description)
    keysearch_list = keysearch.split(" ")
    key = []
    for j in keysearch_list:
        if j not in key:
            key.append(j)
    print(key)
    keysearch = ""
    for k in key:
        keysearch = keysearch + k + " "
    print("Scraping search results for the keyword: " + keysearch)
    
    tag_list = keysearch.split(" ")
    browser = webdriver.Firefox()
    browser.get(f'https://www.youtube.com/results?search_query={keysearch}&sp=EgIQAQ%253D%253D')
    browser.maximize_window()

    """
    Please note here you need to use an Adblock to avoid advertisement videos to be a part of your list
    Add the filepath to your .xpi file
    """
    extension = "{your addon file location}"
    #browser.install_addon(extension, temporary = True)
    #Un-comment the above line to make the extension installation work
    

    # Change value of While Loop to scroll more pages
    i=0
    while i<=1:
        html = browser.find_element_by_tag_name('html')
        '''
        The code in the next line takes the page to end. Since in YouTube if you want more
        videos to load, you have to scroll down to the end of the page
        '''
        html.send_keys(Keys.END)
        time.sleep(3)
        i+=1
        
    v_l = browser.find_elements_by_xpath('//*[@id="video-title"]')
    link = []
    for i in v_l:
        link.append(i.get_attribute('href'))
        
    #Use a print statement to check if all the links are present properly before moving on the scraping part    
       
    wait = WebDriverWait(browser,15)
    df = pd.DataFrame(columns = ['Link','Title','URL','Views','Likes','Dislikes','Subcount','Date','Days','Score','Tags'])
    k=0
    for x in link:
        try:
            i = 0
            browser.get(x)
            time.sleep(3)
            v_link = x
            v_title = wait.until(EC.presence_of_element_located((By.XPATH,'//h1[@class="title style-scope ytd-video-primary-info-renderer"]'))).text
            v_views = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/div[5]/div[2]/ytd-video-primary-info-renderer/div/div/div[1]/div[1]/yt-view-count-renderer/span[1]'))).text
            try:    
                v_views = int(v_views.strip(' views').replace(',', '', 2))
            except:
                v_views = 1
            v_likes = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'ytd-toggle-button-renderer.ytd-menu-renderer:nth-child(1) > a:nth-child(1) > yt-formatted-string:nth-child(2)'))).text
            v_dislikes = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'ytd-toggle-button-renderer.style-scope:nth-child(2) > a:nth-child(1) > yt-formatted-string:nth-child(2)'))).text
            
            #if (v_likes == 0 & v_dislikes == 0):
                #v_like_dislike = 0
            
            #Likes
            try:
                if (operator.contains(v_likes,'K')):
                    if(operator.contains(v_likes,'.')):
                        pos = len(v_likes)-v_likes.find('.')-1 #length from the end
                        a1 = v_likes.replace('.', '', 1)
                        num = (int(a1[:len(a1)-1])*1000)/(10**(pos-1))
                        v_likes = num
                    else:
                        v_likes=int(v_likes[ :len(v_likes)-1])*(1000)
                elif operator.contains(v_likes,'M'):
                    if(operator.contains(v_likes,'.')):
                        pos = len(v_likes)-v_likes.find('.')-1 #length from the end
                        a1 = v_likes.replace('.', '', 1)
                        num = (int(a1[:len(a1)-1])*1000000)/(10**(pos-1))
                        v_likes = num
                    else:
                        v_likes=int(v_likes[ :len(v_likes)-1])*(1000000)
                else:
                    v_likes = int(v_likes)
            except:
                v_likes = 1

            #Dislikes
            try:
                if (operator.contains(v_dislikes,'K')):
                    if(operator.contains(v_dislikes,'.')):
                        pos = len(v_dislikes)-v_dislikes.find('.')-1 #length from the end
                        a1 = v_dislikes.replace('.', '', 1)
                        num = (int(a1[:len(a1)-1])*1000)/(10**(pos-1))
                        v_dislikes = num
                    else:
                        v_dislikes=int(v_dislikes[ :len(v_dislikes)-1])*(1000)
                elif operator.contains(v_dislikes,'M'):
                    if(operator.contains(v_dislikes,'.')):
                        pos = len(v_dislikes)-v_dislikes.find('.')-1 #length from the end
                        a1 = v_dislikes.replace('.', '', 1)
                        num = (int(a1[:len(a1)-1])*1000000)/(10**(pos-1))
                        v_dislikes = num
                    else:
                        v_dislikes=int(v_dislikes[ :len(v_dislikes)-1])*(1000000)
                else:
                    v_dislikes = int(v_dislikes)
            except:
                v_dislikes = 1
            
            v_like_dislike = ((v_likes-v_dislikes)/v_likes)
            
            v_subcount = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="owner-sub-count"]'))).text
            v_subcount = v_subcount.strip(" subscribers")
            try:
                if operator.contains(v_subcount,'M'):
                    if(operator.contains(v_subcount,'.')):
                        pos = len(v_subcount)-v_subcount.find('.')-1 #length from the end
                        a1 = v_subcount.replace('.', '', 1)
                        num = (int(a1[:len(a1)-1])*1000000)/(10**(pos-1))
                        v_subcount = num
                    else:
                        v_subcount=int(v_subcount[ :len(v_subcount)-1])*(1000000)
                elif operator.contains(v_subcount,'K'):
                    if(operator.contains(v_subcount,'.')):
                        pos = len(v_subcount)-v_subcount.find('.')-1 #length from the end
                        a1 = v_subcount.replace('.', '', 1)
                        num = (int(a1[:len(a1)-1])*1000)/(10**(pos-1))
                        v_subcount = num
                    else:
                        v_subcount = int(v_subcount[ :len(v_subcount)-1])*(1000)
                else:
                    v_subcount = int(float(v_subcount))
            except:
                v_subcount = 1
            v_urls = browser.find_elements_by_xpath('//div[@class="ytp-cued-thumbnail-overlay-image"]')
            for i in v_urls:
                v_url=i.get_attribute('style')[23:-3]
                break
            v_date = browser.find_element_by_xpath("//div[@id='date']").text
            if(operator.contains(v_date,'Premiered')):
                v_date = v_date[10:]
            elif(operator.contains(v_date,'Streamed live on')):
                v_date = v_date[17:]

            v_date = v_date[1:].replace(",","",1)
            v_days = number_of_days(v_date)
        
            try:
                url = x
                html_content = urlopen(url)
                soup = BeautifulSoup(html_content,'lxml')
                v_tags = [tag["content"] for tag in soup.findAll("meta",property="og:video:tag")]
            except:
                print('Error')
            co = 0
            
            for tl in tag_list:
                for t in v_tags:
                    if operator.contains(t, tl):
                        co+=1
            v_tag = co/(len(tag_list))
            
            # Score formula
            try:
                v_score = (((70*v_views)/700000) + (50*(v_likes/19000)) - (20*(v_dislikes/370)) + (160*v_like_dislike) +(20*(v_views/v_days)/7000)+(30*(v_likes/v_days)/200) + (12 * v_tag))/43
            except:
                v_days = 1
                v_likes = 1
                v_score = (((70*v_views)/700000) + (50*(v_likes/19000)) - (20*(v_dislikes/370)) + (160*v_like_dislike)+(20*(v_views/v_days)/7000)+(30*(v_likes/v_days)/200) + (12 * v_tag))/43
            
            
            print('{}: {}/{} ,{} , {:.2f}'.format(url,co,len(tag_list),v_tag,v_score))
            #This statement is for printing all the links every time it is extracted

            
            df.loc[len(df)] = [v_link,v_title,v_url,v_views,v_likes,v_dislikes,v_subcount,v_date,v_days,v_score,v_tags]
            k
            k+=1
            print(k)
        #Exception added since some YouTube ads bypass the adblock
        except Exception as e:
            print(e)
            continue
    df = df.sort_values(by='Score', ascending = 0)
    return df
    browser.close()

n = int(input("How many Links would you like to print? "))
df1 = search()
df = df1.nlargest(n,'Score')
print(df)
