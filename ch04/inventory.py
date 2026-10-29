# inventory.py - menu-driven stock manager
inventory = {
    "pencil": {"qty": 120, "price": 8.50},
    "notebook": {"qty": 15, "price": 45.00},
    "eraser": {"qty": 4, "price": 12.00},
}
LOW_STOCK = 10

def show():
    print(f"\n{'Item':<12}{'Qty':>6}{'Price':>10}{'Value':>12}")
    print("-" * 40)
    total = 0
    for name, item in sorted(inventory.items()):
        value = item["qty"] * item["price"]
        total += value
        flag = "  LOW" if item["qty"] < LOW_STOCK else ""
        print(f"{name:<12}{item['qty']:>6}{item['price']:>10.2f}{value:>12,.2f}{flag}")
    print("-" * 40)
    print(f"{'Total value':<28}{total:>12,.2f}")

while True:
    choice = input("\n[s]how [a]dd [r]emove [u]pdate qty [q]uit: ").lower()
    if choice == "s":
        show()
    elif choice == "a":
        name = input("Item name: ").strip().lower()
        qty = int(input("Quantity: "))
        price = float(input("Price: "))
        inventory[name] = {"qty": qty, "price": price}
    elif choice == "r":
        name = input("Item to remove: ").strip().lower()
        if inventory.pop(name, None) is None:
            print("No such item.")
    elif choice == "u":
        name = input("Item: ").strip().lower()
        if name in inventory:
            inventory[name]["qty"] += int(input("Change (+/-): "))
        else:
            print("No such item.")
    elif choice == "q":
        break
