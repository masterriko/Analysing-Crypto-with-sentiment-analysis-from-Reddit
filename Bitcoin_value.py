from csv import reader
import pandas as pd

with open("BTCUSDT_HourlyBars.csv", "r", encoding="utf-8") as read_obj:
    """Writes Bitcoin hourly price change percentage to a new file """
    csv_reader = reader(read_obj, delimiter=';' )
    header = next(csv_reader)
    for row in csv_reader:
        difference = float(row[4]) - float(row[1]) * 0.00000001
        difference_Percentage = round(difference/float(row[1]) * 100 - 100, 5) #glede na open kolk je zrastlo, padlo
        df = pd.DataFrame({"Time":[row[0]], "difference":[difference], "differencePercentage":[difference_Percentage]}, columns=["Time", "difference", "differencePercentage"])
        df.to_csv("Percentage.csv", mode = "a", sep =";", index=False, header = False)
    
print("finished!")
