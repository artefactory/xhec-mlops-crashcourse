# DSB MLOPS CRASH COURSE

The purpose of this course is to introduce the main concepts of Machine Learning Operations, or MLOps for short, and illustrate their interest and usage through a simple use case.

# Prerequisites
For the best experience, we recommend that you have Docker installed on your machine.

# How to set up
This repository aims to simplify as much as possible the setup of the infrastructure required for this course. It will create two docker containers, one to host the Jupyter lab that you are going to use for experiments, and the other to host the mlflow server you will log your experiments into.

## Step 1: Installing prerequisites
Let's first make sure you have access to the Docker.

### Docker
Check that you have Docker desktop installed in your machine. If that is not the case, just follow the official instructions:

* [Install Docker - Mac OS](https://docs.docker.com/desktop/install/mac-install/)
* [Install Docker - Linux](https://docs.docker.com/desktop/install/linux-install/)
* [Install Docker - Windows](https://docs.docker.com/desktop/install/windows-install/)

For those of you working on Windows, you will need to update Windows Subsystem for Linux. To do so, simply open PowerShell and run:

```bash
wsl --update
```

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


Now, we will guide you to build the required Docker Images. With a terminal, go to the root of this folder.

First check that you have `make` installed by running `make -v`

<details>
    <summary><b>If you have `make` and `bash` installed on your terminal</b></summary>
    Then simply run:
    <p><pre>make prepare-mlops-crashcourse</pre></p>
</details>

<details>
    <summary><b>Without `make` and `bash` installed on your terminal</b></summary>
    Please run:
    <p><pre>docker build -t mlops_notebooks ./lesson/
docker build -t mlops_mlflow ./mlflow_server/</pre></p>
</details>


## Step 3: Launch the course

Follow these steps to mount the two containers and open the user interface to start the course.


<details>
    <summary><b>If you have `make` and `bash` installed on your terminal</b></summary>
    You can directly bundle all this section's commands by typing:
    <p><pre>make launch-mlops-crashcourse</pre></p>
</details>

<details>
    <summary><b>Without `make` and `bash` installed on your terminal</b></summary>
    First, create a network:
    <p><pre>docker network create --driver bridge mlops-crashcourse</pre></p>
    <p>Then:</p>
    <p><pre>docker run -it --rm --user root -p 10000:8888 -p 8000:8000 -p 4200:4200 -v ${PWD}/mlflow_server/local:/mlflow -e JUPYTER_ENABLE_LAB=yes -e JUPYTER_TOKEN=docker -e MLFLOW_TRACKING_URI=http://mlflow:5001 --network mlops-crashcourse --name jupyter -d mlops_notebooks</pre></p>
    <p>And:</p>
    <p><pre>docker run -it -d --rm -p 5001:5000 -v ${PWD}/mlflow_server/local:/mlflow --network mlops-crashcourse --name mlflow mlops_mlflow</pre></p>
    <p>You can then open your favorite browser and open in two tabs the two urls we will be working with:</p>
    <ul>
    <li>http://localhost:10000</li>
    <li>http://localhost:5001</li>
    <ul>
</details>

Once the Jupyter server is launched, you will need to use a token to attach your browser to it. The token you should use is `MLOPS`.

## Step 4: Time to work

All the activities of this course can be found in the `notebooks` folder. If you are using docker, then you will be working on jupyter lab and the folder will be immediately visible from the root. If instead, you are running this course locally on your computer, then you can find the notebooks under `lesson/notebooks`.

> If you encounter difficulties during, don't hesitate to call us for help

## Step 5: Cleanup

Once you are done with the course, you can follow these steps to clean your workspace.

> Careful! This will destroy all your work if you did not save it locally.

<details>
    <summary><b>If you have `make` and `bash` installed on your terminal</b></summary>

    Then simply run:
    ```bash
    make clean-mlops-crashcourse
    ```
</details>

<details>
    <summary><b>Without `make` and `bash` installed on your terminal</b></summary>
    Please run

    ```bash
	docker stop jupyter
	docker stop mlflow
	docker image rm mlops_notebooks
	docker image rm mlops_mlflow
    docker network rm mlops-crashcourse
    ```
</details>
