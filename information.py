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
    ]
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
