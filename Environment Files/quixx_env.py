"""
GYMNASIUM ENVIRONMENT WRAPPER FOR QUIXX

- Agent = Player 0
- Opponent = Player 1 (random legal moves)
- One step = agent's full decision as the active player
- Opponent's full turn (white + colored) is handled automatically inside the step
- Passive white-sum opportunity is given to the agent when opponent is active
"""

import gymnasium as gym
from gymnasium import spaces
import numpy as np
import random
from quixx_game import QuixxGame, Color


class QuixxEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 4}

    def __init__(self, render_mode=None):
        super().__init__()
        self.render_mode = render_mode
        self.game = QuixxGame(num_opponents=1)

        # Observation space (unchanged)
        low = np.zeros(48 + 2 + 1 + 1 + 6, dtype=np.int8)
        high = np.array([1]*48 + [4, 4, 4, 1] + [6]*6, dtype=np.int8)
        self.observation_space = spaces.Box(low=low, high=high, dtype=np.int8)

        self.action_space = spaces.MultiDiscrete([5, 9])  # white_choice, second_choice

    def _get_obs(self):
        obs = []
        for color in Color:
            obs.extend(self.game.rows[0][color])
        obs.extend(self.game.penalties)
        obs.append(sum(self.game.globally_locked.values()))
        obs.append(1 if self.game.active_player == 0 else 0)   # is_agent_active
        if self.game.current_roll:
            obs.extend(self.game.current_roll["whites"])
            for c in Color:
                obs.append(self.game.current_roll["colored"][c])
        else:
            obs.extend([0] * 6)
        return np.array(obs, dtype=np.int8)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.game.reset(seed)
        self.game.roll_dice()
        if self.render_mode == "human":
            self.render()
        return self._get_obs(), {}

    def step(self, action):
        white_choice, second_choice = action
        player = self.game.active_player

        # Record previous score before any actions
        old_score = self.game.calculate_score(0)

        took_agent_action = False

        # Agent decision making
        if player == 0: # 0 == agent is active player (rolls the dice)
            # White-sum
            if white_choice > 0:
                color = list(Color)[white_choice - 1]
                if self.game.cross(0, color, self.game.current_roll["white_sum"], is_white_sum=True):
                    took_agent_action = True

            # Colored combo
            if second_choice > 0:
                idx = second_choice - 1
                color_idx = idx // 2
                w_idx = idx % 2
                color = list(Color)[color_idx]
                num = self.game.current_roll["whites"][w_idx] + self.game.current_roll["colored"][color]
                if self.game.cross(0, color, num, is_white_sum=False):
                    took_agent_action = True

            # Penalty only if active player did nothing
            if not took_agent_action:
                self.game.take_penalty(0)

        else: # Agent is inactive
            # Agent decides on white-sum only
            if white_choice > 0:
                color = list(Color)[white_choice - 1]
                if self.game.cross(0, color, self.game.current_roll["white_sum"], is_white_sum=True):
                    took_agent_action = True

            # Opponent (active) plays randomly
            legal_opp = self.game.get_legal_moves(1, is_active_player=True)
            if legal_opp:
                opp_action = random.choice(legal_opp)
                w_c, sec_c = opp_action
                if w_c > 0:
                    color = list(Color)[w_c - 1]
                    self.game.cross(1, color, self.game.current_roll["white_sum"], is_white_sum=True)
                if sec_c > 0:
                    idx = sec_c - 1
                    color_idx = idx // 2
                    w_idx = idx % 2
                    color = list(Color)[color_idx]
                    num = self.game.current_roll["whites"][w_idx] + self.game.current_roll["colored"][color]
                    self.game.cross(1, color, num, is_white_sum=False)

        # New score after all moves on this roll
        new_score = self.game.calculate_score(0)
        reward = new_score - old_score # Reward function focuses on improving current score!

        # Small bonus for exploration (taking a legal move)
        # I added this because at first the agent would learn to do nothing to avoid penalties, but that also means it never discovers the positive rewards from crossing numbers. This encourages at least some interaction with the game state.
        if took_agent_action:
            reward += 0.1

        # End of turn
        self.game.active_player = 1 - self.game.active_player
        self.game.roll_dice()

        terminated = self.game.is_done()
        if terminated:
            reward += new_score * 0.05 # Reward for ending the game with a higher score.

        obs = self._get_obs()
        info = {
            "score": new_score,
            "active_player": self.game.active_player,
            "legal_moves": self.game.get_legal_moves(
                self.game.active_player,
                is_active_player=(self.game.active_player == 0)
            )
        }

        if self.render_mode == "human":
            self.render()

        return obs, reward, terminated, False, info

    def render(self):
        print("\n" + "="*80)
        print(f"QUIXX — Active player: {'AGENT' if self.game.active_player == 0 else 'OPPONENT'}")
        print("="*80)
        for p in range(2):
            label = "AGENT" if p == 0 else "OPPONENT"
            print(f"{label} penalties: {self.game.penalties[p]}/4")
            for color in Color:
                row = self.game.rows[p][color]
                lock = "X" if row[11] else " "
                print(f"  {color.value:<7} | " + " | ".join("X" if c else " " for c in row[:11]) + f" | 🔒{lock} |")
        print(f"Globally locked: {sum(self.game.globally_locked.values())}")
        if self.game.current_roll:
            print(f"White dice: {self.game.current_roll['whites']} (sum={self.game.current_roll['white_sum']})")
        print("="*80)