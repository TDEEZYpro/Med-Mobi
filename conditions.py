from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as WebD
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time


#headles browsing
def headless_window():
  #install chromedriver or any driver that accommodates the browser that you are using
  #put it in windows C in program files
  PATH = "C:\Program Files (x86)\chromedriver.exe"
  # instance of Options class allows
  # us to configure Headless Chrome
  options = Options()
    
  # this parameter tells Chrome that
  # it should be run without UI (Headless)
  options.headless = True

  # initializing webdriver for Chrome with our options
  tDriver = webdriver.Chrome(PATH,options=options)
  return tDriver


#array to hold all the content
all_videos_title = []


def getting_info(driver, name):
  # getting a website
  driver.get("https://nidirect.gov.uk/campaigns/illnesses-and-conditions")
  #accessing the search bar in the website
  search = driver.find_element(By.ID, 'edit-query-health-az')

  #accepting cookies
  acept = driver.find_element(By.XPATH,"//*[@id='popup-buttons']/button[1]")
  time.sleep(1)
  acept.click()

  #searching for a condition on the website
  search.send_keys(name)
  search.send_keys(Keys.RETURN)
  # clicking a link
  ele = driver.find_element(By.XPATH,"//*[@id='health-conditions-results']/ol/li[1]/h3/a")
  time.sleep(1)
  ele.click()


  wait = WebD(driver, 100)
  #checks if there's content
  main = wait.until(EC.presence_of_element_located((By.ID,"main-content")))
  #finds the html or css that contains the content
  articles = main.find_elements(By.TAG_NAME,"article")
  return articles

def get_info(arti):
  #prints all content on that page
  for article in arti:
    dea = article.find_element(By.CSS_SELECTOR,"#main-article > h1")
    all_videos_title.append(dea.text)
    #getting short description about the condition
    header = article.find_element(By.XPATH,"//*[@id='main-article']/div[2]")
    all_videos_title.append(header.text)

    #getting the list of symptoms
    sympMains = article.find_element(By.CSS_SELECTOR,"#main-article > p:nth-child(8)")
    all_videos_title.append(sympMains.text)

    symptoms = article.find_element(By.XPATH,"//*[@id='main-article']/ul[1]")
    all_videos_title.append(symptoms.text)
    
    treatment = article.find_element(By.ID,"toc-2")
    all_videos_title.append(treatment.text)

    treat1 = article.find_element(By.XPATH,"//*[@id='main-article']/p[14]")
    all_videos_title.append(treat1.text)
    treat2 = article.find_element(By.XPATH,"//*[@id='main-article']/p[15]")
    all_videos_title.append(treat2.text)
    treat3 = article.find_element(By.XPATH,"//*[@id='main-article']/p[16]")
    all_videos_title.append(treat3.text)
  for i in all_videos_title:
    print(i)
  return i


searchNam = input("enter condition or symptoms: ")

if (len(searchNam) == 0):
  searchNam = input("enter condition or symptoms: ")
  driver = headless_window()
  articles = getting_info(driver, searchNam)
  info = get_info(articles)
else:
  driver = headless_window()
  articles = getting_info(driver, searchNam)
  info = get_info(articles)