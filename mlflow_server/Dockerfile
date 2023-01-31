FROM python:3-slim
ARG MLFLOW_VERSION=1.26.1

WORKDIR /mlflow/
RUN pip install --no-cache-dir psycopg2-binary mlflow==$MLFLOW_VERSION
EXPOSE 5000

ENV BACKEND_URI sqlite:////mlflow/mlflow.db
ENV ARTIFACT_ROOT /mlflow/artifacts
ENV ARTIFACT_DESTINATION /mlflow/artifacts

CMD mlflow server --backend-store-uri ${BACKEND_URI} --default-artifact-root ${ARTIFACT_ROOT} --artifacts-destination ${ARTIFACT_DESTINATION} --serve-artifacts --host 0.0.0.0 --port 5000
