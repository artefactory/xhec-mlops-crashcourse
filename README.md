# X-HEC MLOPS CRASH COURSE

The purpose of this course is to introduce the main concepts of Machine Learning Operations or MLOps for short, and illustrate their interest and usage through a simple use case.

# Prerequisites
For best experience, we recommand that you have Docker installed on your machine.

# How to set up
This repository aims to simplify as much as possible the setup of the infrastructure required for this course. It will create two docker containers, one to host the Jupyter lab that you are going to use for experiments, and the other to host the mlflow server you will log your experiments into.

## Step 1: Installing prerequisites
Let's first make sure you have access to the required tool, namely Docker.

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

<details>
    <summary><b>If you have `make` and `bash` installed on your terminal</b></summary>
    Then simply run:
    ```bash
    make prepare-mlops-crashcourse
    ```
</details>

<details>
    <summary><b>Without `make` and `bash` installed on your terminal</b></summary>
    Please run 

    ```bash
    docker build -t mlops_notebooks ./lesson/
    docker build -t mlops_mlflow ./mlflow_server/
    ```
</details>


## Step 3: Launch the course

Follow these steps to mount the two containers and open the User interface to start the course.


<details>
    <summary><b>If you have `make` and `bash` installed on your terminal</b></summary>
    You can directly bundle all this section commands typing:

    ```bash
    make launch-mlops-crashcourse
    ```
</details>

<details>
    <summary><b>Without `make` and `bash` installed on your terminal</b></summary>
    ```bash
    docker network create --driver bridge mlops-crashcourse
    ```

    Then:

    ```bash
    docker run -it --rm --user root -p 10000:8888 -p 8000:8000 -p 4200:4200 -v ${PWD}/mlflow_server/local:/mlflow -e JUPYTER_ENABLE_LAB=yes -e JUPYTER_TOKEN=docker -e MLFLOW_TRACKING_URI=http://mlflow:5001 --network mlops-crashcourse --name jupyter -d mlops_notebooks
    ```

    And:

    ```bash
    docker run -it -d --rm -p 5001:5000 -v ${PWD}/mlflow_server/local:/mlflow --network mlops-crashcourse --name mlflow mlops_mlflow
    ```

    You can then open your favorite browser and open in two tabs the two urls we will be working with:
    * http://localhost:10000
    * http://localhost:5001
</details>

Once the Jupyter server is launched, you will need to use a token to attach your browser to it. The token you should use is `MLOPS`.



## Step 4: Cleanup

Once you are done with the course, you can follow these steps to clean your workspace. Careful! This will destroy all your work if you did not save it locally.

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



# TODO
* Crash test
