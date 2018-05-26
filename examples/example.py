"""Example Case of the Script"""

import sys
sys.path.insert(0, '..')

from instapy import InstaPy

# if you don't provide arguments, the script will look for INSTA_USER and INSTA_PW in the environment
session = InstaPy(username='feitoamaocom', password='123itap')

"""Logging in"""
# logs you in with the specified username and password
session.login()
    
# you can put in as much tags as you want, likes 100 of each tag
session.like_by_tags(['feitoamao'], amount=10)


session.unfollow_users(
    amount=10)  # unfollows 10 of the accounts your following -> instagram will only unfollow 10 before you'll be 'blocked
#  for 10 minutes' (if you enter a higher number than 10 it will unfollow 10, then wait 10 minutes and will continue then)


"""Extras"""
# Reduces the amount of time under sleep to a given percentage
# It might be useful to test the tool or to increase the time for slower connections (percentage > 100)
session.set_sleep_reduce(20)


"""Ending the script"""
# clears all the cookies, deleting you password and all information from this session
session.end()
