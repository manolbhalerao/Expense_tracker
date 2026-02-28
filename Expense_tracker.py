import pandas as pd
import os
import datetime
import calendar


class ExpenseTracker:
    def __init__(self, file_path="expense.csv", budget=2000):
        self.file_path = file_path
        self.budget = budget
        self.load_data()

    # ------------------ LOAD DATA ------------------
    def load_data(self):
        if os.path.exists(self.file_path):
            self.df = pd.read_csv(self.file_path)
        else:
            self.df = pd.DataFrame(columns=["ID", "Date", "Name", "Category", "Amount"])
            self.df.to_csv(self.file_path, index=False)

    # ------------------ SAVE DATA ------------------
    def save_data(self):
        self.df.to_csv(self.file_path, index=False)

    # ------------------ ADD EXPENSE ------------------
    def add_expense(self):
        name = input("Enter expense name: ")
        try:
            amount = float(input("Enter expense amount: "))
        except exception as e:
            print("Some error occurred",e)
            return

        categories = ["Food", "Travel", "Home", "Health", "Shopping", "Other"]
        print("Select category:")
        for i, cat in enumerate(categories):
            print(f"{i+1}. {cat}")

        choice = int(input("Enter choice: ")) - 1
        if choice not in range(len(categories)):
            print("Invalid category!")
            return

        category = categories[choice]
        date = datetime.date.today().strftime("%Y-%m-%d")

        if self.df.empty:
            new_id = 1
        else:
            new_id = int(self.df["ID"].max()) + 1

        new_row = {
            "ID": new_id,
            "Date": date,
            "Name": name,
            "Category": category,
            "Amount": amount
        }

        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
        self.save_data()
        print("Expense added successfully!")

    # ------------------ VIEW ALL ------------------
    def view_expenses(self):
        if self.df.empty:
            print("No expenses recorded.")
        else:
            print(self.df)

    # ------------------ CATEGORY SUMMARY ------------------
    def category_summary(self):
        if self.df.empty:
            print("No data available.")
            return

        summary = self.df.groupby("Category")["Amount"].sum()
        print("\nExpenses by Category:")
        print(summary)

    # ------------------ MONTHLY SUMMARY ------------------
    def monthly_summary(self):
        if self.df.empty:
            print("No data available.")
            return

        self.df["Date"] = pd.to_datetime(self.df["Date"], errors="coerce")
        now = datetime.datetime.now()
        current_month_data = self.df[
            (self.df["Date"].dt.month == now.month) &
            (self.df["Date"].dt.year == now.year)
        ]

        total = current_month_data["Amount"].sum()
        print(f"\nTotal spent this month: ₹{total:.2f}")

    # ------------------ BUDGET ANALYSIS ------------------
    def budget_analysis(self):
        if self.df.empty:
            print("No expenses recorded.")
            return

        total_spent = self.df["Amount"].sum()
        remaining = self.budget - total_spent

        now = datetime.datetime.now()
        days_in_month = calendar.monthrange(now.year, now.month)[1]
        remaining_days = days_in_month - now.day

        print(f"\nTotal Spent: ₹{total_spent:.2f}")
        print(f"Remaining Budget: ₹{remaining:.2f}")

        if remaining_days > 0:
            daily_budget = remaining / remaining_days
            print(f"Suggested Daily Budget: ₹{daily_budget:.2f}")

    # ------------------ DELETE EXPENSE ------------------
    def delete_expense(self):
        if self.df.empty:
            print("No expenses to delete.")
            return

        expense_id = int(input("Enter Expense ID to delete: "))
        if expense_id not in self.df["ID"].values:
            print("Expense ID not found!")
            return
        self.df = self.df[self.df["ID"] != expense_id]
        self.save_data()
        print("Expense deleted successfully!")

    # ------------------ MENU LOOP ------------------
    def run(self):
        while True:
            print("\n==== Expense Tracker Menu ====")
            print("1. Add Expense")
            print("2. View All Expenses")
            print("3. Category Summary")
            print("4. Monthly Summary")
            print("5. Budget Analysis")
            print("6. Delete Expense")
            print("7. Exit")

            choice = input("Enter choice: ")

            if choice == "1":
                self.add_expense()
            elif choice == "2":
                self.view_expenses()
            elif choice == "3":
                self.category_summary()
            elif choice == "4":
                self.monthly_summary()
            elif choice == "5":
                self.budget_analysis()
            elif choice == "6":
                self.delete_expense()
            elif choice == "7":
                print("Exiting program...")
                break
            else:
                print("Invalid choice!")


if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.run()
