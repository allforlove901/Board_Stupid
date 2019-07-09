# Name:         Brett Nelson
# Course:       CSC 480
# Instructor:   Daniel Kauffman
# Assignment:   Board Stupid
# Term:         Winter 2019

import random, math

# function to check the result of a 2d board
def get_utility_2d(board):
    # check rows, cols, and diags for win
    dim = int(math.sqrt(len(board)))
    row_res = check_rows(board, dim)
    if row_res != 0:
        return row_res
    col_res = check_cols(board, dim)
    if col_res != 0:
        return col_res
    diag_res = check_diagonals(board, dim)
    if diag_res != 0:
        return diag_res

    # no win found, check if game over
    for i in range(len(board)):
        if board[i] == 0:
            return None
    # game over, return cat
    return 0


# function to check if a set of boards has a win result
def get_utility_3d(boards):
    game_over = True
    for board in boards:
        status = get_utility_2d(board)
        if status != None:
            if status != 0:
                return status
        else:
            game_over = False

    dim = int(math.sqrt(len(boards[0])))
    # check cross columns
    check_cc_res = check_cross_cols(boards, dim)
    if check_cc_res != 0:
        return check_cc_res
    # check cross diagonals
    check_cd_res = check_cross_diagonals(boards, dim)
    if check_cd_res != 0:
        return check_cd_res
    # check diagonal diagonals
    check_dd_res = check_diagonal_diagonals(boards, dim)
    if check_dd_res != 0:
        return check_dd_res

    if game_over:
        return 0
    else:
        return None


# function to check cross columns for win scenarios
def check_cross_cols(boards, dim):
    # check cross columns
    for i in range(len(boards[0])):
        mark = boards[0][i]
        if mark != 0:
            for j in range(len(boards)):
                if boards[j][i] != mark:
                    break
                if j == len(boards):
                    return mark
    return 0


# function to check cross diagonals for a win scenario
def check_cross_diagonals(boards, dim):
    # check top side cross_diag
    inc_val = dim
    for i in range(dim):
        mark = boards[0][i]
        if mark != 0:
            for j in range(len(boards)):
                if boards[j][i + inc_val * j] != mark:
                    break
                if j == len(boards):
                    return mark
    # check right side cross_diag
    inc_val = -1
    for i in range(dim):
        mark = boards[0][dim * i + dim - 1]
        if mark != 0:
            for j in range(len(boards)):
                if boards[j][dim * i + dim - 1 + inc_val * j] != mark:
                    break
                if j == len(boards):
                    return mark
    # check bottom side cross_diag
    inc_val = dim * -1
    for i in range(dim):
        mark = boards[0][dim * (dim - 1) + i]
        if mark != 0:
            for j in range(len(boards)):
                if boards[j][dim * (dim - 1) + i + inc_val] != mark:
                    break
                if j == len(boards):
                    return mark
    # check left side cross_diag
    inc_val = 1
    for i in range(dim):
        mark = boards[0][i * dim]
        if mark != 0:
            for j in range(len(boards)):
                if boards[j][i * dim + inc_val] != mark:
                    break
                if j == len(boards):
                    return mark
    return 0


# function to check diagonal diagonals for win scenario
def check_diagonal_diagonals(boards, dim):
    # get corners
    c1 = 0
    c2 = dim - 1
    c3 = dim * (dim - 1)
    c4 = dim * dim - 1
    # get increment amounts
    c1_inc = dim + 1
    c2_inc = dim - 1
    c3_inc = 1 - dim
    c4_inc = -1 - dim
    # get starting markers
    mark1 = boards[0][c1]
    mark2 = boards[0][c2]
    mark3 = boards[0][c3]
    mark4 = boards[0][c4]


    if mark1 != 0:
        for i in range(len(boards)):
            if boards[i][c1 + i * c1_inc] != mark1:
                break
            if i == dim - 1:
                return mark1
    if mark2 != 0:
        for i in range(len(boards)):
            if boards[i][c2 + i * c2_inc] != mark2:
                break
            if i == dim - 1:
                return mark2
    if mark3 != 0:
        for i in range(len(boards)):
            if boards[i][c3 + i * c3_inc] != mark3:
                break
            if i == dim - 1:
                return mark3
    if mark4 != 0:
        for i in range(len(boards)):
            if boards[i][c4 + i * c4_inc] != mark4:
                break
            if i == dim - 1:
                return mark4
    return 0


# function to find next best move
def find_best_move(boards, player, best_move, table):
    state = State(0, 0, [])
    table[boards] = state
    num_plays = 0
    best_move.append(0)
    qw = []

    while True:
        play_through(boards, player, table, qw)
        num_plays += 1
        for i in range(len(state.frontier)):
            if len(qw) > 0 and state.frontier[i] == qw[0]:
                best_move[0] = get_move_index(boards, state.frontier[i])
                while True:
                    j = 0
            s = table[state.frontier[i]]

        best_ratio = 0
        best_i = 0
        for i in range(len(state.frontier)):
            s = table[state.frontier[i]]
            if s.plays > 0:
                ratio = ((s.wins + 1) / (s.plays + 1))
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_i = i
        best_move[0] = get_move_index(boards, state.frontier[best_i])


