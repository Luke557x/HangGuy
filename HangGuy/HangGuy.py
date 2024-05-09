
# HangGuy
# Luke Fleming

# This project was written in a day, is a bit under-commented. Just play the game, it's supposed to be fun.

import numpy as np
import random

# Constants (or game settings)
REMOVE_PROPER_NOUNS = True
REMOVE_HYPHENATED_WORDS = True
MAX_STRIKES = 7

print("Starting...")

with open('all-words.txt', 'r') as file:
    guessWords = [line.strip() for line in file]
guessWords = [line.strip() for line in guessWords if line.strip()]
# guessWords are the words that the bot will guess
print("Loaded words!")

# Optionally remove all proper nouns. There's a lot of odd ones in there, and they might be difficult to guess.
if REMOVE_PROPER_NOUNS:
    w = 0
    while w < len(guessWords):
        while guessWords[w].isupper() or str(guessWords[w][0]).isupper() and w < len(guessWords) - 1:
            guessWords = guessWords[:w] + guessWords[w + 1:]
        w += 1
    guessWords = guessWords[:len(guessWords) - 1]  # assumes the final word is uppercase
else:
    for i in range(0, len(guessWords)):
        guessWords[i] = guessWords[i].lower()

# doesn't remove the last word. Check all-words to make sure it's not hypenated.
if REMOVE_HYPHENATED_WORDS:
    w = 0
    while w < len(guessWords):
        while guessWords[w].find("-") != -1:
            guessWords = guessWords[:w] + guessWords[w + 1:]
        w += 1

