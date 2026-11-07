import re
from datetime import datetime


class Expense:
    """Stores one expense record."""

    def __init__(self, amount, category, date, payment):
        self.__amount = amount
        self.category = category
        self.date = date
        self.payment = payment

    @property
    def amount(self):
        return self.__amount

    def display(self):
        return (
            f"{self.date} | {self.category} | "
            f"Rs.{self.amount:.2f} | {self.payment}"
        )


class ExpenseTracker:
    def __init__(self, filename="expenses.txt"):
        self.filename = filename
        self.expenses = []
        self.load_data()

    def load_data(self):
        """Load saved expenses when the program starts."""
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                for line in file:
                    parts = line.strip().split("|")

                    if len(parts) != 4:
                        continue

                    date, category, amount_text, payment = parts

                    try:
                        amount = float(amount_text)
                        datetime.strptime(date, "%d-%m-%Y")
                    except ValueError:
                        continue

                    if amount <= 0 or len(category.strip()) < 3:
                        continue

                    if payment not in ("Cash", "Online"):
                        continue

                    self.expenses.append(
                        Expense(amount, category, date, payment)
                    )

        except FileNotFoundError:
            # No saved file yet. It will be created when an expense is added.
            pass

    def save_expense(self, expense):
        """Append one new record to the file immediately."""
        with open(self.filename, "a", encoding="utf-8") as file:
            file.write(
                f"{expense.date}|{expense.category}|"
                f"{expense.amount}|{expense.payment}\n"
            )

    def add_expense(self):
        """Accept, validate, save and add a new expense."""
        try:
            amount = float(input("Enter amount (Rs.): "))
            if amount <= 0:
                print("Entry not saved: amount must be greater than zero.")
                return

            category = input("Enter category (at least 3 characters): ").strip()
            if len(category) < 3 or "|" in category:
                print("Entry not saved: category must have at least 3 characters.")
                return

            date = input("Enter date (DD-MM-YYYY): ").strip()
            if not re.fullmatch(r"\d{2}-\d{2}-\d{4}", date):
                print("Entry not saved: use DD-MM-YYYY.")
                return

            try:
                datetime.strptime(date, "%d-%m-%Y")
            except ValueError:
                print("Entry not saved: enter a real calendar date.")
                return

            payment_input = input("Payment method (Cash/Online): ").strip().lower()
            if payment_input not in ("cash", "online"):
                print("Entry not saved: choose Cash or Online.")
                return

            payment = payment_input.title()
            expense = Expense(amount, category, date, payment)

            # Save first; then update the in-memory list.
            self.save_expense(expense)
            self.expenses.append(expense)

            print("Expense saved successfully.")

        except ValueError:
            print("Entry not saved: amount must be a valid number.")

    def show_expenses(self):
        if not self.expenses:
            print("No saved expenses to display.")
            return

        print("\nDATE | CATEGORY | AMOUNT | PAYMENT")
        print("-" * 55)
        for expense in self.expenses:
            print(expense.display())

    def total_expense(self):
        total = sum(expense.amount for expense in self.expenses)
        print(f"Total expenditure: Rs.{total:.2f}")

    def highest_expense(self):
        if not self.expenses:
            print("No saved expenses to analyse.")
            return

        highest = max(self.expenses, key=lambda expense: expense.amount)
        print("Highest expense:", highest.display())

    def category_report(self):
        if not self.expenses:
            print("No saved expenses to analyse.")
            return

        report = {}
        for expense in self.expenses:
            report[expense.category] = (
                report.get(expense.category, 0) + expense.amount
            )

        print("\nCATEGORY-WISE EXPENDITURE")
        for category, total in report.items():
            print(f"{category}: Rs.{total:.2f}")

    def check_budget(self):
        try:
            budget = float(input("Enter budget (Rs.): "))
            if budget <= 0:
                print("Budget must be greater than zero.")
                return

            total = sum(expense.amount for expense in self.expenses)

            if total > budget:
                print(f"Budget exceeded by: Rs.{total - budget:.2f}")
            else:
                print(f"Remaining budget: Rs.{budget - total:.2f}")

        except ValueError:
            print("Please enter a valid numerical budget.")


def main():
    tracker = ExpenseTracker()

    while True:
        print("\n===== PERSONAL EXPENSE TRACKER =====")
        print("1. Add Expense")
        print("2. View Saved Expenses")
        print("3. Total Expenditure")
        print("4. Highest Expense")
        print("5. Category Report")
        print("6. Check Budget")
        print("7. Exit")

        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            tracker.add_expense()
        elif choice == "2":
            tracker.show_expenses()
        elif choice == "3":
            tracker.total_expense()
        elif choice == "4":
            tracker.highest_expense()
        elif choice == "5":
            tracker.category_report()
        elif choice == "6":
            tracker.check_budget()
        elif choice == "7":
            print("Expense Tracker closed.")
            break
        else:
            print("Invalid option. Choose a number from 1 to 7.")


if __name__ == "__main__":
    main()
