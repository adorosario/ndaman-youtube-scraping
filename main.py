from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import re
import csv
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

# -------------------------TO GET THE YOUTUBE VIDEO URL AND SAVE TO A CSV-----------------------------

chrome_option = webdriver.ChromeOptions()
chrome_option.add_experimental_option("detach", True)
key_phrase = input("input keypharse: ")
driver = webdriver.Chrome(options=chrome_option)
driver.maximize_window()
driver.get(f"https://www.youtube.com/results?search_query={key_phrase}+tutorial")
sleep(2)
videos = driver.find_elements(By.CSS_SELECTOR,"div#scroll-container #text")[2].click()
sleep(3)
x = 0
while True:
    x+=1
    driver.execute_script("scrollBy(0,500)")
    sleep(0.5)
    # try:
    #     element = driver.find_element(By.CSS_SELECTOR,"#message.style-scope.ytd-message-renderer")
    # except NoSuchElementException:
    #     continue
    if x > 120:
        break
vid_links = driver.find_elements(By.CSS_SELECTOR,"a#video-title")
print(len(vid_links))
with open("vid_url.csv", "w") as file:
    writer = csv.writer(file)
    for link in vid_links:
        video_link = link.get_attribute("href")
        if video_link is not None:
            video_link = video_link.strip()
            if video_link:
                writer.writerow([video_link])
driver.quit()


#---------------------------- TO GET THE YOUTUBE URL AND JASPER URL-------------------------------
# Open the CSV file containing video URLs
#
# # Open the CSV file containing video URLs
with open("vid_url.csv", "r") as file:
    all_list = file.readlines()

# Set up Chrome WebDriver
chrome_option = webdriver.ChromeOptions()
chrome_option.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_option)
driver.maximize_window()

# Open the output CSV file to append data
with open("testing.csv", "w", newline="") as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['KEY PHRASE','CHANNEL NAME','CHANNEL LINK','VIDEO TITTLE','VIEWS','SUBSCRIBERS','DATE OF POST','YOUTUBE VIDEO URL','JASPER URL',])
    # Loop over each video URL in the list
    for v_link in all_list:
        v_link = v_link.strip()  # Remove any leading/trailing whitespace
        driver.get(v_link)
        sleep(3)
        driver.execute_script("scrollBy(0,500)")
        sleep(3)
        # getting the mettedata
        try:
            video_tittle = driver.find_element(By.CSS_SELECTOR,"h1.style-scope.ytd-watch-metadata .style-scope.ytd-watch-metadata").text
            channel = driver.find_element(By.CSS_SELECTOR,"a.yt-simple-endpoint.style-scope.yt-formatted-string")
            channel_name = channel.text
            subscribers = driver.find_element(By.CSS_SELECTOR,"#owner-sub-count").text
            views = driver.find_elements(By.CSS_SELECTOR,"span.bold.style-scope.yt-formatted-string")[0].text
            date_of_post = driver.find_elements(By.CSS_SELECTOR,"span.bold.style-scope.yt-formatted-string")[2].text
        except:
            continue
        keypharse = f"'{key_phrase}'"
        channel_link = channel.get_attribute("href")
        try:
            see_more = driver.find_element(By.CSS_SELECTOR, "#expand").click()
            sleep(2)
            vid_description = driver.find_element(By.CSS_SELECTOR,
                                                  ".style-scope.ytd-text-inline-expander span.yt-core-attributed-string.yt-core-attributed-string--white-space-pre-wrap")
        except:
            continue
        search_pharse = key_phrase.split(".")[0]
        # print(search_pharse)
        link_in_vid = vid_description.find_elements(By.TAG_NAME, "a")

        # Flag to check if a link has already been found for the current video
        link_found = False

        # Loop over each link in the video description
        for hrefs in link_in_vid:
            vid_txt = hrefs.text
            href = hrefs.get_attribute("href")
            if f"www.{search_pharse}" in vid_txt.lower() or f"/{search_pharse}" in vid_txt.lower():
                if "redirect" in href:
                    print(v_link)
                    # print(href)
                    # print(channel_name)
                    # print(subscribers)
                    # print(video_tittle)
                    # print(views)
                    # print(date_of_post)
                if not link_found:  # Check if a link has already been found for the current video
                    csv_writer.writerow([keypharse,channel_name,channel_link,video_tittle,views,subscribers,date_of_post,v_link, href,])  # Write to CSV file
                    link_found = True  # Set flag to True after finding the first link
            else:
               continue

        print("\n")

# Close the WebDriver
driver.quit()


