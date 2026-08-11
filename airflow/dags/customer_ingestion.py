from airflow.dags._factory import build_dag

dag = build_dag("customer_ingestion", "*/15 * * * *")
