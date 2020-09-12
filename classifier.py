import pandas as pd
import matplotlib.pyplot as plt


# -------------------------------------------------------------------------------------------------------------------
# We are creating a function called strip_punctuation, which takes one parameter, a string which represents a word
# and we will remove characters that are considered punctuation from everywhere in the word
# -------------------------------------------------------------------------------------------------------------------

def strip_punctuation(word, punctuation):
    aux_word = word
    for character in word:
        if character in punctuation:
            aux_word = aux_word.replace(character, "")

    return aux_word


# -------------------------------------------------------------------------------------------------------------------
# Takes three parameters, a string which represents one or more sentences, and calculates
# how many words in the string are considered positive words. The other parameter uses the list
# positive_words to determine what words will count as positive. The last parameter represents the punctuation chars
# The function should return a positive integer - how many occurrences there are of positive words in the text.
# Note that all of the words in positive_words are lower cased, so we convert all the words in the input string
# to lower case as well.
# -------------------------------------------------------------------------------------------------------------------

def get_pos(sentence, positive, punctuation):
    number_of_positive_words = 0
    sentence_lower = sentence.lower()
    for word in sentence_lower.split(" "):
        if strip_punctuation(word, punctuation) in positive:
            number_of_positive_words += 1

    return number_of_positive_words


# We are doing exactly the same but with negative words
def get_neg(sentence, negative, punctuation):
    number_of_negative_words = 0
    sentence_lower = sentence.lower()
    for word in sentence_lower.split(" "):
        if strip_punctuation(word, punctuation) in negative:
            number_of_negative_words += 1

    return number_of_negative_words


def list_of_positive_words(punctuation):
    positive = []
    with open("./files/positive_words.txt") as positive_file:
        for line in positive_file:
            # The file has a couple of ; at the beginning of the notes, we are counting how many
            # punctuation chars are there so we don't include the notes in our positive words list
            number_of_punctuation = 0
            for character in line:
                if character in punctuation:
                    number_of_punctuation += 1
            # We are asking if length of line is greater than 1 to not include blank spaces in our list
            if number_of_punctuation == 0 and len(line) > 1:
                positive.append(line.strip())
        return positive


def list_of_negative_words(punctuation):
    negative = []
    with open("./files/negative_words.txt") as negative_file:
        for line in negative_file:
            # The file has a couple of ; at the beginning of the notes, we are counting how many
            # punctuation chars are there so we don't include the notes in our positive words list
            number_of_punctuation = 0
            for character in line:
                if character in punctuation:
                    number_of_punctuation += 1
            # We are asking if length of line is greater than 1 to not include blank spaces in our list
            if number_of_punctuation == 0 and len(line) > 1:
                negative.append(line.strip())
        return negative


# -------------------------------------------------------------------------------------------------------------------
# Finally, we are opening project_twitter_data.csv which has the fake generated twitter data
# (the text of a tweet, the number of retweets of that tweet, and the number of replies to that tweet).
# This function, will detect how positive or negative each tweet is.
# Then, we will create a csv file called resulting_data.csv, which contains the
# Number of Retweets, Number of Replies, Positive Score (which is how many happy words are in the tweet),
# Negative Score (which is how many angry words are in the tweet), and the Net Score
# (how positive or negative the text is overall) for each tweet.
# -------------------------------------------------------------------------------------------------------------------

def analysis(punctuation, positive, negative):
    with open("./files/project_twitter_data.csv") as tweets:
        tweets_list = []
        headers = []
        for line in enumerate(tweets):
            if line[0] != 0:
                tweet = line[1].strip().split(",")
                # Condition to make sure to not append the blank lines
                if len(tweet) > 1:
                    tweet.append(str(get_pos(tweet[0], positive, punctuation)))
                    tweet.append(str(get_neg(tweet[0], negative, punctuation)))
                    # Overall = Positive - Negative
                    tweet.append(str(int(tweet[-2]) - int(tweet[-1])))
                    tweet = tuple(tweet)
                    tweets_list.append(tweet)

    # Now that we have all we need we will write our new data in the other CSV file

    with open("./files/resulting_data.csv", "w") as result:
        result.write(
            "{}, {}, {}, {}, {}\n".format("Number of Retweets", "Number of Replies", "Positive Score", "Negative Score",
                                          "Net Score"))
        for tweet in tweets_list:
            result.write("{}, {}, {}, {}, {}\n".format(tweet[1], tweet[2], tweet[3], tweet[4], tweet[5]))


def plot():
    df = pd.read_csv("./files/resulting_data.csv", delimiter=",")
    df.columns = (df.columns.str.replace("^ ", "")).str.replace(" $", "")
    y = df['Number of Retweets']
    x = df['Net Score']
    plt.xlabel('Net Score')
    plt.ylabel('Number of Retweets')
    plt.scatter(x, y)
    plt.show()


punctuation_chars = ["'", '"', ",", "!", ":", ";", '#', '@']
positive_words = list_of_positive_words(punctuation_chars)
negative_words = list_of_negative_words(punctuation_chars)
analysis(punctuation_chars, positive_words, negative_words)
plot()
print("Program terminated")
