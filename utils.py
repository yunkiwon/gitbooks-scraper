from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import json 

# get link as input: 

# anchored HTML element: 

class Gitbook: 
    links = []
    def __init__(self) -> None:
        pass

    def get_menu(url):
        print(url) 
        driver = webdriver.Firefox()
        driver.get(url)

        # get menu items: 
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "nav")))

        # finds menu in selenium 
        def get_path(url):
            base_url_end_index = url.find("/", 8)  # Finds the index of the end of the base URL
            if base_url_end_index == -1:
                return "/"
            else:
                return url[base_url_end_index:]
        
        def select_menu(): 
            try: 
                time.sleep(1)
                # because gitbooks uses dynamic classnames, we need to find an anchor attribute that won't change: 
                anchor = driver.find_elements(By.XPATH, "//div[@data-testid='page.desktopTableOfContents']")[0]
                # find item by aref reference to "/" while also ignoring hidden mobile menu 
                home_link = anchor.find_elements(By.XPATH, f"//a[@href='{base}' and @data-rnwrdesktop-fnigne='true']")[0]
                # now we have the main Table of Contents by desktop view 
                menu_item = home_link.find_element(By.XPATH, "./../..")
                return menu_item 
            except: 
                print("Error, or No menu found")
                return        

        def is_same_path(reference: str) -> bool:
            # Remove the scheme (http, https, etc.) from the URLs
            anchor_no_scheme = url.replace("http://", "").replace("https://", "")
            reference_no_scheme = reference.replace("http://", "").replace("https://", "")

            # Find the first slash in each URL, which marks the end of the netloc (host and port)
            anchor_slash_index = anchor_no_scheme.find("/")
            reference_slash_index = reference_no_scheme.find("/")

            # Extract the paths from each URL
            anchor_path = anchor_no_scheme[anchor_slash_index:]
            reference_path = reference_no_scheme[reference_slash_index:]

            # Check if the reference path is a sub-path of the anchor path
            return reference_path.startswith(anchor_path) 


        # base = get_path(url)
        def expand(index=0):
            # we need to repetitively scrape and identify the buttons each recursive run because their positions change
            # as elements are clicked. 
            # finds all expand buttons in menu:
            try:
                menu_item = select_menu()
                # find all svg elements (aka buttons) inside the menu 
                buttons = menu_item.find_elements(By.TAG_NAME, "svg")
                # end condition -- aka we've clicked all the buttons available on the screen:  
                if index > len(buttons)-1: 
                    return 
                currButton = buttons[index]
                link = currButton.find_element(By.XPATH, "./../..").get_attribute("href")
                # if the link is not part of the same subdomain, then we don't need to expand it:
                if not is_same_path(link): 
                    expand(index+1)
                    return
                driver.execute_script("arguments[0].scrollIntoView();", currButton)
                # need method here to make sure the button doesn't link to an outer page: 
                currButton.click()
                expand(index+1)
                return 
            except: 
                print("Error, or No buttons found")
                return

        def get_links(): 
            # finds all links in menu: 
                # because gitbooks uses dynamic classnames, we need to find an anchor attribute that won't change: 
                urls: list = []
                menu_item = select_menu()
                links = menu_item.find_elements(By.TAG_NAME, "a")
                for link in links: 
                    url = link.get_attribute("href")
                    print(url)
                    if is_same_path(url):
                        urls.append(url)
                return urls
                
        expand()
        urls = get_links()
        output = {}
        print(urls) 

        def build_url_dict(urls):
        # create an empty dictionary to store the results
            result = {}
            # iterate over the URLs and split them into components
            for url in urls:
                components = [x for x in url.split("/") if x !=""][3:]  # ignore the protocol, domain, and empty first component
                print(components) 
                # iterate over the components and add them to the dictionary
                current_dict = result
                for component in components:
                    if component not in current_dict:
                        current_dict[component] = {"text": ""}
                    current_dict = current_dict[component]
            return result



        struct = build_url_dict(urls)

        def scrape(subdomain): 
            link = url + subdomain 
            driver.get(link)
            # get menu items: 
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "nav"))) 
            anchor = driver.find_elements(By.TAG_NAME, "main")[0]
            # find item by aref reference to "/" while also ignoring hidden mobile menu 
            # return all text of this element: 
            text = anchor.text
            return text
            # now we have the main Table of Contents by desktop view 

        # recursive loop to traverse through output and create a link, then scrape the link. how do we actually fucking scrape this stuff? 
        def scrape_over_nested(d, func, prev=''): 
            for k, v in d.items(): 
                if isinstance(v, dict): 
                    route = prev + k + "/"
                    scrape_over_nested(v, func, route)
                else: 
                    d = func(prev) 


        # def formatter(obj): 
        #     temp = obj 
        #     for k, v in temp.items(): 
        #         if isinstance(v, dict) & len(v) > 1: 
        #             v = formatter(v)
        #             v["summary"] = v["text"]
        #             v.pop("text", None)
        #             return v 
        #         elif isinstance(v, dict): 
        #             temp[k] = v["text"]
        #         else: 
        #             return 
        #     return temp 
        
        scrape_over_nested(struct, scrape)
        driver.close()
        print(struct)
        json.dump(struct, open("output.json", "w"))
        return struct 
    
    def scrape(url): 
        driver = webdriver.Firefox()
        driver.get(url)
        # get menu items: 
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "nav"))) 
        anchor = driver.find_elements(By.TAG_NAME, "main")[0]
        # find item by aref reference to "/" while also ignoring hidden mobile menu 
        # return all text of this element: 
        text = anchor.text
        driver.close()
        return text
    