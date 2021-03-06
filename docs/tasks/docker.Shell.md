# docker.Shell

## Description
This task executes a shell command from within a docker container.

## Required Parameters

* image
  * Name of the docker image that will be used to create the container that the shell command will be run inside of.
* version
  * Version of the docker image that will be used to create the container that the shell command will be run inside of.
* command
  * Shell command that will be executed inside of the created container.

## Optional Parameters
* workDir
  * Working directory that the task will use inside of the container. (`'/project'` by default)
    * The directory that the task is called from will be mounted to this directory on the created container.

# Navigation
* [Home](../../README.md)
* [Task Documentation](README.md)
