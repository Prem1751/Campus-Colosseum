import random
import time
from unittest import result
import information as p
import enemies as e

# รายละเอียดสกิลตามธาตุ
skill_info = {
    "Water": [
        ("Normal Attack","โจมตีด้วยการพุ่งชน"),
        ("Water Pulse", "โจมตีด้วยพลังน้ำ"),
        ("Aqua Shield", "โจมตีด้วยพลังน้ำ"),
        ("Tidal Wave", "คลื่นน้ำโจมตีรุนแรง"),
        ("Aqua Burst", "โจมตีรุนแรงและทำให้บอสติด Stun")
    ],
    "Wood": [
        ("Normal Attack", "โจมตีด้วยการกระทืบ"),
        ("Leaf Strike", "โจมตีด้วยพลังพืช"),
        ("Vine Whip", "โจมตีด้วยเถาวัลย์"),
        ("Forest Force", "โจมตีด้วยพลังป่า"),
        ("Nature Break", "โจมตีรุนแรงโดยใช้พลังป้องกัน")
    ],
    "Fire": [
        ("Normal Attack", "โจมตีด้วยการข่วน"),
        ("Flame Shot", "โจมตีด้วยไฟ"),
        ("Burning Flame", "โจมตีและทำให้ศัตรูติด Burn"),
        ("Inferno", "โจมตีด้วยไฟรุนแรง"),
        ("Blazing Burst", "โจมตีด้วยไฟมหาศาล")
    ]
}

# =====================================
# ระบบแพ้ทาง - ชนะทางของธาตุ
# =====================================
def get_type_effectiveness(attacker_element, defender_element):
    multiplier = p.get_type_multiplier(
        attacker_element,
        defender_element
    )

    if multiplier > 1.0:
        return multiplier, "Strong"
    elif multiplier < 1.0:
        return multiplier, "Weak"

    return 1.0, "Base"

# =====================================
# ระบบคำนวณความเสียหาย
# =====================================

def attack(attacker, defender):
    print(f"\n⚔️ {attacker['name']} โจมตี {defender['name']}!")

    # โจมตีพลาด 10%
    if random.random() < 0.10:
        print("💨 ผลการโจมตี: MISS!")
        print("💬 การโจมตีไม่โดนเป้าหมาย")
        print(f"❤️ HP ของ {defender['name']}: "
              f"{defender['HP']}/{defender.get('maxHP', defender['HP'])}")
        return 0

    # คำนวณดาเมจพื้นฐานตามสูตรเดิม
    base_damage = max(
        1,
        int(attacker["DMG"] - defender["DEF"])
    )

    # ตรวจสอบความได้เปรียบของธาตุ
    multiplier, result = get_type_effectiveness(
        attacker["element"],
        defender["element"]
    )

    damage = max(1, int(base_damage * multiplier))

    # ลด HP เป้าหมาย
    old_hp = defender["HP"]
    defender["HP"] = max(0, defender["HP"] - damage)
    actual_damage = old_hp - defender["HP"]

    # แสดงผลแบบอ่านง่าย
    print("🎯 ผลการโจมตี: โจมตีสำเร็จ!")

    if result == "Strong":
        print("🔥 ได้เปรียบทางธาตุ! (Super Effective)")
    elif result == "Weak":
        print("🛡️ เสียเปรียบทางธาตุ (Not Very Effective)")
    else:
        print("⚡ การโจมตีปกติ")

    print(f"💥 สร้างความเสียหาย: {actual_damage} หน่วย")
    print(f"❤️ HP ของ {defender['name']}: "
          f"{defender['HP']}/{defender.get('maxHP', defender['HP'])}")

    if defender["HP"] <= 0:
        print(f"💫 {defender['name']} หมดสภาพการต่อสู้!")

    return actual_damage

# =====================================
# ระบบเลือกสกิลของผู้เล่น
# =====================================

def choose_player_action(player):
    while True:
        print("-----------------------------")
        print("1", skill_info[player["element"]][0][0], "-", skill_info[player["element"]][0][1])
        print("2", skill_info[player["element"]][1][0], "-", skill_info[player["element"]][1][1])
        print("3", skill_info[player["element"]][2][0], "-", skill_info[player["element"]][2][1])
        print("4", skill_info[player["element"]][3][0], "-", skill_info[player["element"]][3][1])
        print("5", skill_info[player["element"]][4][0], "-", skill_info[player["element"]][4][1],f"([until turn {until_turn}/4])")
        choice = input("เลือกคำสั่ง (1-5): ").strip()

        if choice in ("1", "2", "3", "4"):
            return choice
        elif choice == "5":
            if until_turn < 4:
                print("===================================")
                print(f"⚠️ คุณยังไม่สามารถใช้สกิล {skill_info[player['element']][4][0]} ได้! (ต้องรอจนถึงเทิร์นที่ 4)")
                continue

        print("⚠️ คำสั่งไม่ถูกต้อง กรุณาเลือก 1-5")
        print("💚 คุณยังไม่เสียเทิร์น!")

