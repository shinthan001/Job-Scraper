import time
import random
import logging

def random_sleep():
       sleep_time = random.randint(10,20)
       time.sleep(sleep_time)
       logging.warning('Sleeping for {} seconds.\n'.format(sleep_time))