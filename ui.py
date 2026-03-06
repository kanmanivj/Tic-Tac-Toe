
import tkinter as tk
from tkinter import messagebox
from constants import *
from logic import check_winner, is_draw, get_ai_move
import logic


# main window

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic-Tac-Toe")
        self.resizable(False, False)
        self.configure(bg=BG)
        self.geometry("520x620")
        self.eval('tk::PlaceWindow . center')

        self.current_frame = None
        self.show_menu()

    def show_frame(self, frame):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame
        frame.pack(fill="both", expand=True)

    def show_menu(self):
        self.show_frame(MenuScreen(self))

    def show_setup(self, mode):
        self.show_frame(SetupScreen(self, mode))

    def show_game(self, p1_name, p2_name, mode, difficulty,
                  scores=None, keep_scores=False):
        self.show_frame(GameScreen(
            self, p1_name, p2_name, mode, difficulty,
            scores, keep_scores
        ))

# menu

class MenuScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)

        tk.Label(self, text="Welcome",
                 font=("Helvetica", 42, "bold"),
                 bg=BG, fg=TEXT_LIGHT).pack(pady=(50, 5))

        tk.Label(self, text="Tic-Tac-Toe",
                 font=FONT_TITLE, bg=BG, fg=TEXT_LIGHT).pack()

        tk.Label(self, text="Choose a game mode to start",
                 font=FONT_SUB, bg=BG, fg=TEXT_LIGHT).pack(pady=(6, 40))

        self._btn("Human vs Human",   X_COLOUR,
                  lambda: master.show_setup('hvh'))
        self._btn("Human vs Computer", O_COLOUR,
                  lambda: master.show_setup('hvc'))

        tk.Label(self, text="v1.0 - Built with Python + Tkinter",
                 font=FONT_LABEL, bg=BG, fg=TEXT_LIGHT).pack(side="bottom", pady=16)

    def _btn(self, text, colour, cmd):
        tk.Button(self, text=text, font=FONT_BTN,
                  bg=colour, fg="#1a1a2e",
                  activebackground=colour,
                  relief="flat", cursor="hand2",
                  width=24, height=2, command=cmd).pack(pady=8)

# setup screen

class SetupScreen(tk.Frame):
    def __init__(self, master, mode):
        super().__init__(master, bg=BG)
        self.master = master
        self.mode = mode

        tk.Label(self, text="Game Setup",
                 font=FONT_TITLE, bg=BG, fg=TEXT_LIGHT).pack(pady=(40, 6))

        tk.Label(self, text="Fill in the details below",
                 font=FONT_SUB, bg=BG, fg=TEXT_LIGHT).pack(pady=(0, 30))

        self._field_label("Player 1 name  (plays as X)")
        self.p1_entry = self._entry()

        if mode == 'hvh':
            self._field_label("Player 2 name  (plays as O)")
            self.p2_entry = self._entry()
            self.diff_var = None
        else:
            self.p2_entry = None
            tk.Label(self, text="AI Difficulty",
                     font=FONT_LABEL, bg=BG, fg=TEXT_LIGHT).pack(pady=(18, 4))
            self.diff_var = tk.StringVar(value='easy')
            row = tk.Frame(self, bg=BG)
            row.pack()
            for label, val in [("Easy", "easy"), ("Hard", "hard")]:
                tk.Radiobutton(row, text=label, variable=self.diff_var,
                        value=val, font=FONT_BTN,
                        bg=ACCENT, fg="#1a1a2e",
                        selectcolor=X_COLOUR,
                        activebackground=ACCENT,
                        indicatoron=0, width=12, pady=6,
                        relief="flat", cursor="hand2").pack(side="left", padx=6)

        btn_row = tk.Frame(self, bg=BG)
        btn_row.pack(pady=36)

        tk.Button(btn_row, text="Back", font=FONT_BTN,
          bg=PANEL_BG, fg=TEXT_LIGHT,
          activebackground=BTN_HOVER,
          highlightbackground=PANEL_BG,
          relief="flat", cursor="hand2", width=10,
          command=master.show_menu).pack(side="left", padx=8)

        tk.Button(btn_row, text="Start Game", font=FONT_BTN,
          bg=ACCENT, fg="#1a1a2e", activebackground=ACCENT,
          highlightbackground=ACCENT,
          relief="flat", cursor="hand2", width=14,
          command=self.start).pack(side="left", padx=8)

    def _field_label(self, text):
        tk.Label(self, text=text, font=FONT_LABEL,
                 bg=BG, fg=TEXT_LIGHT).pack(pady=(10, 3))

    def _entry(self):
        e = tk.Entry(self, font=FONT_SUB, bg=PANEL_BG, fg=TEXT_LIGHT,
             insertbackground=TEXT_LIGHT, relief="solid",
             highlightthickness=1, highlightbackground=TEXT_LIGHT,
             width=22, justify="center")
        e.pack(ipady=7)
        return e

    def start(self):
        p1 = self.p1_entry.get().strip() or "Player 1"
        if self.mode == 'hvh':
            p2 = self.p2_entry.get().strip() or "Player 2"
            diff = None
        else:
            p2 = "Computer"
            diff = self.diff_var.get()
        self.master.show_game(p1, p2, self.mode, diff)

