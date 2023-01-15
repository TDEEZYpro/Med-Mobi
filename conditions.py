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

# Accepting web cookies
def accepting_cookies(driver):
  # getting a website
    driver.get("https://nidirect.gov.uk/campaigns/illnesses-and-conditions")

    #accepting cookies
    cookie = driver.find_element(By.XPATH,"//*[@id='popup-buttons']/button[1]")
    time.sleep(1)
    cookie.click()

all_info = []
#searching for a disease and getting all the disease a person might possibly have
def searching_web(name):
  accepting_cookies(driver)
  #accessing the search bar in the website
  search = driver.find_element(By.ID, 'edit-query')

  #searching for a condition on the website
  search.send_keys(name)
  search.send_keys(Keys.RETURN)
  time.sleep(10)

  # list all disease might possibly have
  all_disease = driver.find_elements(By.CLASS_NAME,"card__title")
 
  # show all possible diseases 
  for disease in all_disease:
    print(disease.text)
  print("These are all the diseases based on the symptoms you've searched")
  disease_Name = input("Please type the name of the disease as it is, e.g Whooping cough or Hay fever: ").capitalize()
  
  # show all possible diseases based on symptoms
  time.sleep(3)
  for disease in all_disease:
  
    if(disease_Name == disease.text):
      driver.find_element(By.LINK_TEXT, disease_Name).click()

      if(disease_Name == "Cough"):
        wait = WebD(driver, 100)
        #checks if there's content
        main = wait.until(EC.presence_of_element_located((By.ID,"main-content")))
        #finds the html or css that contains the content
        articles = main.find_elements(By.ID,"main-article")

        for article in articles:
          # Name of the disease
          heading = article.find_element(By.CLASS_NAME,"page-title")
          all_info.append(heading.text)

          # summary of the disease
          summary = article.find_element(By.CLASS_NAME,"page-summary")
          all_info.append(summary.text)

          # causes 
          symptom = article.find_element(By.ID,"toc-3")
          all_info.append(symptom.text)

          symptom1 = article.find_element(By.CSS_SELECTOR,"body > div:nth-child(6) > main:nth-child(4) > article:nth-child(1) > ul:nth-child(26)")
          all_info.append(symptom1.text)

          # treatment
          treatment = article.find_element(By.ID,"toc-0")
          all_info.append(treatment.text)

          treat = article.find_element(By.CSS_SELECTOR,"body > div:nth-child(6) > main:nth-child(4) > article:nth-child(1) > ul:nth-child(8)")
          all_info.append(treat.text)

      else:

        wait = WebD(driver, 100)
        #checks if there's content
        main = wait.until(EC.presence_of_element_located((By.ID,"main-content")))
        #finds the html or css that contains the content
        articles = main.find_elements(By.ID,"main-article")

        for article in articles:
          # Name of the disease
          heading = article.find_element(By.CLASS_NAME,"page-title")
          all_info.append(heading.text)

          # summary of the disease
          summary = article.find_element(By.CLASS_NAME,"page-summary")
          all_info.append(summary.text)

          # symptoms
          symptom = article.find_element(By.ID,"toc-0")
          all_info.append(symptom.text)
        
          symptoms2 = article.find_elements(By.CSS_SELECTOR,"body > div:nth-child(6) > main:nth-child(4) > article:nth-child(1) > ul:nth-child(9)")
          for symptom in symptoms2:
            all_info.append(symptom.text)

          
        
          # treatment
          treatment = article.find_element(By.ID,"toc-2")
          all_info.append(treatment.text)

          treat = article.find_element(By.CSS_SELECTOR,"body div[role='presentation'] main[id='main-content'] article[id='main-article'] p:nth-child(1)")
          all_info.append(treat.text)

          treat2 =article.find_element(By.CSS_SELECTOR,"body div[role='presentation'] main[id='main-content'] article[id='main-article'] p:nth-child(1)")
          all_info.append(treat2.text)

      # To display specific information from the web
      for i in all_info:
        print(i)
      return i



search_Name = input("Please enter your condition or symptoms ")

if(len(search_Name)==0):
  search_Name = "Please enter your condition or symptoms"
  driver = headless_window()
  web_search = searching_web(search_Name)

else:
  driver = headless_window()
  web_search = searching_web(search_Name)

time.sleep(5)