import datetime
import time
from time import gmtime, strftime
import re
#import sys
#import glob

def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

if __name__ == '__main__':
    logfile = open("/var/log/ejabberd/ejabberd.log","r")
    loglines = follow(logfile)
    fail_keyword = 'ejabberd_c2s:659.*Failed authentication'
    accept_keyword = 'ejabberd_c2s:640.*Accepted authentication'
    failed_log = {} # dict for record down the failed login

    today = strftime("%Y-%m-%d")
    login_log = open("/var/log/ejabberd/login"+today+".log","w") # create new log for login attempts
    for line in loglines:
        curr_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        if re.search(fail_keyword, line):
            #print(line)
            info = line.split()
            user,vhost = info[6].split('@')
            ip_addr = info[9]
            #print(curr_time + " " + user + " " + ip_addr + " FAILED") # write this into a file later
            login_log.write(curr_time + " " + user + " " + ip_addr + " FAILED\n") # write this into a file later
            if user not in failed_log: # if user not in failed_log, create it with 0
                failed_log[user] = 0
            failed_log[user] += 1 # increase failed attempt here
            print(failed_log)
            if failed_log[user] > 5:
                print(curr_time + " " + user + "BANNED")
                # execute bash cammand ejabberdctl
                import subprocess
                # ejabberdctl ban-account max.chan im02.limadvisors.com fail_auth
                ban_cmd = "ejabberdctl ban-account" + user + " " + vhost + "fail_auth"
                subprocess.run(['ejabberdctl','ban-account',user,vhost,'fail_auth'])
                failed_log[user] = 0 # reset to 0

        if re.search(accept_keyword, line):
            #print(line)
            info = line.split()
            user = info[6]
            #print(curr_time + " " + user + " ACCEPTED")
            login_log.write(curr_time + " " + user + " ACCEPTED\n")
            if user not in failed_log: # if user not in failed_log, create it with 0
                failed_log[user] = 0
            failed_log[user] = 0 # reset to 0
            print(failed_log)
