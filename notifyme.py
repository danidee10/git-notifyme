import argparse
from datetime import datetime, timedelta
import sys
import subprocess
import time
import os

# Because i didn't want to use a global variable to keep track of current_hash and update it
#TODO Fix this when i'm not tired as f**k
hashes = {
    'current_hash': None,
    'latest_hash': None
}

# experimental decorator to execute thread after n seconds
def execute_every(interval):
    def decorator(func):
        def wrapper(*args, **kwargs):
            return threading.Timer(interval, func)
        return wrapper
    return decorator


extract_info = {
    'commiter': '--format=%cn',
    'commiter_email': '--format=%ce',
    'commit_date': '--format=%cr',
    'commit_subject': '--format=%s',
    'author_name': '--format=%an'
}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('repo', type=str, nargs='+')
    parser.add_argument('--remote', type=str, default='origin',
                        help='Remote url of the repo, defaults to origin')
    parser.add_argument('--branch', type=str, default='master',
                        help='Repository branch to watch, defaults to master')
    parser.add_argument('--interval', type=str,
                        help='Interval to check for updates, format is hh:mm:ss')

    args = parser.parse_args()
    repo, remote, branch, interval = args.repo, args.remote, args.branch, args.interval
    remote = remote + '/' + branch

    return repo, remote, branch, interval

def interval_to_secs(interval):
    #convert interval to seconds
    try:
        interval = datetime.strptime(interval, '%H:%M:%S')
    except ValueError:
        print('Invalid interval, interval should be in this format "hh:mm:ss"')
        sys.exit(1)

    interval = timedelta(hours=interval.hour, minutes=interval.minute, seconds=interval.second)
    interval  = interval.total_seconds()

    return interval

def check_for_updates(repo, remote):

    # fetch from remote and get hash again
    subprocess.check_output(['git fetch {}'.format(remote.split('/')[0])], cwd=repo, shell=True)
    latest_hash = subprocess.check_output(['git rev-parse {}'.format(remote)], cwd=repo, shell=True)
    hashes['latest_hash'] = latest_hash.decode('utf-8').strip('\n')

    if hashes['latest_hash'] != hashes['current_hash']:
        hashes['current_hash'] = hashes['latest_hash']

        commiter, committer_email, commit_subject = get_commit_details(repo)

        message = "New commit(s) on {}\nCommiter: {}Commiter email: {}Subject: {}".format(os.path.basename(repo), commiter, committer_email, commit_subject)

        subprocess.call(['notify-send', message])

def get_commit_details(repo):
    commiter = subprocess.check_output(['git log -1 {}'.format(extract_info['commiter'])], cwd=repo, shell=True).decode('utf-8')
    commiter_email = subprocess.check_output(['git log -1 {}'.format(extract_info['commiter_email'])], cwd=repo, shell=True).decode('utf-8')
    commit_subject = subprocess.check_output(['git log -1 {}'.format(extract_info['commit_subject'])], cwd=repo, shell=True).decode('utf-8')

    return commiter, commiter_email, commit_subject

def main():
    repos, remote, branch, interval = parse_args()
    interval = interval_to_secs(interval)

    while True:
        print('==========checking for updates=============')
        for repo in repos:
            check_for_updates(repo, remote)

        time.sleep(interval)


if __name__ == '__main__':
    main()
