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


    player = {
        "name": name,
        "element": element,
        "Lv": 1,
        "HP": HP,
        "maxHP": HP,
        "DMG": DMG,
        "DEF": DEF,
        "SPE": SPE,
        "Speed": SPE,
        "evo": 0
    }

    print("\n========== YOUR POKEMON ==========")
    print("Name:", name)
    print("Element:", element)
    print("Level:", player["Lv"])
    print("HP:", HP)
    print("DMG:", DMG)
    print("DEF:", DEF)
    print("Speed:", SPE)

    return player


def main():
    # 1. เลือกโปเกมอน
    player = choose_pokemon()

    # 2. เข้า Stage 1 ทันที
    print("\n========== STAGE 1 ==========")

    enemy = create_stage1()

    # 3. เริ่มต่อสู้
    result = battle.battle(player, enemy)

    if result:
        print("\nYou cleared Stage 1!")
    else:
        print("\nGame Over!")


if __name__ == "__main__":
    main(
