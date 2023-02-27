
from utils import Gitbook
import argparse 
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
import json


if __name__ == "__main__": 
    parser = argparse.ArgumentParser()    
    # urls = [
    #   "https://docs.convexfinance.com/convexfinance/" 
    # ] 

    # for url in urls: 
    #     Gitbook.get_menu(url)
    with open("output.json") as f:
        data = json.load(f)
        formatted = Gitbook.get_menu(data)
        print(formatted)
        json.dump(formatted, open("formatted.json", "w"))
    # use a docs frontend to break up tasks into different endpoints: 
    # 
    
