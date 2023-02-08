# DSB MLOPS CRASH COURSE

The purpose of this course is to introduce the main concepts of Machine Learning Operations, or MLOps for short, and illustrate their interest and usage through a simple use case.

## Step 1: Setting up a virtual environment with required packages.

    To create a virtual environment, run:
    ```bash
    python3 -m venv .venv
    ```
    Then run
    ```bash
    source .venv/bin/activate
    ```

    Simplify your installation by running
    ```bash
    pip install wheel
    ```

    Ensure your pip version is up to date by running:
    ```bash
    pip install --upgrade pip
    ```

    To install the requirements, run :
    ```bash
    pip install -r lesson/requirements.txt
    ```

## Step 2: Starting the jupyter server.

    Just run
    ```bash
    jupyter notebook ./lesson/notebooks
    ```
