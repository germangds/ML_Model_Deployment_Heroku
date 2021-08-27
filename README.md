# ML_Model_Deployment_Heroku: Bike sharing prediction API

In this python project, I have converted a basic machine learning notebook to a deployable web application launched in Heroku. The important key learnings from this project are as follows: (1) Basic usage of GIT commands (2) Basic understanding of the GIT Workflow (3) Exporting environments for easy app deployment and reproducibility purposes (4) Test creation for data validation.

## Model Usage

```
$ pip install -r requirements.txt
$ python app.py 5000
```

Then train the model, opening http://0.0.0.0:5000/train in your browser.

And finally, test the prediction by opening [this sample
request](http://0.0.0.0:5000/predict?date=2012-11-01&hour=10&weather_situation=clear&temperature=0.3&feeling_temperature=0.31&humidity=0.8&windspeed=0.0)
in your browser.
