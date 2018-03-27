import sys
sys.path.insert(0, '..')  # imports from parent folder
import random

import os
import multiprocessing
import datetime
import time
import json
import demjson

from instapy import InstaPy
from instapy import util
# from util import update_activity


class Payload(object):
    def __init__(self, d):
        self.__dict__ = d


def worker(sel):
    print("MULTI - Started as", sel.username, "at",
          datetime.datetime.now().strftime("%H:%M:%S"))
    session = InstaPy(username=sel.username,
                      password=sel.password,
                      headless_browser=True)
    session.login()

    session.set_do_follow(enabled=True, percentage=25, times=2)
    session.set_dont_unfollow_active_users(enabled=True, posts=10)
    session.set_user_interact(amount=5, randomize=True,
                              percentage=25, media='Photo')

    session.set_lower_follower_count(limit=1)
    session.set_upper_follower_count(limit=250)
    session.set_dont_include(sel.friends)
    session.set_smart_hashtags(sel.tags, limit=3, sort='top', log_tags=True)

    # end setup

    session.unfollow_users(amount=random.randint(
        444, 666), sleep_delay=(random.randint(44, 111)))
    print("MULTI -", sel.username, "finished unfollowing at",
          datetime.datetime.now().strftime("%H:%M:%S"))

    session.follow_user_followers(sel.usersToFollowFollowers, amount=random.randint(
        sel.follows-50, sel.follows+50), randomize=True, interact=True, sleep_delay=random.randint(100, 300))

    print("MULTI -", sel.username, "finished following followers at",
          datetime.datetime.now().strftime("%H:%M:%S"))

    session.like_by_locations(sel.location, amount=sel.likesLocation)
    # print("MULTI -", instaUser[sel], "finished liking by location",
    #       datetime.datetime.now().strftime("%H:%M:%S"))

    session.like_by_tags(amount=random.randint(
        likes/2-50, likes/2+50), use_smart_hashtags=True)

    session.like_by_feed(amount=random.randint(
        likes/2-50, likes/2+50), randomize=True, unfollow=True, interact=True)
#    print("MULTI -",instaUser[sel],"finished liking by feed at",datetime.datetime.now().strftime("%H:%M:%S"))


#     print("MULTI -",instaUser[sel],"finished instaTags at",datetime.datetime.now().strftime("%H:%M:%S"))

    session.end()
    print("MULTI -", instaUser[sel], "finished run at",
          datetime.datetime.now().strftime("%H:%M:%S"))


if __name__ == '__main__':
    print("MULTI -", "Starting at", datetime.datetime.now().strftime("%H:%M:%S"))
    jobs = []
    try:
        with open('data.json') as data_file:
            data = json.load(data_file)
            for element in data:
                p = Payload(element)
                process = multiprocessing.Process(target=worker, args=(p,))
                jobs.append(process)
                process.start()
                # no delay cause some instances of chrome to give errors and stop
                time.sleep(188)
    except (ValueError, KeyError, TypeError):
        print("JSON format error")
