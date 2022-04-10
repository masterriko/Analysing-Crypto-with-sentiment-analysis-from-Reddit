from csv import reader
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

post_time= []
post_score_title = []
post_score_text = []
bitcoin_time = [] 
bitcoin_price_change = [] 
post_author = []
good_prediction = {}
bad_prediction = {}
storage = int(input("How much data do you need: "))
begin = int(input("Where would you like to start: "))
columns = {"Authors" : 2, "Flair" : 4,"Score": 5, "Comments": 6, "ScoreTitle" : 7, "ScoreSelfText" : 8, "None" : 1}

print()
print("Filter data by(Authors, Flair, Score, Comments, ScoreTitle, ScoreSelfText)")
print("Choose None if you wouldn't like to apply any filters...")

while True:
    parameter = input("input: ")
    if parameter not in columns.keys():
        print("Check your spelling...")
        continue
    print()
    if parameter == "None":
        break
    if parameter in ["Score", "Comments", "ScoreTitle", "ScoreSelfText"]:
        try:
            value = float(input("Choose your value: "))  
        except:
            print("Please choose a number not...")
            print("Restarting...")
            print()
        
    else:
        value = input("Choose your value: ")
    break
        
        
with open("SentimentReversed.csv", mode = "r", encoding = "utf-8") as file:
    csv_reader = reader(file, delimiter = ";")
    data1 = list(csv_reader)

for i, d in enumerate(data1):
    try:
        if i > begin:
                if parameter == "None":
                    if d[0][:-2].isdigit():
                        post_time.append(int(d[0][:-2]))
                        post_score_title.append(float(d[7]))
                        post_score_text.append(float(d[8]) if len(d[8]) != 0 else None)
                        post_author.append(d[2])
                else:
                    if parameter in ["Score", "Comments", "ScoreTitle", "ScoreSelfText"]:
                        if float(d[columns[parameter]]) > value:
                            if d[0][:-2].isdigit():
                                post_time.append(int(d[0][:-2]))
                                post_score_title.append(float(d[7]))
                                post_score_text.append(float(d[8]) if len(d[8]) != 0 else None)
                                post_author.append(d[2])


                    elif d[columns[parameter]] == value:
                            if d[0][:-2].isdigit():
                                post_time.append(int(d[0][:-2]))
                                post_score_title.append(float(d[7]))
                                post_score_text.append(float(d[8]) if len(d[8]) != 0 else None)
                                post_author.append(d[2])
    except:
        continue
    if i > storage:
        break

with open("Percentage.csv", mode = "r", encoding = "utf-8") as file:
    csv_reader = reader(file, delimiter = ";")
    data2 = list(csv_reader)

