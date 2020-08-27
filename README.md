# SQLAlchemy Challenge
**Completed By:** Lauren Stein
----

<img src="images/hawaii.jpg">

## Part 1: Climate Analysis and Exploration
**Objective:** Conduct climate analysis on the 7 Hawaii weatherstations to assess annual rainfall and temperature
* 
# SQL Challenge
**Completed By:** Lauren Stein\
**Objective:** Utilize SQLAlchemy to conduct data analysis for Hawaii weather station recordings and generate an API to browse the data

---

## Part 1: Climate Analysis and Exploration
[Workflow](climate_starter.ipynb)
1. Create a [sqlite database](Resources/hawaii.sqlite) and SQLAlchemy to perform SQL queries and analyze with python
2. Retrieve last 12 months of preciptitation data - run summary statistics and plot the data
**Precipitation Analysis**
<img src="images/hawaii_rainfall.png">

3. Create a histogram to assess temperature frequencies for the Hawaii station with the most recordings
**Temperature Analysis**
<img src="images/top_station_temp_heat.png">


## Part 2: Create a Hawaii Climate API
[Workflow](app.py)
1. Homepage: available routes
2. **api/v1.0/preciptiation**: summary statistics for Hawaii precipitation
3. **api/v1.0//tobs**: Temperature for most active weather station
4. **api/v1.0/<start>**:Summary statistics for each weather station from starting date to last recording
5. **api/v1.0/<start>/<end>**: User defined date range for each weather station's summary statistics

## Bonus Analysis
[workflow](climate_starter.ipynb) _see Bonus Section_

**Trip Tempearture Analysis**\
***Holiday Vacation: 11/20/2020 - 11/26/20***
1. Calculate the average temperature for the month and day of the beginning trip date
<img src= "images/hawaii_trip_avg.png">

2. Calculatue the temperature norms: minimum, maximum, and average for the month/day of the trip duration
<img src= "images/hawaii_trip_norms.png">
