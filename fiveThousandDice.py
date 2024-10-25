import sys
import random

print('Welcome to 5,000 dice.')
rules = input('Do you want to read the rules? (Y/N)')
if rules.upper() == 'Y':
    print('''
OBJECTIVE:
Be the first player to score 5,000 points!
Roll 5 dice and earn points by collecting three of a kind, 1's and 5's.
Once a player reaches 5,000 points, each player gets one last turn to try and earn the top score.
          
COUNTERS:
Points are obtained through counters.
Counters are:
1's
5's
Any 3 of a kind
          
SCORING:
1 = 100pts each or 1,000pts for three,
5 = 50pts each or 500pts for three,
3 of a kind = *00pts (200 - 600)

ADDITIONAL:
You must initially score 350 points to add a score to the board, then you can score at any time.
You must save at least one counter to continue rolling. i.e. save at least one scoring die from your current roll to continue.
    If your roll is 1, 2, 2, 3, 4.. you can save both 2's to try for a third. But, you also have to save the 1 to roll again.
    If your next roll is 1, 2, 2, 5, 6 because you saved 1, 2, 2; then your current score is 150 and you have to keep 1, 2, 2, 5 to roll again.
If you roll no counters ('garbage'), your turn is over and you lose your points accumulated in that turn.
If all five dice are counters, you can continue increasing your score by rerolling all five dice again.
''')

# The player turn. One of these for each turn. Return the next player.
def rollLoop(playerTurn: int) -> int:
    score = 0
    currScore = 0
    diceRoll = []
    keepDice = []
    while True:
        print(f"It's player {playerTurn}'s turn.")
        turn = input('Do you want to...\n(R)oll Dice\n(K)eep Dice\nShow (D)ice\n(S)core Roll/End Turn\nShow (A)ll Scores\nShow (C)urrent Score\n(Q)uit Game\n')
        if turn.upper() == 'R':
            if not keepDice:
                score += currScore
                currScore = 0
            if len(keepDice) == 5:
                score += currScore
                currScore = 0
                keepDice = []
            diceRoll = rollDice(5 - len(keepDice), diceRoll[0:len(keepDice)])
            if currScore == checkScore(diceRoll):
                showDice(diceRoll, score, currScore)
                print('You blew it.')
                showScores()
                return playerTurn
            currScore = checkScore(diceRoll)
            showDice(diceRoll, score, currScore)
            if checkScore(diceRoll) == 0:
                print('You blew it!')
                showScores()
                return playerTurn
        elif turn.upper() == 'K':
            if not diceRoll:
                print('You do not have any dice to keep. Roll first.')
                continue
            else:
                try:
                    keepDice = [int(i) for i in (input('Which dice do you want to keep? e.g. 12, 123, 35\n'))]
                except ValueError:
                    print('Please enter a valid combo. e.g. 12, 123, 35')
                diceRoll = saveDice(keepDice, diceRoll)
                #TODO Need to make sure you keep the same dice as last time unless rolling all.
                showDice(diceRoll, score, currScore)
        elif turn.upper() == 'D':
            showDice(diceRoll, score, currScore)
        elif turn.upper() == 'S':
            if playerScores[playerTurn] == 0:
                if (score + checkScore(diceRoll)) < 350:
                    print("You need at least 350 points to get on the board.")
                else:
                    playerScores[playerTurn] += score + checkScore(diceRoll)
                    showScores()
                    return playerTurn
            else:
                playerScores[playerTurn] += score + currScore
                showScores()
                return playerTurn
        elif turn.upper() == 'A':
            showScores()
        elif turn.upper() == 'C':
            print(f"Your current score is {score}, don't blow it")
        elif turn.upper() == 'Q':
            sys.exit()
        else:
            print('Enter a valid move. ("S", "K", "R", "D", "C", "Q")')
            continue

# Choose the number of players and load a score card in playerScores.
def numPlayers() -> int:
    while True:  
        players = input('How many people are playing? (1 - 10)')
        if players not in [str(i) for i in range(1, 11)]:
            print('Please enter a number between 1 and 10')
        else:
            return int(players)

# Print all player scores.
def showScores() -> None:
    for player, score in playerScores.items():
        print()
        print(f'Player {player} score is {score}')
        print()

