FROM ghcr.io/mlflow/mlflow:v2.1.1

WORKDIR /mlflow/
EXPOSE 5000

ENV BACKEND_URI sqlite:////mlflow/mlflow.db
ENV ARTIFACT_ROOT /mlflow/artifacts
ENV ARTIFACT_DESTINATION /mlflow/artifacts

CMD mlflow server --backend-store-uri ${BACKEND_URI} --default-artifact-root ${ARTIFACT_ROOT} --artifacts-destination ${ARTIFACT_DESTINATION} --serve-artifacts --host 0.0.0.0 --port 5000
