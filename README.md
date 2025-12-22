# Loan Approval Prediction System

A Django web application that uses machine learning to predict whether a loan will be approved or not based on a person's data.

## What is this

This is my final project. It consists of two parts:

1. Data Science part - here I analyzed data and trained the model
2. Django web application - here users can enter data and get results

## Project Structure

```
16/
    data_science/
        loan_prediction_analysis.ipynb    # my analysis notebook
        loan_model.pkl                     # trained model (created after running notebook)
        feature_columns.pkl                # column list (also created)
        loan_data.csv                      # training data
    
    web_app/
        loan_app/                         # main Django project
            settings.py
            urls.py
            ...
        predictor/                        # my application
            models.py
            views.py
            forms.py
            urls.py
            ...
        templates/                         # HTML files
            base.html
            login.html
            register.html
            loan_form.html
            result.html
        manage.py
        db.sqlite3                         # database (created automatically)
        static/                            # folder for static files (CSS, JS)
    
    README.md                              # general project description
    requirements.txt                       # list of libraries
    ІНСТРУКЦІЯ_ЗАПУСКУ.md                 # detailed instructions
```

## How to use

1. First, you need to register - create an account
2. Then log in to the system
3. Fill out the form with loan data (gender, income, loan amount, etc.)
4. Click the button and see the result - approved or not

## Data Science part

In the notebook I did the following:

1. EDA - looked at the data, built graphs, checked for missing values
2. Cleaning - filled missing values, corrected data
3. Encoding - converted categorical variables to numbers
4. Scaling - normalized numerical data
5. Modeling - created a Pipeline with RandomForestClassifier
6. GridSearchCV - found the best parameters
7. Evaluation - checked how the model works
8. Saving - saved the model to a pickle file

## Technologies used

For Data Science:
- pandas - for working with data
- numpy - for calculations
- scikit-learn - for machine learning
- matplotlib and seaborn - for graphs
- jupyter - for notebook

For web application:
- Django 4.2
- SQLite - database
- Bootstrap 5 - for beautiful appearance
- HTML/CSS

## Model

I used RandomForestClassifier. First, I process the data through StandardScaler and OneHotEncoder, then train the model. I used GridSearchCV to find the best parameters.

Most important features that affect the result:
1. Credit_History - credit history
2. LoanAmount - loan amount
3. ApplicantIncome - applicant income
4. CoapplicantIncome - co-applicant income
5. Loan_Amount_Term - loan term

## Possible improvements
Could add:
- More models for comparison
- Better graphs in the web interface
- Prediction history for each user
- API
- Better design
- Tests
- Hash passwords
- Use HTTPS
- Add protection against attacks
