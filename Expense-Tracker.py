import calendar
import datetime
from typing import List

# Define the Expense class
class Expense:
    def __init__(self, name: str, category: str, amount: float):
        self.name = name
        self.category = category
        self.amount = amount

    def __repr__(self):
        return f"Expense(name='{self.name}', category='{self.category}', amount={self.amount})"

def main():
    print("Running Expense Tracker!")
    expense_file_path = "expense.csv"
    budget = 2000

    # Get user input for expense
    expense = get_user_input()

    # Write their expense to a file
    save_expense_to_file(expense, expense_file_path)

    # Read file and summarize expenses
    summarize_expense(expense_file_path, budget)

def get_user_input():
    print("Welcome to the expense tracker! 🤑")
    expense_name = input("Enter expense name: ")

    # Handle invalid input for expense amount
    while True:
        try:
            expense_amount = float(input("Enter expense amount: "))
            break
        except ValueError:
            print("Invalid amount. Please enter a valid number.")

    Expense_categories = [
        "🍔 Food",
        "🏠 Home",
        "🎉 Fun",
        "💼 Work"
    ]

    while True:
        print("Select a category:")
        for i, category_name in enumerate(Expense_categories):
            print(f"{i + 1}. {category_name}")

        value_range = f"[1-{len(Expense_categories)}]"
        
        # Handle invalid category input
        try:
            selected_index = int(input(f"Enter a category number {value_range}: ")) - 1
            if selected_index in range(len(Expense_categories)):
                selected_category = Expense_categories[selected_index]
                break
            else:
                print("Invalid category number. Please select a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    return Expense(name=expense_name, category=selected_category, amount=expense_amount)

def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"Saving user expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a", encoding="utf-8") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")

def summarize_expense(expense_file_path, budget):
    print("Summarizing user expenses...")
    expenses: List[Expense] = []

    # Handle file not found error
    try:
        with open(expense_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                try:
                    expense_name, expense_amount, expense_category = line.split(",")
                    line_expense = Expense(
                        name=expense_name, amount=float(expense_amount), category=expense_category
                    )
                    expenses.append(line_expense)
                except ValueError:
                    print(f"Skipping invalid line: {line}")
                    continue
    except FileNotFoundError:
        print("No expenses recorded yet.")
        return

    # Calculate expenses by category
    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        amount_by_category[key] = amount_by_category.get(key, 0) + expense.amount

    print("📈 Expenses by category:")
    for key, amount in amount_by_category.items():
        print(f"{key}: ${amount:.2f}")

    # Calculate total spending and remaining budget
    total_spent = sum(exp.amount for exp in expenses)
    print(f"Total spent: ${total_spent:.2f}")

    remaining_budget = budget - total_spent
    print(f"Budget remaining: ${remaining_budget:.2f}")

    # Get the current date
    now = datetime.datetime.now()

    # Number of days in the current month
    days_in_month = calendar.monthrange(now.year, now.month)[1]

    # Remaining days in the month
    remaining_days = days_in_month - now.day

    print("Remaining days in the month:", remaining_days)

    # Prevent division by zero error
    if remaining_days > 0:
        daily_budget = remaining_budget / remaining_days
        print(green(f"Budget per day: ${daily_budget:.2f}"))
    else:
        print("No days left in the month to calculate a daily budget.")

def green(text):
    return f"\033[92m{text}\033[0m"

if __name__ == "__main__":
    main()
