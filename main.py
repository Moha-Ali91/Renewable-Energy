import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error,r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# App title
st.title ('ML RENEWABLE ENERGY') 

# Loading the dataset
df=pd.read_csv("C:\\Users\\hp\Downloads\\WorldBank Renewable Energy Consumption_WorldBank Renewable Energy Consumption.csv")

# Display the first 5 rows
st.write(df.head())

# User input: number of rows to display
num_rows = st.slider("Select the number of rows", min_value=1, max_value=len(df), value=5)
st.write("Here are the rows you have selected from the dataset:")
st.write(df.head(num_rows))

# Display the shape of the dataset
st.write('Number of rows and columns in the dataset:', df.shape)

# Display the summary statistics of the dataset
st.write('Summary statistics of the dataset:')
st.write(df.describe())

# Check for duplicates
if st.checkbox("Check for duplicates"):
    st.write(df[df.duplicated()])

# Total number of duplicates
if st.checkbox("Check for total number duplicates"):
    st.write(df.duplicated().sum())

# Drop 'Country Code' column
df = df.drop('Country Code', axis=1)

# Convert 'Year' column to datetime objects first
df['Year'] = pd.to_datetime(df['Year'], format='%d/%m/%Y')  # Adjust format for MM/DD/YYYY

# Encode categorical variables
encoded_columns = ['Region', 'Income Group', 'Indicator Name', 'Country Name', 'Indicator Code', 'Year']
le_dict = {col: LabelEncoder() for col in encoded_columns}

for column in encoded_columns:
    le_dict[column].fit(df[column])
    df[column] = le_dict[column].transform(df[column])

# Prepare features and target variable
X = df.drop('Energy Consump.', axis=1)
y = df['Energy Consump.']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest Regressor
rf_regressor = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)

# Train the model
rf_regressor.fit(X_train, y_train)

# Make predictions
y_pred = rf_regressor.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Print the model
st.write(f"Mean Squared Error: {mse}")
st.write(f"R-squared: {r2}")

# User input for new data
st.sidebar.write("## Enter new data for prediction")
Country_Name = st.sidebar.selectbox("Country Name", le_dict['Country Name'].classes_)
Income_Group = st.sidebar.selectbox("Income Group", le_dict['Income Group'].classes_)
Indicator_Code = st.sidebar.selectbox("Indicator Code", le_dict['Indicator Code'].classes_)
Indicator_Name = st.sidebar.selectbox("Indicator Name", le_dict['Indicator Name'].classes_)
Region = st.sidebar.selectbox("Region", le_dict['Region'].classes_)
Year= st.sidebar.number_input("Year")

# Encode user input
encoded_input = {
    'Country Name': le_dict['Country Name'].transform([Country_Name])[0],
    'Income Group': le_dict['Income Group'].transform([Income_Group])[0],
    'Indicator Code': le_dict['Indicator Code'].transform([Indicator_Code])[0],
    'Indicator Name': le_dict['Indicator Name'].transform([Indicator_Name])[0],
    'Region': le_dict['Region'].transform([Region])[0],
    'Year': Year
}

# Convert to DataFrame
encoded_input_df = pd.DataFrame([encoded_input])

# Predict using the model
if st.sidebar.button('Predict Energy Consump.'):
    prediction = rf_regressor.predict(encoded_input_df)[0]
    st.sidebar.write('Predicted energy consumption:', prediction)

