import streamlit as st
import pandas as pd 
from input.image_to_df import image_to_df
from categorizer.data_combiner import combine
from categorizer.categorize_transaction import categorize_transaction
from analysis.expense_analyzer import *
from analysis.expense_summarizer import summarize_expenses
from analysis.chatbot import get_chat_response
from categorizer.categorizer import categorizer

@st.fragment
def render_chatbot(expense_context=""):
    """Render the finance chatbot in the sidebar."""
    st.title("💬 Finance Assistant")
    if expense_context:
        st.caption("I've analyzed your data. Ask me to clarify anything!")
        # Add a small expandable summary for reference in the sidebar
        with st.expander("📊 Current Analysis Summary", expanded=False):
            st.write(expense_context)
    else:
        st.caption("Ask me anything about personal finance!")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        icon = "🧑" if msg["role"] == "user" else "🤖"
        st.chat_message(msg["role"], avatar=icon).write(msg["content"])

    if user_input := st.chat_input("e.g. How can I save more?"):
        st.chat_message("user", avatar="🧑").write(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.spinner("Thinking..."):
            reply = get_chat_response(user_input, st.session_state.chat_history[:-1], expense_context)
        st.chat_message("assistant", avatar="🤖").write(reply)
        st.session_state.chat_history.append({"role": "model", "content": reply})


def main():
    st.set_page_config(page_title="Personal Expense Tracker", layout="wide")
    st.title("Personal Expense Tracker")
    st.write("Upload your financial transaction data in CSV or Image format to track and analyze your expenses and income.")   
    
    uploaded_file = st.file_uploader("Choose a CSV or Image file", type=["csv", "jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        combined_df = pd.DataFrame()
        
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
                combined_df = combine(df_csv, categorized_df)
                
            elif uploaded_file.type in ["image/jpeg", "image/png"]:
                df_img = image_to_df(uploaded_file)
                response = categorizer(df_img)
                categorized_df = categorize_transaction(response)
                combined_df = combine(df_img, categorized_df)
            
            else :
                st.error("Unsupported file type.")
                return

        if combined_df.empty:
            st.warning("No transactions found to analyze.")
            return

        st.divider()
        st.subheader("Categorized Data")
        st.dataframe(combined_df, use_container_width=True)
        
        st.subheader("Income")
        income = combined_df[combined_df['transaction_type'] == 'income']['amount_spent'].sum()
        st.write(f"${income:,.2f}")

        col1, col2 = st.columns(2)
        
        top_exp = top_expenses_by_category(combined_df)
        bottom_exp = bottom_expenses_by_category(combined_df)

        with col1:
            st.subheader("Top Expenses")
            st.write(top_exp)
            
        with col2:
            st.subheader("Bottom Expenses")
            st.write(bottom_exp)
                
        st.divider()
        st.subheader("Investment and Savings")
        investment, savings = investment_analysis(combined_df)
        c1, c2 = st.columns(2)
        c1.metric("Investment", f"${investment:,.2f}")
        c2.metric("Savings", f"${savings:,.2f}")

        st.divider()
        st.subheader("Visualizations")
        v1, v2, v3 = st.columns(3)
        with v1: plot_income_vs_expenses(combined_df)
        with v2: plot_expenses_by_category(combined_df)

        st.divider()
        st.subheader("AI-Generated Comprehensive Summary")
        with st.spinner("Generating summary..."):
            summary = summarize_expenses(top_exp, bottom_exp, income, investment, savings)
            st.info(summary)

        st.session_state["analysis_context"] = (
            f"=== User's Financial Overview ===\n"
            f"Total Income: ${income:,.2f}\n"
            f"Total Investment: ${investment:,.2f}\n"
            f"Total Savings: ${savings:,.2f}\n\n"
            f"Top Expenses by Category:\n{top_exp.to_string()}\n\n"
            f"Bottom Expenses by Category:\n{bottom_exp.to_string()}\n\n"
            f"AI Summary:\n{summary}"
        )

    with st.sidebar:
        render_chatbot(st.session_state.get("analysis_context", ""))

if __name__ == "__main__":
    main()
