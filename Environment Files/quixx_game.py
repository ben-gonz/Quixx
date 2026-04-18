"""
QUIXX GAME LOGIC -- CORE RULES

This file defines the underlying rules and state transitions for a simplified
2-player version of Qwixx.

- Players: 2 total (0 = agent, 1 = opponent)
- Rows/colors: Red, Yellow, Green, Blue
- Each row contains 11 playable numbers plus 1 lock slot
- Red/Yellow progress left to right
- Green/Blue progress right to left
- A row can become globally locked for all players

TURN STRUCTURE
- One player is the active player each turn
- Dice rolled every turn: 2 white + 4 colored
- Active player may use white-sum, one colored+white combo, both (must take white sum first), or neither for a penalty
- Inactive player may only use the white-sum (handled externally)

CROSSING RULES
- Marks must be strictly farther along the row than current progress
- Skipped spaces cannot be revisited
- No marks in globally locked rows

LOCKING RULES
- Lock a row only with ≥5 prior marks + terminal number (12 for R/Y, 2 for G/B)
- Only one player can claim the lock per roll

SCORING & END
- Triangular scoring per row
- -5 per penalty
- Game ends at 2 global locks or 4 penalties by any player
"""

import random
import numpy as np
from enum import Enum

class Color(Enum):
    RED = "RED"
    YELLOW = "YELLOW"
    GREEN = "GREEN"
    BLUE = "BLUE"

class QuixxGame:
    def __init__(self, num_opponents=1, seed=None):
        self.num_opponents = num_opponents
        self.reset(seed)

    def reset(self, seed=None):
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        self.rows = [{color: [False]*11 + [False] for color in Color} for _ in range(1 + self.num_opponents)]
        self.penalties = [0] * (1 + self.num_opponents)
        self.globally_locked = {color: False for color in Color}
        self.current_roll = None
        self.active_player = random.randint(0, self.num_opponents)
        self.locked_this_turn = set()  # for same-turn locking

    def roll_dice(self):
        """One roll per full turn"""
        whites = [random.randint(1, 6) for _ in range(2)]
        colored = {c: random.randint(1, 6) for c in Color}
        self.current_roll = {
            "whites": whites,
            "colored": colored,
            "white_sum": sum(whites)
        }
        self.locked_this_turn.clear()
        return self.current_roll

    def is_valid_cross(self, player_idx, color, number, is_white_sum=False):
        if self.globally_locked[color]:
            return False
        if is_white_sum:
            if number != self.current_roll["white_sum"]:
                return False
        else:
            possible = [w + self.current_roll["colored"][color] for w in self.current_roll["whites"]]
            if number not in possible:
                return False

        row = self.rows[player_idx][color]
        target_idx = (12 - number) if color in (Color.GREEN, Color.BLUE) else (number - 2)
        if not (0 <= target_idx <= 10):
            return False

        crossed_indices = [i for i, crossed in enumerate(row[:11]) if crossed]
        last_crossed = max(crossed_indices) if crossed_indices else -1
        return target_idx > last_crossed and not row[target_idx]

    def cross(self, player_idx, color, number, is_white_sum=False):
        """Mark a box. Returns True if successful."""
        if not self.is_valid_cross(player_idx, color, number, is_white_sum):
            return False

        row = self.rows[player_idx][color]
        prior_crosses = sum(row[:11])
        idx = (12 - number) if color in (Color.GREEN, Color.BLUE) else (number - 2)
        row[idx] = True

        # Locking
        is_lock_number = (color in (Color.RED, Color.YELLOW) and number == 12) or \
                         (color in (Color.GREEN, Color.BLUE) and number == 2)
        if is_lock_number and prior_crosses >= 5 and color not in self.locked_this_turn:
            row[11] = True
            self.globally_locked[color] = True
            self.locked_this_turn.add(color)
        return True

    def take_penalty(self, player_idx):
        self.penalties[player_idx] += 1

    def calculate_score(self, player_idx=0):
        score_table = [0, 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78]
        total = sum(score_table[sum(self.rows[player_idx][c])] for c in Color)
        total -= 5 * self.penalties[player_idx]
        return total

    def is_done(self):
        return sum(self.globally_locked.values()) >= 2 or any(p >= 4 for p in self.penalties)

    def get_legal_moves(self, player_idx, is_active_player=True):
        """Legal moves for current player on current roll"""
        if not self.current_roll:
            return [(0, 0)]

        moves = []
        roll = self.current_roll

        # White-sum option (available to everyone)
        for c_idx, color in enumerate(Color):
            if self.is_valid_cross(player_idx, color, roll["white_sum"], is_white_sum=True):
                moves.append((c_idx + 1, 0))   # white on this color

        # Colored combo ONLY for active player
        if is_active_player:
            for c_idx, color in enumerate(Color):
                for w_idx, w in enumerate(roll["whites"]):
                    num = w + roll["colored"][color]
                    if self.is_valid_cross(player_idx, color, num, is_white_sum=False):
                        moves.append((0, c_idx * 2 + w_idx + 1))

            # Both moves (white first + colored)
            for w_c_idx, w_color in enumerate(Color):
                if not self.is_valid_cross(player_idx, w_color, roll["white_sum"], is_white_sum=True):
                    continue
                for c_c_idx, c_color in enumerate(Color):
                    if c_color in self.locked_this_turn:  # same-turn lock rule
                        continue
                    for w_idx, w in enumerate(roll["whites"]):
                        num = w + roll["colored"][c_color]
                        if self.is_valid_cross(player_idx, c_color, num, is_white_sum=False):
                            moves.append((w_c_idx + 1, c_c_idx * 2 + w_idx + 1))

        # Always allow pass (0,0)
        moves.append((0, 0))
        return list(dict.fromkeys(moves))  # remove duplicates, preserve order