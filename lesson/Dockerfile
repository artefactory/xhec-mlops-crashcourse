FROM jupyter/datascience-notebook

# Set working directory to /app
WORKDIR /app

# Copying and installing course requirements
COPY ./mlops_crashcourse.ipynb .
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN mkdir data

# Expose port 8888 for jupyter lab 
EXPOSE 8888
EXPOSE 5000

# Run Jupyter Lab when container starts up 
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root"]