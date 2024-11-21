import getDates
import re
class parseTest:
    # Regex pattern to match a date range, like "11-21"
    pattern = r"\d{1,2}-\d{1,2}"
    possibleTitle = ["Test","Examen","Quiz"]
    months = [
    "janvier",
    "février",
    "mars",
    "avril",
    "mai",
    "juin",
    "juillet",
    "août",
    "septembre",
    "octobre",
    "novembre",
    "décembre"
]
    title = []
    dates = []
    obj = getDates.getTestDate
    line = []
    ClassTitle = ''
    def get(path):
        parseTest.obj.readPdf(path)
        parseTest.line = parseTest.obj.line
        parseTest.split()
        parseTest.removeEmptyOrUnSpecifiedDate()
        parseTest.ChangeToGoogleTime()
    def split():
        for i in parseTest.line:
            result = i.split()
            parseTest.getTitle(result)
            parseTest.getDate(result)
    def getTitle(result):
        for i in range(len(result) - 1):  # Loop until second-to-last element
            if result[i] in parseTest.possibleTitle:  # If current word is in possible titles
                title = result[i]  # Start with the matching word
                title += ' ' + result[i + 1]  # Add the next word to form the title
                parseTest.title.append(title)# Append the title to parseTest.title

    def getDate(result):
        for i in range(len(result) - 1):  # Loop until second-to-last element
            if result[i] in parseTest.months:  # If current word is a month
                title = result[i-1]  # places day
                title += ' ' + result[i]  # place month
                title += ' ' + result[i+1] #places year
                parseTest.dates.append(title)# Append the title to parseTest.title
    def removeEmptyOrUnSpecifiedDate():
        if len(parseTest.dates) > len(parseTest.title):
            parseTest.dates.pop()
        elif len(parseTest.dates) < len(parseTest.title):
            parseTest.title.pop()
        indices = []
    
        # Iterate through each string in the list
        for i, text in enumerate(parseTest.dates):
        # Find matches using regex
            if re.search(parseTest.pattern, text):  # If there's a match
                indices.append(i)  # Append the index where the match was found
        if len(indices) > 0:
            for i in indices:
                parseTest.dates.pop(i)
                parseTest.title.pop(i)
        
    def ChangeToGoogleTime(): #ex 2015-07-28
        for i in range(len(parseTest.dates)):
            tmp = parseTest.dates[i].split()
            print(tmp)
            

obj = parseTest
obj.get('plan-de-cours.pdf')
