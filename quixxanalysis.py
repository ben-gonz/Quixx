import random

class QuixxCard:
    def __init__(self, player_name="Player"):
        self.name = player_name
        self.red = [False] * 11    # 2 to 12
        self.yellow = [False] * 11 # 2 to 12
        self.green = [False] * 11  # 12 to 2
        self.blue = [False] * 11   # 12 to 2
        self.locks = {"red": False, "yellow": False, "green": False, "blue": False}
        self.penalties = 0
        self.max_penalties = 4

    def is_valid_move(self, color, number):
        idx = number - 2
        if color in ["red", "yellow"]:
            last_crossed = -1
            for i, crossed in enumerate(self.__dict__[color]):
                if crossed:
                    last_crossed = i
            return not self.__dict__[color][idx] and idx > last_crossed
        else:  # green, blue
            last_crossed = 11
            for i, crossed in enumerate(self.__dict__[color]):
                if crossed:
                    last_crossed = i
            return not self.__dict__[color][idx] and idx < last_crossed

    def can_lock_row(self, color):
        crosses = sum(self.__dict__[color])
        if crosses >= 7:  # Too many crosses, locking unlikely
            return False
        if color in ["red", "yellow"]:
            return not self.red[10] or crosses >= 5  # 12 still open or lockable
        else:
            return not self.__dict__[color][0] or crosses >= 5  # 2 still open or lockable

    def cross_off(self, color, number):
        if self.is_valid_move(color, number):
            idx = number - 2
            self.__dict__[color][idx] = True
            if sum(self.__dict__[color]) >= 5 and number in [2, 12]:
                self.locks[color] = True

    def take_penalty(self):
        if self.penalties < self.max_penalties:
            self.penalties += 1
            return True
        return False

    def score(self):
        scoring = [0, 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78]
        total = 0
        for color in ["red", "yellow", "green", "blue"]:
            crosses = sum(self.__dict__[color])
            total += scoring[crosses]
            if self.locks[color]:
                total += scoring[crosses + 1]  # Lock bonus
        return total - (self.penalties * 5)

    def print_state(self):
        print(f"{self.name}'s Card:")
        print(f"Red: {[i+2 for i, x in enumerate(self.red) if x]} (Locked: {self.locks['red']})")
        print(f"Yellow: {[i+2 for i, x in enumerate(self.yellow) if x]} (Locked: {self.locks['yellow']})")
        print(f"Green: {[12-i for i, x in enumerate(self.green) if x]} (Locked: {self.locks['green']})")
        print(f"Blue: {[12-i for i, x in enumerate(self.blue) if x]} (Locked: {self.locks['blue']})")
        print(f"Penalties: {self.penalties}/{self.max_penalties}")

def roll_dice():
    return {
        "W1": random.randint(1, 6),
        "W2": random.randint(1, 6),
        "R": random.randint(1, 6),
        "Y": random.randint(1, 6),
        "G": random.randint(1, 6),
        "B": random.randint(1, 6)
    }

def get_options(dice, is_roller=True):
    options = []
    white_sum = dice["W1"] + dice["W2"]
    options.append(("white", white_sum))
    if is_roller:
        for color, die in [("red", "R"), ("yellow", "Y"), ("green", "G"), ("blue", "B")]:
            options.append((color, dice[die] + dice["W1"]))
            options.append((color, dice[die] + dice["W2"]))
    return options

def evaluate_move(card, color, number):
    if not card.is_valid_move(color, number):
        return -float("inf")
    crosses = sum(card.__dict__[color])
    scoring = [0, 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78]
    
    temp_card = QuixxCard("Temp")
    temp_card.__dict__[color] = card.__dict__[color].copy()
    temp_card.cross_off(color, number)
    
    # New condition: Never cross if it prevents locking later
    if not temp_card.can_lock_row(color) and crosses < 5:
        return -float("inf")  # Block move unless it locks now or keeps locking possible
    
    # Locking priority
    if crosses >= 4 and number in [2, 12]:
        return 300 + crosses * 10
    
    # Early game: Keep options open
    if crosses < 4:
        if color in ["red", "yellow"] and number <= 7:
            return 20 + crosses
        if color in ["green", "blue"] and number >= 7:
            return 20 + crosses
        return crosses
    
    # Mid/late game: Maximize crosses
    return (scoring[crosses + 1] - scoring[crosses]) + (crosses * 5)

def best_move(card, options, is_roller=False):
    best_score = 0
    best_option = (None, None)
    has_valid_move = False
    
    for color, number in options:
        if color == "white":
            for c in ["red", "yellow", "green", "blue"]:
                score = evaluate_move(card, c, number)
                if score > -float("inf"):
                    has_valid_move = True
                if score > best_score:
                    best_score = score
                    best_option = (c, number)
        else:
            score = evaluate_move(card, color, number)
            if score > -float("inf"):
                has_valid_move = True
            if score > best_score:
                best_score = score
                best_option = (color, number)
    
    if is_roller and not has_valid_move and card.penalties < card.max_penalties:
        print(f"{card.name}: Forced penalty (no valid moves)")
        return ("penalty", None)
    
    if best_score < 10:
        return (None, None)
    
    return best_option

def play_turn(players, roller_idx, turn):
    dice = roll_dice()
    print(f"\nTurn {turn}")
    print(f"Roller: {players[roller_idx].name}")
    print(f"Roll: W1={dice['W1']}, W2={dice['W2']}, R={dice['R']}, Y={dice['Y']}, G={dice['G']}, B={dice['B']}")
    
    all_stuck = True
    for i, player in enumerate(players):
        is_roller = (i == roller_idx)
        options = get_options(dice, is_roller)
        move = best_move(player, options, is_roller)
        
        if move[0] == "penalty":
            if player.take_penalty():
                print(f"{player.name}: Took a penalty ({player.penalties}/{player.max_penalties})")
                all_stuck = False
        elif move[0]:
            player.cross_off(move[0], move[1])
            print(f"{player.name}: Crossed {move[1]} in {move[0]}{' (Locked)' if player.locks[move[0]] else ''}")
            all_stuck = False
        else:
            print(f"{player.name}: Skipped move")
        print(f"{player.name} Score: {player.score()}")
    
    game_over = False
    summary = []
    locked_details = []
    for player in players:
        locked_colors = [color for color, locked in player.locks.items() if locked]
        if len(locked_colors) >= 2:
            summary.append(f"{player.name} locked {locked_colors[0].capitalize()}")
            locked_details.append(f"{player.name} locked {', '.join(c.capitalize() for c in locked_colors)}")
            game_over = True
    
    if game_over:
        print(f"\nGame ended. {'; '.join(summary)}.")
        print("Game Over!")
        for detail in locked_details:
            print(detail)
        return True
    
    if all_stuck:
        print("\nGame ended. All players are stuck.")
        print("Game Over!")
        return True
    
    return False

# Simulate 4 players
players = [
    QuixxCard("You"),
    QuixxCard("Player 2"),
    QuixxCard("Player 3"),
    QuixxCard("Player 4")
]

# Main game loop
turn = 0
while True:
    turn += 1
    roller_idx = (turn - 1) % 4
    if play_turn(players, roller_idx, turn):
        break

# Final scores and state
print("\nFinal Scores:")
for player in players:
    print("================================")
    print(f"{player.name}: {player.score()}")
    player.print_state()