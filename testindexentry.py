#!/bin/python
import os
import sys
import yaml
from subprocess import check_call, CalledProcessError, call
import stat
import shutil

class TestConsts:
    testdir = os.path.abspath("./cccp-index-test")
    indxfile = os.path.abspath("./index.yml")

    if not os.path.exists(testdir):
        os.mkdir(testdir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

class MessageType:
    error = 1
    info = 2
    success = 3


class StaticHandler:

    @staticmethod
    def print_msg(messagetype, msg, testentry):

        pre_pmsg = ""
        pre_fmsg = ""

        if messagetype == MessageType.error:
            pre_pmsg = "\n \033[1;31m[ERROR]\033[0m "
            pre_fmsg = "ERROR\t"

        elif messagetype == MessageType.info:
            pre_pmsg = "\n \033[1;33m[INFO]\033[0m "
            pre_fmsg = "INFO\t"

        elif messagetype == MessageType.success:
            pre_pmsg = "\n \033[1;32m[SUCCESS]\033[0m "
            pre_fmsg = "SUCCESS\t"

        print pre_pmsg + msg
        print

        testentry.write_info(pre_fmsg + msg)

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

        if not gitpath.startswith("/"):
            gitpath = "/" + gitpath

        fnm = tid + "_" + appid + "_" + jobid
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

        self._cccp_test_dir = self._git_Data_Location + self._gitpath

        if not self._cccp_test_dir.endswith("/"):
            self._cccp_test_dir += "/"

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

            if StaticHandler.execcmd(cmd) or self._gitBranch == "master":
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
        """Run sanity checks on the cccp.yml file"""

        # FIXME : Finish this method

        # Map location of the cccp.yml file
        cccpyamlfilepath = ""

        StaticHandler.print_msg(MessageType.info, "Checking if a cccp.yml file exists at specified location", self)

        # Check if the cccp.yml file exists
        pthexists = False
        for itm in ["cccp.yml", ".cccp.yml", "cccp.yaml", ".cccp.yaml"]:

            cccpyamlfilepath = self._cccp_test_dir + itm

            if os.path.exists(cccpyamlfilepath):
                pthexists = True
                break

        if not pthexists:
            StaticHandler.print_msg(MessageType.error, "Missing cccp.yml file, skipping...", self)
            return

        StaticHandler.print_msg(MessageType.success, "Found cccp.yml file", self)

        # Check if the job id supplied matches with job id in cccp.yml
        with open(cccpyamlfilepath) as cccpyamlfile:
            cccpyaml = yaml.load(cccpyamlfile)

        StaticHandler.print_msg(MessageType.info, "Matching job id with one in cccp.yml", self)

#        print str.format("index jid : {0}\ncccp jid : {1}", self._jobid, cccpyaml["job-id"])

        if self._jobid == cccpyaml["job-id"]:

            StaticHandler.print_msg(MessageType.success, "Job id matched, continuing...", self)

        else:

            StaticHandler.print_msg(MessageType.error, "Job Ids dont match, skipping...", self)
            return



        return

    def run_tests(self):

        self._init_entries()

        if self._clone_repo():
            self._test_cccp_yaml()

        return

class Tester:

    def __init__(self):

        return

    def run(self):

        if os.path.exists(TestConsts.indxfile):

            with open(TestConsts.indxfile) as indexfile:
                indexentries = yaml.load(indexfile)

            i = 0

            for item in indexentries["Projects"]:

                if i > 0:

                    TestEntry(item["id"], item["app-id"], item["job-id"], item["git-url"], item["git-path"], item["git-branch"], item["notify-email"]).run_tests()
                    print "\nNext Entry....\n"

                i += 1

        return


def mainf():

    if len(sys.argv) <= 1:
        tester = Tester()
        tester.run()

    print "\nTests completed\n"
    print "You can view the test results at " + TestConsts.testdir + "/" + "[id]_[appid]_[jobid]/test.info\n"

if __name__ == '__main__':
    mainf()