"""register_model.py
Registers a model to MLflow if available, otherwise simulates registration by copying
the model into a local `registry/` folder. This keeps the demo runnable without cloud.
"""
import os
import sys
import shutil


def simulated_register(model_path: str):
    os.makedirs('registry', exist_ok=True)
    dest = os.path.join('registry', os.path.basename(model_path))
    shutil.copy2(model_path, dest)
    print(f"[registry] Simulated registration: copied {model_path} -> {dest}")


def mlflow_register(model_path: str):
    import mlflow
    from mlflow.tracking import MlflowClient
    mlflow_tracking = os.environ.get('MLFLOW_TRACKING_URI')
    if mlflow_tracking:
        mlflow.set_tracking_uri(mlflow_tracking)
    else:
        # default to local mlruns dir
        mlflow.set_tracking_uri('file://' + os.path.abspath('mlruns'))

    with mlflow.start_run() as run:
        # log the model file as an artifact
        mlflow.log_artifact(model_path, artifact_path='model')
        run_id = run.info.run_id
        artifact_uri = f"runs:/{run_id}/model/{os.path.basename(model_path)}"
        client = MlflowClient()
        try:
            model_name = os.environ.get('MLFLOW_MODEL_NAME', 'PhishShield')
            res = client.create_registered_model(model_name)
        except Exception:
            pass
        mv = client.create_model_version(name=os.environ.get('MLFLOW_MODEL_NAME','PhishShield'), source=artifact_uri, run_id=run_id)
        print(f"[registry] Registered model version: {mv.version} for model '{mv.name}'")


def main():
    model_path = sys.argv[1] if len(sys.argv) > 1 else 'poisoned_model.joblib'
    try:
        import mlflow
    except Exception:
        print('[registry] mlflow not available; using simulated registry')
        simulated_register(model_path)
        return

    try:
        mlflow_register(model_path)
    except Exception as e:
        print('[registry] mlflow registration failed:', e)
        print('[registry] falling back to simulated registration')
        simulated_register(model_path)


if __name__ == '__main__':
    main()
