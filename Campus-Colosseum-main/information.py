import random

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
    Req_EXP = (50 * (1.12 ** (LV - 1))) // 1
    Total_EXP = 0
    while LV < 100:
        if EXP >= Req_EXP:
            EXP -= Req_EXP
            LV += 1
        else:
            break

    next_req_exp = int(50 * (1.12 ** (LV - 1))) if LV < 100 else 0
    return LV, Total_EXP, next_req_exp



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

def water_damage(target, base_power, SPE, skill, attacker_stat_value, target_def):
    """
    target: ข้อมูลฝั่งเป้าหมาย (เช่น ธาตุ, เกราะ)
    base_power: ความแรงพื้นฐานของสกิลนั้น ๆ
    attacker_stat_value: ค่าสแตดที่ใช้โจมตี (เช่น DMG สำหรับสายไฟ, Speed สำหรับสายน้ำ)
    target_def: ค่าเกราะ (DEF) ของเป้าหมาย
    """
    special = 0
    if skill == 1:
        base_power = 20  # ความแรงพื้นฐานของสกิลน้ำ 1
        effectiveness = "none"
    elif skill == 2:
        base_power = 10  # ความแรงพื้นฐานของสกิลน้ำ 2
        effectiveness = "-My_SPE"
    elif skill == 3:
        base_power = 70  # ความแรงพื้นฐานของสกิลน้ำ 3
        effectiveness = "none"
    elif skill == 4:
        base_power = 110  # ความแรงพื้นฐานของสกิลน้ำ 4
        effectiveness = "none"
        special = SPE * 0.5  # เพิ่มความแรงสกิลตาม Speed ของผู้โจมตี
    else:
        raise ValueError("Invalid skill number. Must be between 1 and 4.")
    
    # 1. คำนวณดาเมทตั้งต้นจากสแตดผู้โจมตี + ความแรงสกิล
    raw_damage = base_power + (attacker_stat_value * 0.8) + special
    
    # 2. หักลบด้วยเกราะ (DEF) ของเป้าหมาย โดยใช้สูตรสัดส่วน (Percentage Reduction)
    # เกราะยิ่งเยอะ ดาเมทยิ่งลดลงเป็นเปอร์เซ็นต์ (ป้องกันดาเมทติดลบ หรือตีไม่เข้าเลย)
    def_multiplier = 100 / (100 + target_def)
    mitigated_damage = raw_damage * def_multiplier
    
    tgt_elem = target.get('element')
    
    if (tgt_elem == 'Fire'):
        element_multiplier = 1.5  # ได้เปรียบธาตุ (แรงขึ้น 50%)
    elif (tgt_elem == 'Wood'):
        element_multiplier = 0.7  # เสียเปรียบธาตุ (เบาลง แต่ยังตีเข้า)
    else:
        element_multiplier = 1.0 # ธาตุเดียวกัน หรือไม่มีความได้เปรียบ/เสียเปรียบ

    # 4. ตัวแปรสุ่มความแกว่ง (RNG Variation 85% - 115%) เพื่อความสมจริงแบบโปเกมอน
    rng = random.uniform(0.85, 1.15)
    
    # 5. คำนวณดาเมทสุทธิ
    final_damage = mitigated_damage * element_multiplier * rng
    
    # กำหนดให้ดาเมทต่ำสุดคือ 1 เสมอ
    return max(1, int(final_damage))

