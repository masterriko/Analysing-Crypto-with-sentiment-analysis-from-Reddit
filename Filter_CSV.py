with open("DataSet.csv","r", encoding="utf-8") as in_file, open("Final_data.csv","w", encoding="utf-8") as out_file:
    """Cleans duplicates from CSV file"""
    seen = set() # set for fast O(1) amortized lookup
    
    for line in in_file:
        if line in seen: 
          continue # skip duplicate

        seen.add(line)
        out_file.write(line)

print("Finished...")