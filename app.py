import streamlit as st
import pandas as pd
import numpy as np

def calculate_monthly_mortgage(principal, annual_interest_rate, years):
    monthly_interest_rate = annual_interest_rate / 12 / 100
    n_payments = years * 12
    monthly_payment = principal * (monthly_interest_rate * (1 + monthly_interest_rate) ** n_payments) / ((1 + monthly_interest_rate) ** n_payments - 1)
    return monthly_payment

def calculate_annual_data(loan_amount, interest_rate, term_years, monthly_mortgage, monthly_rental_income, monthly_expenses, maintenance, upfront_costs, down_payment):
    annual_data = []
    principal_remaining = loan_amount
    total_equity = down_payment
    previous_year_equity = down_payment  # Initialize previous year equity with the initial down payment

    for year in range(1, term_years + 1):
        annual_interest_paid = 0
        annual_principal_paid = 0
        
        for month in range(1, 13):
            monthly_interest = principal_remaining * (interest_rate / 12 / 100)
            principal_paid = monthly_mortgage - monthly_interest
            principal_remaining -= principal_paid
            annual_interest_paid += monthly_interest
            annual_principal_paid += principal_paid

        total_equity += annual_principal_paid
        equity_gained_this_year = total_equity - previous_year_equity
        previous_year_equity = total_equity

        annual_rental = monthly_rental_income * 12
        annual_maintenance = maintenance * 12
        annual_misc_expenses = monthly_expenses * 12
        # annual_total_expenses = annual_maintenance + annual_misc_expenses + annual_interest_paid
        annual_total_expenses = annual_maintenance + annual_misc_expenses + (monthly_mortgage*12)
        annual_balance = annual_rental - annual_total_expenses
        annual_return = equity_gained_this_year + annual_balance
        initial_investment = down_payment + upfront_costs
        annual_return_percentage = (annual_return / initial_investment) * 100

        annual_data.append([principal_remaining, annual_interest_paid, monthly_mortgage * 12,
                            annual_misc_expenses, annual_maintenance, annual_rental, annual_balance,
                            total_equity, equity_gained_this_year, annual_return, annual_return_percentage])
    
    columns = ['Outstanding Principal', 'Annual Interest', 'Annual Mortgage Payment', 'Annual Misc.', 
               'Annual Maintenance', 'Annual Rental Income', 'Annual Balance', 'Current Equity', 
               'Equity Gained in Current Year', 'Annual Return', 'Annual Return %']
    
    return pd.DataFrame(annual_data, columns=columns, index=range(1, term_years + 1))


st.title('Investment Rental Property ROI Calculator')

# User inputs
price_of_home = st.number_input('Price of the Home', value=400000)
down_payment_percent = st.number_input('% Down Payment', value=20.0)
loan_tenure = st.number_input('Loan Tenure', value=30)
annual_interest_rate = st.number_input('Annual Rate of Interest (%)', value=6.5)
upfront_costs = st.number_input('One-time Upfront Costs', value=10000)
monthly_rental_income = st.number_input('Monthly Rental Income', value=2700)
monthly_expenses_input = sum([
    st.number_input('Property Taxes', value=270),
    st.number_input('HOA Fees', value=350),
    st.number_input('Home Insurance', value=233),
    st.number_input('Mortgage Insurance', value=0),
])
maintenance = st.number_input('Maintenance', value=200)
# monthly_expenses = monthly_expenses_input + maintenance

down_payment = price_of_home * (down_payment_percent / 100)
loan_amount = price_of_home - down_payment
monthly_mortgage = calculate_monthly_mortgage(loan_amount, annual_interest_rate, loan_tenure)


if st.button('Calculate'):
    annual_data = calculate_annual_data(loan_amount, annual_interest_rate, loan_tenure, monthly_mortgage, 
                                        monthly_rental_income, monthly_expenses_input, maintenance, 
                                        upfront_costs, down_payment)
    st.write(f'Monthly Mortgage Payment: ${monthly_mortgage:.2f}')
    st.write(annual_data)