# Print the current roll nicely.
def showDice(diceRoll: list, score: int, currScore: int) -> None:
    dice = {0: ['|         |','|         |','|         |'],
            1: ['|         |','|    0    |','|         |'],
            2: ['|         |','| 0     0 |','|         |'],
            3: ['| 0       |','|    0    |','|       0 |'],
            4: ['| 0     0 |','|         |','| 0     0 |'],
            5: ['| 0     0 |','|    0    |','| 0     0 |'],
            6: ['| 0     0 |','| 0     0 |','| 0     0 |']}
    if not diceRoll:
        print("You haven't rolled the dice yet.")
        return
    print(f'    Die 1  \t  Die 2    \t   Die 3   \t   Die 4   \t   Die 5')
    print(f'-----------\t-----------\t-----------\t-----------\t-----------')
    print(f'{dice[diceRoll[0]][0]}\t{dice[diceRoll[1]][0]}\t{dice[diceRoll[2]][0]}\t{dice[diceRoll[3]][0]}\t{dice[diceRoll[4]][0]}')
    print(f'{dice[diceRoll[0]][1]}\t{dice[diceRoll[1]][1]}\t{dice[diceRoll[2]][1]}\t{dice[diceRoll[3]][1]}\t{dice[diceRoll[4]][1]}')
    print(f'{dice[diceRoll[0]][2]}\t{dice[diceRoll[1]][2]}\t{dice[diceRoll[2]][2]}\t{dice[diceRoll[3]][2]}\t{dice[diceRoll[4]][2]}')
    print(f'-----------\t-----------\t-----------\t-----------\t-----------')

    print(f'\nYour current score is {currScore + score}')

# Calculate a score from the current roll.
def checkScore(diceRoll: list) -> int:
    scoreCheck = 0
    if 1 in diceRoll:
        if diceRoll.count(1) >= 3:
            scoreCheck += 1000 + ((diceRoll.count(1) - 3) * 100)
        if diceRoll.count(1) < 3:
            scoreCheck += 100 * diceRoll.count(1)
    if 2 in diceRoll:
        if diceRoll.count(2) >= 3:
            scoreCheck += 200
    if 3 in diceRoll:
        if diceRoll.count(3) >= 3:
            scoreCheck += 300
    if 4 in diceRoll:
        if diceRoll.count(4) >= 3:
            scoreCheck += 400
    if 5 in diceRoll:
        if diceRoll.count(5) >= 3:
            scoreCheck += 500 + ((diceRoll.count(5) - 3) * 50)
        if diceRoll.count(5) < 3:
            scoreCheck += 50 * diceRoll.count(5)
    if 6 in diceRoll:
        if diceRoll.count(6) >= 3:
            scoreCheck += 600
    return scoreCheck

# Check playerScores for a winner.
def checkWin(playerTurn: int, playerScores: dict, players: int) -> bool:
    for i in range(1, players + 1):
        if playerScores[i] >= 5000:
            print(f'Player {playerTurn} has reached 5,000 points! The other players get one more turn to earn the highest score.')
            return False
    return True

# Save selected dice from the roll. Check if they are good to save.
# Return 5 dice with 0's as placeholders for dice not saved.
def saveDice(keepDice: list, diceRoll: list) -> list:
    toSave = []
    for i in keepDice:
        toSave.append(diceRoll[int(i) - 1])
    if checkScore(toSave) == 0:
        print('You cannot save this combination of dice because they have no scoring counters.')
        return diceRoll
    for i in range(5 - len(toSave)):
        toSave.append(0)
    return toSave

# Roll and return 5 dice. If dice were saved, move them to the front of the roll and roll the remaining of 5 dice.    
def rollDice(numDice: int, keptDice=[]) -> list:
    diceRoll = []
    if numDice == 5:
        for i in range(5):
            roll = random.randint(1, 6)
            diceRoll.append(roll)
    else:
        diceRoll = keptDice
        for i in range(5 - len(diceRoll)):
            roll = random.randint(1, 6)
            diceRoll.append(roll)
    return diceRoll

# Globals
running = True
players = numPlayers() # Select number of players.
playerScores = {(i + 1): 0 for i in range(players)} # Dictionary of Players (1 - x) and scores initialized at 0.
playerTurn = 1 # Player 1 starts the game.

# Game loop. Run a player's turn and exit the loop if a player has won.
while running:
    playerTurn = rollLoop(playerTurn)
    running = checkWin(playerTurn, playerScores, players)
    if playerTurn < players:
        playerTurn += 1
    else:
        playerTurn = 1

# Someone has won, give every other player one more turn.
if playerTurn != 1:
    playerTurn -= 1
else:
    playerTurn = players
for i in range(1, players + 1):
    if i != playerTurn:
        rollLoop(i)

# Winner is whoever has the highest score after the last extra turn.
print(f'Player {max(playerScores, key=playerScores.get)} has won the game!')