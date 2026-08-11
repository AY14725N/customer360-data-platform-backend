from airflow.dags._factory import build_dag

dag = build_dag("customer_identity_resolution", "0 * * * *")
