import sys
#sys.path.insert(0, '..')  # imports from parent folder
import random
import psutil

import os
import multiprocessing
import datetime
import time
import json
import demjson

from instapy import InstaPy
from instapy import util
# from util import update_activity
from bs4 import BeautifulSoup  
from selenium import webdriver
# from __future__ import print_function

pool= multiprocessing.Pool(processes=(multiprocessing.cpu_count() - 2))





def wait():
    while True:
        time.sleep(15)
        cpu=float(os.popen('''grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }' ''').readline())
        mem = psutil.virtual_memory().percent
        if cpu < 40 and mem < 40:
            break

class Payload(object):
    def __init__(self, d):
        self.__dict__ = d


def worker(sel):
    print("MULTI - Started as", sel.username, "at",datetime.datetime.now().strftime("%H:%M:%S"))
    session = InstaPy(username=sel.username,password=sel.password,headless_browser=True)
    session.login()
    time.sleep(2)
    
    
    session.set_dont_include(sel.friends)
    session.set_smart_hashtags(sel.tags, limit=3, sort='top', log_tags=True)
    time.sleep(2)
    if(sel.currentlyFollowing>2500):
        print(sel.username+'is following more than 2500 (',sel.currentlyFollowing,')')
        session.unfollow_users(amount=random.randint(444, 666), sleep_delay=(random.randint(44, 111)))
        time.sleep(2)
        print("MULTI -", sel.username, "finished unfollowing at", datetime.datetime.now().strftime("%H:%M:%S"))
    # session.set_dont_unfollow_active_users(enabled=True, posts=6)
    # session.set_do_follow(enabled=True, percentage=25, times=2)
    # session.set_user_interact(amount=5, randomize=True,percentage=25, media='Photo')
        
    else:
        time.sleep(2)
        session.set_relationship_bounds(enabled=True,
                        potency_ratio=-1.1,
                        delimit_by_numbers=True,
                        max_followers=666,
                        max_following=5555,
                        min_followers=11,
                        min_following=11)
        
        time.sleep(2)
    
        session.like_by_tags(sel.tags, amount=random.randint(sel.likes/2-50, sel.likes/2+50))


            #, use_smart_hashtags=False)

        session.follow_user_followers(sel.usersToFollowFollowers, amount=random.randint(sel.follows-50, sel.follows+50), randomize=True, interact=True, sleep_delay=random.randint(100, 300))
        print("MULTI -", sel.username, "finished following followers at", datetime.datetime.now().strftime("%H:%M:%S"))


    time.sleep(2)
    
    session.end()
    print("MULTI -", instaUser[sel], "finished run at",datetime.datetime.now().strftime("%H:%M:%S"))





    #session.like_by_locations(sel.location, amount=sel.likesLocation)
    # print("MULTI -", instaUser[sel], "finished liking by location",
    #       datetime.datetime.now().strftime("%H:%M:%S"))


    # session.like_by_feed(amount=random.randint(
    #     likes/2-50, likes/2+50), randomize=True, unfollow=True, interact=True)
#    print("MULTI -",instaUser[sel],"finished liking by feed at",datetime.datetime.now().strftime("%H:%M:%S"))


#     print("MULTI -",instaUser[sel],"finished instaTags at",datetime.datetime.now().strftime("%H:%M:%S"))




def UpdateData():
    driver = webdriver.Chrome('./assets/chromedriver')

    print("Updating Data -", "Starting at", datetime.datetime.now().strftime("%H:%M:%S"))
        # jobs = []
    try:
        with open('data.json') as data_file:
            data = json.load(data_file)
            data_file.close()

            data_file = open("data.json", "r") # Open the JSON file for reading
            newData = json.load(data_file) # Read the JSON into the buffer
            data_file.close() # Close the JSON file

            for i, element in enumerate(data):

                p = Payload(element)
                # print(p.username)
                driver.get("https://www.instagram.com/"+p.username)
                soup = BeautifulSoup(driver.page_source,"html.parser")

                time.sleep(1)
                for title in soup.select("._h9luf"):   
                    posts = title.select("._fd86t")[0].text
                    follower = title.select("._fd86t")[1]['title']
                    following = int(title.select("._fd86t")[2].text.replace(',',''))
                    newData[i]["currentlyFollowing"]=following


                    print("User: {} Posts: {} Follower: {} Following: {} Time: {}".format(p.username,posts,follower,following,datetime.datetime.now().strftime("%H:%M:%S")))

            data_file = open("data.json", "w+")
            data_file.write(json.dumps(newData))
            data_file.close()
            driver.quit()
    except (ValueError, KeyError, TypeError):
        print("JSON format error")

if __name__ == '__main__':
    while True:
        wait()
        UpdateData()
        print("MULTI -", "Starting at", datetime.datetime.now().strftime("%H:%M:%S"))
        jobs = []
        try:
            with open('data.json') as data_file:
                data = json.load(data_file)
                for element in data:
                    p = Payload(element)
                    wait()
                    process = multiprocessing.Process(target=worker, args=(p,))
                    wait()
                    jobs.append(process)
                    wait()
                    process.start()
                    wait()

                for job in jobs:
                    job.join()
                    
        except (ValueError, KeyError, TypeError):
            print("JSON format error")
            sys.exit()
