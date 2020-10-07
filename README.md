# Backorder-Prediction

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flask)
[![Website myfakewebsitethatshouldnotexist.at.least.i.hope](https://img.shields.io/website-up-down-green-red/http/myfakewebsitethatshouldnotexist.at.least.i.hope.svg)](https://www.google.com/url?q=https%3A%2F%2Fbackorder-prediction.el.r.appspot.com)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)


#### -- Project Status: Completed

## Project Intro
Backorder is a common supply chain problem, impacting an inventory system service level and effectiveness. Identifying parts with the highest chances of shortage prior its occurrence can present a high opportunity to improve an overall company's performance. Backorder management forms an important subset of the inventory management analysis. The percentage of items backordered and the number of backorder days are important measures of the quality of a company's customer service and the effectiveness of its inventory management. A company that consistently sees items in backorder, might be running too lean. Such a company might be losing out on business by not providing the products demanded by its customers. This is because when an item is on backorder, a customer might look somewhere else for a substitute product, especially if the expected waiting time until the product becomes available is considerably long. This can provide an opportunity for once loyal customers to try other companies' products and potentially switch. Thus, it is a huge disadvantage in a highly competitive industry, where the number of alternatives available are huge or in an industry where brand loyalty is very low. Difficulties in proper inventory management leading to enormous back orders, can eventually lead to loss of market share as customers become frustrated with the company's lack of product availability. Moreover, customers waiting for their backordered products must receive shipping notifications on the shipping date they’ve been provided. This means that customers must be kept in the loop in case of any delays or changes, to avoid a storm of complaints and help maintain a good reputation for the company. 

To skip the description and get started :) [cilck here!](https://github.com/Vaishnavi-ambati/Backorder-Prediction/blob/master/README.md#getting-started)

### Methods Used
* Inferential Statistics
* Machine Learning
* Data Visualization
* Predictive Modeling
* Hyperparameter Tuning
* Flask integration

##### Technologies Used:
Type | Used
--- | --- 
Language | Python 3.7
IDE |	PyCharm
Database	|MySQL
Frontend	| HTML5, CSS3, Bootstrap
Integration	| Flask
Deployment |	Google Cloud Platform


## Project Description

The dataset has 23 columns including 22 features and one target column.
Features |	Description
--- | ---
sku |	Random ID for the product
national_inv	| Current inventory level for the part
lead_time |	Transit time for product (if available)
in_transit_qty	| Amount of product in transit from source
forecast_3_month |	Forecast sales for the next 3 months
forecast_6_month |	Forecast sales for the next 6 months
forecast_9_month |	Forecast sales for the next 9 months
sales_1_month	| Sales quantity for the prior 1 month time period
sales_3_month	| Sales quantity for the prior 3 month time period
sales_6_month	| Sales quantity for the prior 6 month time period
sales_9_month	| Sales quantity for the prior 9 month time period
min_bank	| Minimum recommend amount to stock
potential_issue |	Source issue for part identified
pieces_past_due	| Parts overdue from source
perf_6_month_avg	| Source performance for prior 6 month period
perf_12_month_avg	| Source performance for prior 12 month period
local_bo_qty	| Amount of stock orders overdue
deck_risk	| Part risk flag
oe_constraint |	Part risk flag
ppap_risk	| Part risk flag
stop_auto_buy	| Part risk flag
rev_stop	| Part risk flag
went_on_backorder |	Product actually went on backorder. This is the target value.

* I was very much confused with the sales and forecasts columns in the dataset. High correlation between these variables impacted the accuracy a lot. It was not like dropping the correlated features since every features in sales and forecasts is important. So, I have dropped one feature at a time and combination of features at a time and trained the model and picked the model with the best accuracy.


The Process flow of the project:
![flow](https://user-images.githubusercontent.com/50202237/84906666-e088c500-b0cf-11ea-99eb-8ae5e366254e.png)


## Getting Started

1. Clone this repo (for help see this [tutorial](https://help.github.com/articles/cloning-a-repository/)).
2. Raw Data is being kept [here](https://drive.google.com/file/d/1BpeG2gH1VgLW2p5lj7MZavKcmw5Jz4cj/view?usp=sharing)
3. Data processing/transformation scripts are being kept [here](https://github.com/Vaishnavi-ambati/Backorder-Prediction/tree/master/Modules).
4. After cloning the repo, open an editor of your choice and create a new environment.(for help see this [tutorial](https://realpython.com/lessons/creating-virtual-environment/))
5. Install the required modules in the environment using the requirements.txt file. (for help see this [tutorial](https://note.nkmk.me/en/python-pip-install-requirements/))
6. Open the script.sql file in Mysql and run the script to create database and tables
7. Open DbInsertion.py file and change the connection to your values (line 36)
   Ex: connection = mysql.connector.connect(host="127.0.0.1", user="your username", password="your password",
                                                 database="databaseName")
8. After installing the required modules. You are all set! Run the 'main.py' file and the app will be hosted in your local server.

Note: If you have any issues with project or with the setup. You can always contact me or raise an issue. :)
