import tkinter as tk
from tkinter import messagebox

# Define constants
TRAINING_PLAN_COSTS = {
    'Beginner': 2000,
    'Intermediate': 5000,
    'Elite': 7000
}

PRIVATE_COACHING_COST_PER_HOUR = 500
COMPETITION_ENTRY_FEE = 2500

WEIGHT_CATEGORIES = {
    'Flyweight': 66,
    'Lightweight': 73,
    'Light - Middleweight': 81,
    'Middleweight': 90,
    'Light - Heavyweight': 100,
    'Heavyweight': float('inf')  # Represents no upper limit for Heavyweight
}

ELIGIBLE_COMPETITION_CATEGORIES = ['Light - Middleweight', 'Middleweight', 'Light - Heavyweight']

# Function to determine weight category based on the entered weight
def determine_weight_category(weight):
    for category, limit in WEIGHT_CATEGORIES.items():
        if weight <= limit:
            return category
    return "Heavyweight"  # Default if weight exceeds all categories

# Function to calculate fees
def calculate_fees(training_plan, competitions_entered, private_coaching_hours):
    try:
        # Validate private coaching hours
        if private_coaching_hours > 5:
            raise ValueError("Private coaching hours cannot exceed 5 per week.")

        weekly_fee = TRAINING_PLAN_COSTS[training_plan]
        monthly_training_cost = weekly_fee * 4
        private_coaching_cost = private_coaching_hours * PRIVATE_COACHING_COST_PER_HOUR
        competition_cost = competitions_entered * COMPETITION_ENTRY_FEE
        total_cost = monthly_training_cost + private_coaching_cost + competition_cost

        return monthly_training_cost, private_coaching_cost, competition_cost, total_cost

    except ValueError as e:
        return None, None, None, e

# Function to handle form submission
def submit_form():
    try:
        # Gather and validate the data from the form
        athlete_name = name_entry.get().strip()
        if not athlete_name:
            raise ValueError("Athlete name cannot be empty.")

        training_plan = training_plan_var.get()
        if training_plan not in TRAINING_PLAN_COSTS:
            raise ValueError("Invalid training plan. Please select 'Beginner', 'Intermediate', or 'Elite'.")

        try:
            weight = float(weight_entry.get())
            if weight <= 0:
                raise ValueError("Weight must be a positive number.")
        except ValueError:
            raise ValueError("Invalid weight. Please enter a valid number.")

        private_coaching_hours = int(coaching_hours_entry.get())
        if private_coaching_hours < 0:
            raise ValueError("Private coaching hours cannot be negative.")
        if private_coaching_hours > 5:
            raise ValueError("Private coaching hours cannot exceed 5 per week.")

        competition_participation = participate_var.get()

        if training_plan == 'Beginner':
            if weight < WEIGHT_CATEGORIES['Flyweight']:
                messagebox.showinfo("Weight Category", "Your weight is less than Flyweight.")
            messagebox.showinfo("Result", "As a Beginner, you are not eligible to participate in competitions.")
            monthly_training_cost, private_coaching_cost, _, total_cost = calculate_fees(
                training_plan, 0, private_coaching_hours
            )
            result = (f"Monthly training cost: Rs. {monthly_training_cost:.2f}\n"
                      f"Private coaching cost: Rs. {private_coaching_cost:.2f}\n"
                      f"Total monthly cost: Rs. {total_cost:.2f}")
            messagebox.showinfo("Costs", result)
        else:
            competition_weight_category = determine_weight_category(weight)
            eligible_for_competition = competition_weight_category in ELIGIBLE_COMPETITION_CATEGORIES

            if competition_participation and not eligible_for_competition:
                messagebox.showinfo("Result", f"Sorry, you are not in an eligible weight category for competitions ({competition_weight_category}).")

            competitions_entered = int(competitions_entry.get())
            if competitions_entered < 0:
                raise ValueError("Number of competitions cannot be negative.")

            # Increment competition count if participating
            if competition_participation:
                competitions_entered += 1

            monthly_training_cost, private_coaching_cost, competition_cost, total_cost = calculate_fees(
                training_plan, competitions_entered, private_coaching_hours
            )

            result = (f"Monthly training cost: Rs. {monthly_training_cost:.2f}\n"
                      f"Private coaching cost: Rs. {private_coaching_cost:.2f}\n"
                      f"Competition cost: Rs. {competition_cost:.2f}\n"
                      f"Total monthly cost: Rs. {total_cost:.2f}")
            messagebox.showinfo("Costs", result)

    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Function to update UI based on selected training plan
def update_ui_based_on_training_plan():
    training_plan = training_plan_var.get()
    if training_plan == 'Beginner':
        participate_checkbox.config(state='disabled')
        competitions_entry.config(state='disabled')
    else:
        participate_checkbox.config(state='normal')
        competitions_entry.config(state='normal')

# Create the main application window
root = tk.Tk()
root.title("Athlete Fee Calculator")

# Create and place widgets
tk.Label(root, text="Athlete Name:").grid(row=0, column=0, padx=10, pady=5)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Training Plan:").grid(row=1, column=0, padx=10, pady=5)

# Create radio buttons for training plan
training_plan_var = tk.StringVar(value='Beginner')
tk.Radiobutton(root, text="Beginner", variable=training_plan_var, value="Beginner", command=update_ui_based_on_training_plan).grid(row=1, column=1, padx=10, pady=5, sticky='w')
tk.Radiobutton(root, text="Intermediate", variable=training_plan_var, value="Intermediate", command=update_ui_based_on_training_plan).grid(row=2, column=1, padx=10, pady=5, sticky='w')
tk.Radiobutton(root, text="Elite", variable=training_plan_var, value="Elite", command=update_ui_based_on_training_plan).grid(row=3, column=1, padx=10, pady=5, sticky='w')

tk.Label(root, text="Current Weight (kg):").grid(row=4, column=0, padx=10, pady=5)
weight_entry = tk.Entry(root)
weight_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="Private Coaching Hours:").grid(row=5, column=0, padx=10, pady=5)
coaching_hours_entry = tk.Entry(root)
coaching_hours_entry.grid(row=5, column=1, padx=10, pady=5)

participate_var = tk.BooleanVar()
participate_checkbox = tk.Checkbutton(root, text="Participate in Competition", variable=participate_var)
participate_checkbox.grid(row=6, column=0, columnspan=2, pady=5)

tk.Label(root, text="Number of Competitions:").grid(row=7, column=0, padx=10, pady=5)
competitions_entry = tk.Entry(root)
competitions_entry.grid(row=7, column=1, padx=10, pady=5)

tk.Button(root, text="Submit", command=submit_form).grid(row=8, column=0, columnspan=2, pady=10)

# Initialize the UI state based on the default selected training plan
update_ui_based_on_training_plan()

# Run the application
root.mainloop()
