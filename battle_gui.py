import tkinter as tk
from tkinter import ttk
import information
import battle
import enemies
import io
from contextlib import redirect_stdout

BG = "#080808"
BLUE_CARD = "#e5f3ff"
PINK_CARD = "#fde9e7"
BLUE = "#2479c8"
GREEN = "#21865e"


class PokemonGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Campus Colosseum")
        self.root.geometry("900x760")
        self.root.minsize(780, 700)
        self.root.configure(bg=BG)
        self.show_starter_screen()

    def show_starter_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="CAMPUS COLOSSEUM",
                 font=("Arial", 24, "bold"), fg="white", bg=BG).pack(pady=(24, 8))
        tk.Label(self.root, text="Choose your confidant",
                 font=("Arial", 15), fg="white", bg=BG).pack(pady=(0, 16))

        self.choice_frame = tk.Frame(self.root, bg=BG)
        self.choice_frame.pack(expand=True)

        starters = [
            ("Water_Starter", "Water", information.stat_water),
            ("Wood_Starter", "Wood", information.stat_wood),
            ("Fire_Starter", "Fire", information.stat_fire),
        ]
        for name, element, stat_func in starters:
            self.make_starter_card(name, element, stat_func)

        tk.Label(self.root, text="Choose one Pokémon to begin!",
                 font=("Arial", 12), fg="#ffd166", bg=BG).pack(pady=18)

    def make_starter_card(self, name, element, stat_func):
        card = tk.Frame(self.choice_frame, bg="#202b3c", padx=15, pady=15)
        card.pack(side="left", padx=10, pady=10)
        art = information.mon_dex[name][0]["art"]
        tk.Label(card, text="\n".join(art), font=("Courier New", 9),
                 fg="white", bg="#202b3c", justify="left").pack(pady=10)
        tk.Label(card, text=f"{information.mon_dex[name][0]['name'].replace('_', ' ')}\nElement: {element}",
                 font=("Arial", 12, "bold"), fg="white", bg="#202b3c").pack(pady=8)
        hp, dmg, defense, speed = stat_func(1, 0)
        tk.Label(card, text=f"HP: {hp}\nDMG: {dmg}\nDEF: {defense}\nSPE: {speed}",
                 font=("Arial", 10), fg="#dce6f1", bg="#202b3c",
                 justify="left").pack(pady=8)
        ttk.Button(card, text="Choose",
                   command=lambda: self.choose_pokemon(name, element, stat_func)).pack(pady=8)

    def show_battle_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg=BG)

        panel = tk.Frame(self.root, bg=BG, highlightbackground="#333333",
                         highlightthickness=1, padx=12, pady=10)
        panel.pack(fill="both", expand=True, padx=10, pady=10)

        header = tk.Frame(panel, bg=BG)
        header.pack(fill="x", pady=(0, 12))
        tk.Label(header, text="Pokémon Battle", font=("Arial", 16, "bold"),
                 fg="white", bg=BG).pack(side="left")
        self.stage_badge = tk.Label(header, text="STAGE 1",
                                    font=("Arial", 9, "bold"), fg="white",
                                    bg="#292929", padx=9, pady=4)
        self.stage_badge.pack(side="right")

        cards = tk.Frame(panel, bg=BG)
        cards.pack(fill="x")
        cards.grid_columnconfigure(0, weight=1, uniform="cards")
        cards.grid_columnconfigure(1, weight=1, uniform="cards")

        self.player_card = tk.Frame(cards, bg=BLUE_CARD, padx=13, pady=12)
        self.player_card.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        self.enemy_card = tk.Frame(cards, bg=PINK_CARD, padx=13, pady=12)
        self.enemy_card.grid(row=0, column=1, sticky="nsew", padx=(6, 0))

        tk.Label(self.player_card, text="YOUR POKÉMON", font=("Arial", 11, "bold"),
                 fg="#135b94", bg=BLUE_CARD).pack(anchor="w")
        self.player_name = tk.Label(self.player_card, text="", font=("Arial", 12, "bold"),
                                    fg="#111111", bg=BLUE_CARD)
        self.player_name.pack(anchor="w", pady=(14, 4))
        self.player_subtitle = tk.Label(self.player_card, text="", font=("Arial", 10),
                                        fg="#111111", bg=BLUE_CARD)
        self.player_subtitle.pack(anchor="w")
        self.player_exp_text = tk.Label(
            self.player_card, text="EXP: 0", font=("Arial", 9),
            fg="#135b94", bg=BLUE_CARD
        )
        self.player_exp_text.pack(anchor="w", pady=(3, 0))
        self.player_art = tk.Label(self.player_card, text="", font=("Courier New", 10),
                                   fg="#111111", bg=BLUE_CARD, justify="center", height=5)
        self.player_art.pack(fill="x", pady=(8, 4))
        self.player_hp_text = tk.Label(self.player_card, text="", font=("Arial", 9),
                                       fg="#111111", bg=BLUE_CARD)
        self.player_hp_text.pack(fill="x")
        self.player_hp = ttk.Progressbar(self.player_card, length=300,
                                         maximum=self.player["maxHP"],
                                         value=self.player["HP"],
                                         style="Player.Horizontal.TProgressbar")
        self.player_hp.pack(fill="x", pady=(7, 8))
        self.player_stats = tk.Label(self.player_card, text="", font=("Arial", 9),
                                     fg="#222222", bg=BLUE_CARD)
        self.player_stats.pack(anchor="w")

        self.enemy_role_label = tk.Label(self.enemy_card, text="ENEMY", font=("Arial", 11, "bold"),
                                         fg="#b92d27", bg=PINK_CARD)
        self.enemy_role_label.pack(anchor="w")
        self.enemy_name = tk.Label(self.enemy_card, text="", font=("Arial", 12, "bold"),
                                   fg="#111111", bg=PINK_CARD)
        self.enemy_name.pack(anchor="w", pady=(14, 4))
        self.enemy_subtitle = tk.Label(self.enemy_card, text="", font=("Arial", 10),
                                       fg="#111111", bg=PINK_CARD)
        self.enemy_subtitle.pack(anchor="w")
        self.enemy_art = tk.Label(self.enemy_card, text="", font=("Courier New", 10),
                                  fg="#111111", bg=PINK_CARD, justify="center", height=5)
        self.enemy_art.pack(fill="x", pady=(8, 4))
        self.enemy_hp_text = tk.Label(self.enemy_card, text="", font=("Arial", 9),
                                      fg="#111111", bg=PINK_CARD)
        self.enemy_hp_text.pack(fill="x")
        self.enemy_hp = ttk.Progressbar(self.enemy_card, length=300, maximum=100,
                                        value=100, style="Enemy.Horizontal.TProgressbar")
        self.enemy_hp.pack(fill="x", pady=(7, 8))
        self.enemy_stats = tk.Label(self.enemy_card, text="", font=("Arial", 9),
                                    fg="#222222", bg=PINK_CARD)
        self.enemy_stats.pack(anchor="w")

        # Battle Log: แยกหัวข้อชัดเจน เพิ่มสีและเวลาให้อ่านง่าย
        log_header = tk.Frame(panel, bg="#17212b")
        log_header.pack(fill="x", pady=(14, 0))
        tk.Label(
            log_header, text="⚔ BATTLE LOG",
            font=("Arial", 11, "bold"), fg="#ffd166", bg="#17212b"
        ).pack(side="left", padx=10, pady=7)
        ttk.Button(
            log_header, text="ล้างข้อความ",
            command=self.clear_battle_log
        ).pack(side="right", padx=8, pady=4)

        log_frame = tk.Frame(
            panel, bg="#17212b", highlightbackground="#34445c",
            highlightthickness=1, padx=6, pady=6
        )
        log_frame.pack(fill="both", expand=True)

        self.battle_log = tk.Text(
            log_frame, height=7, wrap="word",
            font=("Consolas", 11), bg="#101820", fg="#f1f5f9",
            insertbackground="white", relief="flat", padx=10, pady=8,
            spacing1=2, spacing3=4, state="disabled"
        )
        log_scroll = ttk.Scrollbar(
            log_frame, orient="vertical", command=self.battle_log.yview
        )
        self.battle_log.configure(yscrollcommand=log_scroll.set)
        self.battle_log.pack(side="left", fill="both", expand=True)
        log_scroll.pack(side="right", fill="y")

        self.battle_log.tag_configure(
            "time", foreground="#8b9aaa", font=("Consolas", 9)
        )
        self.battle_log.tag_configure(
            "damage", foreground="#ff7675", font=("Consolas", 11, "bold")
        )
        self.battle_log.tag_configure(
            "good", foreground="#7bed9f", font=("Consolas", 11, "bold")
        )
        self.battle_log.tag_configure(
            "skill", foreground="#ffd166", font=("Consolas", 11, "bold")
        )
        self.battle_log.tag_configure(
            "normal", foreground="#f1f5f9", font=("Consolas", 11)
        )

        tk.Label(panel, text="เลือกการกระทำ", font=("Arial", 11, "bold"),
                 fg="white", bg=BG).pack(anchor="w", pady=(12, 7))
        self.skill_frame = tk.Frame(panel, bg=BG)
        self.skill_frame.pack(fill="x")
        self.skill_frame.grid_columnconfigure(0, weight=1, uniform="skills")
        self.skill_frame.grid_columnconfigure(1, weight=1, uniform="skills")

        skill_names = {
            "Water": ["โจมตีปกติ", "Water Pulse", "Aqua Shield", "Tidal Wave", "Aqua Burst"],
            "Wood": ["โจมตีปกติ", "Leaf Strike", "Vine Whip", "Forest Force", "Nature Break"],
            "Fire": ["โจมตีปกติ", "Flame Shot", "Burning Flame", "Inferno", "Blazing Burst"],
        }
        self.skill_buttons = []
        for index, skill_name in enumerate(skill_names[self.player["element"]]):
            choice = str(index + 1)
            color = BLUE if index == 0 else GREEN
            btn = tk.Button(self.skill_frame, text=skill_name, fg="white", bg=color,
                            activebackground=color, activeforeground="white",
                            relief="flat", font=("Arial", 10, "bold"),
                            command=lambda c=choice: self.player_turn(c))
            btn.grid(row=index // 2, column=index % 2, sticky="ew",
                     padx=4, pady=4, ipady=10)
            self.skill_buttons.append(btn)
        self.start_battle()

    def clear_battle_log(self):
        self.battle_log.config(state="normal")
        self.battle_log.delete("1.0", "end")
        self.battle_log.config(state="disabled")

    def battle_log_message(self, message):
        from datetime import datetime

        message = str(message).strip()
        if not message:
            return

        lower_message = message.lower()
        if any(word in lower_message for word in (
            "damage", "ดาเมจ", "โจมตี", "miss", "พลาด", "hp"
        )):
            tag = "damage"
        elif any(word in lower_message for word in (
            "ชนะ", "victory", "ได้รับ", "ฟื้นฟู", "heal", "burn", "stun"
        )):
            tag = "good"
        elif any(word in lower_message for word in (
            "skill", "สกิล", "ใช้ท่า", "ใช้สกิล"
        )):
            tag = "skill"
        else:
            tag = "normal"

        timestamp = datetime.now().strftime("%H:%M:%S")
        self.battle_log.config(state="normal")
        self.battle_log.insert("end", f"[{timestamp}] ", "time")
        self.battle_log.insert("end", message + "\n", tag)
        self.battle_log.see("end")
        self.battle_log.config(state="disabled")

    def choose_pokemon(self, name, element, stat_func):
        hp, dmg, defense, speed = stat_func(1, 0)
        self.player = {
            "name": information.mon_dex[name][0]["name"],
            "starter_key": name, "element": element, "Lv": 1,
            "HP": hp, "maxHP": hp, "DMG": dmg, "DEF": defense,
            "SPE": speed, "Speed": speed, "evo": 0, "EXP": 0,
            "original_DMG": dmg,
        }
        self.show_battle_screen()

    def start_battle(self):
        self.stage = getattr(self, "stage", 1)
        self.stage_exp = [120, 350, 900, 2200, 5000, 11000,
                          24000, 50000, 100000, 250000]
        self.create_enemy()
        self.update_battle_ui()
        self.battle_log_message(
            f"{self.player['name']} เตรียมพร้อมต่อสู้! พบ {self.enemy['name']}"
        )

    def create_enemy(self):
        stage_functions = {
            1: enemies.stage1, 2: enemies.stage2, 3: enemies.stage3,
            4: enemies.stage4, 5: enemies.stage5, 6: enemies.stage6,
            7: enemies.stage7, 8: enemies.stage8, 9: enemies.stage9,
            10: enemies.stage10
        }
        self.enemy = stage_functions[self.stage]()
        self.enemy.setdefault("maxHP", self.enemy["HP"])
        self.enemy.setdefault("burn_turns", 0)
        self.enemy.setdefault("stun_turns", 0)
        self.player.setdefault("debuff_turns", 0)
        self.player["original_DMG"] = self.player["DMG"]
        self.battle_over = False

    def update_battle_ui(self):
        # Player panel: mon_dex uses list indices 0, 1, 2 for stages 1, 2, 3.
        self.stage_badge.config(
            text=(f"BOSS · STAGE {self.stage}" if self.stage == 10 else f"STAGE {self.stage}"),
            bg=("#7f1d1d" if self.stage == 10 else "#292929")
        )
        art_key = self.player.get("starter_key", "Water_Starter")
        art_stage = max(0, min(int(self.player.get("evo", 0)), 2))
        player_dex_entry = information.mon_dex[art_key][art_stage]
        art = player_dex_entry["art"]
        self.player["name"] = player_dex_entry["name"]
        self.player_name.config(text=self.player["name"])
        self.player_subtitle.config(
            text=f"ธาตุ {self.player['element']} · เลเวล {self.player['Lv']} · ร่าง {art_stage}"
        )
        self.player_exp_text.config(text=f"EXP เลเวลนี้: {self.player.get('EXP', 0):,}")
        self.player_art.config(text="\n".join(art))
        self.player_hp_text.config(
            text=f"HP  {self.player['HP']:,} / {self.player['maxHP']:,}")
        self.player_hp.configure(maximum=max(1, self.player["maxHP"]),
                                 value=max(0, self.player["HP"]))
        self.player_stats.config(
            text=f"DMG {self.player['DMG']} · DEF {self.player['DEF']} · SPE {self.player['SPE']}")

        # Match enemy names against the real mon_dex entries; use boss_dex art for the boss.
        is_boss = self.stage == 10 or self.enemy.get("element") == "Eternal"
        ttk.Style(self.root).configure("Boss.Horizontal.TProgressbar", troughcolor="#5b2528", background="#ff4d4d")
        enemy_name_key = str(self.enemy.get("name", "")).replace(" ", "_")
        enemy_art = None
        if is_boss:
            boss_data = information.mon_dex.get("boss_dex", {}).get(enemy_name_key)
            if boss_data:
                enemy_art = boss_data.get("art")
        if not enemy_art:
            for entries in information.mon_dex.values():
                if not isinstance(entries, list):
                    continue
                for entry in entries:
                    if entry.get("name", "").split(" (")[0] == enemy_name_key:
                        enemy_art = entry.get("art")
                        break
                if enemy_art:
                    break
        if not enemy_art:
            enemy_art = ["   ( ?.? )", "    /|/", "    /|"]
        if is_boss:
            self.enemy_card.config(bg="#351719", highlightbackground="#ff4d4d", highlightthickness=2)
            for widget in (self.enemy_role_label, self.enemy_name, self.enemy_subtitle,
                           self.enemy_art, self.enemy_hp_text, self.enemy_stats):
                widget.config(bg="#351719", fg=("#ff6b6b" if widget in (self.enemy_role_label, self.enemy_name) else "#ffe5e5"))
            self.enemy_role_label.config(text="☠ FINAL BOSS ☠")
            self.enemy_hp.configure(style="Boss.Horizontal.TProgressbar")
        else:
            self.enemy_card.config(bg=PINK_CARD, highlightthickness=0)
            self.enemy_role_label.config(text="ENEMY", fg="#b92d27", bg=PINK_CARD)
            for widget in (self.enemy_name, self.enemy_subtitle, self.enemy_art,
                           self.enemy_hp_text, self.enemy_stats):
                widget.config(bg=PINK_CARD, fg="#111111" if widget != self.enemy_stats else "#222222")
            self.enemy_hp.configure(style="Enemy.Horizontal.TProgressbar")

        self.enemy_name.config(text=self.enemy["name"].replace("_", " "))
        boss_tag = " · BOSS" if is_boss else ""
        self.enemy_subtitle.config(
            text=f"ธาตุ {self.enemy['element']} · Lv. {self.enemy['Lv']}{boss_tag}"
        )
        self.enemy_art.config(text="\n".join(enemy_art))
        self.enemy_hp_text.config(
            text=f"HP  {self.enemy['HP']:,} / {self.enemy['maxHP']:,}")
        self.enemy_hp.configure(maximum=max(1, self.enemy["maxHP"]),
                                value=max(0, self.enemy["HP"]))
        self.enemy_stats.config(
            text=f"DMG {self.enemy['DMG']} · DEF {self.enemy['DEF']} · SPE {self.enemy['SPE']}")

    def player_turn(self, choice):
        if self.battle_over:
            return
        for btn in self.skill_buttons:
            btn.config(state="disabled")
        try:
            output = io.StringIO()
            with redirect_stdout(output):
                enemy_first = enemies.has_turn_priority(self.enemy, self.player)
                if enemy_first:
                    battle.boss_action(self.enemy, self.player)
                    if self.player["HP"] > 0 and self.enemy["HP"] > 0:
                        battle.player_skill(self.player, self.enemy, choice)
                else:
                    battle.player_skill(self.player, self.enemy, choice)
                    if self.enemy["HP"] > 0 and self.player["HP"] > 0:
                        battle.boss_action(self.enemy, self.player)
                if self.player["HP"] > 0 and self.enemy["HP"] > 0:
                    battle.apply_status(self.player, self.enemy)

            messages = output.getvalue().strip()
            if messages:
                for line in messages.splitlines():
                    if line.strip():
                        self.battle_log_message(line)
            self.update_battle_ui()
            if self.enemy["HP"] <= 0:
                self.finish_battle(True)
            elif self.player["HP"] <= 0:
                self.finish_battle(False)
            else:
                for btn in self.skill_buttons:
                    btn.config(state="normal")
        except Exception as error:
            self.battle_log_message(f"เกิดข้อผิดพลาด: {error}")
            for btn in self.skill_buttons:
                btn.config(state="normal")

    def finish_battle(self, won):
        self.battle_over = True
        for btn in self.skill_buttons:
            btn.config(state="disabled")

        if not won:
            self.battle_log_message(
                f"คุณแพ้ในด่าน {self.stage}! เลือกว่าจะทำอย่างไรต่อ"
            )
            self.show_lose_options()
            return

        reward = self.stage_exp[self.stage - 1]
        previous_exp = self.player.get("EXP", 0)
        old_level = self.player.get("Lv", 1)
        total_exp = previous_exp + reward
        new_level, remaining_exp, next_req_exp = information.LVUP(
            total_exp, old_level
        )
        self.player["Lv"] = new_level
        self.player["EXP"] = remaining_exp

        # Evolution occurs at levels 25 and 50.
        new_evo = 2 if new_level >= 50 else 1 if new_level >= 25 else 0
        evolved = new_evo > self.player.get("evo", 0)
        self.player["evo"] = new_evo

        # Recalculate stats when the level/evolution changes.
        stat_func = {
            "Water": information.stat_water,
            "Wood": information.stat_wood,
            "Fire": information.stat_fire,
        }[self.player["element"]]
        hp, dmg, defense, speed = stat_func(new_level, new_evo)
        old_max_hp = self.player.get("maxHP", hp)
        hp_gain = max(0, hp - old_max_hp)
        self.player["maxHP"] = hp
        self.player["HP"] = min(hp, self.player.get("HP", hp) + hp_gain)
        self.player["DMG"] = dmg
        self.player["DEF"] = defense
        self.player["SPE"] = speed
        self.player["Speed"] = speed
        self.player["original_DMG"] = dmg

        self.battle_log_message(
            f"ชนะด่าน {self.stage}! ได้รับ {reward} EXP"
        )
        if new_level > old_level:
            self.battle_log_message(f"เลเวลเพิ่ม! Lv. {old_level} → Lv. {new_level}")
        if evolved:
            self.battle_log_message(f"วิวัฒนาการเป็นร่างที่ {new_evo + 1} แล้ว!")
        self.update_battle_ui()
        self.show_exp_window(reward, previous_exp, old_level, next_req_exp, evolved)

    def show_exp_window(self, reward, previous_exp, old_level, _old_next_req, evolved):
        """หน้าต่างสรุปรางวัล EXP เลเวล และระยะห่างจาก Evolution"""
        popup = tk.Toplevel(self.root)
        popup.title("Battle Rewards")
        popup.configure(bg="#101820")
        popup.resizable(False, False)
        popup.transient(self.root)
        popup.grab_set()

        width, height = 430, 430
        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - width) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - height) // 2
        popup.geometry(f"{width}x{height}+{x}+{y}")

        tk.Label(
            popup, text="VICTORY!",
            font=("Arial", 22, "bold"),
            fg="#7bed9f", bg="#101820"
        ).pack(pady=(22, 4))

        tk.Label(
            popup, text=f"เอาชนะ {self.enemy['name']} สำเร็จ",
            font=("Arial", 12, "bold"),
            fg="white", bg="#101820"
        ).pack(pady=(0, 15))

        details = tk.Frame(popup, bg="#1d2a35", padx=18, pady=14)
        details.pack(fill="x", padx=22)

        tk.Label(
            details, text="EXP ที่ได้รับ",
            font=("Arial", 11), fg="#dce6f1", bg="#1d2a35"
        ).grid(row=0, column=0, sticky="w", pady=5)

        tk.Label(
            details, text=f"+{reward:,} EXP",
            font=("Arial", 12, "bold"), fg="#ffd166", bg="#1d2a35"
        ).grid(row=0, column=1, sticky="e", pady=5)

        tk.Label(
            details, text="เลเวลปัจจุบัน",
            font=("Arial", 10, "bold"), fg="#dce6f1", bg="#1d2a35"
        ).grid(row=1, column=0, sticky="w", pady=4)
        tk.Label(
            details, text=f"Lv. {self.player['Lv']}" + (f"  (เลเวลอัป +{self.player['Lv'] - old_level})" if self.player['Lv'] > old_level else ""),
            font=("Arial", 11, "bold"), fg="#7bed9f", bg="#1d2a35"
        ).grid(row=1, column=1, sticky="e", pady=4)

        next_level_exp = int(50 * (1.12 ** (self.player['Lv'] - 1))) if self.player['Lv'] < 100 else 0
        exp_left = max(0, next_level_exp - self.player.get('EXP', 0))
        tk.Label(
            details, text="EXP เลเวลถัดไป",
            font=("Arial", 10), fg="#dce6f1", bg="#1d2a35"
        ).grid(row=2, column=0, sticky="w", pady=4)
        tk.Label(
            details, text=(f"สะสม {self.player.get('EXP', 0):,} / {next_level_exp:,}  (ขาด {exp_left:,})" if self.player['Lv'] < 100 else "ถึงเลเวลสูงสุดแล้ว"),
            font=("Arial", 9, "bold"), fg="#ffd166", bg="#1d2a35"
        ).grid(row=2, column=1, sticky="e", pady=4)

        if self.player['Lv'] < 25:
            evo_text = f"อีก {25 - self.player['Lv']} เลเวลถึงร่าง 2 (Lv. 25)"
        elif self.player['Lv'] < 50:
            evo_text = f"อีก {50 - self.player['Lv']} เลเวลถึงร่าง 3 (Lv. 50)"
        else:
            evo_text = "วิวัฒนาการครบแล้ว (ร่าง 3)"
        tk.Label(
            details, text="ความคืบหน้า Evolution",
            font=("Arial", 10), fg="#dce6f1", bg="#1d2a35"
        ).grid(row=3, column=0, sticky="w", pady=4)
        tk.Label(
            details, text=evo_text,
            font=("Arial", 9, "bold"), fg="#7bed9f", bg="#1d2a35",
            wraplength=210, justify="right"
        ).grid(row=3, column=1, sticky="e", pady=4)

        if evolved:
            tk.Label(
                popup, text=f"วิวัฒนาการสำเร็จ! {self.player['name']}",
                font=("Arial", 10, "bold"), fg="#ffd166", bg="#101820"
            ).pack(pady=(8, 0))

        details.grid_columnconfigure(0, weight=1)
        details.grid_columnconfigure(1, weight=1)

        if self.stage >= 10:
            next_text = "พิชิตครบทั้ง 10 ด่านแล้ว!"
            button_text = "จบเกม"
        else:
            next_text = f"เตรียมตัวเข้าสู่ด่าน {self.stage + 1}"
            button_text = "ไปด่านถัดไป"

        tk.Label(
            popup, text=next_text, font=("Arial", 10),
            fg="#dce6f1", bg="#101820"
        ).pack(pady=12)

        def continue_after_reward():
            popup.grab_release()
            popup.destroy()

            if self.stage >= 10:
                self.battle_log_message(
                    "ยินดีด้วย! คุณชนะครบทั้ง 10 ด่านแล้ว!"
                )
                return

            self.player["HP"] = self.player["maxHP"]
            self.stage += 1
            self.battle_log_message(
                f"ฟื้นฟู HP เต็มแล้ว กำลังเข้าสู่ด่าน {self.stage}..."
            )
            self.update_battle_ui()
            self.root.after(500, self.next_stage)

        ttk.Button(
            popup, text=button_text,
            command=continue_after_reward
        ).pack(pady=(0, 18), ipadx=12, ipady=4)

        popup.protocol("WM_DELETE_WINDOW", continue_after_reward)

    def show_lose_options(self):
        """เปิดหน้าต่างแยกเมื่อแพ้"""
        popup = tk.Toplevel(self.root)
        self.lose_popup = popup
        popup.title("Game Over")
        popup.configure(bg="#101820")
        popup.resizable(False, False)
        popup.transient(self.root)
        popup.grab_set()
        popup.protocol("WM_DELETE_WINDOW", lambda: None)

        width, height = 390, 300
        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - width) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - height) // 2
        popup.geometry(f"{width}x{height}+{x}+{y}")

        tk.Label(
            popup, text="GAME OVER", font=("Arial", 23, "bold"),
            fg="#ff7675", bg="#101820"
        ).pack(pady=(22, 6))
        tk.Label(
            popup, text=f"แพ้ในด่าน {self.stage}",
            font=("Arial", 12, "bold"), fg="white", bg="#101820"
        ).pack(pady=3)
        tk.Label(
            popup, text=f"{self.player['name']} · เลเวล {self.player['Lv']}\nEXP สะสม {self.player.get('EXP', 0):,}",
            font=("Arial", 10), fg="#dce6f1", bg="#101820", justify="center"
        ).pack(pady=(3, 14))

        buttons = tk.Frame(popup, bg="#101820")
        buttons.pack(fill="x", padx=22)

        def close_then(callback):
            popup.grab_release()
            popup.destroy()
            callback()

        ttk.Button(
            buttons, text="ลองด่านนี้อีกครั้ง",
            command=lambda: close_then(self.retry_stage)
        ).pack(fill="x", pady=4)

        if self.stage > 1:
            ttk.Button(
                buttons, text="กลับไปด่านก่อนหน้า",
                command=lambda: close_then(self.previous_stage)
            ).pack(fill="x", pady=4)

        ttk.Button(
            buttons, text="เริ่มเกมใหม่",
            command=lambda: close_then(self.restart_game)
        ).pack(fill="x", pady=4)

    def retry_stage(self):
        """เริ่มศัตรูด่านเดิมใหม่และฟื้นฟู HP"""
        self.player["HP"] = self.player["maxHP"]
        self.player["DMG"] = self.player.get("original_DMG", self.player["DMG"])
        self.player["debuff_turns"] = 0
        self.create_enemy()
        self.update_battle_ui()
        self.battle_log_message(f"ลองด่าน {self.stage} อีกครั้ง!")

        for btn in self.skill_buttons:
            btn.config(state="normal")

    def previous_stage(self):
        """ย้อนกลับไปสู้ด่านก่อนหน้า"""
        if self.stage <= 1:
            self.retry_stage()
            return

        self.stage -= 1
        self.player["HP"] = self.player["maxHP"]
        self.player["DMG"] = self.player.get("original_DMG", self.player["DMG"])
        self.player["debuff_turns"] = 0
        self.create_enemy()
        self.update_battle_ui()
        self.battle_log_message(f"ย้อนกลับมาที่ด่าน {self.stage}")

        for btn in self.skill_buttons:
            btn.config(state="normal")

    def restart_game(self):
        """กลับไปหน้าเลือก Pokémon และเริ่มเกมใหม่"""
        self.stage = 1
        self.show_starter_screen()

    def next_stage(self):
        self.create_enemy()
        self.update_battle_ui()
        self.battle_log_message(
            f"ด่าน {self.stage}: พบ {self.enemy['name']}!")
        for btn in self.skill_buttons:
            btn.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    app = PokemonGameGUI(root)
    root.mainloop()
