from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from collections import Counter

#IMPORTANT! Webscrapers are legal, but not all sites allow it, I am NOT responsible for how you use this code.
#Respect the website's robots.txt file and Terms of Service to avoid any legal issues - Jim Versteeg
def setup_driver_with_profile():
    user_data_dir = r"C:\Users\'USERNAME'\AppData\Local\Google\Chrome\User Data"  #Replace 'USERNAME' with your actual user path
    profile_dir = "Profile 1"  #Replace with your specific profile directory (Usaully "Profile" or "Profile 1" or "Default")

    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument(f"--profile-directory={profile_dir}")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


def block_user(driver, creator_username):
    account_url = f"https://9gag.com/u/{creator_username}" #
    driver.get(account_url)

    try:
        #Wait for the page to load, also important to not overload a site
        time.sleep(2)

        #Click the options menu button on the page of the user
        options_button = driver.find_element(By.XPATH, '//*[@id="main"]/div[1]/div/div[2]/div/div/div[1]/a')
        options_button.click()

        #Wait for the dropdown menu to appear
        time.sleep(1)

        #Click the block button
        block_button = driver.find_element(By.XPATH, '//*[@id="main"]/div[1]/div/div[2]/div/div/div[2]/ul/li[3]/a')
        block_button.click()

        #Wait for the confirmation button to appear
        time.sleep(1)

        #Confirm the block action
        confirm_button = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div[2]/div/button[2]')
        confirm_button.click()

        print(f"Blocked user: {creator_username}")

    except Exception as e:
        print(f"Failed to block user {creator_username}: {e}")


def fetch_post_data_creator_no_duplicates():
    driver = setup_driver_with_profile()  #Use the profile-configured driver instead of a new one
    url = "https://9gag.com/fresh" #You can also change this to https://9gag/com/trending instead
    driver.get(url)

    driver.implicitly_wait(5)

    post_data = []
    creators = []
    visited_links = set()
    scroll_pause_time = 2
    max_posts = 500

    try:
        while len(post_data) < max_posts:
            elements = driver.find_elements(By.CLASS_NAME, "badge-evt.badge-track")
            for element in elements:
                title = element.text.strip()
                href = element.get_attribute("href")

                if title and href and href not in visited_links:
                    visited_links.add(href)

                    driver.execute_script("window.open(arguments[0], '_blank');", href)
                    driver.switch_to.window(driver.window_handles[-1])

                    time.sleep(1)

                    try:
                        creator_element = driver.find_element(By.CLASS_NAME, "creator")
                        creator_name = creator_element.find_element(By.TAG_NAME, "a").text.strip() if creator_element else "Unknown Creator"
                        creators.append(creator_name)

                    except Exception as e:
                        creator_name = f"Error scraping creator: {e}"

                    post_data.append({
                        "title": title,
                        "link": href,
                        "creator": creator_name,
                    })

                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

                if len(post_data) >= max_posts:
                    break

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)

        creator_counts = Counter(creators)


        for creator, count in creator_counts.items():
            if count >= 4:  #Block users with atleast X amount of posts
                print(f"User {creator} appears {count} times. Blocking...")
                block_user(driver, creator)

        return post_data, creator_counts

    finally:
        driver.quit()


#Fetch and print post data with creator counts
post_data, creator_counts = fetch_post_data_creator_no_duplicates()
if post_data:
    print("Scraped Data:")
    for idx, post in enumerate(post_data, start=1):
        print(f"{idx}. Title: {post['title']}")
        print(f"   Link: {post['link']}")
        print(f"   Creator: {post['creator']}")

    print("\nCreator Mentions:")
    sorted_creators = sorted(creator_counts.items(), key=lambda x: x[1], reverse=True)
    for creator, count in sorted_creators:
        print(f"{creator}: {count} times")
else:
    print("No posts found. Check the page structure or class names.")