running = True
while running:
    print("Welcome to Hang Guy!")
    print("What would you like to do? Please enter a single number as your response.")
    print("1: Guess the Computer's Word")
    print("2: Have the Computer guess your word")
    answ = str(input())
    while answ != str(1) and answ != str(2):
        print("Invalid Input! Please enter '1' or '2'")
        answ = str(input())
    if answ == str(1):
        print()
        print()

        guessedLetters = np.array([], dtype=str)
        wrongLetters = np.array([], dtype=str)
        wordToGuess = random.choice(guessWords)
        strikes = 0
        guessingWord = ""
        for x in range(0, len(wordToGuess)):
            guessingWord += "_ "

        win = False
        # Main Game Loop:
        while win is False and strikes < MAX_STRIKES:
            print(guessingWord)
            print(str(strikes) + " out of " + str(MAX_STRIKES))
            if strikes > 0:
                print(wrongLetters)

            print()
            print("Guess a letter.")
            # print("btw the word is " + wordToGuess)
            gLetter = input().lower()
            gussedLetters = np.append(guessedLetters, gLetter)
            print()
            if wordToGuess.find(gLetter) != -1 and len(gLetter) == 1:
                print("Nice!")
                for lnum in range(0, len(wordToGuess)):
                    if gLetter == wordToGuess[lnum]:
                        guessingWord = guessingWord[:lnum * 2] + gLetter + guessingWord[lnum * 2 + 1:]
            else:
                print("Not in the word.")
                wrongLetters = np.append(wrongLetters, gLetter)
                strikes += 1

            if guessingWord.find("_") == -1:
                win = True
                print("You won!")
                print("The word was " + wordToGuess)
        if not win:
            print("You Lost! ")
            print("The word was " + wordToGuess)
        print()
        print("Hit Enter to play again, or type 'STOP' to close the program.")
        if input() == "STOP":
            running = False
        print()

    else:
        print("To check if your word is considered a real word, please enter it now.")
        print("(This will have no impact on how the computer guesses, if you are")
        print("certain your word is real, just hit enter)")

        testWord = input().lower()

        if len(testWord) != 0:
            while guessWords.count(testWord.lower()) < 1:
                print("This word is not recognized. Please try a different one.")
                testWord = input().lower()
            print(testWord + " is recognized as a real word. Please hit enter")
            input()
        else:
            print("Okay.")
        print()

        print("How many letters is your word?")
        wordLength = int(input())

        possibleGuesses = np.array([], dtype=str)
        for word in guessWords:
            if len(word) == wordLength:
                possibleGuesses = np.append(possibleGuesses, word)

        alph = "ebcdafghijklmnopqrstuvwxyz"
        correct = ""
        incorrects = ""
        for i in range(0, wordLength):
            correct += "_"

        won = False

        strikes = 0

        while not won:

            inc = 0

            newGuessable = np.array([], dtype=str)
            for word in possibleGuesses:
                okayWord = True
                for letter in incorrects:
                    if word.count(letter) != 0:
                        okayWord = False
                if okayWord:
                    newGuessable = np.append(newGuessable, word)
            possibleGuesses = np.copy(newGuessable)

            # eliminating letters not present in possibleGuesses
            newAlph = ""
            for letter in alph:
                hasLetter = False
                for word in possibleGuesses:
                    if word.count(letter) != 0:
                        hasLetter = True
                        break
                if hasLetter:
                    newAlph += letter
            alph = newAlph

            # eliminating words where letters are out of place
            inc = 0
            for letter in correct:
                if letter != "_":
                    newGuessable = np.array([], dtype=str)
                    for word in possibleGuesses:
                        if word[inc] == letter:
                            newGuessable = np.append(newGuessable, word)
                    possibleGuesses = np.copy(newGuessable)
                inc += 1

            # re-eliminating letters not present in possibleGuesses
            newAlph = ""
            for letter in alph:
                hasLetter = False
                for word in possibleGuesses:
                    if word.count(letter) != 0:
                        hasLetter = True
                        break
                if hasLetter:
                    newAlph += letter
            alph = newAlph

            # organizing alphabet by frequency
            freq = np.zeros(len(alph))
            total = 0
            for word in possibleGuesses:
                for letter in word:
                    for x in range(0, len(alph)):
                        if letter == alph[x]:
                            freq[x] += 1
                            total += 1
                            break

            for i in range(0, len(freq) - 1):
                for j in range(i + 1, len(freq)):
                    if freq[j] > freq[i]:
                        temp = freq[j]
                        freq[j] = freq[i]
                        freq[i] = temp
                        temp2 = alph[j]
                        if j < len(alph) - 1:
                            alph = alph[:j] + alph[i] + alph[j + 1:]
                        else:
                            alph = alph[:j] + alph[i]
                        if i < len(alph) - 1:
                            alph = alph[:i] + temp2 + alph[i + 1:]
                        else:
                            alph = alph[:i] + temp2

            if len(possibleGuesses) == 1:
                print("CPU: I've got it! The word is '" + possibleGuesses[0] + "'")
                won = True
                break

            myChoice = alph[0]
            print("CPU: Is there a '" + myChoice + "'?")
            print("[Y/N]")
            answ = input()
            while answ.lower() != "y" and answ.lower() != "n":
                print("Please enter 'Y' or 'N'")
                answ = input()
            if answ.lower() == "y":
                print("CPU: Great! What position(s) is it in?")
                print("Please enter a list of numbers, separated by spaces")
                lPositions = input()
                lPositions = [int(x) - 1 for x in lPositions.split()]
                for num in lPositions:
                    if num + 1 == len(correct):
                        correct = correct[:num] + myChoice
                    else:
                        correct = correct[:num] + myChoice + correct[num + 1:]
            else:
                print("CPU: Thats too bad...")
                incorrects += myChoice
                strikes += 1
            cLoc = alph.find(myChoice)
            if cLoc == len(alph) - 1:
                alph = alph[:len(alph) - 1]
            else:
                alph = alph[:cLoc] + alph[cLoc + 1:]

            if correct.find("_") == -1:
                print("CPU: I've got it! The word is '" + correct + "'")
                won = True
            else:
                print("CPU: Here what I've got so far: " + correct)
        print()
        print("Guessed word with " + str(strikes) + " strikes")
