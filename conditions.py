from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as WebD
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
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



all_info=[]
def search_results(driver, name):
 
  # getting a website
  driver.get("https://nidirect.gov.uk/campaigns/illnesses-and-conditions")
  #accessing the search bar in the website
  search = driver.find_element(By.ID, 'edit-query-health-az')

  #accepting cookies
  cookie = driver.find_element(By.XPATH,"//*[@id='popup-buttons']/button[1]")
  time.sleep(1)
  cookie.click()

  #searching for a condition on the website
  search.send_keys(name)
  search.send_keys(Keys.RETURN)
  time.sleep(10)


  title =[]
  symptoms = []
  # getting the title
  title =driver.find_elements(By.XPATH,"//*[@id='health-conditions-results']/ol/li/h3/a")
  symptoms = driver.find_elements(By.XPATH,"//*[@id='health-conditions-results']/ol/li/div[1]/ul/li")
  for i, s in zip(title, symptoms):
    # try:

    if(i.text == name):
      # clicking a link
      link = driver.find_element(By.XPATH,"//*[@id='health-conditions-results']/ol/li/h3/a")
      time.sleep(1)
      link.click()

      wait = WebD(driver, 100)
      #checks if there's content
      main = wait.until(EC.presence_of_element_located((By.ID,"main-content")))
      #finds the html or css that contains the content
      articles = main.find_elements(By.TAG_NAME,"article")
      
      for article in articles:
        #getting short description about the condition
        descrip = article.find_element(By.XPATH,"//*[@id='main-article']/div[2]")
        all_info.append(descrip.text)

        #getting the list of symptoms
        symptom = article.find_element(By.CSS_SELECTOR,"#main-article > p:nth-child(8)")
        all_info.append(symptom.text)

        symptoms = article.find_element(By.XPATH,"//*[@id='main-article']/ul[1]")
        all_info.append(symptoms.text)
        
        treatment = article.find_element(By.ID,"toc-2")
        all_info.append(treatment.text)

        treat1 = article.find_element(By.XPATH,"//*[@id='main-article']/p[14]")
        all_info.append(treat1.text)
        treat2 = article.find_element(By.XPATH,"//*[@id='main-article']/p[15]")
        all_info.append(treat2.text)
        treat3 = article.find_element(By.XPATH,"//*[@id='main-article']/p[16]")
        all_info.append(treat3.text)
      for i in all_info:
        print(i)
      return i
      
    elif(s.text == name.lower()):
      # clicking a link
      link = driver.find_element(By.XPATH,"//*[@id='health-conditions-results']/ol/li/h3/a")
      time.sleep(1)
      link.click()

      wait = WebD(driver, 100)
      #checks if there's content
      main = wait.until(EC.presence_of_element_located((By.ID,"main-content")))
      #finds the html or css that contains the content
      articles = main.find_elements(By.TAG_NAME,"article")

      for article in articles:
        heading = article.find_element(By.CSS_SELECTOR,"#main-article > h1")
        all_info.append(heading.text)
        #getting short description about the condition
        descrip = article.find_element(By.XPATH,"//*[@id='main-article']/div[2]")
        all_info.append(descrip.text)

        #getting the list of symptoms
        symptom = article.find_element(By.CSS_SELECTOR,"#main-article > p:nth-child(8)")
        all_info.append(symptom.text)

        symptoms = article.find_element(By.XPATH,"//*[@id='main-article']/ul[1]")
        all_info.append(symptoms.text)
        
        treatment = article.find_element(By.ID,"toc-2")
        all_info.append(treatment.text)

        treat1 = article.find_element(By.XPATH,"//*[@id='main-article']/p[14]")
        all_info.append(treat1.text)
        treat2 = article.find_element(By.XPATH,"//*[@id='main-article']/p[15]")
        all_info.append(treat2.text)
        treat3 = article.find_element(By.XPATH,"//*[@id='main-article']/p[16]")
        all_info.append(treat3.text)
      for i in all_info:
        print(i)
      return i

    elif (i.text != name):
      i ="I'm sorry, that term is not available on this website"
      print(i) 
      break
   
searchNam = input("enter condition or symptoms: ").capitalize()

if (len(searchNam) == 0):
  searchNam = input("enter condition or symptoms: ").capitalize()
  driver = headless_window()
  articles = search_results(driver, searchNam)
  
else:
  driver = headless_window()
  articles = search_results(driver, searchNam)
 


