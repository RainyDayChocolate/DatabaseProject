export PYTHONPATH=.:$PYTHONPATH
psql template1 < sqls/app_setUp.sql
python3 app/loads_data.py
