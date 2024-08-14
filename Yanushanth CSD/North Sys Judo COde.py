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
        print(f"Error: {e}")
        return None, None, None, None

# Function to determine weight category based on the entered weight
def determine_weight_category(weight):
    for category, limit in WEIGHT_CATEGORIES.items():
        if weight <= limit:
            return category
    return "Heavyweight"  # Default if weight exceeds all categories

# Main program logic
def main():
    while True:
        try:
            # Gather athlete's name
            while True:
                try:
                    athlete_name = input("Enter athlete name: ").strip()
                    if not athlete_name:
                        raise ValueError("Athlete name cannot be empty. Please enter a valid athlete name.")
                    break
                except ValueError as e:
                    print(f"Error: {e}. Please enter a valid athlete name.")

            # Gather and validate the training plan
            while True:
                try:
                    training_plan = input("Enter training plan (Beginner, Intermediate, Elite): ").strip()
                    if training_plan not in TRAINING_PLAN_COSTS:
                        raise ValueError("Invalid training plan. Please enter 'Beginner', 'Intermediate', or 'Elite'.")
                    break
                except ValueError as e:
                    print(f"Error: {e}. Please enter a valid training plan.")

            # Gather and validate the weight
            while True:
                try:
                    weight = float(input("Enter current weight in kg: ").strip())
                    if weight <= 0:
                        raise ValueError("Weight must be a positive number.")
                    break
                except ValueError as e:
                    print(f"Error: {e}. Please enter a valid weight.")

            if training_plan == 'Beginner':
                # Check if weight is less than Flyweight
                if weight < WEIGHT_CATEGORIES['Flyweight']:
                    print("As a Beginner, your weight is less than Flyweight. You are not eligible to participate in competitions.")
                else:
                    print("You are a Beginner. You are not eligible to participate in competitions.")
                
                # Gather and validate private coaching hours
                while True:
                    try:
                        private_coaching_hours = int(input("Enter number of hours for private coaching: ").strip())
                        if private_coaching_hours < 0:
                            raise ValueError("Private coaching hours cannot be negative.")
                        if private_coaching_hours > 5:
                            raise ValueError("Private coaching hours cannot exceed 5 per week.")
                        break
                    except ValueError as e:
                        print(f"Error: {e}. Please enter a valid number of private coaching hours.")

                # Calculate fees without competition costs
                monthly_training_cost, private_coaching_cost, _, total_cost = calculate_fees(
                    training_plan, 0, private_coaching_hours
                )

                # Output results
                print(f"\nAthlete: {athlete_name}")
                print(f"Current weight: {weight} kg")
                print(f"Monthly training cost: Rs. {monthly_training_cost:.2f}")
                print(f"Private coaching cost: Rs. {private_coaching_cost:.2f}")
                print(f"Total monthly cost: Rs. {total_cost:.2f}")

            else:
                print("Congratulations!!! You are eligible to participate in competitions.")

                # Determine weight category based on the entered weight
                competition_weight_category = determine_weight_category(weight)
                print(f"Automatically determined weight category: {competition_weight_category}")

                # Check if the athlete is eligible for competition
                eligible_for_competition = competition_weight_category in ELIGIBLE_COMPETITION_CATEGORIES

                if eligible_for_competition:
                    print("Congratulations!!! You are eligible to participate in competitions.")
                else:
                    print(f"Sorry, you are not in an eligible weight category for competitions ({competition_weight_category}).")

                # Gather and validate private coaching hours
                while True:
                    try:
                        private_coaching_hours = int(input("Enter number of hours for private coaching: ").strip())
                        if private_coaching_hours < 0:
                            raise ValueError("Private coaching hours cannot be negative.")
                        if private_coaching_hours > 5:
                            raise ValueError("Private coaching hours cannot exceed 5 per week.")
                        break
                    except ValueError as e:
                        print(f"Error: {e}. Please enter a valid number of private coaching hours.")

                # Gather and validate number of competitions entered
                while True:
                    try:
                        competitions_entered = int(input("Enter number of competitions entered this month: ").strip())
                        if competitions_entered < 0:
                            raise ValueError("Number of competitions cannot be negative.")

                        # Ask if the athlete participated in an additional competition
                        while True:
                            try:
                                additional_competition = input("Did you participate in an additional competition? (yes/no): ").strip().lower()
                                if additional_competition == 'yes':
                                    competitions_entered += 1
                                    break
                                elif additional_competition == 'no':
                                    break
                                else:
                                    raise ValueError("Please enter 'yes' or 'no'.")
                            except ValueError as e:
                                print(f"Error: {e}. Please enter 'yes' or 'no'.")

                        # Calculate fees
                        monthly_training_cost, private_coaching_cost, competition_cost, total_cost = calculate_fees(
                            training_plan, competitions_entered, private_coaching_hours
                        )
                        break
                    except ValueError as e:
                        print(f"Error: {e}. Please enter a valid number of competitions.")

                # Output results
                print(f"\nAthlete: {athlete_name}")
                print(f"Current weight: {weight} kg")
                print(f"Monthly training cost: Rs. {monthly_training_cost:.2f}")
                print(f"Private coaching cost: Rs. {private_coaching_cost:.2f}")
                print(f"Competition cost: Rs. {competition_cost:.2f}")
                print(f"Total monthly cost: Rs. {total_cost:.2f}")

            # Ask if the user wants to add another athlete
            while True:
                try:
                    another_athlete = input("Do you want to add details for another athlete? (yes/no): ").strip().lower()
                    if another_athlete not in ['yes', 'no']:
                        raise ValueError("Please enter 'yes' or 'no'.")
                    if another_athlete != 'yes':
                        return
                    break
                except ValueError as e:
                    print(f"Error: {e}. Please enter 'yes' or 'no'.")

        except ValueError as e:
            print(f"Error: {e}. Please try again.")
        except KeyError as e:
            print(f"Error: {e}. Please enter a valid category.")

if __name__ == "__main__":
    main()