for i, d in enumerate(data2):
    bitcoin_time.append(int(d[0]) // 1000)
    bitcoin_price_change.append(float(d[2]))
    if i > storage:
        break
    
def group_title_and_text(title, text):
    """groups title and text score of sentiment analysis and returns a new list.
    If text is deleted by moderator or there is no text than it will only compute title sentiment score"""
    new_flair_analysis = []
    for ti, te in zip(title, text):
        if te == None or te == -0.8307421803474426:
            new_flair_analysis.append(ti)
        else:
            new_flair_analysis.append((ti + te)/2)
    return new_flair_analysis

def group_data_by_hour(data_flair, time_flair , time_btc):
    """groups posts sentiment analysis by hour and gets an average"""
    a = []
    res = []
    for b in time_btc:
        for t, d in zip(time_flair, data_flair):
            if b - 3600 < t < b:
                a.append(d)
        res.append(sum(a) / len(a) if len(a) != 0 else 0)
        a = []
    return res

def number_of_predictions(data):
    """computes how many predictions were made"""
    i = 0
    for d in data:
        if d != 0:
            i += 1
    return i

def accuracy(data, price_change):
    """gets all the score from post by hour and compares it to actual price. The return value
    is a list of good and bad predictions and an accuracy score."""
    j = 0
    a = []
    for d, p in zip(data, price_change):
        if d != 0:
            if d > 0:
                if p < 0:
                    a.append("Bad")
                else:
                    a.append("Good")
                    j += 1
            else:
                if p < 0:
                    a.append("Good")
                    j += 1
                else:
                    a.append("Bad")
        else:
            a.append(None)
    return round(j / number_of_predictions(data) * 100 if number_of_predictions(data) != 0 else 0, 2), a, j


    

post_score = group_title_and_text(post_score_title, post_score_text)
hourly = group_data_by_hour(post_score, post_time, bitcoin_time)

for x, y,z,h in zip(accuracy(hourly, bitcoin_price_change)[1], bitcoin_time,hourly, bitcoin_price_change):
    print("Prediction:",x,"---Time",  y, "Score: ", z, "Bitcoin price change:", h)
    
print("Accuracy: ", accuracy(hourly, bitcoin_price_change)[0], "%")
print("Number of predictions:", number_of_predictions(hourly))

hourly_score = group_data_by_hour(post_score, post_time, bitcoin_time)
author_time_score = list(zip(post_author , post_time, post_score))
for au, ti, sc in author_time_score: #Creates two dictionaries on how many bad and good predictions authors make.
    for btct, pr in zip(bitcoin_time, bitcoin_price_change): 
        if btct - 3600 < ti < btct:
            if len(au) != 0:
                if pr > 0 and sc > 0:
                    if au not in good_prediction.keys():
                        good_prediction[au] = 1
                    else:
                        good_prediction[au] += 1
                elif pr < 0 and sc < 0:
                    if au not in good_prediction.keys():
                        good_prediction[au] = 1
                    else:
                        good_prediction[au] += 1
                elif pr == 0 and sc == 0:
                    continue
                else:
                    if au not in bad_prediction.keys():
                        bad_prediction[au] = 1
                    else:
                        bad_prediction[au] += 1

for x in good_prediction.keys(): #checks if there is no bad prediction
    if bad_prediction.get(x) == None:
        bad_prediction[x] = 1
        
#We find five authors with the most good predictions
best_five_keys = sorted(good_prediction, key=lambda x: good_prediction[x], reverse=True)[0:5]

best_five_values = [good_prediction[x] for x in best_five_keys]

plt.bar(best_five_keys, best_five_values, color ="red")
plt.xticks(
rotation=45, 
horizontalalignment="right",
fontweight="light",
fontsize="x-large"
)
 
# x-axis label
plt.xlabel("Authors")
# frequency label
plt.ylabel("Nummber of accurate sentiment positive posts")
# plot title
plt.title("Graph accurate-posts/best-authors")
# function to show the plot
plt.show()

summation_good_predictions = sum(good_prediction.values()) #we use percentage of good predictions as a coefficient for accuracy of an author
best_five_keys_percentage = sorted(good_prediction, key=lambda x: good_prediction[x]/(bad_prediction[x] + good_prediction[x]) * good_prediction[x]/summation_good_predictions, reverse=True)[0:5]
best_five_values_percentage_relative_to_all = [good_prediction[x]/(bad_prediction[x] + good_prediction[x]) * good_prediction[x]/summation_good_predictions for x in best_five_keys_percentage]
best_five_values_percentage = [good_prediction[x]/(bad_prediction[x] + good_prediction[x]) for x in best_five_keys_percentage]

#We make a graph with two y axis. One representing accuracy with coefficient and the other representing accuracy 
fig = plt.figure(figsize=(10,5)) 
ax = fig.add_subplot(111) 
ax2 = ax.twinx() 
ax.set_xticklabels(ax.get_xticklabels(),rotation=45) # Rotation 45 degrees
width = 0.1
ind = np.arange(len(best_five_keys_percentage))
ax.set_ylabel("Sentiment percentage without coef")
ax2.set_ylabel("Sentiment percentage relative to all")
ax.set_xlabel("Authors")
ax.bar(ind, best_five_values_percentage, width, color="red", label="without coefficient")
ax2.bar(ind + 2 * width, best_five_values_percentage_relative_to_all, width, color="blue", label="relative to all")
ax.set(xticks=(ind + 1.5 * width), xticklabels=best_five_keys_percentage, xlim=[2 * width - 1, len(best_five_keys_percentage)])
ax.legend(["Without coefficient"], bbox_to_anchor=(1,1))
ax2.legend(["Relative to all coefficient"], bbox_to_anchor=(1,0.87))
plt.show()

tab1 = []
tab2 = []
hourly_data_price_accuracy = []

for h, b in zip(hourly, bitcoin_price_change):
    tab1.append(h)
    tab2.append(b)
    a = accuracy(tab1, tab2) 
    hourly_data_price_accuracy.append(a[0])

to_date = [datetime.utcfromtimestamp(x) for x in bitcoin_time]
plt.plot(to_date, hourly_data_price_accuracy, color ="blue")
plt.xticks(rotation=90, fontsize = "xx-small")
plt.show()







    
