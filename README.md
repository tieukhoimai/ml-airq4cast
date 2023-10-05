# AirQ4Cast - Air Quality Forecasting

 The second runner-up of Greenovator Hackathon 2021 organized by Bosch Vietnam and Quang Trung Software City (QTSC)

An AI-based application demo on Android Studio that analyzes and predicts the impact that tree cover density and traffic have on the air quality of real-time IoT data and streaming. 

https://english.thesaigontimes.vn/air-quality-monitoring-led-stickers-win-top-prize-at-greenovator-competition/

## About Competition

Bosch Vietnam and QTSC jointly organized the ‘Greenovator Hackathon 2021’ with the theme “Technologies for a Blue Sky”. The competition encourages Vietnam’s youth and engineering students to design innovative solutions addressing three main areas: 
- (1) improve outdoor air quality status.
- (2) manage traffic flow effectively to reduce congestion.
- (3) and reduce vehicle emissions resulting in cleaner air.

At the boot camp, all top ten teams will be provided with the knowledge critical for further development of their initial ideas, including: 
- (1) air quality data collected by Bosch Immission Monitoring Box (IMB)
- (2) information regarding the traffic situation in Quang Trung Software City area, recorded by Bosch’s AI-powered intelligent CCTV system.

The competition will end with a 48-hour hackathon on October 29th and 30th, where the teams will deploy and present their finest work for the coveted title. 

## Project Description

The project includes 3 phase:
- Data Collection: Using API calls to retrieve sensor data from Bosch IMB and intelligent CCTV system, and calculated NDVI/EVI from Landsat8 satellite imagery.
- Model Development: Creating multivariate time series forecasting models with additional factors (tree cover, real-time traffic volume) for accurate predictions.
- Integration: Developing an ML pipeline and integrating the forecasting model into a mobile application.

This repository only includes the source code to develop the forecasting model of Phase 2.

## Dataset
The dataset was collected between October 15, 2021 and January 20, 2022 (updated after the competition), and it includes:

- (1) Air quality data - temperature, humidity, PM 2.5, PM 10,... are measured in real time - is collected by Bosch IMB system
- (2) Traffic volume data (Camera IP: 127.0.0.2): the traffic situation is recorded by Bosch's intelligent CCTV system.

!['Traffic Volumn'](public/traffic_volumn.png 'Traffic Flows by Hour (Camera IP: 127.0.0.2)')

- (3) NDVI and EVI data calculated from Landsat8 satellite images in the Quang Trung Software Park area.

!['Satellite Image Landsat8 and NDVI image'](public/ndvi.png 'Satellite Image Landsat8 and NDVI image')

## Directory Structure
```
airq4cast/
├── data/ - save raw data
├── model/ - save trained models
├── result/ - save actual and predicted value
├── public/ - save public resources (image and video)
├── models.py
├── processing_data.py
├── viz.ipynyb
├── requirements.txt
├── README.md
└── .gitignore
```

## Steps to run the project
1. Install requirement
    - `pip install -r requirements.txt`
2. Preprocess data 
    - `python processing_data.py`
3. Create a `model` folder and train the model
    - `python models.py`
4. Perform viz result
    - Run the notebook `viz.ipynb`

## Performance

!['Result'](public/result.png 'result')

| |RMSE|R-Squared|
|:----|:----|:----|
|Decision Tree|3.863|0.9353|
|LightGBM|3.280|0.9533|
|Random Forest|29.358|0.9626|
|SVM|25.485|0.9718|
|XGBoost|35.839|0.9443|

## Demo

https://github.com/tieukhoimai/ml-airq4cast/assets/57632496/73c36e55-a5da-4895-b2b0-ae65496f21ff

