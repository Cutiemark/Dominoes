import random
# Write your code here


def print_domino_snake(snake):
    if len(snake) > 5:
        print(f"{snake[0]}{snake[1]}{snake[2]}...{snake[-3]}{snake[-2]}{snake[-1]}")
    else:
        print(*snake, sep="")


def do_move(move_, pieces):
    if move_ > 0:
        domino_snake.append(pieces.pop(move_ - 1))  # pop returns value and deletes the element
    elif move_ < 0:
        domino_snake.insert(0, pieces.pop(abs(move_) - 1))  # insert(0) = append from left side
    elif move_ == 0 and len(stock_pieces) > 0:
        pieces.append(stock_pieces.pop(0))


def legality(move_, pieces):
    if move_ < 0:
        if pieces[abs(move_) - 1][1] != domino_snake[0][0]:
            if pieces[abs(move_) - 1][0] != domino_snake[0][0]:
                # print("Illegal move. Please try again.")
                return True
            else:
                pieces[abs(move_) - 1][0], pieces[abs(move_) - 1][1] = pieces[abs(move_) - 1][1], pieces[abs(move_) - 1][0]
                return False
    if move_ > 0:
        if pieces[move_ - 1][0] != domino_snake[-1][1]:
            if pieces[move_ - 1][1] != domino_snake[-1][1]:
                # print("Illegal move. Please try again.")
                return True
            else:
                pieces[move_ - 1][0], pieces[move_ - 1][1] = pieces[move_ - 1][1], pieces[move_ - 1][0]
                return False
    # if move_ == 0 and len(stock_pieces) == 0:
    #     return True
    return False


def advanced_ai():
    score = []
    for one_piece in range(len(computer_pieces)):
        score.append(sum(x.count(computer_pieces[one_piece][0]) for x in domino_snake) +
                     sum(x.count(computer_pieces[one_piece][0]) for x in computer_pieces) +
                     sum(x.count(computer_pieces[one_piece][1]) for x in domino_snake) +
                     sum(x.count(computer_pieces[one_piece][1]) for x in computer_pieces))
    # print(computer_pieces)
    # print(score)
    max_index = 1
    while True:
        if score.count(0) == len(score):
            ai_move = 0
            break
        else:
            max_value = max(score)
            max_index = score.index(max_value)
            # print(f"Max index: {max_index + 1}")
            ai_move = max_index + 1
            if legality(ai_move, computer_pieces):
                score[max_index] = 0
                ai_move = -ai_move
                if legality(ai_move, computer_pieces):
                    score[max_index] = 0
                    continue
            # print(score)
            break
    do_move(ai_move, computer_pieces)


def game_over():
    if len(computer_pieces) == 0:
        print("Status: The game is over. The computer won!")
        return True
    elif len(player_pieces) == 0:
        print("Status: The game is over. You won!")
        return True
    elif domino_snake[0][0] == domino_snake[-1][-1] and sum(x.count(domino_snake[0][0]) for x in domino_snake) == 8:
        print("Status: The game is over. It's a draw!")
        return True
    else:
        return False


full_domino_set = [
    [0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6],
    [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6],
    [2, 2], [2, 3], [2, 4], [2, 5], [2, 6],
    [3, 3], [3, 4], [3, 5], [3, 6],
    [4, 4], [4, 5], [4, 6],
    [5, 5], [5, 6],
    [6, 6]
]
doubles = [
    [0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6]
]
while True:
    stock_pieces = random.sample(full_domino_set, 14)
    players_sets = [x for x in full_domino_set if x not in stock_pieces]
    computer_pieces = random.sample(players_sets, 7)
    player_pieces = [x for x in players_sets if x not in computer_pieces]
    highest_double_comp = [-1, -1]
    highest_double_player = [-1, -1]
    domino_snake = []
    status = ""
    for piece in doubles:
        if piece in computer_pieces:
            if piece > highest_double_comp:
                highest_double_comp = piece
        if piece in player_pieces:
            if piece > highest_double_player:
                highest_double_player = piece
    if highest_double_comp == highest_double_player == [-1, -1]:
        # print("No doubles!")
        continue
    else:
        if highest_double_comp > highest_double_player:
            domino_snake.append(highest_double_comp)
            computer_pieces.remove(highest_double_comp)
            status = "player"
        else:
            domino_snake.append(highest_double_player)
            player_pieces.remove(highest_double_player)
            status = "computer"
    break
while True:
    print("======================================================================")
    print(f"Stock size: {len(stock_pieces)}")
    print(f"Computer pieces: {len(computer_pieces)}")
    print()
    print_domino_snake(domino_snake)
    print()
    print("Your pieces:")
    for index in range(len(player_pieces)):
        value = player_pieces[index]
        print(f"{index + 1}:{value}")
    print()
    if game_over():
        break
    if status == "computer":
        input("Status: Computer is about to make a move. Press Enter to continue...")
        # while True:
        #     move = random.randint(-len(computer_pieces), len(computer_pieces) - 1)
        #     if not legality(move, computer_pieces):
        #         break
        # do_move(move, computer_pieces)
        advanced_ai()
        status = "player"
    else:
        print("Status: It's your turn to make a move. Enter your command.")
        move = 0
        while True:
            try:
                move = int(input())
            except ValueError:
                print("Invalid input. Please try again.")
                continue
            if abs(int(move)) <= len(player_pieces):
                if not legality(move, player_pieces):
                    break
                else:
                    print("Illegal move. Please try again.")
            else:
                print("Invalid input. Please try again.")
                continue
        while True:
            do_move(move, player_pieces)
            break
        status = "computer"
