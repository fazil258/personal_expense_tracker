import streamlit as st
import pandas as pd 
from input.image_to_df import image_to_df
from categorizer.data_combiner import combiner
from categorizer.categorize_transaction import categorize_transaction
from analysis.expense_analyzer import *
from analysis.expense_summarizer import summarize_expenses
from categorizer.categorizer import categorizer

def main():
    st.set_page_config(page_title="Personal Expense Tracker", layout="wide")
    st.title("Personal Expense Tracker")
    st.write("Upload your financial transaction data in PDF or Image format to track and analyze your expenses and income.")   
    
    uploaded_file = st.file_uploader("Choose a CSV or Image file", type=["csv", "jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        enriched_df = pd.DataFrame()
        
        with st.spinner("Processing file..."):
            if uploaded_file.type == "text/csv":
                df_csv= pd.read_csv(uploaded_file)
                if df_csv.empty:
                    st.error("Could not extract any data from the CSV.")
                    return
                
                if 'description' not in df_csv.columns:
                    text_cols = [c for c in df_csv.columns if df_csv[c].dtype == 'object']
                    if text_cols:
                        df_csv= df_csv.rename(columns={text_cols[0]: 'description'})
                    else:
                        st.error("No description column found in CSV.")
                        return

                if 'amount' not in df_csv.columns:
                    num_cols = [c for c in df_csv.columns if df_csv[c].dtype in ['float64', 'int64']]
                    if num_cols:
                        df_csv= df_csv.rename(columns={num_cols[0]: 'amount_spent'})
                    else:
                        df_csv['amount_spent'] = 0
                else:
                    df_csv= df_csv.rename(columns={'amount': 'amount_spent'})

                response = categorizer(df_csv)
                categorized_df = categorize_transaction(response)
                enriched_df = combiner(df_csv, categorized_df)
                
            elif uploaded_file.type in ["image/jpeg", "image/png"]:
                df_img = image_to_df(uploaded_file)
                response = categorizer(df_img)
                categorized_df = categorize_transaction(response)
                enriched_df = combiner(df_img,categorized_df)
            
            else :
                st.error("Unsupported file type.")
                return

        if enriched_df.empty:
            st.warning("No transactions found to analyze.")
            return

        st.divider()
        st.subheader("Categorized Data")
        st.dataframe(enriched_df, use_container_width=True)
        
        st.subheader("Income")
        income = enriched_df[enriched_df['transaction_type'] == 'income']['amount_spent'].sum()
        st.write(f"${income:,.2f}")

        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top Expenses")
            st.write(top_expenses_by_category(enriched_df))
            
        with col2:
            st.subheader("Bottom Expenses")
            st.write(bottom_expenses_by_category(enriched_df))
                
        st.divider()
        st.subheader("Investment and Savings")
        investment, savings = investment_analysis(enriched_df)
        c1, c2 = st.columns(2)
        c1.metric("Investment", f"${investment:,.2f}")
        c2.metric("Savings", f"${savings:,.2f}")

        st.divider()
        st.subheader("Visualizations")
        v1, v2, v3 = st.columns(3)
        with v1: plot_income_vs_expenses(enriched_df)
        with v2: plot_expenses_by_category(enriched_df)

        st.divider()
        st.subheader("AI-Generated Comprehensive Summary")
        with st.spinner("Generating summary..."):
            summary = summarize_expenses(
                top_expenses_by_category(enriched_df), 
                bottom_expenses_by_category(enriched_df), 
                income, 
                investment, 
                savings
            )
            st.info(summary)

if __name__ == "__main__":
    main()
