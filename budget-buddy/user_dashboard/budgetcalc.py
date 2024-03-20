def calculate_daily_budget(salary, savings_percentage):
    daily_budget = (salary / 30) * (1 - savings_percentage / 100)
    return daily_budget

def main():
    salary = float(input("Enter your monthly salary: "))
    savings_percentages = [15, 20, 30]

    for savings_percentage in savings_percentages:
        daily_budget = calculate_daily_budget(salary, savings_percentage)
        remaining_amount = 0

        for day in range(1, 31):
            user_input = input(f"Day {day}: Enter your spending for today (press Enter to skip): ")
            if user_input.strip(): 
                spending = float(user_input)
                if spending > daily_budget:
                    print("Warning: Your spending exceeds today's budget!")
                else:
                    remaining_amount += daily_budget - spending
            else:
                remaining_amount += daily_budget
            
            if day < 30:
                print(f"Remaining amount for tomorrow: {remaining_amount:.2f}")
                print()

        print(f"Total unspent amount for the month with {savings_percentage}% savings: {remaining_amount:.2f}")
        print("------------------------------------------------------")

if __name__ == "__main__":
    main()
