#
# Includes for the job manager
#

import getpass # getpass.getuser() returns the username
import pexpect
import pyinotify
import os
import sys
#import _mysql
import MySQLdb as db
import random
import datetime
#import jobman

# GLOBALS:
root_dir = "/var/www-django/jobsd"
log_file = "{0}/jobs_log".format(root_dir)
path_to_stdout = "{0}/jobs_finished".format(root_dir)
path_to_errout = "{0}/jobs_errors".format(root_dir)
path_to_uploads = "{0}/jobs_uploads".format(root_dir)

def log_msg(message, lvl=1):
    """
    Log some message to the global log file
    """
    global log_file
    lvl_code = { 1: "INFO", 2: "EROR" }
    if len(message) < 1:
        return
    with open(log_file, "a") as f:
        f.write("{0} ({1}): {2}".format(datetime.datetime.utcnow(), 
                                         lvl_code[lvl], 
                                         message))
    return

"""
These are the modules which handle jobs. They have the same
name as their job filename extension.
Modules so far: 
    sce    scilab
    py     python

"""
def sce(path_to_file, job_id):
    """
    Handle .sce and .sci files (scilab)
    """
    global log_file
    global root_dir
    global path_to_stdout
    global path_to_errout
    path_to_output = "{0}/{1}".format(path_to_stdout, job_id)
    path_to_err_output = "{0}/{1}_err".format(path_to_errout, job_id)
    log_msg("Using output path {0}".format(path_to_output))
    tmp_cmd = "scilab-adv-cli"        
    os.chdir(path_to_stdout)
    log_msg("Spawning {0} with pexpect for job id {1}".format(tmp_cmd, job_id))
    child = pexpect.spawn(tmp_cmd)
    child.expect('-->')
    # NOTE: This is not exec in a shell, which would be dangerous
    # This is exec within the scilab context, which is benign
    child.sendline('exec "{0}"'.format(path_to_file))
    # Now just wait for EOF
    child.expect(pexpect.EOF)
    log_msg("Job id {0} completed.".format(job_id))


def py(path_to_file, job_id):
    # Need some way of keeping users from uploading harmful scripts:
    # Perhaps change user to nobody group nobody
    global root_dir
    global log_file
    global path_to_stdout
    global path_to_errout
    # TODO TODO TODO 
    pass

#class EventHandler(pyinotify.ProcessEvent):
#    """
#    When a new file is detected in /jobs_uploads, this is called. 
#    Determine the correct module,
#    call it with pexpect, and 
#    process results.
#    """
#    print "EventHandler initialized..."
#    print "Running as user {0}".format(getpass.getuser())
#    def process_IN_CREATE(self, event):
#        basepath, extension = os.path.splitext(event.pathname)
#        module_list = { ".sce" : sce, ".py" : py } # the main list of modules
#        job_id = random.randint(1,9999999999999) # TODO: from the database
#        log_msg("EventHandler recieved filename {0} for module {1}.".format(path_to_file, extension))
#        try:
#            module_list[extension](event.pathname, job_id)
#        except Exception as e:
#            log_msg("Cannot find a module for file extension {0}.".format(extension), 2)
#            log_msg("{0} - {1}".format(e.args[0], e.args[1]), 2)

import threading
#infile = file("transfer", "r")

import atexit

class InputThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        atexit.register(self.cleanup) #not sure this really does anything...
    
    def run(self):
        while 1:
            print("waiting for data...")
            self.f = file("transfer", "r")
            messege = self.f.readlines() #this will wait for new messages to come through
            self.f.close()
            print("recieved:{0}".format(messege))
            
    def cleanup(self):
        try:
            self.f.close()
        except: #cant close the file, it's not open yet
            pass

t = InputThread()
t.setDaemon(True)
t.start()


import time
try:
    while 1:
        time.sleep(100)
except:
    #t.cleanup()
    pass
    