#!/bin/bash

#################################################################################################
#	Script generates default entries into cccp-index/index.yml for the CentOs-Dockerfiles.	#
#												#
#	Author : Mohammed Zeeshan Ahmed (mohammed.zee1000@gmail.com)				#
#################################################################################################

# Globals : 

centosdfpath=$1;
git_url=$2;
git_branch=$3;
notify_email=$4;

function err(){
	mode=$1;
	exitc=1;
	errmsg="";

	case $mode in
		INDEX_INCORRECT)
			errmsg="The path specified as the index file is not a file or does not exist.";
			exitc=2;
		;;
		INVAL_DFPATH)
			errmsg="The location specified for centos dockerfiles path is invalid.";
			exitc=3;
		;;	
	esac	

	echo -e "ERROR : $errmsg";
	exit $exitc;
}

function indexentry(){
	# Usage: indexentry mode id appid jobid gitpath
	mode=$1;
	theid=$2;
	app_id=$3;
	job_id=$4;
	git_path=$5;
	echo "$git_path"; #TEST

	indexpath="./index.yml"; # The path of the index.yml file. Please set this before running this script.
	tmpfile="/tmp/$RANDOM";

	case $mode in
		CHK_INDEXPATH)   # Mode checks if indexpath value points to a file.
			if [ -f $indexpath ]; then
				# If index path exists then its fine.
				return;		
							
			fi
			# Ask user to set the value.
			err INDEX_INCORRECT;
		;;
		GEN_ENTRY)
			#entry="- id\t\t: $theid\n";
			entry="app-id\t: $app_id\n";
			entry+="job-id\t: $job_id\n";
			entry+="git-url\t: $git_url\n";
			entry+="git-path\t: $git_path\n";
			entry+="git-branch\t: $git_branch\n";
			entry+="notify-email: $notify_email\n";
			echo -e $entry >> $tmpfile;
			sed -e 's/^/  /' -i $tmpfile;
			content=$(cat $tmpfile);
			echo -en "- id\t\t: $theid\n$content" > $tmpfile;
			sed -e 's/^/  /' -i $tmpfile;
			#cat $tmpfile; #TEST;
			cat $tmpfile >> $indexpath;
			echo >> $indexpath;
		;;
	esac
	
}

function genindexentry(){

        mode=$1;
        project=$2;


        case $mode in
                OSV)
			echo "** generating indx entry for $project $osversion...";
                        osversion=$3;
                        t="?"; # Temp variable, used below to get first character from osversion
                        JOBID="${osversion%"${osversion#${t}}"}${osversion: -1}-$project" # JOBID = FirstChar(osversion)LastChar(osversion)-PROJECTNAME
			git_path="$project/$osversion/";


                ;;
                DIRECT)
			echo "** generating indx entry for $project No OS Version associated ...";
                        JOBID="centos-dockerfile-$project";
			git_path="$project/"
                ;;
        esac
	#echo "$git_path"; #TEST
	indexentry GEN_ENTRY "default" "centos" $PROJECT $JOBID "$git_path";
}

function usage(){
	echo "USAGE $0 <CENTOSDOCKERFILEPATH> <GITURL> <GITBRANCH> <NOTIFYEMAIL>";
	exit 5000;
}

# MAIN BEGINS


# Check if parameters were passed.
if [ $# -lt 4  ]; then
	usage;
fi

proceed="z";
while true; do
        echo;
        echo "Please ensure that the indexpath value has been set in the script";
        printf "Proceed with generation (y/n) : ";
        read proceed;
        #echo $proceed; #TEST
        echo
        if [ "$proceed" = "y" ]; then
                break;
        elif [ "$proceed" = "n" ]; then
                exit 0;
        fi
done

indexentry CHK_INDEXPATH;

# Check if path is a valid directory
if [ ! -d $centosdfpath ]; then

	err INVAL_DFPATH; # Inform user of invalid path

fi

# Check every project directory in the Centos-Dockerfiles
for project in `ls $centosdfpath`; do
         #echo $project; # TEST
        if [ -d $centosdfpath/$project  ]; then

                echo "Found project : $project, getting in..."
                ls $centosdfpath/$project | grep centos &> /dev/null; # Check if centosX directories are present in the project dir

                # if there is a match process os versions
                if [ $? -eq 0 ]; then

                        echo "* Project contains centosX where X is a version, switching to osversion mode...";

                        for osversion in `ls $centosdfpath/$project`; do

                                genindexentry OSV $project $osversion;

                        done
                else
                        echo "* Project does not contain centosX directories, switching to direct mode...";
                        genindexentry DIRECT $project;
                fi
        fi
        echo;
done

