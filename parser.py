import getDates
class parseTest:
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

obj = parseTest
obj.get('plan-de-cours.pdf')
print(obj.dates)
print(obj.title)

