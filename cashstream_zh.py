# Import necessary libraries
import streamlit as st

# Function to calculate monthly mortgage payment
def calculate_mortgage(principal, annual_interest_rate, years, repayment_method):
    monthly_interest_rate = annual_interest_rate / 12 / 100
    months = years * 12
    if repayment_method == '等额本金':
        monthly_payment = (principal / months) + (principal * monthly_interest_rate)
    elif repayment_method == '等额本息':
        monthly_payment = (principal * monthly_interest_rate * (1 + monthly_interest_rate) ** months) / ((1 + monthly_interest_rate) ** months - 1)
    return monthly_payment

# Function to calculate net cash flow
def calculate_net_cash_flow(rental_income, monthly_mortgage, property_management_fee, vacancy_rate):
    vacancy_loss = rental_income * vacancy_rate
    net_cash_flow = rental_income - monthly_mortgage - property_management_fee - vacancy_loss
    return net_cash_flow

# Function to calculate cash on cash return
def calculate_cash_on_cash_return(net_cash_flow, down_payment, initial_investment):
    cash_on_cash_return = (net_cash_flow * 12 / (down_payment + initial_investment)) * 100
    return cash_on_cash_return

# Function to calculate cap rate
def calculate_cap_rate(noi, property_value):
    cap_rate = (noi / property_value) * 100
    return cap_rate

# Streamlit app
st.title('房产投资计算器')

# Input fields
property_value = st.number_input('房产总价（元）', min_value=100000, step=10000)
rental_income = st.number_input('每月租金收入（元）', min_value=1000, step=100)
property_management_fee = st.number_input('每月物业管理费（元）', min_value=0, step=100)
vacancy_rate = st.slider('空置率 (%)', min_value=0.0, max_value=10.0, value=5.0) / 100

# Advanced settings (hidden by default)
with st.expander("贷款设置"):
    loan_type = st.selectbox('贷款类型', ['公积金贷款', '商业贷款'])
    repayment_method = st.selectbox('还款方式', ['等额本金', '等额本息'], index=1)

    # Default interest rates
    default_interest_rates = {
        '公积金贷款': 2.85,
        '商业贷款': 3.1
    }

    # Interest rate retrieval
    interest_rate = st.number_input('年利率 (%)', min_value=0.0, max_value=10.0, value=default_interest_rates[loan_type])

    # Down payment and loan term
    down_payment_percentage = st.number_input('首付比例 (%)', min_value=20.0, max_value=100.0, value=20.0) / 100
    loan_term_years = st.number_input('贷款年限 (年)', min_value=1, max_value=30, value=30)

# Calculate mortgage payment
down_payment = property_value * down_payment_percentage
loan_amount = property_value - down_payment
monthly_mortgage = calculate_mortgage(loan_amount, interest_rate, loan_term_years, repayment_method)

# Calculate net cash flow and cash on cash return
net_cash_flow = calculate_net_cash_flow(rental_income, monthly_mortgage, property_management_fee, vacancy_rate)
cash_on_cash_return = calculate_cash_on_cash_return(net_cash_flow, down_payment, 0)  # Assuming no other initial investments

# Calculate NOI and Cap Rate
noi = rental_income * 12*(1-vacancy_rate)-property_management_fee  # Net Operating Income
cap_rate = calculate_cap_rate(noi, property_value)

# Display results
st.write(f'首月按揭还款: {monthly_mortgage:.2f} 元')
st.write(f'每月净现金流: {net_cash_flow:.2f} 元')
st.write(f'租售比: 1/{property_value/rental_income:.0f}')
st.write(f'现金回报率: {cash_on_cash_return:.2f}%')
st.write(f'资本化率: {cap_rate:.2f}%')