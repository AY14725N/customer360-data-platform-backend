from airflow.dags._factory import build_dag

dag = build_dag("transactions_pipeline", "*/10 * * * *")
