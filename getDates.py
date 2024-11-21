# Import necessary modules
from pypdf import PdfReader  # Library to handle reading PDF files
import datetime  # Module to work with date and time

# Define the getTestDate class that processes PDFs to extract test information (like date and title)
class getTestDate:
    # List of possible keywords representing types of tests or assessments
    days = ['Examen', 'Quiz', 'Test', 'Travail']
    
    # List to store the indices of lines that contain test-related dates
    indices = []
    
    # List to store the lines of text from the PDF
    line = []
    
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
    
    # Variable to store the class name (extracted from the PDF)
    ClassName = ''
    
    # Get the current year (used for extracting dates)
    current_year = datetime.datetime.now().year
    
    # Method to find all occurrences of a substring in a string, returning the indices
    def find_all(a_str, sub):
        start = 0
        while True:
            start = a_str.find(sub, start)  # Find the next occurrence of the substring
            if start == -1: return  # If no more occurrences are found, return
            yield start  # Yield the current index
            start += len(sub)  # Move to the next possible start position

    # Method to read and process the PDF file
    def readPdf(path):
        # Create a PdfReader object to read the provided PDF file
        reader = PdfReader(path)
        
        # Extract the text from the first page and split it into words
        page1 = reader.pages[0]
        page1 = page1.extract_text()
        Split1 = page1.split()
        
        # Extract the class name from the first page (using the findClassName method)
        getTestDate.ClassName = getTestDate.findClassName(Split1)
        
        # Loop through each page in the PDF to extract the relevant information
        for i in reader.pages:
            getTestDate.indices.clear()  # Clear previous indices before processing a new page
            page = i
            text = page.extract_text()  # Extract text from the current page
            
            # Look for each keyword (Examen, Quiz, Test, Travail) to find test references
            for i in getTestDate.days:
                indicetmp = list(getTestDate.find_all(text, i))  # Find all occurrences of the test type in the page text
                if len(indicetmp) > 0:
                    for i in indicetmp:
                        getTestDate.indices.append(i)  # Append each index where a test type is found
            
            # Call GetLine to process the lines that contain the indices
            getTestDate.GetLine(text)
    
    # Method to get the lines that contain the test type indices
    def GetLine(text):
        for i in getTestDate.indices:  # For each index where a test type is found
            start = text.rfind('\n', 0, i) + 1  # Find the start of the line
            end = text.find('\n', i)  # Find the end of the line
            if end == -1:  # If no newline is found, set the end to the end of the text
                end = len(text)
            getTestDate.line.append(text[start:end])  # Append the line containing the test type to the line list

    # Method to find the class name in a list of words (Split1 from the first page)
    def findClassName(text):
        for sigle in getTestDate.sigle:  # Loop through each possible course or test code
            for word in text:  # Loop through each word in the provided text
                if sigle in word:  # If the course code is found in the word
                    return word  # Return the matched word (class name)
        return None  # Return None if no class name is found
