import bs4
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import requests

# Creating a directory to save images
folder_name = 'D:/Project/Project-Celebrity Face Detection - v2/Data Collection/downloads2'
if not os.path.isdir(folder_name):
    os.makedirs(folder_name)


# Initialize Chrome WebDriver without specifying executable_path
driver = webdriver.Chrome()

# Navigate to Google
driver.get("https://www.google.com")

# Find the search input element by name and enter keywords
search = driver.find_element(By.NAME, 'q')
key_words = "Chris Hemsworth with glasses"
quantity = 10  # Replace with the desired quantity
search.send_keys(key_words, Keys.ENTER)

# Click on the "Images" tab using explicit wait
elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Images")))
elem.click()

# Scroll down to load more images
value = 0
for _ in range(20):
    driver.execute_script("scrollBy(" + str(value) + ", 1000);")
    value += 1000
    time.sleep(1)


#Scrolling all the way up
driver.execute_script("window.scrollTo(0, 0);")

time.sleep(3)

# Define the number of images to download
num_images_to_click = 20
downloaded_images = 0


# image result using the specified class selector
image_results = driver.find_elements(By.CSS_SELECTOR, '.Q4LuWd.rg_i')
time.sleep(3)

enlarged_image = driver.find_elements(By.CSS_SELECTOR, '.qmmlRd.n4hgof')

for image_result in image_results:
   try: 
      # Use ActionChains to perform a click action
      ActionChains(driver).move_to_element(image_result).click().perform()
    
      # Wait for a moment before moving to the next image (you can adjust this time)
      time.sleep(3)
    
      # Wait for the enlarged image to appear
      enlarged_image = driver.find_element(By.CSS_SELECTOR, '.r48jcc.pT0Scc.iPVvYb')
    
      image_url = enlarged_image.get_attribute('src')

      # Generate a unique filename for the image
      filename = os.path.join(folder_name, f"image{downloaded_images + 1}.jpg")

      # Download and save the image
      response = requests.get(image_url)
      if len(response.content) > 10240:
        with open(filename, 'wb') as file:
          file.write(response.content)
          downloaded_images += 1

   except Exception as e:
        # Handle the "no such element" exception
        print(f"Exception: {e}")
        continue  # Continue to the next image
  
# Close the WebDriver when done
driver.quit()