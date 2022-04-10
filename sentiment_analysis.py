import pandas as pd
#import textblob
from csv import reader
import pandas
from flair.models import TextClassifier
from flair.data import Sentence
import regex as re
from segtok.segmenter import split_single


classifier = TextClassifier.load("sentiment-fast")

def clean(raw):
    """ Remove hyperlinks and markup """
    result = re.sub("<[a][^>]*>(.+?)</[a]>", "Link.", raw)
    result = re.sub('&gt;', "", result)
    result = re.sub('&#x27;', "'", result)
    result = re.sub('&quot;', '"', result)
    result = re.sub('&#x2F;', ' ', result)
    result = re.sub('<p>', ' ', result)
    result = re.sub('</i>', '', result)
    result = re.sub('&#62;', '', result)
    result = re.sub('<i>', ' ', result)
    result = re.sub("\n", '', result)
    return result
def make_sentences(text):
    """ Break apart text into a list of sentences """
    sentences = [sent for sent in split_single(text)]
    return sentences

def number(text):
        """Returns float from classifier"""
        text = Sentence(text)
        classifier.predict(text)
        for label in text.labels:
            if label.value == "POSITIVE":
                    number = float(label.score)
            elif label.value == "NEGATIVE":
                    number = - float(label.score)
            return number
print(number("sample"))

with open("Final_data.csv", "r", encoding="utf-8") as read_obj:
        """Takes selftext and title and writes their sentiment scores to a new file """
        csv_reader = reader(read_obj, delimiter=";" )
        for row in csv_reader:
            try:
                wordsClassifier = clean(row[1]) 
                sentences = []
                for _ in make_sentences(wordsClassifier):
                    sentences.append(number(_))
                row.append(sum(sentences)/len(sentences))
                sentences = []
                wordsClassifier = clean(row[3])
                for _ in make_sentences(wordsClassifier):
                    sentences.append(number(_))
                if sentences != [None]:
                    summation = 0
                    for _ in sentences:
                        if _ != None:
                            summation += _ 
                    row.append(summation/len(sentences))
                else:
                    row.append(None)
                df = pd.DataFrame({"Time":[row[0]], "Title":[row[1]], "Authors":[row[2]], "Text":[row[3]], "Flair": [row[4]], "Score": [row[5]], "Comments" : [row[6]], "ScoreTitle" : [row[7]], "ScoreSelfText" : [row[8]]}, columns=["Time", "Title", "Authors", "Text", "Flair", "Score", "Comments", "ScoreTitle", "ScoreSelfText"])
                df.to_csv("Sentiment.csv", mode = "a", sep =";", index=False, header=False)
            except:
                pass


