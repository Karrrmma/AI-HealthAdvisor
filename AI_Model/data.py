from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# URL and browser setup
url = 'https://www.nhsinform.scot/illnesses-and-conditions/a-to-z/'

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

service = Service(executable_path='./chromedriver')
driver = webdriver.Chrome(service=service, options=options)

# Batch settings
batch_size = 5  # Number of items to process per batch
skip_count = 37  # Start index
csv_file = 'nhs_conditions_batch_data.csv'

# Data structure to hold results
data = []

try:
    driver.get(url)
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'li')))

    while True:
        # Refresh the list of <li> elements at the start of each batch
        all_elements = driver.find_elements(By.TAG_NAME, 'li')

        if skip_count >= len(all_elements):
            print("All items processed. Exiting.")
            break

        # Process a batch of elements
        batch_end = min(skip_count + batch_size, len(all_elements))
        print(f"Processing batch: {skip_count} to {batch_end - 1}")

        for index in range(skip_count, batch_end):
            try:
                current_item = all_elements[index]
                link = current_item.find_element(By.TAG_NAME, 'a')
                link_text = link.text
                print(f"Clicking on item {index}: {link_text}")
                link.click()

                # Wait for content to load
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'wp-block-heading')))
                content_elements = driver.find_elements(By.XPATH, './/h2 | .//p')

                # Initialize a dictionary for this condition
                page_data = {
                    "Condition Name": link_text,
                    "About": "",
                    "Symptoms": "",
                    "Causes": "",
                    "Diagnosis": ""
                }

                # Group <p> content under <h2> headings
                current_feature = "About"
                for element in content_elements:
                    if element.tag_name == 'h2':
                        heading_text = element.text.strip().lower()
                        if "symptom" in heading_text:
                            current_feature = "Symptoms"
                        elif "cause" in heading_text:
                            current_feature = "Causes"
                        elif "diagnose" in heading_text or "diagnosis" in heading_text:
                            current_feature = "Diagnosis"
                        else:
                            current_feature = "About"
                    elif element.tag_name == 'p':
                        page_data[current_feature] += element.text.strip() + " "

                # Append the condition data to the list
                data.append(page_data)

                # Go back and refresh the list
                driver.back()
                wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'li')))

            except Exception as e:
                print(f"Error processing item {index} ({link_text}): {e}")
                time.sleep(5)  # Short delay before retrying next item

            time.sleep(1)  # Short delay between items

        # Save data to CSV after completing a batch
        print(f"Saving batch {skip_count // batch_size + 1} to CSV...")
        pd.DataFrame(data).to_csv(csv_file, index=False)
        print(f"Batch {skip_count // batch_size + 1} saved to {csv_file}.")

        # Update skip_count to move to the next batch
        skip_count = batch_end
        time.sleep(2)  # Short pause before starting the next batch

finally:
    driver.quit()
    print("Browser session closed.")

# Final save to CSV
df = pd.DataFrame(data)
df.to_csv(csv_file, index=False)
print(f"Final data saved to {csv_file}")
