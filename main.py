from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Set up Chrome options to keep the browser open
chrome_option = webdriver.ChromeOptions()
chrome_option.add_experimental_option("detach", True)

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_option)
driver.get("http://orteil.dashnet.org/experiments/cookie/")

# Locate the cookie element
cookie = driver.find_element(By.ID, "cookie")

# Set intervals and game duration
click_interval = 0.1  # Click interval
check_upgrade_interval = 5  # Check for upgrades every 5 seconds
game_duration = 300  # Run the game for 5 minutes

# Start time to track game duration and interval for upgrades
start_time = time.time()
last_upgrade_check = start_time

try:
    while True:
        # Click the cookie
        cookie.click()

        # Check for upgrades every 5 seconds
        if time.time() - last_upgrade_check > check_upgrade_interval:
            last_upgrade_check = time.time()  # Reset the upgrade check time

            # Get current cookie count
            money = int(driver.find_element(By.ID, "money").text.replace(",", ""))
            # Get all items in the store
            store_items = driver.find_elements(By.CSS_SELECTOR, "#store b")

            # Dictionary to store affordable upgrades and their prices
            affordable_upgrades = {}

            for item in store_items:
                if item.text:
                    name_price = item.text.split(" - ")
                    if len(name_price) > 1:
                        item_name = name_price[0]
                        item_price = int(name_price[1].replace(",", ""))

                        # Check if the item is affordable
                        if money >= item_price:
                            affordable_upgrades[item_name] = item_price

            # If there are affordable upgrades, buy the most expensive one
            if affordable_upgrades:
                most_expensive_item = max(affordable_upgrades, key=affordable_upgrades.get)
                driver.find_element(By.ID, f"buy{most_expensive_item}").click()

        # Stop the bot after 5 minutes
        if time.time() - start_time > game_duration:
            break

    # Get and print the cookies per second (cps)
    cps = driver.find_element(By.ID, "cps").text
    print("Cookies per second:", cps)

finally:
    # Close the driver after the game ends
    driver.quit()
