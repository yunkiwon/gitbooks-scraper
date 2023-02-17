
from utils import Gitbook
import argparse 
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup



if __name__ == "__main__": 
    parser = argparse.ArgumentParser()    
    urls = [
      "https://docs.convexfinance.com/convexfinance/" 
    ] 

    for url in urls: 
        Gitbook.get_menu(url)

    # use a docs frontend to break up tasks into different endpoints: 
    # 
    
