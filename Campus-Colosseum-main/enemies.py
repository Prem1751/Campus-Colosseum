import random

import information as p

def stat_eternal(Lv, evo):
    elemental_stats = (
        p.stat_water(Lv, evo),
        p.stat_wood(Lv, evo),
        p.stat_fire(Lv, evo),
    )
    return tuple(sum(values) / len(values) for values in zip(*elemental_stats))

STAT_FUNC = {
    "Water": p.stat_water,
    "Wood": p.stat_wood,
    "Fire": p.stat_fire,
    "Eternal": stat_eternal
}

# ปรับเปลี่ยนค่าพลังได้ที่นี่เพื่อปรับสมดุลของเกมตามความเหมาะสม
STAGE_STATS = {
    1: {"DMG": 15, "DEF": 18, "Speed": 10},
    2: {"DMG": 28, "DEF": 12, "Speed": 15},
    3: {"DMG": 22, "DEF": 25, "Speed": 35},
    4: {"DMG": 35, "DEF": 35, "Speed": 20},
    5: {"DMG": 50, "DEF": 20, "Speed": 25},
    6: {"DMG": 40, "DEF": 30, "Speed": 45},
    7: {"DMG": 65, "DEF": 45, "Speed": 30},
    8: {"DMG": 85, "DEF": 35, "Speed": 40},
    9: {"DMG": 75, "DEF": 50, "Speed": 60},
    10: {"DMG": 120, "DEF": 70, "Speed": 80},
}


def get_speed(unit):
    return float(unit.get("Speed", unit.get("SPE", 0)))

 #  ใครสปีดมากกว่าจะได้โจมตีก่อน แค่ถ้าห่างไม่มากต้องช่วงชิงกันเพื่อแย่งเทิร์นโจมตี
def has_turn_priority(enemy, player):
    enemy_speed = get_speed(enemy)
    player_speed = get_speed(player)
    speed_diff = enemy_speed - player_speed

    if speed_diff <= 0:
        return False

    if speed_diff >= 20:
        return True

    roll = random.random()
    win_chance = 0.5 + (speed_diff / 40)
    return roll < min(win_chance, 0.95)


def stage1():
    monHP = 120
    monLv = 3
    stats = STAGE_STATS[1]
    return make_enemy("Leaf_Sprout", "Wood", monHP, monLv, dmg=stats["DMG"], defense=stats["DEF"], speed=stats["Speed"])


def stage2():
    monHP = 200
    monLv = 7
    stats = STAGE_STATS[2]
    return make_enemy("Flame_Spark", "Fire", monHP, monLv, dmg=stats["DMG"], defense=stats["DEF"], speed=stats["Speed"])


def stage3():
    monHP = 320
    monLv = 12
    stats = STAGE_STATS[3]
    return make_enemy("Aqua_Puff", "Water", monHP, monLv, dmg=stats["DMG"], defense=stats["DEF"], speed=stats["Speed"])


def stage4():
    monHP = 480
    monLv = 17
    stats = STAGE_STATS[4]
    return make_enemy("Branch_Guard", "Wood", monHP, monLv, dmg=stats["DMG"], defense=stats["DEF"], speed=stats["Speed"])


def stage5():
    monHP = 650
    monLv = 22
    stats = STAGE_STATS[5]
    return make_enemy("Blaze_Fang", "Fire", monHP, monLv, dmg=stats["DMG"], defense=stats["DEF"], speed=stats["Speed"])


def stage6():
    monHP = 850
    monLv = 28
    stats = STAGE_STATS[6]
    return make_enemy("Aqua_Fin", "Water", monHP, monLv, dmg=stats["DMG"], defense=stats["DEF"], speed=stats["Speed"])


def stage7():
    monHP = 1100
    monLv = 36
    stats = STAGE_STATS[7]
    return make_enemy("Forest_Titan", "Wood", monHP, monLv, dmg=stats["DMG"], defense=stats["DEF"], speed=stats["Speed"])


def stage8():
    monHP = 1400
    monLv = 42
    stats = STAGE_STATS[8]
    return make_enemy("Solar_Inferno", "Fire", monHP, monLv, dmg=stats["DMG"], defense=stats["DEF"], speed=stats["Speed"])


def stage9():
    monHP = 1800
    monLv = 49
    stats = STAGE_STATS[9]
    return make_enemy("Tidal_Levi", "Water", monHP, monLv, dmg=stats["DMG"], defense=stats["DEF"], speed=stats["Speed"])


