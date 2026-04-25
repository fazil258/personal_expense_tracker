import pandas as pd

CATEGORIES_MAP = {
    "Food": "expense", "Travel": "expense", "Entertainment": "expense",
    "Utilities": "expense", "Health": "expense", "Education": "expense",
    "Shopping": "expense", "Others": "expense", "Income": "income",
    "Investment": "investment", "Savings": "savings"
}

def get_transaction_type(category):
    if not category:
        return "expense"
    if isinstance(category, str):
        return CATEGORIES_MAP.get(category.capitalize(), "expense")
    return "expense"


def categorize_transaction(category_list, transaction_type=None):
    records = []
    if not isinstance(category_list, list):
        category_list = [category_list] if category_list else []
        
    for item in category_list:
        if not isinstance(item, dict): continue
        t_type = get_transaction_type(item.get("category", "Others"))
        records.append({
            "description": item.get("description", "Unknown description"),
            "category": item.get("category", "Others"),
            "transaction_type": t_type
        })
    return pd.DataFrame(records)