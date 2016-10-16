import argparse
from datetime import datetime, timedelta
import sys
import threading
from functools import wraps


# experimental decorator to execute thread after n seconds
def execute_every(interval):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return threading.Timer(interval, func)
        return wrapper
    return decorator



def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=str,
                        help='Repository to watch, defaults to origin')
    parser.add_argument('--branch', type=str, default='master',
                        help='Repository branch to watch, defaults to master')
    parser.add_argument('--interval', type=str,
                        help='Interval to check for updates, format is hh:mm:ss')

    args = parser.parse_args()
    repo, branch, interval = args.repo, args.branch, args.interval

    return repo, branch, interval

def parse_args(repo, branch, interval):
    repository = repo + '/' + branch

    #convert interval to seconds in python
    try:
        interval = datetime.strptime(interval, '%H:%M:%S')
    except ValueError:
        print('Invalid interval, interval should be in this format "hh:mm:ss"')
        sys.exit(1)

    interval = timedelta(hours=interval.hour, minutes=interval.minute, seconds=interval.second)
    print(interval.total_seconds())



if __name__ == '__main__':
    repo, branch, interval = get_args()
    parse_args(repo, branch, interval)
