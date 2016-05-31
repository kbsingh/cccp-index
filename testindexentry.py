#!/bin/python
import os
import sys
import yaml
from subprocess import check_call, CalledProcessError, call
import stat
import shutil

class TestConsts:
    testdir = os.path.abspath("./cccp-index-test")

    if not os.path.exists(testdir):
        os.mkdir(testdir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

class MessageType:
    error = 1
    info = 2
    success = 3


class StaticHandler:

    @staticmethod
    def print_msg(messagetype, msg, testentry):

        pre = ""

        if messagetype == MessageType.error:
            pre = "\n \033[1;31m[ERROR]\033[0m "

        elif messagetype == MessageType.info:
            pre = "\n \033[1;33m[INFO]\033[0m "

        elif messagetype == MessageType.success:
            pre = "\n \033[1;32m[SUCCESS]\033[0m "

        print pre + msg
        print

        testentry.write_info(msg)

        return

    @staticmethod
    def execcmd(cmd):

        success = True

        try:
            check_call(cmd)
            success = True

        except CalledProcessError:
            success = False

        return success

class TestEntry:

    def __init__(self, tid, appid, jobid, giturl, gitpath, gitbranch, notifyemail):

        fnm = tid + "_" + appid + "_" + "jobid"
        self._testLocation = TestConsts.testdir + "/" + fnm

        if os.path.exists(self._testLocation):
            shutil.rmtree(self._testLocation)

        os.mkdir(self._testLocation, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

        self.testinfo = self._testLocation + "/" + "test.info"

        self._id = tid
        self._appid = appid
        self._jobid = jobid
        self._giturl = giturl
        self._gitpath = gitpath
        self._gitBranch = gitbranch
        self._notifyEmail = notifyemail
        self._git_Data_Location = self._testLocation + "/" + "thegit"

        return

    def write_info(self, msg):
        """Allows outsiders to write to this Entries test.info file."""

        with open(self.testinfo, "a") as infofile:
            infofile.write("\n" + msg + "\n")

        return

    def _init_entries(self):

        info = str.format("ID : {0}\nAPP ID : {1}\nJOB ID : {2}\n", self._id, self._appid, self._jobid)
        print info
        info += "GIT : " + self._giturl + "\n"

        info += "######################################################################################################"
        info += "\n"

        with open(self.testinfo, "w") as infofile:
            infofile.write(info)

        return

    def _clone_repo(self):
        """Function attempts to clone the git repo associated with the entry"""

        success = True

        cmd = ["git", "clone", self._giturl, self._git_Data_Location]
        StaticHandler.print_msg(MessageType.info, "Attempting to clone repo", self)

        if StaticHandler.execcmd(cmd):
            StaticHandler.print_msg(MessageType.success, "Clone successful, going ahead...", self)
            currpath = os.path.abspath(".")
            os.chdir(self._git_Data_Location)

            StaticHandler.print_msg(MessageType.info, "Attempting to checkout branch...", self)

            cmd = ["git", "branch", self._gitBranch]

            if StaticHandler.execcmd(cmd):
                cmd = ["git", "checkout", self._gitBranch]
                call(cmd)
                StaticHandler.print_msg(MessageType.success, "Checked out requested branch", self)

            else:
                StaticHandler.print_msg(MessageType.error, "Could not find mentioned branch", self)
                success = False

            os.chdir(currpath)

        else:
            StaticHandler.print_msg(MessageType.error, "Git repo clone failed, skipping", self)
            success = False

        return success

    def _test_cccp_yaml(self):

        cccpyamlfilepath = self._git_Data_Location + self._gitpath + "cccp.yml"
        print

        StaticHandler.print_msg(MessageType.info, "Checking if a cccp.yml file exists at specified location", self)

        if not os.path.exists(cccpyamlfilepath):
            StaticHandler.print_msg(MessageType.error, "Missing cccp.yml file.", self)
            return

        StaticHandler.print_msg(MessageType.success, "Found cccp.yml file", self)


        return

    def run_tests(self):

        self._init_entries()

        if self._clone_repo():
            self._test_cccp_yaml()

        return

def mainf():
    t = TestEntry("a", "b", "c", "heel", "tata", "master", "hello@hello.com")
    t.run_tests()
    t = TestEntry("default", "bamachrn", "python", "https://github.com/bamachrn/cccp-python", "/", "bamachrn-test", "bamachrn@gmail.com")
    t.run_tests()
    # T

if __name__ == '__main__':
    mainf()