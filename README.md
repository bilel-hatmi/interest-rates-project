# Stochastic Models for Interest Rates in Discrete Time


In this project we implement, analyze and compare the Ho-Lee and HJM models in discrete time in order to price contingent claims, specifically caplets.

## Requirements

We suggest to set up a virtual environment in the working folder by doing the following:

```
virtualenv --python python3 venv
```

To activate it, simply run

```
source venv/bin/activate
```

To run the application, you will need to run

```
pip install -r requirements.txt
```

When you have installed all the required libraries, simply run `python3 app.py` and follow the generated link.

## App

Our app allows you to price caplets by entering the parameters you wish! The payoff can be any function of 'x'. The default payoff is a call. You can adapt it to price a put!


![App Screenshot](img/app_img.JPG)

## Files 

The files `ho_lee.py`, `hjm.py` and `plot_tree.py` gather all the functions needed to run `app.py`. In the `notebooks` folder, you will find a more detailed analysis of the Ho-Lee and HJM models.


## Disclaimer

All information provided by this program is for educational and entertainment purposes only and should not be construed as financial advice. The accuracy, completeness, adequacy, or currency of the content is not warranted or guaranteed. Any investment decisions made based on the information provided by this program are done at your own risk. The program is not liable for any financial losses or damages arising from the use of the information provided. Past performance is not indicative of future results. Always do your own research and consult with a licensed financial advisor before making any investment decisions.






