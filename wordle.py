import random

dictionary = []

try:
    with open('wordlist.txt') as f:
        for line in f:
            dictionary.append(line.strip())
except FileNotFoundError:
    print("file not found")

#eliminates words from the word bank given the result of a guess
def update_word_bank(possible_list, guess, result):
    temp_tuple = tuple(possible_list)
    for word in temp_tuple:
        for i in range(0, len(guess)):
            #letter is green but not in same place in word
            if result[i] == "g" and guess[i] != word[i]:
                possible_list.remove(word)
                break
            #letter is yellow but not in word at all
            elif result[i] == "y" and guess[i] not in word:
                possible_list.remove(word)
                break
            #letter is yellow but in same place
            elif result[i] == "y" and guess[i] == word[i]:
                possible_list.remove(word)
                break
            #letter is white but in word not as a repeat
            elif result[i] == "w" and guess[i] in word and guess.count(guess[i]) == 1:
                possible_list.remove(word)
                break
    return possible_list

#computes the result string given a guess and answer
def compute_result(guess, answer):
    res = ""
    for i in range(0, 5):
        if (guess[i] == answer[i]):
            res = res + "g"
        elif (guess[i] in answer):
            res = res + "y"
        else:
            res = res + "w"
    return res

#simulates a game of wordle with random guesses an returns the number of guesses needed
def sim_wordle(dictionary, initalguess = None):
    possible_list = dictionary.copy()
    answer = possible_list[random.randrange(0, len(possible_list))]
    for i in range(0, 6):
        if (i == 0 and initalguess != None):
            guess = initalguess
        else:
            guess = possible_list[random.randrange(0, len(possible_list))]
        result = compute_result(guess, answer)
        if (result == "ggggg"):
            return i+1
        else:
            possible_list = update_word_bank(possible_list, guess, result)
            if (len(possible_list) == 0):
                print("Error: word is not in dictionary")
                break
    return 7

#simulates a game of wordle with random guesses an returns the number of guesses needed
def sim_wordle_score(dictionary, initalguess = None):
    possible_list = dictionary.copy()
    answer = possible_list[random.randrange(0, len(possible_list))]
    for i in range(0, 6):
        if (i == 0 and initalguess != None):
            guess = initalguess
        else:
            guess = get_next_suggest(possible_list)
        result = compute_result(guess, answer)
        if (result == "ggggg"):
            return i+1
        else:
            possible_list = update_word_bank(possible_list, guess, result)
            if (len(possible_list) == 0):
                print("Error: word is not in dictionary")
                break
    return 7


#play a game of wordle manually
def play_wordle(dictionary):
    possible_list = dictionary.copy()
    for i in range(0, 6):
        print("Please enter your guess:")
        guess = input()
        print("Please enter your result as a 5-letter string (w for white tile, y for yellow tile, g for green tile):")
        result = input()
        if (result == "ggggg"):
            print("Good job on solving the wordle in", i + 1, "guesses!")
            exit()
        else:
            possible_list = update_word_bank(possible_list, guess, result)
            if (len(possible_list) == 0):
                print("Error: word is not in dictionary")
                break
            rand_num = random.randrange(0, len(possible_list))
            print("Suggested next guess is", possible_list[rand_num])
    print("We did not solve the wordle...")

#simulates 1000 games of wordle with no inital guess and prints average score
def average_random_guess_noinit():
    counter = 0
    counter_two = 0
    for i in range(0, 1000):
        num_guesses = sim_wordle(dictionary)
        counter += num_guesses
        if num_guesses != 7:
            counter_two +=1
    print("The average over 1000 wordle games was", counter / 1000, "guesses with success rate of", counter_two / 1000)

#simulates 1000 games of wordle with inital guess and prints average score
def average_random_guess_init(starting_word):
    counter = 0
    counter_two = 0
    for i in range(0, 1000):
        num_guesses = sim_wordle(dictionary, starting_word)
        counter += num_guesses
        if num_guesses != 7:
            counter_two +=1
    print("The average over 1000 wordle games with inital guess", starting_word, "was", counter / 1000, "guesses with success rate of", counter_two / 1000)

#simulates 1000 games of wordle with scoring system and inital guess and prints average score
def average_random_guess_init_score(starting_word):
    counter = 0
    counter_two = 0
    for i in range(0, 1000):
        num_guesses = sim_wordle_score(dictionary, starting_word)
        counter += num_guesses
        if num_guesses != 7:
            counter_two +=1
    print("The average over 1000 wordle games with inital guess", starting_word, "with score method was", counter / 1000, "guesses with success rate of", counter_two / 1000)

#get the next suggested word based on score
def get_next_suggest(possible_list):
    three_letters = "eariot"
    two_letters = "nslcudp"
    one_letters = "mhgbfywkvxzjq"
    scores = []
    for word in possible_list:
        score = 0
        for i in range(0, 5):
            if (word[i] in three_letters):
                score+=3
            elif(word[i] in two_letters):
                score+=2
            elif(word[i] in one_letters):
                score+=1
            else:
                print("Error: Letter not found")
                exit()
        score = len(set(word)) * score
        scores.append(score)
    max_score = max(scores)
    max_index = scores.index(max_score)
    return possible_list[max_index]

#play a game of wordle manually
def play_wordle_score(dictionary):
    possible_list = dictionary.copy()
    for i in range(0, 6):
        print("Please enter your guess:")
        guess = input()
        print("Please enter your result as a 5-letter string (w for white tile, y for yellow tile, g for green tile):")
        result = input()
        if (result == "ggggg"):
            print("Good job on solving the wordle in", i + 1, "guesses!")
            exit()
        else:
            possible_list = update_word_bank(possible_list, guess, result)
            if (len(possible_list) == 0):
                print("Error: word is not in dictionary")
                break
            next_guess = get_next_suggest(possible_list)
            print("Suggested next guess is", next_guess)
    print("We did not solve the wordle...")


#play_wordle(dictionary)
#average_random_guess_noinit()
#average_random_guess_init("crate")
#average_random_guess_init_score("crate")
#play_wordle_score(dictionary)


