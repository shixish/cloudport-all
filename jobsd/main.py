#!/usr/bin/python

"""
Using pyinotify, watch for new incoming jobs.
Using pexpect, start jobs in order rec'd. When one finishes,
Using _mysql, update the database as appropos. 

This should just continue looping forever.
"""
# GLOBALS:
root_dir = "/var/www-django/jobsd"
log_file = "{0}/jobs_log".format(root_dir)
path_to_stdout = "{0}/jobs_finished".format(root_dir)
path_to_errout = "{0}/jobs_errors".format(root_dir)
path_to_uploads = "{0}/jobs_uploads".format(root_dir)

import pyinotify
import os
import sys
import MySQLdb as db
from jobman import *
from base_settings import * #imports the sensitive settings


if __name__ == "__main__":
    #try:
    #    dbconnection = db.connect('localhost', 'username', 'password', 'database')
    #    cur = dbconnection.cursor()
    #except db.Error, e:
    #    log_msg("Database fatal: {0}: {1}".format(e.args[0], e.args[1]), 2)

    log_msg("-------- System Started Up ------------")
    random.seed()
    mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE  # watched events

    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, EventHandler())
    #wdd = wm.add_watch('/tmp', mask, rec=True)
    wdd = wm.add_watch('/var/www-django/jobsd/jobs_uploads', mask, rec=True)

    notifier.loop()
