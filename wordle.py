from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

from random import randint

colorama_init()

def getWord(wordList: str) -> str:
    """Opens a list of words then picks a random word and returns that word"""
    with open(wordList, 'r') as file:
        words = eval(file.readline())

    randomWord = words[randint(0, len(words) - 1)].strip().lower()

    return randomWord

def guess(playerGuess: str, guessWord, individualWords, livesRemaining, validWords=None):
    while True:
        if len(playerGuess) == 5 and playerGuess in validWords: break
        if len(playerGuess) != 5:
            playerGuess = input("You need to submit a five letter guess: ").lower()
        if playerGuess not in validWords:
            playerGuess = input("Word not in word list. Please submit another word: ").lower()

    individualWords.append(colors(guessWord, playerGuess))

    display(individualWords, guessedWords)

    if playerGuess == guessWord:
        print(f"You Win! The word was {Fore.GREEN}{guessWord}{Style.RESET_ALL}!")
        input("Press enter to close")
        exit(0)
    if livesRemaining <= 1:
        print(f"You lose! The word was {Fore.LIGHTYELLOW_EX}{guessWord}{Style.RESET_ALL}")
        input("Press enter to close")
        exit(0)

    guess(input("\nFive letter guess: "), guessWord, individualWords, livesRemaining - 1, validWords=validWords)

def colors(guessWord, playerguess):
    # I have to implement a stupid stupid stupid counter for the letters: Tried didn't work
    # Word:  glows
    # Guess: masse
    # Problem: each s will be yellow even though only one of them should be
    wordguesses = [['', False], ['', False], ['', False], ['', False], ['', False]]

    lettersInWord = countLetters(guessWord)

    for x in enumerate(guessWord):
        good = wordguesses[x[0]][1]
        if playerguess[x[0]] is x[1] and lettersInWord[playerguess[x[0]]] > 0 and not good:
            wordguesses[x[0]][0] = f'{Fore.GREEN}{playerguess[x[0]]}{Style.RESET_ALL}'
            wordguesses[x[0]][1] = True
            lettersInWord[playerguess[x[0]]] -= 1
            wordguesses[x[0]][1] = True

    for x in enumerate(guessWord):
        good = wordguesses[x[0]][1]
        if playerguess[x[0]] is x[1] and lettersInWord[playerguess[x[0]]] > 0 and not good:
            print(lettersInWord[x[1]] > 0)
            wordguesses[x[0]][0] = f'{Fore.GREEN}{playerguess[x[0]]}{Style.RESET_ALL}'
            wordguesses[x[0]][1] = True
            lettersInWord[playerguess[x[0]]] -= 1
        elif playerguess[x[0]] in guessWord and not good and lettersInWord[playerguess[x[0]]] > 0:
            wordguesses[x[0]][0] = f'{Fore.LIGHTYELLOW_EX}{playerguess[x[0]]}{Style.RESET_ALL}'
            wordguesses[x[0]][1] = True
            lettersInWord[playerguess[x[0]]] -= 1

    for x in enumerate(guessWord):
        good = wordguesses[x[0]][1]
        if playerguess[x[0]] in guessWord and not good and lettersInWord[playerguess[x[0]]] > 0:
            wordguesses[x[0]][0] = f'{Fore.LIGHTYELLOW_EX}{playerguess[x[0]]}{Style.RESET_ALL}'
            wordguesses[x[0]][1] = True

    for x in enumerate(guessWord):
        good = wordguesses[x[0]][1]
        if not good:
            wordguesses[x[0]][0] = f'{Fore.LIGHTBLACK_EX}{playerguess[x[0]]}{Style.RESET_ALL}'

    convertMe = []
    for x in enumerate(wordguesses):
        convertMe.append(x[1][0])

    return strArrayToText(convertMe)

def strArrayToText(array: list) -> str:
    """Converts the array of strings into one single string"""
    strWord = ''
    for i in range(len(array)):
        strWord += array[i]
    return strWord

def display(individualWords, guessedWords):
    individualWordsStr = strArrayToText(individualWords)
    guessedWords.append(individualWordsStr)
    individualWords.clear()

    for x in enumerate(guessedWords):
        print(guessedWords[x[0]])

def getValidWords(textFile) -> list:
    with open(textFile) as file:
        validWords = eval(file.readline())
    return validWords

def countLetters(word: str) -> dict:
    counter = {}
    for i in word:
        if i not in counter.keys():
            counter.update({i: 0})
        counter[i] += 1
    return counter

def countBooleans(wordguesses):
    counter = {}
    for i in wordguesses:
        if i[1] not in counter.keys():
            counter.update({i[1]: 0})
        counter[i[1]] += 1
    return counter

if __name__ == "__main__":
    individualWords = []
    guessedWords = []

    validWords = getValidWords('wordleWords.txt')

    guessWord = getWord('wordleWords.txt').lower()

    guess(input('Five Letter Guess: ').lower(), guessWord, individualWords, 6, validWords=validWords)
