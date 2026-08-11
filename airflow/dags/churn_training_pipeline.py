from airflow.dags._factory import build_dag

dag = build_dag("churn_training_pipeline", "0 2 * * 0")
