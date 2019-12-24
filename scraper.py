import csv
import _tkinter

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

class Player:
    def __init__(self, name, id, points):
        self.name = name
        self.id = id
        self.points = points


def advanced_scrape():
    url = "https://docs.google.com/spreadsheets/d/1yLuwRyMC5N3eQps45PXoBHbrgcpZ3f27hi8xrHQVkdc/export?gid=1166083124&format=csv"
    namelist = []
    dict = {}

    with requests.Session() as s:
        download = s.get(url)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            namelist.append(row[0])
            dict[row[0]] = row[27]

        namelist.remove("SUM of Individual Points")
        namelist.remove("Name ")
        del dict["SUM of Individual Points"]
        del dict["Name "]

        print(dict)


def get_player_ids():
    url = "https://docs.google.com/spreadsheets/d/11WMW3yc-FADmU_Hreh3G0xXip_dPhUrFM_BmdCW56M4/export?gid=1270909778&format=csv"
    id_dict = {}

    with requests.Session() as s:
        download = s.get(url)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        count = 0
        for row in my_list:
            if count != 0:
                id_dict[row[1]] = int(row[0])
            count += 1

        return id_dict


def get_points(player_id):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")

    driver = webdriver.Chrome("/Users/jakeheidman/PycharmProjects/untitled/chromedriver")
    driver.get("https://tournaments.spikeball.com/pages/stats?playerId=1")
    textbox = driver.find_element_by_id('playerId')
    textbox.send_keys(player_id)
    submit_button = driver.find_element_by_id('submitButton')
    submit_button.click()
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # print(soup.find("div", {"id": "playerDataFieldData"}))
    playerDataFieldData = soup.find("div", {"id": "playerDataFieldData"})
    text = playerDataFieldData.text
    splitter = text.split('Name: ')
    split2 = splitter[1].split('Depreciated Points Total: ')
    print(split2)


def playertopoints(player_name):
    id_dict = get_player_ids()
    try:
        player_id = id_dict[player_name]
    except:
        print("Player Not Found")
    else:
        print("Player Found")
        return player_id


print(get_points(playertopoints("Tyler Cisek")))
