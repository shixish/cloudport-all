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

from cloudport.settings import JOB_LOG_FILE
from cloudport.settings import JOB_ERROR_DIR
from cloudport.settings import JOB_UPLOAD_DIR
from cloudport.settings import JOB_FINISHED_DIR
from cloudport.dispatcher.signals import job_done
from cloudport.dispatcher.signals import job_start
from django.dispatch import receiver

def log_msg(message, lvl=1):
    """
    Log some message to the global log file
    """
    global JOB_LOG_FILE
    lvl_code = { 1: "INFO", 2: "EROR" }
    if len(message) < 1:
        return
    with open(JOB_LOG_FILE, "a") as f:
        f.write("{0} ({1}): {2}\n".format(datetime.datetime.utcnow(), 
                                         lvl_code[lvl], 
                                         message))
    return

@receiver(job_start)
def job_is_start(sender, event, **kwargs):
    log_msg("JOB START EVENT! %s"%event)

"""
These are the modules which handle jobs. They have the same
name as their job filename extension.
Modules so far: 
    sce    scilab
    py     python

"""
def sce(data):
    """
    Handle .sce and .sci files (scilab)
    """
    #global JOB_LOG_FILE
    #global ROOT_DIR
    #global PATH_TO_STDOUT
    #global PATH_TO_ERROUT
    #path_to_output = "{0}/{1}".format(PATH_TO_STDOUT, job_id)
    #path_to_err_output = "{0}/{1}_err".format(PATH_TO_ERROUT, job_id)
    #log_msg("Using output path {0}".format(path_to_output))
    #tmp_cmd = "scilab-adv-cli"        
    #os.chdir(PATH_TO_STDOUT)
    #log_msg("Spawning {0} with pexpect for job id {1}".format(tmp_cmd, job_id))
    #child = pexpect.spawn(tmp_cmd)
    #child.expect('-->')
    ## NOTE: This is not exec in a shell, which would be dangerous
    ## This is exec within the scilab context, which is benign
    #child.sendline('exec "{0}"'.format(path_to_file))
    ## Now just wait for EOF
    #child.expect(pexpect.EOF)
    #log_msg("Job id {0} completed.".format(job_id))

import subprocess

def py(data):
    # Need some way of keeping users from uploading harmful scripts:
    # Perhaps change user to nobody group nobody
    # TODO TODO TODO
    path = data["directory"]+data["file"]
    subprocess.Popen(['python', path], cwd=data["directory"])
    log_msg("executing: %s"%['python', path])
    pass

import cPickle
import shutil

class EventHandler(pyinotify.ProcessEvent):
    """
    When a new file is detected in /jobs_uploads, this is called. 
    Determine the correct module,
    call it with pexpect, and 
    process results.
    """
    def process_IN_CREATE(self, event):
        error = False;
        try:
            data = cPickle.load(open(event.pathname, "rb"))
            #data = {"file":"test.py", "ext":"py"}
            log_msg("EventHandler recieved data {0}.".format(data))
            module_list = { "sce" : sce, "py" : py } # the main list of modules
            job_id = random.randint(1,9999999999999) # TODO: from the database
            try:
                module_list[data["ext"]](data)
            except Exception as e:
                log_msg("Cannot find a module for file extension {0}.".format(data["ext"]), 2)
                log_msg("Bad {0}".format(e.args[0]), 2)
                error = True
        except:
            log_msg("Invalid input file {0}.".format(event.pathname), 2)
            error = True
        
        basename = os.path.basename(event.pathname)
        if error:
            shutil.move(event.pathname, os.path.join(JOB_ERROR_DIR, basename))
        else:
            shutil.move(event.pathname, os.path.join(JOB_FINISHED_DIR, basename))
        
        #job_start.send(sender="job", event={'test':'ok'})
        job_done.send(sender="something", event={'test':'ok'});
        
        #basepath, extension = os.path.splitext(event.pathname)
        #module_list = { ".sce" : sce, ".py" : py } # the main list of modules
        #job_id = random.randint(1,9999999999999) # TODO: from the database
        #log_msg("EventHandler recieved filename {0} for module {1}.".format(basepath, extension))
        #try:
        #    module_list[extension](event.pathname, job_id)
        #except Exception as e:
        #    log_msg("Cannot find a module for file extension {0}.".format(extension), 2)
        #    log_msg("{0} - {1}".format(e.args[0], e.args[1]), 2)


#import time
#while 1:
#    time.sleep(1)