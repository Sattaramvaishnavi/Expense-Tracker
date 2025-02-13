from expense import Expense
from typing import List
import calendar
import datetime
def main():
    print(f"Running Expense Tracker!")
    expense_file_path="expense.csv"
    budget=2000

    #get user input for expense
    expense=get_user_input()
    

    #write their expense to a file
    save_expense_to_file(expense, expense_file_path)
    #read file and summaraize expenses
    summarize_expense(expense_file_path,budget)

def get_user_input():
    print("Welcome to the expense tracker! 🤑")
    expense_name=input("Enter expense name : ")
    expense_amount=float(input("Enter expense amount: "))
    #print(f"you have entered {expense_name},{expense_amount}")
    Expense_categories=[
        "🍔Food",
        "🏠Home",
        "🎉Fun",
        "💼Work"
    ]
    while True:
        print("select a category")
        for i,category_name in enumerate(Expense_categories):
            print(f"{i+1}.{category_name}") 
        
        value_range= f"[1-{len(Expense_categories)}]"
        selected_index=int(input(f"Enter a category number {value_range}:"))-1
        if selected_index in range(len(Expense_categories)):
            selected_category=Expense_categories[selected_index]
            new_expense=Expense(
                name=expense_name,category=selected_category,amount=expense_amount
            )
            return new_expense
        else:
            print("Invalid category.Please try again!")
          
         

def save_expense_to_file(expense:Expense,expense_file_path):
    print(f"Saving user expense:{expense} to {expense_file_path}")
    with open(expense_file_path,"a",encoding="utf-8") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")
    

def summarize_expense(expense_file_path,budget):
    print(f"summarize user  expense")
    expenses: List[Expense]=[]
    try:
        with open(expense_file_path,"r",encoding="utf-8") as f:
            lines=f.readlines()
            for line in lines:
                #print(line)
                line=line.strip()
                if not line:
                    continue
                try:
                    expense_name,expense_amount,expense_category=line.split(",")
                    line_expense=Expense(
                        name=expense_name,amount=float(expense_amount),category=expense_category
                    )
                #print(line_expense)
                    expenses.append(line_expense)
                except ValueError:
                    print(f"Skipping invalid line:{line}")
                    continue
    except FileNotFoundError:
        print("no expenses recorded yet")
        return
    #print(expenses)
    amount_by_category={}
    for expense in expenses:
        key=expense.category
        if key in amount_by_category:
            amount_by_category[key]+=expense.amount
        else:
            amount_by_category[key]=expense.amount
    #print(amount_by_category)
    print("📈 Expenses by category:")
    for key,amount in amount_by_category.items():
        print(f"{key}: ${amount:.2f}")

    total_spent=sum([ex.amount for ex in expenses])
    print(f"total spent: ${total_spent:.2f} ")

    remaining_budget=budget-total_spent
    print(f"Budget remaining: ${remaining_budget:.2f} ")

    #get the current date
    now=datetime.datetime.now()
    #number of days in current month
    days_in_month=calendar.monthrange(now.year,now.month)[1]
    #remaining days in month
    remaining_days=days_in_month-now.day
    print("Remaining days in the month:",remaining_days)
    daily_budget=remaining_budget/remaining_days
    print(green(f"budget per day: ${daily_budget:.2f}"))

def green(text):
    return f"\033[92m{text}\033[0m"

if __name__== "__main__":
    main()
  
    