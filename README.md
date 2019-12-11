## Database System Final Project

### Participants 

Charly Huang: huangc11@rpi.edu

Kuangzheng Li: lik15@rpi.edu

### Motivation

This DBMS stored several US turbulance data, including Four Kaggle Datasets

+ US Flight Delays

  https://www.kaggle.com/niranjan0272/us-flight-delay

+ US Gun Violence

  https://www.kaggle.com/ericking310/us-gun-violence

+ US Accidents

  https://www.kaggle.com/sobhanmoosavi/us-accidents

+ Historical Hourly Weather Data

  https://www.kaggle.com/selfishgene/historical-hourly-weather-data#humidity.cs

+ Several tiny datasets including US state abbrevation and Airline Code datasets also involved here.

User could use self-guide command line interfaced app to explore within those datasets in a degree. 

### Installation

This project relys on python3 and postgresql

#### Environment Setting

```shell
brew install postgresql
brew services start postgresql
cd Final
python3 -m venv venv3
source ./venv3/bin/activate
pip3 install requirement.txt
tar -xzvf normalized_dataset.tar.gz
tar -xzvf xmls.tar.gz
```

#### Normalization

```
python3 -m normalization "YOUR_ORIGINAL_DATASETS_DOWNLOADED_FROM_KAGGLE"
```

### Load Data

```
bash load_data.sh
```

#### App Start

```
bash launch_client_query_manager.sh
```

### Explorations Example



