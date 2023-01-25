# X-HEC MLOPS CRASH COURSE

The purpose of this course is to introduce the main concepts of Machine Learning Operations or MLOps for short, and illustrate their interest and usage through a simple use case.

# Prerequisites
The only prerequisite of this course is to have Docker installed on your machine.

# How To
This repository aims to simplify as much as possible the setup of the infrastructure required for this course. It will create two docker containers, one to host the Jupyter lab that you are going to use for experiments, and the other to host the mlflow server you will log your experiments into.

## Step 1: Check prerequisites
Let's first make sure you have access to all the required tools, namely Docker, bash and make
### Mac
* [Docker is installed](https://docs.docker.com/desktop/install/mac-install/)
### Linux
* [Docker is installed](https://docs.docker.com/desktop/install/linux-install/)
### Windows
* [Docker is installed](https://docs.docker.com/desktop/install/windows-install/)

## Step 2: Prepare the course infrastructure
Now, we will guide you to build the required Docker Images
### Mac
* Run :
```bash
make prepare-mlops-crashcourse
```
### Linux
* Run :
```bash
make prepare-mlops-crashcourse
```
### Windows

## Step 3: Launch the course
Follow these steps to mount the two containers and open the User interface to start the course.
### Mac
* Run :
```bash
make launch-mlops-crashcourse
```
### Linux
* Run :
```bash
make launch-mlops-crashcourse
```
### Windows

## Step 4: Cleanup
Once you are done with the course, you can follow these steps to clean your workspace. Careful! This will destroy all your work if you did not save it locally.
### Mac
* Run :
```bash
make clean-mlops-crashcourse
```
### Linux
* Run :
```bash
make clean-mlops-crashcourse
```
### Windows

# TODO
* Create an alternative to the makefile for Windows systems without GNU cmake installed.
* Crash test