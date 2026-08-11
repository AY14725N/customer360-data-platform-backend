from airflow.dags._factory import build_dag

dag = build_dag("support_pipeline", "@hourly")
