import information as p

STAT_FUNC = {
    "Water": p.stat_water,
    "Wood": p.stat_wood,
    "Fire": p.stat_fire,
    "Eternal": p.stat_eternal
}

def stage1():
    monHP = 120
    monLv = 3
    return make_enemy("Leaf_Sprout", "Wood", monHP, monLv)

def stage2():
    monHP = 200
    monLv = 7
    return make_enemy("Flame_Spark", "Fire", monHP, monLv)

def stage3():
    monHP = 320
    monLv = 12
    return make_enemy("Aqua_Puff", "Water", monHP, monLv)

def stage4():
    monHP = 480
    monLv = 17
    return make_enemy("Branch_Guard", "Wood", monHP, monLv)

def stage5():
    monHP = 650
    monLv = 22
    return make_enemy("Blaze_Fang", "Fire", monHP, monLv)

def stage6():
    monHP = 850
    monLv = 28
    return make_enemy("Aqua_Fin", "Water", monHP, monLv)

def stage7():
    monHP = 1100
    monLv = 36
    return make_enemy("Forest_Titan", "Wood", monHP, monLv)

def stage8():
    monHP = 1400
    monLv = 42
    return make_enemy("Solar_Inferno", "Fire", monHP, monLv)

def stage9():
    monHP = 1800
    monLv = 49
    return make_enemy("Tidal_Levi", "Water", monHP, monLv)

def stage10():
    monHP = 2500
    monLv = 60
    return make_enemy("Leviathano_de_Sperouchi", "Eternal", monHP, monLv)

def make_enemy(name, element, monHP, Lv, evo=0):
    _, DMG, DEF, SPE = STAT_FUNC[element](Lv, evo)   # ทิ้ง HP จากสูตร ใช้ HP ที่กรอก
    return {
        "name": name,
        "element": element,
        "Lv": Lv,
        "HP": monHP,
        "DMG": DMG,
        "DEF": DEF,
        "SPE": SPE,
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
    