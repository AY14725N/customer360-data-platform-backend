from airflow.dags._factory import build_dag

dag = build_dag("feature_engineering", "@daily")
