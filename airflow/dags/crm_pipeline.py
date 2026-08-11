from airflow.dags._factory import build_dag

dag = build_dag("crm_pipeline", "@hourly")
