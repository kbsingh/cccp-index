The CentOS Community Container Pipeline
=======================================

This pipeline takes an arbitary Nulecule defined container application on the internet and builds it, tests it and delivers it according to the wishes of the author. This resource is available to anyone on the internet ( with their code hosted at github or otherwise ). We welcome all content, legal and distributeable in the USA.

Amongst other things, one key value of using the pipeline is that it will track when dependancies and content consumed in your container app have updates, and inform you. It can optionally rebuild, test and let you know results when security updates are available.

       -----------    -----------    ------------    -----------    ----------
       |         |    |         |    |          |    |         |    |        |
       |   Git   |--->|  Build  |--->|   Test   |--->| Deliver |--->|Maintain|
       |         |    |         |    |          |    |         |    |        | 
       -----------    -----------    ------------    -----------    ----------

You can read more about AtomicApp, Container Applications and the Nulecule specification at [https://github.com/projectatomic/nulecule](https://github.com/projectatomic/nulecule)

Examples of what these applications and specifications look like are available at

- [https://github.com/projectatomic/nulecule-library](https://github.com/projectatomic/nulecule-library)
- [http://github.com/projectatomic/nulecule/examples](http://github.com/projectatomic/nulecule/examples)

Quickstart
----------

 1. Clone this git repo in github.com
 2. Take the cccp.yml file included in this repo and drop it into the same directory as the Nulecule definition for your app
 3. Populate the cccp template
 4. Send a Pull Request to this git repo with your details added into the index file

If you need help with any of these things and prefer to chat, come join us at #nulecule on irc.freenode.net; We use the list at [https://www.redhat.com/mailman/listinfo/container-tools](https://www.redhat.com/mailman/listinfo/container-tools) for our development and community conversations.

Mechanics
---------

The index file in this git repository contains a yaml formatted list of all container applicatons included in the pipeline. In order to have your container application be included, tested and delivered via the Community Pipeline, it must be listed in this index. We are making resources behind the pipeline available to anyone on the internet who wishes to use them, provided what they are doing isnt illegal and is licensed in a way to be open source compatible. Note that the pipeline, its contents, all build and post build artifacts as well as delivery destinations should be considered publicly available.

The index file is processed hourly, so new inclusions will be picked up fairly quickly. Once in the system, we will poll your git repository for changes every hour and initiate build runs as needed. Details for the build are included in the cccp.yml file that is hosted inside your git repo. Metadata from this file can be used to control the build, request changes to the delivery parth, opt-in or out of the testing options available etc.

The index file is yaml formatted, and must include :

 - *Project ID* : Required: Typically your name or your org name, we will group reports based on project ID
 - *App ID* : Required: This would typically be the name of your app or the git repo name etc
 - *Job ID* : Optional: If you are using cascading Nulecule deps, you can have multiple Job's for the same App ID - rarely needed since the graph is processed from top to bottom.
 - *Git URL* : Required: The complete url to your git repo ( eg. https://github.com/projectatomic/atomicapp ). The Git repo can reside anywhere on the public internet. At this point we only support https:// urls.
 - *Git Path* : Required: The qualified path within the git repo to the cccp.yml file ( and therefore the Nulecule spec )
 - *Git Branch* : Optional: Branch from the git repo you want processed, optional. Defaults to 'master'

This index gives us all the info needed to get your git repo, and locate the cccp.yml file.

cccp.yml
--------

Every Nulecule that we process is required to host a container pipleline control file, called the cccp.yml. You can host it as either .cccp.yml ( and then its just out of the way ), or as cccp.yml. An example of what this file might look like is included in this git repo. Feel free to use that as a template. This file is a standard yaml formated file and includes the following information:

 - Job ID : Required: This must match the Job ID that you insert into the index file
 - Nulecule-file: Optional: you can set a custom filename here to be used as the Nulecule spec file, by default we expect the file to be called: Nulecule
 - Notify: Optional: This can be an email address or an irc channel on freenode.net where you'd like to be notified of sucess/failures. In the future we will add support for more notification mechanisms.
 - Skip: Optional: You can set this to True, and the pipeline will skip this job, till its re-enabled. Defaults to False
 - Test: Optional: Setting this to False, will skip the entire test process and the build step will be followed by delivery. Defaults to True. You can further qualify which tests you want to run by disabling specific tests as below. At this time we have test_base, that runs on the base centos7 os, on baremetal, and test_vagrant that runs inside a centos7 vagrant box hosted with the libvirt provider.
 - Test_Script: Optional: This allows you to specify any test scripts or test harness you would like run. By default we only validate the app can start. If specified this action is called after the basic test has run. And will be called for each of the enabled test environments.
 - DockerIndex: Optional: If enabled, this would result in your built app being delivered to index.docker.io on successful build and test runs
 - CustomDelivery: Optional: If a url is set for CustomDelivery, we will attempt a docker push into the repository hosted at that url. 
 - LocalDelivery: Optional: If set to False, the built app will not be delivered at registry.ci.centos.org. Defaults to True. Note that disabling this would mean that other projects and jobs can then no longer use your components in their dependancy graphs. And unless you have a CustomDelivery set, you yourself wont be able to get to the rendered final images.
 - Upstreams: Optional: An array that can be set to indicate what external registries you would like to pull container content from. By default the pipeline will only consider content hosted locally at registry.ci.centos.org and index.docker.io
 - Auto Rebuild: Optional: If set to False, it will disable the dependancy triggered rebuild for your app. Defaults to True.

More info
---------

If you need help with any of these things and prefer to chat, come join us at #nulecule on irc.freenode.net

We use the list at [https://www.redhat.com/mailman/listinfo/container-tools](https://www.redhat.com/mailman/listinfo/container-tools) for our development and community conversations.
