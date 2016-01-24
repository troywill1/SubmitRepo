# IPND Stage 2 Final Project

# For this project, you'll be building a Fill-in-the-Blanks quiz.
# Your quiz will prompt a user with a paragraph containing several blanks.
# The user should then be asked to fill in each blank appropriately to
# complete the paragraph.
# This can be used as a study tool to help you remember important vocabulary!

# Your game should consist of 3 or more levels, so you should add your own
# paragraphs as well!

# Credit to https://en.wikipedia.org/wiki/Mairzy_Doats and
# http://www.tutorialspoint.com/python/ for quiz content.

easyQuiz = """Python ___1___ do not need explicit declaration to reserve
memory space. The ___2___ happens automatically when you assign a value
to a variable. The ___3___ sign is used to assign values to varables. The
operand to the left of the = operator is the ___4___ of the variable and the
operand to the right of the = operator is the ___5___ stored in the variable."""

mediumQuiz = """Decision ___1___ is anticipation of conditions occurring during
execution of the program and specifying ___2___ taken according to the
conditions. Decision structures evaluate multiple expressions which produce
___3___ or ___4___ as outcome. You need to determine which action to take and
which statements to execute if outcome is ___3___ or ___4___ otherwise."""

hardQuiz = """Mairzy doats and dozy doats and liddle lamzy divey. A kiddley
divey too, Wooden shoe! If the words sound queer and funny to your ear, a little
bit jumbled and jivey, 'Sing ___1___ eat ___2___ and ___3___ eat ___2___ and
little ___4___ eat ___5___.''"""

easyAnswers = ["variables", "declaration", "equal", "name", "value"]
mediumAnswers = ["making", "actions", "TRUE", "FALSE"]
hardAnswers = ["mares", "oats", "does", "lambs", "ivy"]

# We've also given you a file called fill-in-the-blanks.pyc which is a working
# version of the project.
# A .pyc file is a Python file that has been translated into "byte code".
# This means the code will run the same as the original .py file, but when you
# open it
# it won't look like Python code! But you can run it just like a regular Python
# file to see how your code should behave.

# Hint: It might help to think about how this project relates to the Mad Libs
# generator you built with Sean. In the Mad Libs generator, you take a paragraph
# and replace all instances of NOUN and VERB. How can you adapt that design to
# work with numbered blanks?

# If you need help, you can sign up for a 1 on 1 coaching appointment:
# https://calendly.com/ipnd1-1/20min/

# Prompts the User to choose the difficulty level.
def get_difficulty():
    """Returns the difficulty level chosen by the User. The returned value
    will be 'easy', 'medium' or 'hard'"""

    level = "None"

    while level == "None":
        print # For readability

        level = raw_input("Please select a difficulty level (easy, medium, hard): ")
        level = level.replace(" ", "") # Remove any whitespace

        if level.lower() == "easy": # Ignore case
            print "You've chosen " + level + "! Good luck!"
            return "easy"
        elif level.lower() == "medium":
            print "You've chosen " + level + "! Good luck!"
            return "medium"
        elif level.lower() == "hard":
            print "You've chosen " + level + "! Good luck!"
            return "hard"
        else:
            print "Opps! Try again..."
            level = "None"


# Prompts the User to provide the number of guesses allowed during the game.
def get_guesses():
    """Return the number of guesses, as a positive integer, that the User
    has selected."""

    guesses = ""

    while type(guesses) != int:
        print # For readability

        print "How many guesses you would like per blank word?"

        try:
            guesses = int(raw_input("Please enter a positive integer: "))

            if not (guesses >= 1): # if not int and positive
                raise ValueError()
        except ValueError:
            print "Opps! Try again..."
            guesses = ""
        else:
            print "Wow! You will have " + str(guesses) + " guesses per blank word."
            print
            return guesses


# Prompts the User to provide the answer for the numbered blank word.
def get_answer(blankNum):
    """Return a word that represents the User's guess at the numbered
    blank word."""

    blankNum += 1 # Otherwise we start at zero instead of 1

    print # For readability

    answer = raw_input("Please enter your answer for __" + str(blankNum) + "__? ")
    answer = answer.replace(" ", "") # Remove any whitespace

    return answer


# Set the correct quiz content based on the User's input
def set_content(difficulty):
    """Returns correct quiz content and answers based on the User's prior
    input of difficulty level."""

    if difficulty == "easy":
        content = easyQuiz
        answers = easyAnswers
    elif difficulty == "medium":
        content = mediumQuiz
        answers = mediumAnswers
    else:
        content = hardQuiz
        answers = hardAnswers

    return content, answers


# Checks to see if the answer given by the User is correct.
def check_answer(answer, answers, answerCount):
    """Returns True if the User's answer matches the correct answer.
    Otherwise, it returns False"""

    print # For readability

    if answer == answers[answerCount]:
        return True
    else:
        return False


# Checks if a word in paragraph is a substring of the numberStr passed in.
def number_in_para(numberStr, paragraph):
    """Returns a 'paragraph blank with number' if a given 'numberStr' is a
    substring of paragraph. Otherwise, return 'None'."""

    numberStr = str(numberStr)

    for word in paragraph:
        if numberStr in word:
            return word
    return None


def replace_blanks(answerCount, answer, string_of_words):
    """Replaces the current numbered blank(s) with the given correct
    answer"""

    print # For readability

    replaced_string = []

    for word in string_of_words:
        result = number_in_para(answerCount + 1, string_of_words)

        if result != None:
            word = word.replace(result, answer) # This will keep punctuation
            replaced_string.append(word)
        else:
            replaced_string.append(word)

    return replaced_string


def win_or_lose(guessesCount, guesses):
    """Prints either a winning or losing message based on the inputs of
    guessesCount and guesses"""

    if guessesCount < guesses:
        print # For readability
        print
        print "Winner, winner! Chicken dinner!"
    else:
        print
        print
        print "Ah, too bad. Try harder!"

    print "Seacrest Out!"


# Play the Fill-in-the-Blanks Quiz game
def play_game():
    """Plays the Fill-in-the-Blanks Quiz game. This function does nothing
    return a value."""

    answerCount = 0
    guessesCount = 0
    guessesLeft = 0

    # Get the desired difficulty level from the User
    difficulty = get_difficulty()

    # Get the desired number of guesses per blank word from the User
    guesses = get_guesses()

    # Set the content based on the User's selected difficulty
    content, answers = set_content(difficulty)

    # Split content into list of words
    string_of_words = content.split()

    # While we haven't run out of guesses or answers
    while (guessesCount < guesses) and (answerCount < len(answers)):

        print content

        # Get the answer from the User for the blank number defined by answerCount
        answer = get_answer(answerCount)

        # Check if the answer entered is correct
        isCorrect = check_answer(answer, answers, answerCount)

        if isCorrect == True:
            print "Whoop! Correct!"
            print # For readability

            # Replace the blank(s) with the correct answer
            replaced_string = replace_blanks(answerCount, answer, string_of_words)

            # Join the list of words back to a string
            content = " ".join(replaced_string)
            # Split the content back into a list for the next answer
            string_of_words = content.split()
            # Clean up our variables
            answerCount += 1
            guessesCount = 0
            replaced_string = [] # Reset so we don't keep adding to the string

        else:
            print
            print "Yikes! That answer is incorrect!"
            guessesCount += 1
            guessesLeft = guesses - guessesCount
            print "You have " + str(guessesLeft) + " left! Try again..."
            print

    # Print the final content
    print content

    # Do we have a winner or a loser?
    win_or_lose(guessesCount, guesses)

# Play ball!
play_game()
