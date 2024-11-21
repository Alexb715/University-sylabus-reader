import getDates
class parse:
    obj = getDates.getTestDate
    line = []
    def get(path):
        parse.obj.readPdf(path)
        parse.line = parse.obj.line
        print(parse.line)
obj = parse
parse.get('plan-de-cours.pdf')