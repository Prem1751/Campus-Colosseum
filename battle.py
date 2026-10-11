import random
import information as p
import enemies as e


# =====================================
# ระบบคำนวณความเสียหาย
# =====================================

def attack(attacker, defender):
    damage = max(1, int(attacker["DMG"] - defender["DEF"]))

    defender["HP"] = max(0, defender["HP"] - damage)

    print(f"\n{attacker['name']} attacks!")
    print(f"Damage: {damage}")
    print(f"{defender['name']} HP: {defender['HP']}")

    return damage


# =====================================
# ระบบเลือกสกิลของผู้เล่น
# =====================================

def player_skill(player, enemy):
    print("\n===== YOUR SKILLS =====")
    print("1. Normal Attack")
    print("2. Skill 1")
    print("3. Skill 2")
    print("4. Skill 3")
    print("5. Skill 4")

    choice = input("Choose your action: ").strip()

    if choice == "1":
        attack(player, enemy)
        return

    if choice not in ("2", "3", "4", "5"):
        print("Invalid choice!")
        return

    skill = int(choice) - 1

    element = player["element"]

    if element == "Water":
        damage = p.water_damage(
            enemy, 0, player["SPE"], skill,
            player["SPE"], enemy["DEF"]
        )

    elif element == "Wood":
        damage = p.wood_damage(
            enemy, 0, player["DEF"], skill,
            player["DMG"], enemy["DEF"]
        )

    elif element == "Fire":
        damage = p.fire_damage(
            enemy, 0, player["DMG"], skill,
            player["DMG"], enemy["DEF"]
        )

    else:
        print("Unknown element!")
        return

    enemy["HP"] = max(0, enemy["HP"] - damage)

    print(f"\n{player['name']} used Skill {skill}!")
    print(f"Damage: {damage}")
    print(f"Enemy HP: {enemy['HP']}")

    # สกิลไฟหมายเลข 1 มีโอกาสทำให้ติดสถานะเผาไหม้
    if element == "Fire" and skill == 1 and enemy["HP"] > 0:
        enemy["burn_turns"] = 2
        print("The enemy is burning!")


# =====================================
# ระบบสถานะผิดปกติ
# =====================================

def apply_status(player, enemy):
    # ความเสียหายจากการเผาไหม้
    if enemy.get("burn_turns", 0) > 0 and enemy["HP"] > 0:
        damage = max(1, int(enemy["HP"] * 0.05))

        enemy["HP"] = max(0, enemy["HP"] - damage)
        enemy["burn_turns"] -= 1

        print(f"Burn damage: {damage}")
        print(f"Enemy HP: {enemy['HP']}")

    # ลด DMG ของผู้เล่นจากดีบัฟ
    if player.get("debuff_turns", 0) > 0:
        player["debuff_turns"] -= 1

        if player["debuff_turns"] == 0:
            player["DMG"] = player["original_DMG"]
            print("Your damage debuff has ended!")


# =====================================
# ระบบ AI บอส
# =====================================

def boss_ai(boss, player):
    boss_hp_ratio = boss["HP"] / boss["maxHP"]
    player_hp_ratio = player["HP"] / player["maxHP"]

    # บอสใกล้แพ้ เข้าสู่โหมดโกรธ
    if boss_hp_ratio <= 0.30:
        if random.random() < 0.70:
            return "special"

    # ผู้เล่นใกล้แพ้ บอสมีโอกาสใช้สกิล
    if player_hp_ratio <= 0.30:
        if random.random() < 0.60:
            return "special"

    # ถ้าผู้เล่นโจมตีแรง บอสอาจใช้ดีบัฟ
    if player["DMG"] >= 40:
        if random.random() < 0.50:
            return "debuff"

    return "attack"


# =====================================
# ระบบการกระทำของบอส
# =====================================

def boss_action(boss, player):
    action = boss_ai(boss, player)

    print(f"\n{boss['name']} is thinking...")

    if action == "attack":
        attack(boss, player)

    elif action == "debuff":
        player["DMG"] = max(1, int(player["DMG"] * 0.75))
        player["debuff_turns"] = 2

        print("BOSS USED DEBUFF!")
        print(f"Your DMG is now {player['DMG']}")

    elif action == "special":
        if boss["element"] == "Eternal":
            skill = random.choice(["light", "burst"])

            if skill == "light":
                damage = int(player["HP"] * 0.35)
                print("LORD OF ETERNAL USED SPLASHING LIGHT!")

            else:
                damage = int(player["HP"] * 0.50)
                print("LORD OF ETERNAL USED DUSKY BURST!")

            player["HP"] = max(0, player["HP"] - damage)

            print(f"Damage: {damage}")
            print(f"Player HP: {player['HP']}")

        else:
            damage = max(1, int(boss["DMG"] * 1.5 - player["DEF"]))

            player["HP"] = max(0, player["HP"] - damage)

            print(f"{boss['name']} used a powerful attack!")
            print(f"Damage: {damage}")
            print(f"Player HP: {player['HP']}")


# =====================================
# ระบบต่อสู้หลัก
# =====================================

def battle(player, enemy):
    player["maxHP"] = player["HP"]
    enemy["maxHP"] = enemy["HP"]

    player["original_DMG"] = player["DMG"]
    player["debuff_turns"] = 0
    enemy["burn_turns"] = 0

    turn = 1

    print("\n================================")
    print("          BATTLE START")
    print("================================")
    print(f"Player: {player['name']}")
    print(f"Enemy: {enemy['name']}")

    while player["HP"] > 0 and enemy["HP"] > 0:
        print(f"\n========== TURN {turn} ==========")
        print(f"Your HP: {player['HP']}/{player['maxHP']}")
        print(f"Enemy HP: {enemy['HP']}/{enemy['maxHP']}")

        # ใช้ Speed ตัดสินว่าใครมีโอกาสเริ่มก่อน
        if e.has_turn_priority(enemy, player):
            print("\nThe boss attacks first!")

            boss_action(enemy, player)

            if player["HP"] > 0:
                player_skill(player, enemy)

        else:
            print("\nYou attack first!")

            player_skill(player, enemy)

            if enemy["HP"] > 0:
                boss_action(enemy, player)

        # ตรวจสอบผลการต่อสู้
        if enemy["HP"] <= 0:
            print("\nYOU WIN!")
            return True

        if player["HP"] <= 0:
            print("\nYOU LOSE!")
            return False

        apply_status(player, enemy)

        if enemy["HP"] <= 0:
            print("\nYOU WIN!")
            return True

        if player["HP"] <= 0:
            print("\nYOU LOSE!")
            return False

        turn += 1

    return player["HP"] > 0
