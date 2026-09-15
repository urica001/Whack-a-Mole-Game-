"""
5 x 5 打地鼠 (Whack-a-Mole)
--------------------------------------------------------------
规则：
  1. 5 行 5 列共 25 个点位，开局随机藏 1 只地鼠，位置固定不动。
  2. 玩家共 5 次机会，每次只能打开一个点位。
  3. 命中           -> "Victory" + 笑脸 😊，游戏结束。
     未命中但上下左右相邻点位有地鼠
                    -> "Cheer up, I heard the sound around."
     四个相邻点位都没有地鼠
                    -> "Miss"
  4. 5 次机会用完仍未找到 -> "Defeat" + 哭脸 😢，公布地鼠位置并揭晓全图。
  5. 一局结束后可点「重新开始」再玩，无需重启程序。
"""

import random
import tkinter as tk
from tkinter import messagebox

SIZE = 5                                   # 场地边长：5 x 5
MAX_TRIES = 5                              # 玩家机会数
N = SIZE * SIZE                            # 点位总数

EMOJI_FONT = ("Segoe UI Emoji", 14)        # 保证 emoji 能正常显示
COLOR_HIT, COLOR_NEAR, COLOR_MISS = "#8BC34A", "#FFE082", "#E0E0E0"


class WhackAMole:
    def __init__(self, root):
        self.root = root
        root.title("打地鼠 5x5")
        root.resizable(False, False)

        # 状态栏 + 重新开始按钮
        bar = tk.Frame(root)
        bar.grid(row=0, column=0, columnspan=SIZE, pady=6)
        self.status = tk.Label(bar, font=("Arial", 12))
        self.status.pack(side=tk.LEFT, padx=8)
        tk.Button(bar, text="重新开始", font=("Arial", 10),
                  command=self.new_game).pack(side=tk.LEFT, padx=8)

        # 5x5 按钮网格，用一维列表保存，序号 0..24
        self.buttons = []
        for i in range(N):
            b = tk.Button(root, text="?", width=5, height=2, font=("Arial", 14),
                          command=lambda i=i: self.open_cell(i))
            b.grid(row=i // SIZE + 1, column=i % SIZE, padx=2, pady=2)
            self.buttons.append(b)

        self.new_game()

    # ---------------- 游戏流程 ----------------
    def new_game(self):
        """重置一局：重新藏地鼠、恢复所有按钮。"""
        self.mole = random.randrange(N)
        self.tries_left = MAX_TRIES
        self.game_over = False
        for b in self.buttons:
            b.config(text="?", state=tk.NORMAL, bg="SystemButtonFace")
        self._update_status()

    def open_cell(self, i):
        """打开第 i 个点位并立刻判定。"""
        if self.game_over or self.buttons[i]["state"] != tk.NORMAL:
            return                             # 已结束或该点位开过了
        self.tries_left -= 1
        self.buttons[i].config(state=tk.DISABLED)

        if i == self.mole:
            self._finish(i, "Victory", "Victory 😊\n一击命中，地鼠被你抓住了！")
        elif self._is_near(i):
            self._mark(i, COLOR_NEAR)
            messagebox.showinfo("Cheer up", "Cheer up, I heard the sound around.")
        else:
            self._mark(i, COLOR_MISS)
            messagebox.showinfo("Miss", "Miss")

        if not self.game_over:
            if self.tries_left:
                self._update_status()
            else:
                self._defeat()

    def _is_near(self, i):
        """地鼠位于 i 的上/下/左/右相邻点位时返回 True。"""
        r, c = divmod(i, SIZE)
        mr, mc = divmod(self.mole, SIZE)
        return abs(r - mr) + abs(c - mc) == 1

    def _mark(self, i, color):
        self.buttons[i].config(text="X", bg=color)

    def _defeat(self):
        """机会用尽仍未找到地鼠：揭晓地鼠位置和全图。"""
        self.game_over = True
        mr, mc = divmod(self.mole, SIZE)
        for i, b in enumerate(self.buttons):
            b.config(state=tk.DISABLED)
            if i == self.mole:
                b.config(text="🐹", bg="#EF5350")
            elif b["text"] == "?":
                b.config(text="·" if self._is_near(i) else "")
        self._update_status()
        messagebox.showinfo(
            "Defeat",
            f"Defeat 😢\n机会用完了，地鼠藏在第 {mr + 1} 行第 {mc + 1} 列。",
        )

    def _finish(self, i, title, msg):
        self.game_over = True
        self._mark(i, COLOR_HIT)
        self.buttons[i].config(text="😊")
        self._update_status()
        messagebox.showinfo(title, msg)

    def _update_status(self):
        self.status.config(text=f"剩余机会: {self.tries_left} / {MAX_TRIES}")


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes("-topmost", True)          # 避免消息框被其他窗口挡住
    WhackAMole(root)
    root.mainloop()