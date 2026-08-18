import pandas as pd
import matplotlib.pyplot as plt

# Professional Inventory Tracker with Continuous Adding, COGS per Unit, Selling Price per Unit, and Visualization

def add_item(inventory, num_items):
    for _ in range(num_items):
        while True:
            item_name = input("Enter item name: ")

            # Check if the item name already exists
            if item_name in inventory:
                print(f"\nError: Item '{item_name}' already exists in the inventory. Please enter a unique item name.")
            elif not item_name.isalpha():
                print("\nError: Item name should contain only letters. Please enter a valid item name.")
            else:
                break

        while True:
            try:
                initial_quantity = int(input("Enter initial quantity: "))
                cogs_per_unit = float(input("Enter Cost of Goods Sold (COGS) per unit: $"))
                selling_price_per_unit = float(input("Enter Selling Price per unit: $"))
                break
            except ValueError:
                print("\nError: Please enter a valid numeric value for quantity, COGS, and selling price.")

        inventory[item_name] = {
            "quantity": initial_quantity,
            "cogs_per_unit": cogs_per_unit,
            "selling_price_per_unit": selling_price_per_unit,
            "profit_per_unit": selling_price_per_unit - cogs_per_unit
        }

        print(f"\n{initial_quantity} units of {item_name} added to the inventory.")

def add_quantity(inventory, name, additional_quantity):
    if name in inventory:
        while True:
            try:
                inventory[name]["quantity"] += int(additional_quantity)
                break
            except ValueError:
                print("\nError: Please enter a valid numeric value for quantity.")
        print(f"\n{additional_quantity} units added to the quantity of {name}.")
    else:
        print(f"\nError: Item '{name}' not found in inventory.")

def remove_quantity(inventory, name, quantity):
    if name in inventory:
        current_quantity = inventory[name]["quantity"]
        while True:
            try:
                if int(quantity) <= current_quantity:
                    inventory[name]["quantity"] -= int(quantity)
                    print(f"\n{quantity} units of {name} removed from the inventory.")
                else:
                    print(f"\nError: Insufficient quantity of {name} in the inventory.")
                break
            except ValueError:
                print("\nError: Please enter a valid numeric value for quantity.")
    else:
        print(f"\nError: Item '{name}' not found in inventory.")

def display_summary(inventory):
    print("\nInventory Summary:")
    for item, details in inventory.items():
        print(f"{item}: Quantity - {details['quantity']} units, COGS per Unit - ${details['cogs_per_unit']:.2f}, Selling Price per Unit - ${details['selling_price_per_unit']:.2f}, Profit per Unit - ${details['profit_per_unit']:.2f}")

def search_item(inventory, name):
    details = inventory.get(name)
    if details is not None:
        print(f"\nItem found:")
        print(f"{name}: Quantity - {details['quantity']} units, COGS per Unit - ${details['cogs_per_unit']:.2f}, Selling Price per Unit - ${details['selling_price_per_unit']:.2f}, Profit per Unit - ${details['profit_per_unit']:.2f}")
    else:
        print(f"\nError: Item '{name}' not found in inventory.")

def visualize_inventory(inventory):
    # Create a pandas DataFrame from the inventory dictionary
    df = pd.DataFrame(inventory).T.reset_index()

    # Check if the inventory is empty
    if df.empty:
        print("\nError: Inventory is empty. Add items to visualize.")
        return

    df.columns = ["Item", "Details"]

    print("\nChoose what to visualize:")
    print("1. Quantity")
    print("2. COGS per Unit")
    print("3. Selling Price per Unit")
    print("4. Profit per Unit")

    choice = input("\nEnter your choice (1-4): ")

    # Plot a bar chart based on user's choice
    if choice == "1":
        column_name = "quantity"
        title = "Quantity"
    elif choice == "2":
        column_name = "cogs_per_unit"
        title = "COGS per Unit"
    elif choice == "3":
        column_name = "selling_price_per_unit"
        title = "Selling Price per Unit"
    elif choice == "4":
        column_name = "profit_per_unit"
        title = "Profit per Unit"
    else:
        print("Invalid choice. Displaying Quantity by default.")
        column_name = "quantity"
        title = "Quantity"

    # Plot a bar chart for visualization
    plt.figure(figsize=(12, 6))
    plt.bar(df["Item"], df["Details"].apply(lambda x: x[column_name]), color='blue', label=title)

    plt.xlabel('Item')
    plt.ylabel(title)
    plt.title(f'Inventory Visualization - {title}')
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    print("Welcome to the Professional Inventory Tracker!")

    inventory = {}

    try:
        while True:
            print("\nMenu:")
            print("1. Add Item")
            print("2. Add Quantity")
            print("3. Remove Quantity")
            print("4. Display Summary")
            print("5. Search Item")
            print("6. Visualize Inventory")
            print("7. Exit")

            choice = input("\nEnter your choice (1-7): ")

            if choice == "1":
                num_items = input("Enter the number of items to add: ")
                while not num_items.isdigit():
                    print("\nError: Please enter a valid numeric value for the number of items.")
                    num_items = input("Enter the number of items to add: ")
                add_item(inventory, int(num_items))

            elif choice == "2":
                item_name = input("Enter item name to add quantity: ")
                additional_quantity = input("Enter additional quantity: ")
                while not additional_quantity.isdigit():
                    print("\nError: Please enter a valid numeric value for additional quantity.")
                    additional_quantity = input("Enter additional quantity: ")
                add_quantity(inventory, item_name, int(additional_quantity))

            elif choice == "3":
                item_name = input("Enter item name to remove quantity: ")
                quantity = input("Enter quantity to remove: ")
                while not quantity.isdigit():
                    print("\nError: Please enter a valid numeric value for quantity.")
                    quantity = input("Enter quantity to remove: ")
                remove_quantity(inventory, item_name, int(quantity))

            elif choice == "4":
                display_summary(inventory)

            elif choice == "5":
                search_item(inventory, input("Enter item name to search: "))

            elif choice == "6":
                visualize_inventory(inventory)

            elif choice == "7":
                print("Exiting the program. Thank you!")
                break

            else:
                print("Invalid choice. Please enter a number from 1 to 7.")

    except ValueError as e:
        print(f"Error: {e}. Please enter a valid quantity or price.")

if __name__ == "__main__":
    main()
