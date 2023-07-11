# Mortgage Calculator

This is a Python class that calculates mortgage details based on current mortgage rates, home prices, and income data.

## Dependencies
- requests
- bs4
- pathlib
- re
- pandas
- datetime
- numpy

## Usage
1. Import the required libraries:
```python
import requests
import bs4
import pathlib
import re
import pandas as pd
from datetime import date
import numpy as np
```
2. Copy the `MortgageCalculator` class into your code.

3. Create an instance of the `MortgageCalculator` class:
```python
calculator = MortgageCalculator()
```
4. Calculate the mortgage details:
```python
mortgage_data = calculator.calculate_mortgage()
```
The `calculate_mortgage` method retrieves the current mortgage rate, home price, and income data, and calculates the monthly payment, total interest, and affordability. It returns a Pandas DataFrame with the calculated data.

5. Save the data to an Excel file:
```python
calculator.save_data_to_excel(mortgage_data)
```
The `save_data_to_excel` method saves the mortgage data to an Excel file named "mortgage_list.xlsx". If the file already exists, it appends the new data to the existing file.

## Example
Here's an example of how to use the `MortgageCalculator` class:
```python
if __name__ == '__main__':
    calculator = MortgageCalculator()
    mortgage_data = calculator.calculate_mortgage()

    calculator.save_data_to_excel(mortgage_data)
    print(mortgage_data)
```
This example calculates the mortgage details and saves the data to an Excel file. The mortgage details are also printed to the console.

Note: Make sure to have an internet connection as the class retrieves data from online sources.

## Disclaimer
This mortgage calculator is provided for informational purposes only. It should not be considered financial or investment advice. The calculated results may not reflect the actual mortgage terms or rates available. Always consult with a qualified financial professional before making any financial decisions.
