import random

def get_type_multiplier(attacker_element, defender_element):
    strong_against = {
        "Water": "Fire",
        "Fire": "Wood",
        "Wood": "Water",
    }

    weak_against = {
        "Water": "Wood",
        "Wood": "Fire",
        "Fire": "Water",
    }

    if defender_element == "Eternal":
        return 0.7

    if strong_against.get(attacker_element) == defender_element:
        return 1.5

    if weak_against.get(attacker_element) == defender_element:
        return 0.7

    return 1.0

# ระบบเก็บข้อมูลโปเกมอน 3 ธาตุ (แต่ละธาตุมี 3 ร่าง)
mon_dex = {
    "Water_Starter": [
        {
            "stage": 1,
            "name": "Aqua_Puff (ร่าง 1)",
            "art": [
                "  /\\_/\\  ",
                " ( o.o ) ",
                "  > ^ <  ",
                " (~~W~~) "   # W แทนธาตุน้ำ
            ]
        },
        {
            "stage": 2,
            "name": "Aqua_Fin (ร่าง 2)",
            "art": [
                "   /\\_/\\   ",
                "  ( o.O )  ",
                "  /| V |\\  ",
                " (~~~~W~~~~)"
            ]
        },
        {
            "stage": 3,
            "name": "Tidal_Levi (ร่าง 3 - Final)",
            "art": [
                "    /\\___/\\    ",
                "   (  >w<  )   ",
                "  //|| V ||\\\\  ",
                " ((~~~~~~~~~)) "
            ]
        }
    ],
    "Wood_Starter": [
        {
            "stage": 1,
            "name": "Leaf_Sprout (ร่าง 1)",
            "art": [
                "    _v_    ",
                "  ( ^.^ ) ",
                "  /  #  \\  ",
                " (___M___)"   # M แทนธาตุไม้
            ]
        },
        {
            "stage": 2,
            "name": "Branch_Guard (ร่าง 2)",
            "art": [
                "    _//\\\\_    ",
                "   (  -.-  )   ",
                "  //| M |\\  ",
                " (((___M___)))"
            ]
        },
        {
            "stage": 3,
            "name": "Forest_Titan (ร่าง 3 - Final)",
            "art": [
                "   /\\_||_/\\   ",
                "  (  @.@  )  ",
                " //|| M ||\\\\ ",
                "((((___M___))))"
            ]
        }
    ],
    "Fire_Starter": [
        {
            "stage": 1,
            "name": "Flame_Spark (ร่าง 1)",
            "art": [
                "   (v_v)   ",
                "  ( *.* )  ",
                "  /  *  \\  ",
                " (___F___)"   # F แทนธาตุไฟ
            ]
        },
        {
            "stage": 2,
            "name": "Blaze_Fang (ร่าง 2)",
            "art": [
                "   /\\*_/\\*   ",
                "  (  +_+  )  ",
                "  /| F |\\  ",
                " (~~~~F~~~~)"
            ]
        },
        {
            "stage": 3,
            "name": "Solar_Inferno (ร่าง 3 - Final)",
            "art": [
                "   /\\*v*/\\   ",
                "  (  >|<  )  ",
                " //|| F ||\\\\ ",
                "((((~~~F~~~))))"
            ]
        }
    ],
    "boss_dex": {
        "Leviathano_de_Sperouchi": {
            "name": "Leviathano de Sperouchi (BOSS)",
            "element": "Water",
            "art": [
                r"             /\   /\  /\   /\             ",
            r"         _.-~~~~~~~~~~~~~~~~~~-._         ",
            r"     .-~~                        ~~-.     ",
            r"   /     \__(O)            (O)__/     \   ",
            r"  |                 ||                 |  ",
            r"  \  VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV  /  ",
            r"   \    /\/\/\/\/\/\  /\/\/\/\/\/\    /   ",
            r"    \________________________________/    ",
            r"      `-._   ||||||||||||||||   _.-'      ",
            r"~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-",
            r" -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~ ",
        ]
    }
}
}


def show_mon(element_key, stage_num):
    mon = mon_dex[element_key][stage_num - 1]
    print(f"=== {mon['name']} ===")
    for line in mon['art']:
        print(line)
    print("-" * 20)


def LVUP(EXP, LV):
    EXP = max(0, int(EXP))
    LV = max(1, int(LV))

    while LV < 100:
        req_exp = int(50 * (1.12 ** (LV - 1)))

        if EXP < req_exp:
            break

        EXP -= req_exp
        LV += 1

    next_req_exp = (
        int(50 * (1.12 ** (LV - 1)))
        if LV < 100 else 0
    )

    return LV, EXP, next_req_exp