# function to find out what number is move to make since I am
def get_move_index(boards, next_boards):
    for i in range(64):
        if boards[i // 16][i % 16] != next_boards[i // 16][i % 16]:
            return i


# functon to run a random playthrough on a board
def play_through(boards, player, table, qw):
    state = table[boards]
    state.plays += 1

    # state hasn't been played, get its frontier
    if not state.has_been_played:
        # extend frontier
        state.frontier.extend(get_frontier(boards, player))
        state.has_been_played = True
        new_states = []
        seen_states = []
        for f in state.frontier:
            if f not in table:
                table[f] = State(0, 0, [])
                new_states.append(f)
            # else, check for winning moves
            else:
                seen_states.append(f)
        for f in new_states:
            pns_res = process_new_state(player, state, table, f, qw)
            if pns_res != None:
                return pns_res
        for f in seen_states:
            if table[f].result != None:
                if table[f].result == player: # f is a winning move
                    if table[f].result == 1:
                        state.wins += 1
                    return table[f].result
                if table[f].result == 0: # f is last move available
                    return table[f].result
    else:
        for f in state.frontier:
            if table[f].result != None:
                if table[f].result == player: # f is a winning move
                    if table[f].result == 1:
                        state.wins += 1
                    return table[f].result
                if table[f].result == 0: # f is last move available
                    return table[f].result
    return move_on(state, table, player, qw)


# function to move to next node in game space
def move_on(state, table, player, qw):
    # game cannot end on this move, so check ucbs and exploit best one
    ucbs = get_ucbs(state.frontier, state.plays, table)
    moves = select_move(ucbs, player)
    next_boards = None
    if len(moves) == 1:
        next_boards = state.frontier[moves[0]]
    else:
        next_boards = state.frontier[random.choice(moves)]
    result = play_through(next_boards, player * -1, table, qw)
    if result == 1:
        state.wins += 1
    return result


# function to handle new state
# f: the boards of new state
def process_new_state(player, state, table, f, qw):
    table[f] = State(0, 0, [])
    f_result = get_utility_3d(f)
    if f_result != None: # f has a result
        table[f].result = f_result
        if f_result == player: # f is a winning move
            if len(qw) == 0:
                qw.append(f)
            state.plays += 1
            if f_result == 1:
                table[f].wins += 1
                table[f].plays += 1
                state.wins += 1
            return f_result
        if f_result == 0: # f is last move available
            table[f].plays += 1
            state.plays += 1
            return f_result


# function to get new game states visible from current state
def get_frontier(boards, player):
    frontier = []
    # go through boards and find open moves to create new states
    for i in range(64):
        if boards[i // 16][i % 16] == 0:
            # create copy of boards with new move made
            new_boards = []
            for j in range(len(boards)):
                new_board = []
                for k in range(len(boards[j])):
                    if j * 16 + k == i:
                        new_board.append(player)
                    else:
                        new_board.append(boards[j][k])
                new_boards.append(tuple(new_board))
            frontier.append(tuple(new_boards))
    return frontier


# function to select move based on highest ucb value
def select_move(ucbs, player):
    min = ucbs[0]
    max = ucbs[0]
    min_indices = [0]
    max_indices = [0]
    # get min and maxes of ucbs
    for i in range(len(ucbs)):
        # max checking
        if ucbs[i] > max:
            max = ucbs[i]
            max_indices = [i]
        elif ucbs[i] == max:
            max_indices.append(i)
        # min checking
        if ucbs[i] < min:
            min = ucbs[i]
            min_indices = [i]
        elif ucbs[i] == min:
            min_indices.append(i)
    # return indices based on player
    return max_indices if player > 0 else min_indices


# function to get UCB for each node
# ucb format [[plays, wins, ucb]...]
def get_ucbs(frontier, total_plays, table):
    ucbs = []
    # go through list of moves and calculate ucb value
    for i in range(len(frontier)):
        state = table[frontier[i]]
        x = (state.wins + 1) / (state.plays + 1)
        y = math.sqrt((2 * math.log(total_plays) + 1) / (state.plays + 1))
        ucb = x + y
        ucbs.append(ucb)
    return ucbs


# function to check for horizontal win situations
def check_rows(board, dim):
    # check rows
    for i in range(dim):
        # get first, check if zero
        mark = board[i * dim]
        if mark != 0:
            # go through row until non-equivalent found
            for j in range(dim):
                if board[i * dim + j] != mark:
                    break
                # win, return mark
                if j == dim - 1:
                    return mark
    return 0


# function to check for vertical win situations
def check_cols(board, dim):
    # check columns
    for i in range(dim):
        # get first, check if zero
        mark = board[i]
        if mark != 0:
            # go through row until non-equivalent found
            for j in range(dim):
                if board[i + dim * j] != mark:
                    break
                # win, return mark
                if j == dim - 1:
                    return mark
    return 0


# function to check for diagonal win situations
def check_diagonals(board, dim):
    # check diagonals
    c1 = 0
    c2 = dim - 1
    c1_inc = dim + 1
    c2_inc = dim - 1
    mark1 = board[c1]
    mark2 = board[c2]
    if mark1 != 0:
        for i in range(dim):
            if board[c1 + i * c1_inc] != mark1:
                break
            if i == dim - 1:
                return mark1
    if mark2 != 0:
        for i in range(dim):
            if board[c2 + i * c2_inc] != mark2:
                break
            if i == dim - 1:
                return mark2
    return 0


# class to represent state objects
class State(object):
    wins = []
    plays = []
    frontier = []
    has_been_played = False
    result = None

    # The class "constructor" - It's actually an initializer
    def __init__(self, wins, plays, frontier):
        self.wins = wins
        self.plays = plays
        self.frontier = frontier