# main game screen

class GameScreen(tk.Frame):
    def __init__(self, master, p1_name, p2_name, mode, difficulty,
                 scores=None, keep_scores=False):
        super().__init__(master, bg=BG)
        self.master = master
        self.p1_name = p1_name
        self.p2_name = p2_name
        self.mode = mode
        self.difficulty = difficulty

        self.board = [str(i) for i in range(9)]
        self.turn = 'X'
        self.game_over = False

        if keep_scores and scores:
            self.scores = scores
        else:
            self.scores = {p1_name: 0, p2_name: 0, 'Draws': 0}
        self._build_ui()

    def _build_ui(self):

        top = tk.Frame(self, bg=PANEL_BG, pady=10)
        top.pack(fill="x")

        tk.Button(top, text="Home", font=("Helvetica", 11, "bold"),
                  bg=PANEL_BG, fg=TEXT_LIGHT, relief="flat",
                  cursor="hand2", activebackground=BTN_HOVER,
                  command=self.master.show_menu).pack(side="left", padx=14)

        tk.Label(top, text="Tic-Tac-Toe",
                 font=("Helvetica", 15, "bold"),
                 bg=PANEL_BG, fg=TEXT_LIGHT).pack(side="left", padx=6)

        if self.difficulty:
            tag = "Easy" if self.difficulty == 'easy' else "Hard"
            tk.Label(top, text=tag, font=FONT_LABEL,
                     bg=PANEL_BG, fg=ACCENT).pack(side="right", padx=14)

        # scoreboard
    
        score_frame = tk.Frame(self, bg=BG, pady=10)
        score_frame.pack(fill="x", padx=20)

        self.score_labels = {}

        p1_info = (self.p1_name, 'X', X_COLOUR)
        p2_info = (self.p2_name, 'O', O_COLOUR)
        draw_info = ('Draws', '', DRAW_COLOUR)

        for name, sym, col in [p1_info, draw_info, p2_info]:
            box = tk.Frame(score_frame, bg=PANEL_BG, padx=14, pady=8)
            box.pack(side="left", expand=True, fill="x", padx=5)

            if len(name) > 9:
                short = name[:8] + "..."
            else:
                short = name

            if sym:
                display = short + " (" + sym + ")"
            else:
                display = short

            tk.Label(box, text=display, font=FONT_LABEL,
                bg=PANEL_BG, fg=col).pack()
            lbl = tk.Label(box, text=str(self.scores[name]),
                   font=FONT_SCORE, bg=PANEL_BG, fg=TEXT_LIGHT)
            lbl.pack()
            self.score_labels[name] = lbl

        self.status_var = tk.StringVar()
        self._update_status()
        tk.Label(self, textvariable=self.status_var,
                 font=("Helvetica", 12, "bold"),
                 bg=BG, fg=ACCENT).pack(pady=(10, 4))

        
        # board grid
        grid_frame = tk.Frame(self, bg="#0a0a1a", padx=6, pady=6)
        grid_frame.pack(padx=24)

        self.buttons = []
        for i in range(9):
            btn = tk.Button(grid_frame, text="", font=FONT_CELL,
                            bg=CELL_BG, fg=TEXT_LIGHT,
                            width=3, height=1,
                            relief="flat", cursor="hand2",
                            highlightthickness=0,
                            highlightbackground=CELL_BG,
                            activebackground=CELL_HOVER,
                            command=lambda idx=i: self._on_click(idx))
            btn.grid(row=i // 3, column=i % 3,
                     padx=4, pady=4, ipadx=14, ipady=14)
            self.buttons.append(btn)

        bottom = tk.Frame(self, bg=BG, pady=14)
        bottom.pack()

        tk.Button(bottom, text="New Round", font=FONT_BTN,
                  bg=O_COLOUR, fg="#1a1a2e", activebackground=O_COLOUR,
                  relief="flat", cursor="hand2", width=14,
                  command=self._new_round).pack(side="left", padx=8)

        tk.Button(bottom, text="Change Players", font=FONT_BTN,
                  bg=PANEL_BG, fg=TEXT_LIGHT, activebackground=BTN_HOVER,
                  relief="flat", cursor="hand2", width=16,
                  command=self._change_players).pack(side="left", padx=8)

    def _update_status(self):
        name = self.p1_name if self.turn == 'X' else self.p2_name
        self.status_var.set(f"{name}'s turn ({self.turn})")

    def _on_click(self, idx):
        if self.game_over:
            return
        if self.board[idx] in ('X', 'O'):
            return
        if self.mode == 'hvc' and self.turn == 'O':
            return
        self._make_move(idx)

        if not self.game_over and self.mode == 'hvc' and self.turn == 'O':
            self._disable_board()
            self.after(450, self._ai_move)

    def _make_move(self, idx):
        self.board[idx] = self.turn
        sym = self.turn
        colour = X_COLOUR if sym == 'X' else O_COLOUR

        self.buttons[idx].config(text=sym, fg=colour,
                                  bg=CELL_BG, state="disabled",
                                  disabledforeground=colour)

        win_combo = check_winner(self.board, sym)
        if win_combo:
            self._highlight_win(win_combo)
            winner = self.p1_name if sym == 'X' else self.p2_name
            self.scores[winner] += 1
            self.score_labels[winner].config(text=str(self.scores[winner]))
            self.status_var.set(f"{winner} wins!")
            self.game_over = True
            logic.total_games += 1
            return

        if is_draw(self.board):
            self.scores['Draws'] += 1
            self.score_labels['Draws'].config(text=str(self.scores['Draws']))
            self.status_var.set("Its a draw!")
            self.game_over = True
            logic.total_games += 1
            logic.total_draws += 1
            return

        self.turn = 'O' if self.turn == 'X' else 'X'
        self._update_status()

    def _ai_move(self):
        if self.game_over:
            return
        idx = get_ai_move(self.board, self.difficulty)
        self._enable_board()
        self._make_move(idx)

    def _highlight_win(self, combo):
        for i in combo:
            self.buttons[i].config(bg=WIN_COLOUR,disabledforeground="#1a1a2e")
        for i, btn in enumerate(self.buttons):
            if i not in combo:
                btn.config(state="disabled")

    def _disable_board(self):
        for btn in self.buttons:
            btn.config(state="disabled")

    def _enable_board(self):
        for i, btn in enumerate(self.buttons):
            if self.board[i] not in ('X', 'O'):
                btn.config(state="normal")

    def _new_round(self):
        self.board = [str(i) for i in range(9)]
        self.turn = 'X'
        self.game_over = False
        for btn in self.buttons:
            btn.config(text="", bg=CELL_BG, fg=TEXT_LIGHT,
                       state="normal", disabledforeground=TEXT_LIGHT,
                       highlightbackground=CELL_BG)
        self._update_status()

    def _change_players(self):
        if self.mode == 'hvh':
            keep = messagebox.askyesno(
                "Same players?",
                f"Are {self.p1_name} and {self.p2_name} still playing?\n\n"
                "Yes - keep scores\nNo - new players, reset scores"
            )
            if keep:
                self.master.show_game(
                    self.p1_name, self.p2_name,
                    self.mode, self.difficulty,
                    scores=self.scores, keep_scores=True
                )
            else:
                self.master.show_setup(self.mode)
        else:
            self.master.show_setup(self.mode)