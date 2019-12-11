export PYTHONPATH=.:$PYTHONPATH
psql template1 < sqls/app_setUp.sql
python3 database_operation/loads_data.py
