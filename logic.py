import random
from constants import WIN_CONDITIONS


total_games = 0
total_draws = 0


def check_winner(board, symbol):
    for combo in WIN_CONDITIONS:
        if all(board[i] == symbol for i in combo):
            return combo
    return None


def is_draw(board):
    return all(cell in ('X', 'O') for cell in board)


def minimax(board, depth, is_my_turn, ai_sym):
    opp = 'O' if ai_sym == 'X' else 'X'

    if check_winner(board, ai_sym):
        return 10 - depth
    if check_winner(board, opp):
        return depth - 10
    if is_draw(board):
        return 0

    free = [i for i, c in enumerate(board) if c not in ('X', 'O')]

    if is_my_turn:
        best = -1000
        for i in free:
            board[i] = ai_sym
            best = max(best, minimax(board, depth + 1, False, ai_sym))
            board[i] = str(i)
        return best
    else:
        best = 1000
        for i in free:
            board[i] = opp
            best = min(best, minimax(board, depth + 1, True, ai_sym))
            board[i] = str(i)
        return best


def best_ai_move(board, ai_sym):
    free = [i for i, c in enumerate(board) if c not in ('X', 'O')]
    best_score = -1000
    best = None
    for i in free:
        board[i] = ai_sym
        score = minimax(board, 0, False, ai_sym)
        board[i] = str(i)
        if score > best_score:
            best_score = score
            best = i
    return best


def get_ai_move(board, difficulty):
    if difficulty == 'easy':
        free = [i for i, c in enumerate(board) if c not in ('X', 'O')]
        return random.choice(free)
    else:
        return best_ai_move(board, 'O')