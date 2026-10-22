
import time
import information
import enemies
import battle


STAGE_EXP = [120, 350, 900, 2200, 5000, 11000, 24000, 50000, 100000, 250000]


# =====================================
# เลือกโปเกมอนเริ่มต้น
# =====================================

def choose_pokemon():
    print("Welcome to the Campus Colosseum")
    print("Let's join the campus to bring the peace back!")
    print("-" * 38)
    print("Choose your own confidant.")
    time.sleep(1)

    information.show_mon("Water_Starter", 1)
    information.show_mon("Wood_Starter", 1)
    information.show_mon("Fire_Starter", 1)

    while True:
        try:
            user_input = input("Choose your confidant (1-3): ").strip()
        except EOFError:
            # ยุติการเลือกโปเกมอนเมื่ออินพุตถูกปิด
            print("\nปิดอินพุตแล้ว ยกเลิกเกม")
            return None

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
    time.sleep(0.5)

    player = {
    "name": name,
    "pokemon_key": name,
    "display_name": information.mon_dex[name][0]["name"],
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

    print("\n" + "-" * 12 + " YOUR POKEMON " + "-" * 12)
    print("Name:", name)
    print("Element:", element)
    print("Level:", player["Lv"])
    print("HP:", HP)
    print("DMG:", DMG)
    print("DEF:", DEF)
    print("Speed:", SPE)
    time.sleep(0.5)

    return player



# =====================================
#       ค่าสถานะและ EXP
# =====================================

def get_required_exp(level):
    """คำนวณ EXP ที่ต้องใช้เพื่อเลื่อนเลเวลถัดไป"""
    return int(50 * (1.12 ** (level - 1)))

def chechk_evolution(player):
    """
    วิวัฒนาการ:
    เลเวล 25 -> วิวัฒนาการขั้นที่ 1
    เลเวล 50 -> วิวัฒนาการขั้นที่ 2
    """

    old_evo = player["evo"]

    if player["Lv"] >= 50:
        target_evo = 2
    elif player["Lv"] >= 25:
        target_evo = 1
    else:
        return

    if target_evo <= old_evo:
        return

    stat_functions = {
        "Water": information.stat_water,
        "Wood": information.stat_wood,
        "Fire": information.stat_fire,
    }

    stat_function = stat_functions[player["element"]]

    # ฟังก์ชัน stat คืนค่า 4 ค่า
    hp, dmg, defense, speed = stat_function(
        player["Lv"], target_evo
    )

    old_max_hp = player["maxHP"]
    old_hp = player["HP"]

    player["evo"] = target_evo
    player["maxHP"] = hp
    player["DMG"] = dmg
    player["DEF"] = defense
    player["SPE"] = speed
    player["Speed"] = speed
    player["original_DMG"] = dmg

    hp_increase = hp - old_max_hp
    player["HP"] = min(hp, max(0, old_hp + hp_increase))

    pokemon_data = information.mon_dex[player["pokemon_key"]][target_evo]
    player["display_name"] = pokemon_data["name"]

    print("\n" + "=" * 40)
    print("✨ Pokémon ของคุณวิวัฒนาการแล้ว! ✨")
    print(f"ชื่อร่างใหม่: {pokemon_data['name']}")
    print(f"Level: {player['Lv']}")
    print(f"HP: {player['HP']}/{player['maxHP']}")
    print(f"DMG: {player['DMG']}")
    print(f"DEF: {player['DEF']}")
    print(f"SPE: {player['SPE']}")
    print("=" * 40)

    information.show_mon(
        player["pokemon_key"],
        target_evo + 1
    )
# เพิ่ม HP ตามส่วน max_HP
    hp_increase = hp - old_max_hp
    player["HP"] = min(hp, max(0, old_hp + hp_increase))

# อัปเดตชื่อหลังวิวัฒนาการ
    pokemon_data = information.mon_dex[player["pokemon_key"]][target_evo]
    player["display_name"] = pokemon_data["name"]

    print("\n" + "=" * 40)
    print("✨ Pokémon ของคุณวิวัฒนาการแล้ว! ✨")
    print(f"{pokemon_data['name']}")
    print(f"LV: {player['Lv']}")
    print(f"HP: {player['HP']}/{player['maxHP']}")
    print(f"ATK: {player['DMG']}")
    print(f"DEF: {player['DEF']}")
    print("=" * 40)

    information.show_mon(player["pokemon_key"], target_evo + 1)

def gain_exp(player, reward):
    old_level = player["Lv"]
    current_exp = player.get("EXP", 0) + reward

    new_level, remaining_exp, next_exp = information.LVUP(
        current_exp, old_level
    )

    player["Lv"] = new_level
    player["EXP"] = remaining_exp
    player["next_req_exp"] = next_exp

    if new_level > old_level:
        stat_functions = {
            "Water": information.stat_water,
            "Wood": information.stat_wood,
            "Fire": information.stat_fire,
        }

        stat_function = stat_functions[player["element"]]

        max_hp, dmg, defense, speed = stat_function(
            new_level, player["evo"]
        )

        hp_increase = max_hp - player["maxHP"]
        player["maxHP"] = max_hp
        player["HP"] = min(
            max_hp,
            max(0, player["HP"] + hp_increase)
        )

        player["DMG"] = dmg
        player["DEF"] = defense
        player["SPE"] = speed
        player["Speed"] = speed
        player["original_DMG"] = dmg

        # ตรวจสอบวิวัฒนาการหลังเลเวลอัป
        chechk_evolution(player)

        print(f"\n🎉 Level Up! Lv.{old_level} -> Lv.{new_level}")
        print(f"HP: {player['HP']}/{player['maxHP']}")
        print(f"DMG: {player['DMG']}")
        print(f"DEF: {player['DEF']}")
        print(f"SPE: {player['SPE']}")
        time.sleep(0.5)

        print(f"\nได้รับ EXP {reward}")
        print(f"EXP คงเหลือ: {player['EXP']}/{player['next_req_exp']}")

    # เพิ่ม HP ตามจำนวน HP สูงสุดที่เพิ่มขึ้น
        hp_increase = max_hp - player["maxHP"]
        player["maxHP"] = max_hp
        player["HP"] = min(max_hp, player["HP"] + hp_increase)

        player["DMG"] = dmg
        player["DEF"] = defense
        player["SPE"] = speed
        player["Speed"] = speed
        player["original_DMG"] = dmg

        chechk_evolution(player)
        
        print(f"\n\n🎉 Level Up! Lv.{old_level} -> Lv.{new_level}")
        print(f"HP: {player['HP']}/{player['maxHP']}")
        print(f"DMG: {player['DMG']}")
        print(f"DEF: {player['DEF']}")
        print(f"SPE: {player['SPE']}")
        time.sleep(0.5)

    print(f"ได้รับ EXP {reward}")
    print(
        f"EXP ปัจจุบัน: {player['EXP']}/"
        f"{player['next_req_exp']}"
    )


def show_exp(player, total_exp):
    required_exp = get_required_exp(player["Lv"])
    exp_needed = max(0, required_exp - total_exp)

    print("\n" + "-" * 12 + " EXP STATUS " + "-" * 12)
    print(f"Level: {player['Lv']}")
    print(f"EXP: {total_exp}/{required_exp}")
    print(f"EXP needed to level up: {exp_needed}")
    time.sleep(0.5)

# =====================================
#       เริ่มเกม
# =====================================
def start():
    player = choose_pokemon()
    if player is None:
        return

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

    total_exp = 0
    current_stage = 0

    while current_stage < len(stages):
        print(f"\n\n{'-' * 12} STAGE {current_stage + 1} {'-' * 12}")
        time.sleep(0.5)

        enemy = stages[current_stage]()
        result = battle.battle(player, enemy)

        if result:
            # ผู้เล่นชนะ
            reward = STAGE_EXP[current_stage]
            total_exp += reward
            gain_exp(player, reward)

            print(f"\nYou cleared Stage {current_stage + 1}!")
            print(f"EXP gained: {reward}")
            time.sleep(0.5)

            show_exp(player, player["EXP"])

            current_stage += 1

            # ฟื้นฟู HP ก่อนเริ่มด่านถัดไป
            if current_stage < len(stages):
                player["HP"] = player["maxHP"]
                print("\nYour HP has been fully restored!")
                print(f"HP: {player['HP']}/{player['maxHP']}")
                time.sleep(0.5)

        else:
            # ผู้เล่นแพ้
            print("\n" + "-" * 12 + " YOU LOSE " + "-" * 12)
            print("1. Give up")
            print("2. Replay previous stage to gain EXP")
            print("3. Retry this stage")
            time.sleep(0.5)

            while True:
                try:
                    choice = input("Choose (1-3): ").strip()
                except EOFError:
                    # ออกจากเมนูเมื่ออินพุตถูกปิด
                    print("\nปิดอินพุตแล้ว ยกเลิกเกม")
                    return

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
                    time.sleep(0.5)

                    player["HP"] = player["maxHP"]
                    old_enemy = stages[previous_stage]()
                    grind_result = battle.battle(player, old_enemy)

                    if grind_result:
                        reward = STAGE_EXP[previous_stage]
                        total_exp += reward
                        gain_exp(player, reward)

                        print("\nYou won the previous stage!")
                        print(f"EXP gained: {reward}")
                        time.sleep(0.5)
                        show_exp(player, player["EXP"])

                    else:
                        print("\nYou lost the previous stage.")

                    player["HP"] = player["maxHP"]
                    print("HP restored!")
                    # กลับไปแสดงเมนูหลังเล่นด่านก่อนหน้าซ้ำ
                    continue

                elif choice == "3":
                    player["HP"] = player["maxHP"]
                    print("\nRetrying current stage...")
                    time.sleep(0.5)
                    break

                else:
                    print("Please choose 1, 2, or 3.")

            # หากผู้เล่นเลือกเล่นด่านก่อนหน้าซ้ำ ให้แสดงเมนูต่อไป
            # จนกว่าจะเลือกลองด่านนี้อีกครั้งหรือยอมแพ้
            if choice == "2":
                continue

    print("\n\nCongratulations!")
    print("You cleared all 10 stages!")
    print(f"Final EXP: {total_exp}")
    show_exp(player, total_exp)


if __name__ == "__main__":
    try:
        start()
    except (KeyboardInterrupt, EOFError):
        # ออกจากเกมอย่างสุภาพเมื่อผู้เล่นกด Ctrl+C หรือปิดอินพุต
        print("\nยกเลิกเกมแล้ว")
