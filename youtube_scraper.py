from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install(version="latest")))


service = Service(ChromeDriverManager(driver_version="139.0.7258.155").install())


# driver = webdriver.Chrome(service=service)
# driver.get("https://www.youtube.com/results?search_query=farming+technology")


# search_box = driver.find_element(By.NAME, "search_query")
# search_box.send_keys("farming technology")  # type text
# search_box.submit()  # press Enter
# wait = WebDriverWait(driver, 30)
def web_scraper(query, max_results):
 
 options = webdriver.ChromeOptions()
 
 options.add_argument("--headless=new")
 driver = webdriver.Chrome(service=service, options=options)
 driver.get(f"https://www.youtube.com/results?search_query={query}")
 wait = WebDriverWait(driver, 20)
 try:
  videos_tab = wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//yt-chip-cloud-chip-renderer//div[text()="Videos"]')
))
  videos_tab.click()
  last_height = driver.execute_script("return document.documentElement.scrollHeight")
  # while len(data) < max_results:
  for i in range(2):
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(4)  # wait for new videos to load

        data = []
        
        # videos = driver.find_elements(By.XPATH, '//ytd-video-renderer')
        # if len(videos) >= max_results:
        #     break

  # wait.until(EC.presence_of_element_located((By.ID, "video-title")))
#   wait.until(EC.presence_of_all_elements_located((By.ID, "video-title")))
#   videos = driver.find_elements(By.ID, "video-title")
#   descriptions = driver.find_elements(
#     By.CSS_SELECTOR, "yt-formatted-string.metadata-snippet-text.style-scope.ytd-video-renderer"
# )


#   for i in range(20):
#      video = driver.find_elements(By.ID, "video-title")[i]
#      desc = driver.find_elements(By.CSS_SELECTOR,
#         "yt-formatted-string.metadata-snippet-text.style-scope.ytd-video-renderer")[i]

#      contents = driver.find_elements(By.ID, "content")
    #  for idx, content in enumerate(contents):
    #   print(f"\n--- Content Block {idx+1} ---")
    # # Find all <a> links inside this block
    #   links = content.find_elements(By.TAG_NAME, "a")
        
        wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'ytd-item-section-renderer')))
        videos = driver.find_elements(By.TAG_NAME, 'ytd-item-section-renderer')
         
        
        for v1 in videos[:max_results]:
         for v in v1.find_elements(By.TAG_NAME, 'ytd-video-renderer'):
          try:
           title = v.find_element(By.ID, 'video-title')
           
           title1 = title.get_attribute('title')
           
          
           
           
           
                
           link = title.get_attribute('href')
    #        descriptions = v.find_element(
    #  By.XPATH, './/div//yt-formatted-string[contains(@class, "metadata-snippet-text")]')
           descriptions=WebDriverWait(v,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'yt-formatted-string.metadata-snippet-text.style-scope.ytd-video-renderer')))
           
    #        descriptions = v.find_element(
    #  By.CSS_SELECTOR, "div.yt-formatted-string.metadata-snippet-container.style-scope.ytd-video-renderer yt-formatted-string.metadata-snippet-text.style-scope.ytd-video-renderer")
           desc = descriptions.text
          
                  
                
                
           data.append({'title' :title1,
        
        
        'link':link, 
        'description': desc

     })
           
          
           
      
          except Exception as e:
            print('error extracting video data:', e)  
          
          # except Exception as e:
          #  print('error extracting video data:', e) 
       
            
     
    #  print(desc.text)
    #  print("-"*60)

  
 except Exception as e:
  print("Error:", e)    
 finally:
    driver.quit()
 df = pd.DataFrame(datas for datas in data)
  
 
# C:/Users/PC/Downloads/chromedriver-1/chromedriver-win64/chromedriver.exe
 return df






