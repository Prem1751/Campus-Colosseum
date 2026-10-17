
import information
import enemies
import battle
import tkinter as tk

def show_art(parent, pokemon):
    art = pokemon.get("art", [])

    label = tk.Label(
        parent,
        text="\n".join(art),
        font=("Courier New", 10),
        justify="left"
    )
    label.pack()
    return label

# =====================================
# เลือกโปเกมอนเริ่มต้น
# =====================================

def choose_pokemon():
    print("Welcome to the Campus Colosseum")
    print("Let's join the campus to bring the peace back!")
    print("--------------------------------------")
    print("Choose your own confidant.")

    information.show_mon("Water_Starter", 1)
    information.show_mon("Wood_Starter", 1)
    information.show_mon("Fire_Starter", 1)

    while True:
        user_input = input("Choose your confidant (1-3): ").strip()

        if user_input == "1":
            name = "Water_Starter"
            element = "Water"
            HP, DMG, DEF, SPE = information.stat_water(1, 0)
            break

        elif user_input == "2":
            name = "Wood_Starter"
            element = "Wood"
            HP, DMG, DEF, SPE = information.stat_wood(1, 0)
            break

        elif user_input == "3":
            name = "Fire_Starter"
            element = "Fire"
            HP, DMG, DEF, SPE = information.stat_fire(1, 0)
            break

        else:
            print("Invalid choice. Please choose 1-3.")

    print(f"\nYou choose {name}")
    information.show_mon(name, 1)

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
        "evo": 0,
        "EXP": 0
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



# =====================================
#       STATS EXP
# =====================================

def get_required_exp(level):
    """Calculate EXP required for the next level."""
    return int(50 * (1.12 ** (level - 1)))

def check_evolution(player):
    old_evo = player.get("evo", 0)
    level = player["Lv"]

    if level >= 50:
        new_evo = 2
    elif level >= 25:
        new_evo = 1
    else:
        new_evo = 0

    if new_evo <= old_evo:
        return

    player["evo"] = new_evo

# แสดงร่างใหม่เมื่อวิวัฒนาการ
    information.show_mon(player["name"], new_evo + 1)

    print(f"\n🎉 {player['name']} evolved!")
    print(f"Evolution: {old_evo} -> {new_evo}")

    stat_functions = {
        "Water": information.stat_water,
        "Wood": information.stat_wood,
        "Fire": information.stat_fire,
    }

    stat_function = stat_functions[player["element"]]
    max_hp, dmg, defense, speed = stat_function(
        player["Lv"], new_evo
    )

    hp_increase = max_hp - player["maxHP"]
    player["maxHP"] = max_hp
    player["HP"] = min(max_hp, player["HP"] + hp_increase)

    player["DMG"] = dmg
    player["DEF"] = defense
    player["SPE"] = speed
    player["Speed"] = speed
    player["original_DMG"] = dmg

    print(f"HP: {player['HP']}/{player['maxHP']}")
    print(f"DMG: {player['DMG']}")
    print(f"DEF: {player['DEF']}")
    print(f"SPE: {player['SPE']}")


def gain_exp(player, reward):
    old_level = player["Lv"]
    current_exp = player.get("EXP", 0) + reward

    new_level, remaining_exp, next_exp = information.LVUP(
        current_exp, old_level
    )

    player["Lv"] = new_level
    player["EXP"] = remaining_exp
    player["next_req_exp"] = next_exp

    # ตรวจ Evolution หลังอัปเดตเลเวล
    check_evolution(player)

    if new_level > old_level:
        print(f"\n🎉 Level Up! Lv.{old_level} -> Lv.{new_level}")
        print(f"HP: {player['HP']}/{player['maxHP']}")
        print(f"DMG: {player['DMG']}")
        print(f"DEF: {player['DEF']}")
        print(f"SPE: {player['SPE']}")

    print(f"ได้รับ EXP {reward}")
    print(
        f"EXP ปัจจุบัน: {player['EXP']}/"
        f"{player['next_req_exp']}"
    )

def show_exp(player, total_exp):
    required_exp = get_required_exp(player["Lv"])
    exp_needed = max(0, required_exp - total_exp)

    print("\n========== EXP STATUS ==========")
    print(f"Level: {player['Lv']}")
    print(f"EXP: {total_exp}/{required_exp}")
    print(f"EXP needed to level up: {exp_needed}")

# =====================================
#       เริ่มเกม
# =====================================
def start():
    player = choose_pokemon()

    stages = [
        enemies.stage1,
        enemies.stage2,
        enemies.stage3,
        enemies.stage4,
        enemies.stage5,
        enemies.stage6,
        enemies.stage7,
        enemies.stage8,
        enemies.stage9,
        enemies.stage10
    ]

    stage_exp = [120, 350, 900, 2200, 5000, 11000, 24000, 50000, 100000, 250000]
    
    total_exp = 0
    current_stage = 0

    while current_stage < len(stages):
        print(f"\n========== STAGE {current_stage + 1} ==========")
        information.show_mon(
    player["name"],
    min(player["evo"] + 1, 3)
)
        enemy = stages[current_stage]()
        result = battle.battle(player, enemy)

        if result:
            # Player wins
            reward = stage_exp[current_stage]
            total_exp += reward
            gain_exp(player, reward)

            print(f"\nYou cleared Stage {current_stage + 1}!")
            print(f"EXP gained: {reward}")

            show_exp(player, player["EXP"])

            current_stage += 1

            # Restore HP before the next stage
            if current_stage < len(stages):
                player["HP"] = player["maxHP"]
                print("\nYour HP has been fully restored!")
                print(f"HP: {player['HP']}/{player['maxHP']}")

        else:
            # Player loses
            print("\n========== YOU LOSE ==========")
            print("1. Give up")
            print("2. Replay previous stage to gain EXP")
            print("3. Retry this stage")

            while True:
                choice = input("Choose (1-3): ").strip()

                if choice == "1":
                    print("\nGame Over!")
                    show_exp(player, total_exp)
                    return

                elif choice == "2":
                    if current_stage == 0:
                        print("There is no previous stage.")
                        print("Please choose option 3 to retry Stage 1.")
                        continue

                    previous_stage = current_stage - 1
                    print(f"\nReplaying Stage {previous_stage + 1}")

                    player["HP"] = player["maxHP"]
                    old_enemy = stages[previous_stage]()
                    grind_result = battle.battle(player, old_enemy)

                    if grind_result:
                        reward = stage_exp[previous_stage]
                        total_exp += reward
                        gain_exp(player, reward)

                        print("\nYou won the previous stage!")
                        print(f"EXP gained: {reward}")
                        show_exp(player, player["EXP"])

                    else:
                        print("\nYou lost the previous stage.")

                    player["HP"] = player["maxHP"]
                    print("HP restored!")
                    # Return to the menu after replaying
                    continue

                elif choice == "3":
                    player["HP"] = player["maxHP"]
                    print("\nRetrying current stage...")
                    break

                else:
                    print("Please choose 1, 2, or 3.")

            # If the player chose to replay the previous stage,
            # keep showing the menu until they choose retry or give up.
            if choice == "2":
                continue

    print("\nCongratulations!")
    print("You cleared all 10 stages!")
    print(f"Final EXP: {total_exp}")
    show_exp(player, total_exp)


if __name__ == "__main__":
    start()
