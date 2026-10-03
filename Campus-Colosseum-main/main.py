import information

print("Welcome to the Campus Colosseum")
print("Let's join the campus to bring the peace back!")
print("--------------------------------------")
print("Choose your own confidant.")
information.show_mon("Water_Starter", 1)
information.show_mon("Wood_Starter", 1)
information.show_mon("Fire_Starter", 1)

choose_mon = True
My_mon = ""
while choose_mon:
    user_input = input("Choose your confidant (1-3): ")
    if user_input == "1":
        print("You choose Water_Starter")
        information.show_mon("Water_Starter", 1)
        choose_mon = False
        My_mon = "water"
    elif user_input == "2":
        print("You choose Wood_Starter")
        information.show_mon("Wood_Starter", 1)
        choose_mon = False
        My_mon = "wood"
    elif user_input == "3":
        print("You choose Fire_Starter")
        information.show_mon("Fire_Starter", 1)
        choose_mon = False
        My_mon = "fire"
    else:
        print("Invalid choice. Please choose a number between 1 and 3.")
