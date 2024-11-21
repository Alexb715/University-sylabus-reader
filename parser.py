# Import necessary modules
import getDates  # External module to handle PDF reading and date extraction
import re  # Regular expression module for pattern matching

# Define the parseTest class which handles parsing of test-related data
class parseTest:
    # List of possible course or test codes
    sigle = [
        'ACAD', 'ADCO', 'ADFI', 'ADFS', 'ADGO', 'ADMI', 'ADMK', 'ADMN', 'ADPU', 'ADRD', 
        'ADRH', 'ADSA', 'ADSF', 'ADSG', 'ADSI', 'ALLE', 'ANGL', 'ARDR', 'ARVI', 'ASTR', 
        'BADI', 'BICH', 'BIOL', 'BIOT', 'BTIL', 'CHIM', 'CRIM', 'DROI', 'ECON', 'EDAN', 
        'EDDP', 'EDDS', 'EDUC', 'EPAP', 'EPED', 'ESPA', 'ETEV', 'ETFA', 'FASS', 'FLSA', 
        'FORS', 'FRAN', 'FRLS', 'FSCI', 'GCIV', 'GEIN', 'GELE', 'GEOG', 'GERO', 'GGEN', 
        'GIZC', 'GLST', 'GMEC', 'HIST', 'ICOM', 'INFO', 'KNEP', 'LING', 'LITT', 'MATH', 
        'MUED', 'MULT', 'MUSI', 'NUAL', 'NUEF', 'ORCO', 'PHIL', 'PHYS', 'PSYC', 'RADI', 
        'RESN', 'SANT', 'SCPO', 'SCRE', 'SCSO', 'SENV', 'SINF', 'SOCI', 'STAT', 'SVIE', 
        'TLMD', 'TRAD', 'TRES', 'TSOC', 'TSTX'
    ]
    
    # Regular expression pattern to match date range (e.g., "11-21")
    pattern = r"\d{1,2}-\d{1,2}"
    
    # List of possible titles for tests
    possibleTitle = ["Test", "Examen", "Quiz", "Travail"]
    
    # List of months in French
    months = [
        "janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", 
        "septembre", "octobre", "novembre", "décembre"
    ]
    
    # Class-level variables to store parsed data
    title = []  # List to store titles of tests
    dates = []  # List to store dates associated with the tests
    obj = getDates.getTestDate  # Object for reading the PDF and getting data
    line = []  # List to store lines from the parsed document
    className = ''  # Variable to store class name (extracted from PDF)
    
    # Main method to process the PDF and extract data
    def get(path):
        parseTest.obj.readPdf(path)  # Read the PDF using the getDates module
        parseTest.line = parseTest.obj.line  # Assign lines from the PDF to parseTest.line
        parseTest.className = parseTest.obj.ClassName  # Get the class name from the object
        parseTest.split()  # Split the lines into words and parse the test titles and dates
        parseTest.addClassNameToTitle()  # Add the class name to each test title
        parseTest.removeEmptyOrUnSpecifiedDate()  # Remove invalid or unspecified dates
        parseTest.ChangeToGoogleTime()  # Format dates into Google Calendar format
        
    # Method to split lines into individual words and extract titles and dates
    def split():
        for i in parseTest.line:
            result = i.split()  # Split each line into words
            parseTest.getTitle(result)  # Extract the title from the words
            parseTest.getDate(result)  # Extract the date from the words
            
    # Method to extract the title from a list of words
    def getTitle(result):
        for i in range(len(result) - 1):  # Loop until second-to-last element to avoid index error
            if result[i] in parseTest.possibleTitle:  # If the current word is a possible title
                title = result[i]  # Start the title with the matched word
                title += ' ' + result[i + 1]  # Add the next word to complete the title
                parseTest.title.append(title)  # Append the full title to the title list
                
    # Method to extract the date from a list of words
    def getDate(result):
        for i in range(len(result) - 1):  # Loop until second-to-last element to avoid index error
            if result[i] in parseTest.months:  # If the current word is a month
                title = result[i-1]  # The day is one word before the month
                title += ' ' + result[i]  # Add the month to the title
                title += ' ' + str(parseTest.obj.current_year)  # Add the current year
                parseTest.dates.append(title)  # Append the full date to the dates list
               
    # Method to remove empty or unspecified dates
    def removeEmptyOrUnSpecifiedDate():
       
        # If there are more dates than titles, remove the last date
        if len(parseTest.dates) > len(parseTest.title):
            parseTest.dates.pop()
        # If there are more titles than dates, remove the last title
        elif len(parseTest.dates) < len(parseTest.title):
            parseTest.title.pop()
        
        # List to store the indices of dates that match the regex pattern
        indices = []
    
        # Iterate through each date to find valid ones
        for i, text in enumerate(parseTest.dates):
            if re.search(parseTest.pattern, text):  # If there's a match for the date pattern
                indices.append(i)  # Append the index where the match was found
        
        # If there are any matched dates, remove the invalid ones
        if len(indices) > 0:
            for i in indices:
                parseTest.dates.pop(i)  # Remove the invalid date
                parseTest.title.pop(i)  # Remove the corresponding title
        
    # Method to change date format to Google Calendar style (YYYY-MM-DD)
    def ChangeToGoogleTime():
        for i in range(len(parseTest.dates)):
            tmp = parseTest.dates[i].split()  # Split the date into day, month, and year
            # Convert month name to month number
            date = tmp[0] + '-' + str(parseTest.months.index(tmp[1]) + 1) + '-' + tmp[2]
            parseTest.dates[i] = date  # Update the date to the new format
    
    # Method to add class name to each test title
    def addClassNameToTitle():
        for i in range(len(parseTest.title)):
            parseTest.title[i] = parseTest.title[i] + ' ' + parseTest.className  # Append class name to title