def player_skill(player, enemy, choice=None):
    
    element = player["element"]

    if choice is None:
        choice = choose_player_action(player)
    
    # โจมตีปกติ
    if choice == "1":
        attack(player, enemy)
        return

    skill = int(choice) - 1
    skill_name, description = skill_info[element][skill]

    print(f"\n✨ {player['name']} ใช้ {skill_name}!")
    print(f"📖 {description}")

    
    # สกิลมีโอกาสพลาด 5%
    if random.random() < 0.05:
        print("\n💨 ผลการใช้สกิล: MISS!")
        print(f"❌ {skill_name} พลาดเป้าหมาย!")
        print("💬 ศัตรูไม่ได้รับความเสียหาย")
        print(
            f"❤️ HP ของ {enemy['name']}: "
            f"{enemy['HP']}/{enemy.get('maxHP', enemy['HP'])}"
        )
        return

    # คำนวณดาเมจด้วยสูตรเดิม
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
        print("⚠️ ไม่รู้จักธาตุของผู้เล่น!")
        return

    old_hp = enemy["HP"]
    enemy["HP"] = max(0, enemy["HP"] - damage)
    actual_damage = old_hp - enemy["HP"]

    print("\n🎯 ผลการโจมตี: สำเร็จ!")

    # แสดงผลความได้เปรียบทางธาตุ
    multiplier, result = get_type_effectiveness(
        player["element"],
        enemy["element"]
    )

    if result == "Strong":
        print("🔥 ได้เปรียบทางธาตุ! (Super Effective)")
    elif result == "Weak":
        print("🛡️ เสียเปรียบทางธาตุ (Not Very Effective)")
    else:
        print("⚡ การโจมตีปกติ")

    print(f"💥 สร้างความเสียหาย: {actual_damage} หน่วย")
    print(
        f"❤️ HP ของ {enemy['name']}: "
        f"{enemy['HP']}/{enemy.get('maxHP', enemy['HP'])}"
    )
    
    # Fire Skill 2: Burn
    if element == "Fire" and skill == 2 and enemy["HP"] > 0:
        enemy["burn_turns"] = 2
        print("🔥 ศัตรูติดสถานะ Burn!")

    # Water Skill 4: Stun
    if element == "Water" and skill == 4 and enemy["HP"] > 0:
        enemy["stun_turns"] = 1
        print("💧 ศัตรูติดสถานะ Stun!")

    if enemy["HP"] <= 0:
        print(f"💫 {enemy['name']} หมดสภาพการต่อสู้!")

# =====================================
# ระบบสถานะผิดปกติ
# =====================================

def apply_status(player, enemy):

    # ความเสียหายจาก Burn
    if enemy.get("burn_turns", 0) > 0 and enemy["HP"] > 0:
        damage = max(1, int(enemy["HP"] * 0.05))
        enemy["HP"] = max(0, enemy["HP"] - damage)
        enemy["burn_turns"] -= 1

        print("\n🔥 สถานะ Burn ทำงาน!")
        print(f"💥 ศัตรูได้รับความเสียหาย {damage} หน่วย")
        print(
            f"❤️ HP ของ {enemy['name']}: "
            f"{enemy['HP']}/{enemy.get('maxHP', enemy['HP'])}"
        )

        if enemy["burn_turns"] == 0:
            print("🔥 สถานะ Burn สิ้นสุดแล้ว")

    # ลด DMG ของผู้เล่นจาก Debuff
    if player.get("debuff_turns", 0) > 0:
        player["debuff_turns"] -= 1

        print("\n🛡️ ผลของ Debuff ยังคงทำงาน")
        print(f"⚔️ DMG ปัจจุบัน: {player['DMG']}")

        if player["debuff_turns"] == 0:
            player["DMG"] = player["original_DMG"]
            print("✨ Debuff สิ้นสุดแล้ว!")
            print(f"⚔️ DMG กลับเป็น {player['DMG']}")


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
    if boss.get("stun_turns", 0) > 0:
        boss["stun_turns"] -= 1
        print(f"{boss['name']} is stunned and cannot act!")
        return
    
 # บอสมีโอกาสโจมตีพลาด 10%
    if random.random() < 0.10:
        print(f"\n💨 {boss['name']} missed the attack!")
        print("❌ BOSS MISS! บอสโจมตีพลาด!")
        return
    
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
    player.setdefault("maxHP", player["HP"])
    enemy["maxHP"] = enemy["HP"]

    player["original_DMG"] = player["DMG"]
    player["debuff_turns"] = 0
    enemy["burn_turns"] = 0
    enemy["stun_turns"] = 0

    turn = 1
    global until_turn
    until_turn = 1

    print("\n" + "-" * 36)
    print("             BATTLE START")
    print("-" * 36)
    print(f"Player: {player['name']}")
    print(f"Enemy: {enemy['name']}")
    time.sleep(1)

    while player["HP"] > 0 and enemy["HP"] > 0:
        print(f"\n\n{'-' * 12} TURN {turn} {'-' * 12}")
        print(f"Your HP: {player['HP']}/{player['maxHP']}")
        print(f"Enemy HP: {enemy['HP']}/{enemy['maxHP']}")
        time.sleep(1)

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
        time.sleep(0.5)

        # ตรวจสอบผลการต่อสู้
        if enemy["HP"] <= 0:
            print("\nYOU WIN!")
            return True

        if player["HP"] <= 0:
            print("\nYOU LOSE!")
            return False

        # ใช้สถานะผิดปกติหลังจบการกระทำของทั้งสองฝ่าย
        apply_status(player, enemy)

        if enemy["HP"] <= 0:
            print("\nThe enemy fainted from a status effect!")
            print("\nYOU WIN!")
            return True

        if player["HP"] <= 0:
            print("\nYOU LOSE!")
            return False
        time.sleep(0.5)
        turn += 1
        until_turn += 1

    return player["HP"] > 0
