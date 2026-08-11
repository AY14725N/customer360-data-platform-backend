from datetime import datetime, timezone

try:
    from airflow.operators.python import PythonOperator

    from airflow import DAG
except ImportError:  # Enables static validation without installing Airflow.
    DAG = None


def _log_pipeline(name: str) -> None:
    print(f"Running {name}")


def build_dag(dag_id: str, schedule: str):
    if DAG is None:
        return None
    with DAG(
        dag_id,
        start_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
        schedule=schedule,
        catchup=False,
        tags=["customer360"],
    ) as dag:
        PythonOperator(task_id="run", python_callable=_log_pipeline, op_args=[dag_id])
    return dag
