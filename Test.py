"""ไฟล์ทดสอบการต่อสู้แบบข้อความ

แก้ค่าที่ส่วนตั้งค่าด้านล่าง แล้วรันด้วยคำสั่ง: python Test.py
"""

import battle
import enemies
import information
import main as game


# ===== ตั้งค่าการทดสอบตรงนี้ =====
STAGE = 10                 # ด่านที่ต้องการทดสอบ: 1-10
STARTER = "Fire"           # เลือก "Water", "Wood" หรือ "Fire"
LEVEL = 100                # เลเวลผู้เล่น: 1-100


# รายชื่อศัตรูเรียงตามด่าน 1 ถึง 10
STAGES = [
    enemies.stage1,
    enemies.stage2,
    enemies.stage3,
    enemies.stage4,
    enemies.stage5,
    enemies.stage6,
    enemies.stage7,
    enemies.stage8,
    enemies.stage9,
    enemies.stage10,
]

# ข้อมูลตัวละครแต่ละธาตุ: ชื่อในเกมและฟังก์ชันคำนวณค่าสถานะ
STARTERS = {
    "Water": ("Water_Starter", information.stat_water),
    "Wood": ("Wood_Starter", information.stat_wood),
    "Fire": ("Fire_Starter", information.stat_fire),
}


def main():
    # ตรวจสอบค่าหลักที่ตั้งไว้ก่อนเริ่มเกม
    if STAGE < 1 or STAGE > 10:
        raise ValueError("STAGE ต้องอยู่ระหว่าง 1 ถึง 10")
    if STARTER not in STARTERS:
        raise ValueError('STARTER ต้องเป็น "Water", "Wood" หรือ "Fire"')
    if LEVEL < 1 or LEVEL > 100:
        raise ValueError("LEVEL ต้องอยู่ระหว่าง 1 ถึง 100")

    # คำนวณร่างวิวัฒนาการและค่าสถานะเริ่มต้นของผู้เล่น
    pokemon_name, get_stats = STARTERS[STARTER]
    evolution = min(LEVEL // 25, 2)
    hp, dmg, defense, speed = get_stats(LEVEL, evolution)

    # ใส่ค่าสถานะผู้เล่นลงในข้อมูลตัวละคร
    player = {
        "name": pokemon_name,
        "pokemon_key": pokemon_name,
        "display_name": information.mon_dex[pokemon_name][evolution]["name"],
        "element": STARTER,
        "Lv": LEVEL,
        "HP": hp,
        "maxHP": hp,
        "DMG": dmg,
        "DEF": defense,
        "SPE": speed,
        "Speed": speed,
        "evo": evolution,
        "EXP": 0,
        "original_DMG": dmg,
    }

    # สร้างศัตรูของด่านที่เลือก โดยใช้ค่าสถานะดั้งเดิมของเกม
    enemy = STAGES[STAGE - 1]()

    print(f"\n\n{'-' * 12} STAGE {STAGE} {'-' * 12}")

    # เรียกใช้ระบบต่อสู้จริงของเกม
    won = battle.battle(player, enemy)
    if not won:
        print("\n" + "-" * 12 + " YOU LOSE " + "-" * 12)
        print("Test battle ended. No EXP was awarded.")
        return

    print("\n\nCongratulations!")
    print("You cleared all 10 stages!")

    # เมื่อชนะ ให้ EXP และคำนวณเลเวลแบบเดียวกับเกมปกติ
    reward = game.STAGE_EXP[STAGE - 1]
    game.gain_exp(player, reward)
    print(f"\nYou cleared Stage {STAGE}!")
    print(f"EXP gained: {reward}")
    game.show_exp(player, player["EXP"])


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nยกเลิกการทดสอบแล้ว")