def stat_water(Lv, evo) :
    HP = 45 + (4 * (Lv - 1)) + (evo * 5)
    DMG = 10 + (2 * (Lv - 1)) + (evo * 2)
    DEF = 12 + (1.5 * (Lv - 1)) + (evo * 3)
    SPE = 18 + (2 * (Lv - 1)) + (evo * 4)

    return HP, DMG, DEF, SPE

def stat_wood(Lv, evo) :
    HP = 55 + (6 * (Lv - 1)) + (evo * 6)
    DMG = 10 + (1 * (Lv - 1)) + (evo * 2)
    DEF = 18 + (3 * (Lv - 1)) + (evo * 4)
    SPE = 10 + (1 * (Lv - 1)) + (evo * 3)

    return HP, DMG, DEF, SPE

def stat_fire(Lv, evo) :  
    HP = 42 + (3 * (Lv - 1)) + (evo * 4)
    DMG = 18 + (3 * (Lv - 1)) + (evo * 3)
    DEF = 10 + (1 * (Lv - 1)) + (evo * 2)
    SPE = 12 + (3 * (Lv - 1)) + (evo * 5)

    return HP, DMG, DEF, SPE

# ฟังก์ชันคำนวณดาเมทจากสกิลน้ำ
def water_damage(target, base_power, SPE, skill, attacker_stat_value, target_def):
    special = 0

    if skill == 1:
        base_power = 25
    elif skill == 2:
        base_power = 10
    elif skill == 3:
        base_power = 70
    elif skill == 4:
        base_power = 110
        special = SPE * 0.5
    else:
        raise ValueError("Invalid skill number. Must be between 1 and 4.")

    # คำนวณดาเมจพื้นฐาน
    raw_damage = base_power + (attacker_stat_value * 0.8) + special

    # ลดดาเมจตามเกราะของเป้าหมาย
    def_multiplier = 100 / (100 + max(0, target_def))
    mitigated_damage = raw_damage * def_multiplier

    # คำนวณความได้เปรียบเสียเปรียบของธาตุน้ำ
    target_element = target.get("element", "")
    element_multiplier = get_type_multiplier("Water", target_element)

    # สุ่มความแรง 85%-115%
    rng = random.uniform(0.85, 1.15)

    final_damage = mitigated_damage * element_multiplier * rng

    return max(1, int(final_damage))

# ฟังก์ชันคำนวณดาเมทจากสกิลไม้
def wood_damage(target, base_power, DEF, skill, attacker_stat_value, target_def):
    special = 0

    if skill == 1:
        base_power = 20
    elif skill == 2:
        base_power = 7
    elif skill == 3:
        base_power = 70
    elif skill == 4:
        base_power = 110
        special = DEF * 0.5
    else:
        raise ValueError("Invalid skill number. Must be between 1 and 4.")

    # คำนวณดาเมจพื้นฐาน
    raw_damage = base_power + (attacker_stat_value * 0.8) + special

    # ลดดาเมจตามเกราะเป้าหมาย
    def_multiplier = 100 / (100 + max(0, target_def))
    mitigated_damage = raw_damage * def_multiplier

    # ใช้ตัวคูณธาตุ Wood
    target_element = target.get("element", "")
    element_multiplier = get_type_multiplier("Wood", target_element)

    # สุ่มความแรง 85%-115%
    rng = random.uniform(0.85, 1.15)

    final_damage = mitigated_damage * element_multiplier * rng

    return max(1, int(final_damage))

# ฟังก์ชันคำนวณดาเมทจากสกิลไฟ
def fire_damage(target, base_power, DMG, skill, attacker_stat_value, target_def):
    special = 0

    if skill == 1:
        base_power = 30
    elif skill == 2:
        base_power = 10
    elif skill == 3:
        base_power = 70
    elif skill == 4:
        base_power = 120
        special = DMG * 0.5
    else:
        raise ValueError("Invalid skill number. Must be between 1 and 4.")

    # คำนวณดาเมจพื้นฐาน
    raw_damage = base_power + (attacker_stat_value * 0.8) + special

    # ลดดาเมจตามเกราะเป้าหมาย
    def_multiplier = 100 / (100 + max(0, target_def))
    mitigated_damage = raw_damage * def_multiplier

    # ใช้ตัวคูณธาตุ Fire
    target_element = target.get("element", "")
    element_multiplier = get_type_multiplier("Fire", target_element)

    # สุ่มความแรง 85%-115%
    rng = random.uniform(0.85, 1.15)

    final_damage = mitigated_damage * element_multiplier * rng

    return max(1, int(final_damage))
