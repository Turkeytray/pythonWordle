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

    letterIndex = 0
    for x in playerGuess:
        letterIndex += 1
        individualWords.append(colors(x, guessWord, letterIndex, playerGuess=playerGuess))

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

def colors(letter, guessWord, letterIndex, playerGuess=''):
    # I have to implement a stupid stupid stupid counter for the letters
    # Word:  glows
    # Guess: masse
    # Problem: each s will be yellow even though only one of them should be
    wordguesses = []
    lettersInWord = countLetters(guessWord)
    lettersInGuess = countLetters(playerGuess)
    print(lettersInGuess)
    if letter is guessWord[letterIndex - 1] and lettersInGuess[letter] > lettersInWord[letter]:
        tempVar = f'{Fore.GREEN}{letter}{Style.RESET_ALL}'
        wordguesses.append(tempVar)
        lettersInGuess[letter] -= 1
    elif letter in guessWord and lettersInGuess[letter] > 0:
        tempVar = f'{Fore.LIGHTYELLOW_EX}{letter}{Style.RESET_ALL}'
        wordguesses.append(tempVar)
        lettersInGuess[letter] -= 1
    else:
        tempVar = f'{Fore.LIGHTBLACK_EX}{letter}{Style.RESET_ALL}'
        wordguesses.append(tempVar)
    return strArrayToText(wordguesses)

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


if __name__ == "__main__":
    individualWords = []
    guessedWords = []

    validWords = getValidWords('wordleWords.txt')

    guessWord = getWord('wordleWords.txt').lower()

    print(guessWord)

    guess(input('Five Letter Guess: ').lower(), guessWord, individualWords, 6, validWords=validWords)
