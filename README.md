# DatabaseProject

Yelp Dataset https://www.yelp.com/dataset/documentation/main

#### Data Cleaning.

- DatabaseProject
    - datasets
        - business.json
        - checkin.json
        - review.json
    - preprocess
        - \_\_init\_\_.py
        - review.py
        - business.py

```
cd DatabaseProject
export PYTHONPATH=.:$PYTHONPATH
python3 preprocess/{table_name}.py dataset/{table_name}.json```
