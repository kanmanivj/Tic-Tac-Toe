# Background & panel colours 
BG          = "#1a1a2e"
PANEL_BG    = "#16213e"
BTN_HOVER   = "#2a2a4e"
CELL_BG     = "#0f3460"
CELL_HOVER  = "#1a4a7a"

# Symbol & result colours 
X_COLOUR    = "#e94560"
O_COLOUR    = "#0f9b8e"
TEXT_LIGHT  = "#ff8c00"  
ACCENT      = "#f5a623"
WIN_COLOUR  = "#f5a623"
DRAW_COLOUR = "#888888"

# Fonts
FONT_TITLE  = ("Helvetica", 22, "bold")
FONT_SUB    = ("Helvetica", 13)
FONT_CELL   = ("Helvetica", 42, "bold")
FONT_LABEL  = ("Helvetica", 11)
FONT_SCORE  = ("Helvetica", 14, "bold")
FONT_BTN    = ("Helvetica", 11, "bold")

# Win conditions 
# Each list is a winning combination of board index positions
WIN_CONDITIONS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],   
    [0, 3, 6], [1, 4, 7], [2, 5, 8],   
    [0, 4, 8], [2, 4, 6]               
]