# X-HEC MLOPS CRASH COURSE

The purpose of this course is to introduce the main concepts of Machine Learning Operations or MLOps for short, and illustrate their interest and usage through a simple use case.

# Prerequisites
The only prerequisite of this course is to have Docker installed on your machine.

# How To
This repository aims to simplify as much as possible the setup of the infrastructure required for this course. It will create two docker containers, one to host the Jupyter lab that you are going to use for experiments, and the other to host the mlflow server you will log your experiments into.

## Step 1: Check prerequisites
Let's first make sure you have access to all the required tools, namely Docker, bash and make

### Docker
Check that you have Docker desktop installed in your machine. If that is not the case, just follow the official instructions:

* [Install Docker - Mac OS](https://docs.docker.com/desktop/install/mac-install/)
* [Install Docker - Linux](https://docs.docker.com/desktop/install/linux-install/)
* [Install Docker - Windows](https://docs.docker.com/desktop/install/windows-install/)

Once docker is installed, make sure that it is running correctly by running:

```bash
docker run -d -p 80:80 docker/getting-started
```

If you check the Docker App, you should see a getting started container running. Once you've checked that this works correctly, remove the container via the UI.

<details>
    <summary><b>Optional</b></summary>
    You can also perform these operations directly from the command line, by running <code>docker ps</code> to check the running containers and <code>docker rm -f [CONTAINER-ID]</code> to remove it.
</details>

## Step 2: Prepare the course infrastructure
Now, we will guide you to build the required Docker Images
### Mac & Linux
* Run :
```bash
make prepare-mlops-crashcourse
```
### Windows
TODO
## Step 3: Launch the course
Follow these steps to mount the two containers and open the User interface to start the course.
### Mac & Linux
* Run :
```bash
make launch-mlops-crashcourse
```
### Windows
TODO

Once the Jupyter server is launched, you will need to use a token to attach your browser to it. The token you should use is `MLOPS`
## Step 4: Cleanup
Once you are done with the course, you can follow these steps to clean your workspace. Careful! This will destroy all your work if you did not save it locally.
### Mac & Linux
* Run :
```bash
make clean-mlops-crashcourse
```
### Windows
TODO

# TODO
* Create an alternative to the makefile for Windows systems without GNU cmake installed.
* Crash test
