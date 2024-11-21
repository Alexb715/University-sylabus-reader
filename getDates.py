from pypdf import PdfReader
class getTestDate:
    days = ['lundi','mardi','mercredi','jeudi','vendredi']
    indices = []
    line = []
    def find_all(a_str, sub):
        start = 0
        while True:
            start = a_str.find(sub, start)
            if start == -1: return
            yield start
            start += len(sub)
    def readPdf(path):
        reader = PdfReader(path)
        for i in reader.pages:
            getTestDate.indices.clear()
            page = i
            text = page.extract_text()
            for i in getTestDate.days:
                indicetmp = list(getTestDate.find_all(text,i))
                if(len(indicetmp) >0):
                    for i in indicetmp:
                        getTestDate.indices.append(i)
            
            getTestDate.GetLine(text)
            

    def GetLine(text):
        for i in getTestDate.indices:
            start = text.rfind('\n',0,i) + 1
            end = text.find('\n',i)
            if end == -1 :
                end = len(text)
            getTestDate.line.append(text[start:end])
