import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def top_expenses_by_category(df, top_n=5):
    if df.empty or 'category' not in df.columns or 'amount_spent' not in df.columns and df['transaction_type'] == 'expense':
        return pd.Series(dtype=float)
    category_expenses = df.groupby('category')['amount_spent'].sum().sort_values(ascending=False)
    return category_expenses.head(top_n)


def bottom_expenses_by_category(df, bottom_n=5):
    if df.empty or 'category' not in df.columns or 'amount_spent' not in df.columns and df['transaction_type'] == 'expense':
        return pd.Series(dtype=float)
    category_expenses = df.groupby('category')['amount_spent'].sum().sort_values(ascending=True)
    return category_expenses.head(bottom_n)


def plot_income_vs_expenses(df):
    if df.empty: return
    income = df[df['transaction_type'] == 'income']['amount_spent'].sum()
    expenses = df[df['transaction_type'] == 'expense']['amount_spent'].sum()
    fig, ax = plt.subplots()
    ax.bar(['Income', 'Expenses'], [income, expenses], color=['green', 'red'])
    ax.set_title('Income vs Expenses')
    ax.set_ylabel('Amount')
    st.pyplot(fig)


def plot_expenses_by_category(df):
    if df.empty: return
    category_expenses = df.groupby('category')['amount_spent'].sum().sort_values(ascending=False)
    if category_expenses.empty: return
    fig, ax = plt.subplots()
    category_expenses.plot(kind='bar', color='red', ax=ax)
    ax.set_title('Expenses by Category')
    ax.set_ylabel('Amount Spent')
    ax.set_xlabel('Category')
    plt.xticks(rotation=45)
    st.pyplot(fig)



def investment_analysis(df):
    if df.empty: return 0, 0
    investment = df[df['transaction_type'] == 'investment']['amount_spent'].sum()
    savings = df[df['transaction_type'] == 'savings']['amount_spent'].sum()
    return investment, savings