def stage10():
    monHP = 2500
    monLv = 60
    stats = STAGE_STATS[10]
    return make_enemy("Leviathano_de_Sperouchi", "Eternal", monHP, monLv, dmg=stats["DMG"], defense=stats["DEF"], speed=stats["Speed"])

# สกิลที่ผู้เล่นจะเผาศัตรู 2 เทิร์น
def FireDOT(enemy):
    print("IT IS YOUR TURN TO BURNING T H E M ! ! !")
    dot_dmg = enemy["HP"] * 5 / 100
    for i in range(2):
        enemy["HP"] = max(0, enemy["HP"] - dot_dmg)
        print("BURN BABY BURN! Enemy HP is now: ", enemy["HP"])
        i += 1

# มอนสเตอร์ลดดาเมจผู้เล่น
def debuff(enemy, player):
    print("IT IS YOUR TURN TO BE DEBUFFED ! ! !")
    debuff_dmg = enemy["HP"] * 5 / 100
    player["DMG"] = max(0, player["DMG"] - debuff_dmg)
    print("DEBUFF APPLIED! Your DMG is now: ", player["DMG"])

# สกิลของลอร์ดออฟอีเทอร์นอล Splashing Light และ Dusky Burst ที่จะทำดาเมจมหาศาลต่อผู้เล่น
def splashinglight_eternal(player):
    print("THE LORD OF ETERNAL IS SPLASHING THE LIGHTS OF ETERNAL ON YOU ! ! !")
    splash_ldmg = player["HP"] * 35 / 100
    player["HP"] -= splash_ldmg
    print("SPLASHING LIGHT APPLIED! Your HP is now: ", player["HP"])

def duskybursted_eternal(player):
    print("YOU HAVE BEEN DUSKY BURSTED BY LORD OF ETERNAL! ! !")
    splash_dmg = player["HP"] * 50 / 100
    player["HP"] -= splash_dmg
    print("DUSKY BURST APPLIED! Your HP is now: ", player["HP"])

def random_skill_turn(element):
    if element == "Eternal":
        return 10
    return random.randint(1, 10)

def use_skill_on_turn(enemy, player, turn):
    if turn != enemy["skill_turn"]:
        return False

    if enemy["element"] == "Eternal":
        random.choice((splashinglight_eternal, duskybursted_eternal))(player)
    else:
        debuff(enemy, player)
    return True

def use_player_skill_on_turn(player_monster, enemy, turn):
    if player_monster["element"] != "Fire":
        return False

    skill_turn = player_monster.setdefault(
        "skill_turn", random_skill_turn(player_monster["element"])
    )
    if turn != skill_turn:
        return False

    FireDOT(enemy)
    return True

def make_enemy(name, element, monHP, Lv, evo=0, dmg=None, defense=None, speed=None):
    if dmg is not None and defense is not None and speed is not None:
        DMG = dmg
        DEF = defense
        Speed = speed
        SPE = speed
    else:
        _, DMG, DEF, SPE = STAT_FUNC[element](Lv, evo)
        Speed = SPE

    return {
        "name": name,
        "element": element,
        "Lv": Lv,
        "HP": monHP,
        "DMG": DMG,
        "DEF": DEF,
        "SPE": SPE,
        "Speed": Speed,
        "skill_turn": random_skill_turn(element),
    }

def tryagain():
    while True:
        choice = input("Do you want to try again? (y/n): ").strip().lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def games():
    stages = [stage1, stage2, stage3, stage4, stage5, stage6, stage7, stage8, stage9, stage10]
    for i, stage_func in enumerate(stages):
        print(f"Stage {i + 1} - {stage_func.__name__}")
        enemy = stage_func()
        print(f"Enemy: {enemy['name']}, Element: {enemy['element']}, HP: {enemy['HP']}, Lv: {enemy['Lv']}")
        while True:
            if enemy['HP'] <= 0 and p.HP > 0:
                print("Monster DIED!")
                lv, total_exp, next_req_exp = p.LVUP(100, 1)
                print(f"Level up! New level: {lv}")
            elif enemy['HP'] > 0 and p.HP <= 0:
                print("Player DIED!")
                if not tryagain():
                    print("The Colosseum wins over the man of campus once again...")
                    return
    else:
        print("Congratulations! You have completed all stages.")
        print()
        print("The Mighty Campus once peaceful and serene once again")
