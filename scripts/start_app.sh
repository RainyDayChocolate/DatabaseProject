export PYTHONPATH=.:$PYTHONPATH
psql < sqls/app_setUp.sql
python3 app/loads_data.py
