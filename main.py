import information

print("welcome to the campus Campus Colosseum")
print("--------------------------------------")
print("choose your confidant")
information.show_mon("Water_Starter", 1)
information.show_mon("Wood_Starter", 1)
information.show_mon("Fire_Starter", 1)

choose_mon = True
while choose_mon:
    user_input = input("choose your confidant (1-3): ")
    if user_input == "1":
        print("you choose Water_Starter")
        information.show_mon("Water_Starter", 1)
        choose_mon = False
    elif user_input == "2":
        print("you choose Wood_Starter")
        information.show_mon("Wood_Starter", 1)
        choose_mon = False
    elif user_input == "3":
        print("you choose Fire_Starter")
        information.show_mon("Fire_Starter", 1)
        choose_mon = False
    else:
        print("Invalid choice. Please choose a number between 1 and 3.")
