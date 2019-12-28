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


def advanced_players():  # returns advanced player dictionary of {name : point} pairs
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
        dict = {key[:-1] if key[-1] == ' ' else key: value
                for key, value in dict.items()}
        return space_sanitizer(dict)



def premier_in_advanced_standings():  # returns premier players in advanced
    premier_data = get_premier_ids()
    advanced_data = space_sanitizer()
    advanced_name_list = list(advanced_data.keys())
    premier_name_list = list(premier_data.keys())
    advanced_in_premier = intersect(advanced_name_list, premier_name_list)
    return advanced_in_premier


def space_sanitizer(adict):
    my_dictionary = {key[:-1] if key[-1] == ' ' else key: value
                     for key, value in adict.items()}
    return my_dictionary


def remove_premier_from_advanced(adict: dict):
    premier_players_in_advanced = premier_in_advanced_standings()
    for i in premier_players_in_advanced:
        del adict[i]
    return adict


def get_premier_ids():  # returns premier players dict with {name: id} pairs
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

def premier_name_and_points():
    a = {}
    prem_dict = get_premier_ids()
    for i in prem_dict.values():
        l = get_points(i)
        print(l)
        a[l[0]] = l[1]
    return l


def premier_name_list():  # returns list of premier player names
    return list(get_premier_ids().keys())


def get_points(player_id):  # returns a list containing premier player data of [player name, player points]
    head = webdriver.ChromeOptions()
    head.headless = True
    path = "/Users/jakeheidman/PycharmProjects/untitled/chromedriver"
    ll = []
    driver = webdriver.Chrome(executable_path=path, options=head)
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
    print(splitter)
    split2 = splitter[1].split('Depreciated Points Total: ')
    print(split2)
    return split2


def name_to_id(player_name):  # returns the id of a player name
    id_dict = get_premier_ids()
    try:
        player_id = id_dict[player_name]
    except:
        print("Player Not Found")
    else:
        print("Player Found")
        return player_id


def intersect(a, b):  # returns intersection of 2 lists
    """ return the intersection of two lists """
    return list(set(a) & set(b))


print(premier_name_and_points())
