from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import csv
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.get("https://www.pinksale.finance/launchpads?chain=BSC")

# Function to scroll down and load more content
def scroll_to_bottom():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Time to load properly
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Scroll to load all content
# scroll_to_bottom()

# Find all the coin elements
coins = driver.find_elements(By.CSS_SELECTOR, ".card-content")



# Testing with one of the links
coin_links = ['https://www.pinksale.finance/launchpad/0xA18f32533d79D8f5f1b590192A2C8470b66C7E02?chain=BSC']

# Extract links for each coin
# coin_links = []
# for coin in coins:
#     try:
#         # Find the "View" button within the current coin element
#         view_button = coin.find_element(By.CLASS_NAME, "view-button")

#         # Extract the href link from the "View" button
#         link = view_button.get_attribute("href")

#         coin_links.append(link)
#     except Exception as e:
#         print(f"An error occurred while extracting links: {str(e)}")

# creating  the csv file
csv_filename = 'crypto_data.csv'
csv_file = open(csv_filename, 'w', newline='')
csv_writer = csv.writer(csv_file)

# Define the header row for the CSV file
header = ['Presale Address', 'Token Name', 'Token Symbol', 'Total Supply', 'Tokens For Presale',
          'Tokens For Liquidity', 'Initial Market Cap', 'Soft Cap', 'Presale Start Time', 'Presale End Time']
csv_writer.writerow(header)

# Loop through each URL
for link in coin_links:
    # Open the link ina new tab
    driver.execute_script(f'window.open("{link}","_blank");')

    # Switch to the new tab
    driver.switch_to.window(driver.window_handles[-1])
    
    # time to load the page properly
    time.sleep(10) 

    try:
        # Wait for the needed elements to load
        presale_address = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="presale-address"]'))
        )

        token_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="token-name"]'))
        )

        token_symbol = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="token-symbol"]'))
        )

        total_supply = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="total-supply"]'))
        )

        tokens_for_presale = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="tokens-for-presale"]'))
        )

        tokens_for_liquidity = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="tokens-for-liquidity"]'))
        )

        initial_market_cap = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="initial-market-cap"]'))
        )

        soft_cap = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="soft-cap"]'))
        )

        presale_start_time = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="presale-start-time"]'))
        )

        presale_end_time = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="presale-end-time"]'))
        )

        # Extracting the data text
        data = [
            presale_address.text, token_name.text, token_symbol.text, total_supply.text,
            tokens_for_presale.text, tokens_for_liquidity.text, initial_market_cap.text,
            soft_cap.text, presale_start_time.text, presale_end_time.text
        ]

        # Write the data to the CSV file
        csv_writer.writerow(data)

    # Where i am stuck because , an error ocuured is what gets printed
    except:
        print(f"An error occurred")


# Close the CSV file after processing all URLs
csv_file.close()
       
driver.quit()