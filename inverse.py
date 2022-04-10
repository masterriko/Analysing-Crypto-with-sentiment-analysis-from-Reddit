import csv
import pandas as pd
with open("Sentiment.csv", "r", encoding="utf-8") as file:
    """Reverses rows in CSV file"""
    for row in reversed(list(csv.reader(file, delimiter = ";"))):
        df = pd.DataFrame({"Time":[row[0]], "Title":[row[1]], "Authors":[row[2]], "Text":[row[3]], "Flair": [row[4]], "Score": [row[5]], "Comments" : [row[6]], "OcenaNaslov" : [row[7]], "OcenaText" : [row[8]]}, columns=["Time", "Title", "Authors", "Text", "Flair", "Score", "Comments", "OcenaNaslov", "OcenaText"])
        df.to_csv("SentimentReversed.csv", mode = "a", sep =";", index=False, header=False)