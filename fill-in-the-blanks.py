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
    """
    Returns the difficulty level chosen by the User.

    Inputs: none.
    Outputs: level (string) - the difficulty level chosen by the User.
    """

    level = "None"

    while level == "None":

        level = raw_input("\nPlease select a difficulty level (easy, medium, hard): ")
        level = level.replace(" ", "") # remove any whitespace
        level = level.lower() # lower the case

        if level in ("easy", "medium", "hard"):
            print "You've chosen " + level + "! Good luck!"
            return level
        else:
            print "Opps! Try again..."
            level = "None"


# Prompts the User to provide the number of guesses allowed during the game.
def get_guesses():
    """
    Return the number of guesses, as a positive integer, that the User
    has selected.

    Inputs: none.
    Outputs: guesses (int) - number of guesses chosen by the User.
    """

    guesses = ""

    while type(guesses) != int:

        print "\nHow many guesses you would like per blank word?"

        try:
            guesses = int(raw_input("Please enter a positive integer: "))

            if not (guesses >= 1): # if not int and positive
                raise ValueError()
        except ValueError:
            print "Opps! Try again..."
            guesses = ""
        else:
            print "Wow! You will have " + str(guesses) + " guesses per blank word.\n"
            return guesses


# Prompts the User to provide the answer for the numbered blank word.
def get_answer(blankNum):
    """
    Return a word that represents the User's guess at the numbered
    blank word.

    Inputs: blankNum (int) - index relating to current answer in question.
    Outputs: answer (string) - The User's current guess.
    """

    blankNum += 1 # Otherwise we start at zero instead of 1

    answer = raw_input("\nPlease enter your answer for ___" + str(blankNum) + "___? ")
    answer = answer.replace(" ", "") # Remove any whitespace

    return answer


# Set the correct quiz content based on the User's input
def set_content(difficulty):
    """
    Returns correct quiz content and answers based on the User's prior
    input of difficulty level.

    Inputs: difficulty (string) - one of three difficulty levels selected by
    the User.
    Outputs: content (string) - paragraph with fill-in-the-blank answers
    based on the difficulty level. answers (list, string) - the correct
    answers to the content string.
    """

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
    """
    Returns True if the User's answer matches the correct answer.
    Otherwise, it returns False.

    Inputs: answer (string) - the User's current guess.
    answers (list, strings) - list of correct answers. answerCount (int) -
    index of the current correct answer.
    Outputs: True or False
    """

    if answer == answers[answerCount]:
        return True
    else:
        return False


def replace_blanks(answerCount, answer, guessesCount, content):
    """
    Replaces the numbered blanks in the quiz paragraph with the correct
    answer given by the User.

    Inputs: answerCount (int) - the answer number we are currently working on.
    answer (string) -  The Users correct answer. guessesCount (int) - The
    number of guesses made by the User. content (string) - The quiz paragraph.
    Outputs: The modified answerCount, guessesCount and the content.
    """
    print "Whoop! Correct!\n"

    # Replace the blank(s) with the correct answer
    numberBlank = "___" + str(answerCount + 1) + "___"
    content = content.replace(numberBlank, answer)

    # Clean up our variables
    answerCount += 1
    guessesCount = 0

    return answerCount, guessesCount, content


def wrong_answer(guessesCount, guesses):
    """
    Notifies the User of a wrong guess and increments the guessesCount.

    Inputs: guessesCount (int) - the current number of guessess. guessess
    (int) - the max allowed guesses as configured by the User during game
    setup.
    Outputs: guessesCount (int)
    """

    print "\nYikes! That answer is incorrect!"
    guessesCount += 1
    print "You have " + str(guesses - guessesCount) + " left! Try again...\n"

    return guessesCount


def win_or_lose(guessesCount, guesses):
    """
    Prints either a winning or losing message based on the inputs of
    guessesCount and guesses.

    Inputs: guessesCount (int) - the current number of guesses the User is on.
    guesses (int) - the max number of guesses configured during game setup.
    Outputs: none.
    """

    if guessesCount < guesses:
        print "\n\nWinner, winner! Chicken dinner!"
    else:
        print "\n\nAh, too bad. Try harder!"

    print "Seacrest Out!"


# Play the Fill-in-the-Blanks Quiz game
def play_game():
    """
    Plays the Fill-in-the-Blanks Quiz game. This function calls all the
    necessary 'helper' functions to setup and play the game. This function
    does not return a value.
    """

    answerCount, guessesCount = 0, 0
    # Get the desired difficulty level from the User
    difficulty = get_difficulty()
    # Get the desired number of guesses per blank word from the User
    guesses = get_guesses()
    # Set the content based on the User's selected difficulty
    content, answers = set_content(difficulty)

    # While we haven't run out of guesses or answers
    while (guessesCount < guesses) and (answerCount < len(answers)):

        print content
        # Get the answer from the User for the blank number defined by answerCount
        answer = get_answer(answerCount)
        # Check if the answer entered is correct
        isCorrect = check_answer(answer, answers, answerCount)

        if isCorrect: # correct answer?
            # Replace the numbered blank with the correct answer
            answerCount, guessesCount, content = replace_blanks(answerCount, answer, guessesCount, content)
        else:
            # Increment the guessesCount and notify the User of a wrong guess
            guessesCount = wrong_answer(guessesCount, guesses)

    # Print the final content
    print content
    # Do we have a winner or a loser?
    win_or_lose(guessesCount, guesses)

# Play ball!
play_game()
