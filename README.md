# Quixx
THIS PROJECT IS A WORK IN PROGRESS

Why am I undertaking this project? My girlfriend's family treasures this game, and I think, besides one lucky win, I can never quite figure out what the best strategy is. Time to use math to get that win % up.

## Quixx Rules
This personal project analyzes the best strategies for **Quixx**, a dice game where you try to maximize your score before the game abruptly ends. The suggested number of players is 2-5. Each player is given a card that looks something like this:

**Red:**  `2 3 4 5 6 7 8 9 10 11 | 12 🔒`

**Yellow:**  `2 3 4 5 6 7 8 9 10 11 | 12 🔒`

**Green:**  `12 11 10 9 8 7 6 5 4 3 | 2 🔒`

**Blue:**  `12 11 10 9 8 7 6 5 4 3 | 2 🔒`

### Scoring System
The scoring table is represented as follows:

| X   | 1x | 2x | 3x | 4x | 5x | 6x | 7x | 8x | 9x | 10x | 11x | 12x |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Points | 1 | 3 | 6 | 10 | 15 | 21 | 28 | 36 | 45 | 55 | 66 | 78 |

Each player will track their score with checkboxes: `[ ] [ ] [ ] [ ]`.

### Total Scores
The total scores for each player are calculated as follows:

- **Red Total**: [ ]
- **Yellow Total**: [ ]
- **Green Total**: [ ]
- **Blue Total**: [ ]

Total score calculation:  
`Red Total + Yellow Total + Green Total + Blue Total - [ ] = [Total]`
