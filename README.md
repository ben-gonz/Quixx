# Quixx
THIS PROJECT IS A WORK IN PROGRESS

Why am I undertaking this project? My girlfriend's family treasures this game, and I think, besides one lucky win, I can never quite figure out what the best strategy is. Time to use math to get that win % up.

## Quixx Rules
This personal project analyzes the best strategies for **Quixx**, a dice game where you try to maximize your score before the game abruptly ends. The suggested number of players is 2-5. There are six dice in play, two white dice, and a red, yellow, green, and blue die. Each player is given a card that looks something like this:

**Red:**  `2 3 4 5 6 7 8 9 10 11 | 12 🔒`

**Yellow:**  `2 3 4 5 6 7 8 9 10 11 | 12 🔒`

**Green:**  `12 11 10 9 8 7 6 5 4 3 | 2 🔒`

**Blue:**  `12 11 10 9 8 7 6 5 4 3 | 2 🔒`


As dice are rolled on each turn, the player who rolls the dice may use the sum of the two white dice to cross a number off their card. Then, the player may use either of the white dice 🎲🎲 in combination with one of the colored die 🎲 to cross off a second number. If the player elects to use the colored die first, they may not use the two white dice in the same turn. Any of the other players can use the white dice on any turn. You can only use the colored die + one white die on your turn. Once a number in a row has been crossed off, you may not cross off any of the numbers to its left. Once you skip a square, it is dead So, the optimal strategy with Red and Yellow is to start with low numbers, and for Green and Blue start with high numbers. Once a player has marked five numbers in any row, that color is "lockable." Once it is lockable, that player may "lock" the color row on subsequent dice throws (by rolling a 2 or 12, depending on the color) 🔒. When the row is locked, the player may also take additional points by crossing off the lock. Other players may take the 2 or 12 if the sum is rolled on the white dice. 

You can elect to receive a penalty if it is your turn and you cannot play or choose not to mark any number. Each player can receive a maximum of four penalties, with each penalty being worth -5 points. The rest of the scoring is as follows.

### Scoring System

| X   | 1x | 2x | 3x | 4x | 5x | 6x | 7x | 8x | 9x | 10x | 11x | 12x |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Points | 1 | 3 | 6 | 10 | 15 | 21 | 28 | 36 | 45 | 55 | 66 | 78 |

Players receive points in each color category based on the amount of numbers crossed off in that cateogry

### Total Scores

Each player has a final score of the sum of each color score, minus any penalties. 
`Red Total + Yellow Total + Green Total + Blue Total - [ ] = [Total]`

### End of Play

The game ends and scores are tallied when two colors have been locked.
