import csv
from StringIO import StringIO

def get_csv_header(data):
    sniffer = csv.Sniffer()
    dialect = sniffer.sniff(data)
    if not sniffer.has_header(data):
        # Header not found at first try, so let's just look at first line
        data = data.split("\n")[0]
    dialect = sniffer.sniff(data)
    reader = csv.reader(StringIO(data), dialect)
    return reader.next()

def get_csv_lines(data, header):
    snif = csv.Sniffer()
    dialect = snif.sniff(data)
    reader = csv.DictReader(StringIO(data),fieldnames=header,dialect=dialect)
    return list(reader)

if __name__ == "__main__":
    import os
    path = os.getcwd() + "/example/sample_csv.csv"
    data = open(path).read()
    header = get_csv_header(data)
    assert(header == ['Name', 'Surname', 'Email', 'Tel'])
    lines = get_csv_lines(data, header)
    assert(lines==[{'Tel': 'Tel', 'Surname': 'Surname', 'Name': 'Name', 'Email': 'Email'}, {None: [''], 'Tel': '48133205', 'Surname': 'Musizza', 'Name': 'Lorenzo', 'Email': 'info@1000asa.com'}, {None: [''], 'Tel': '48144205', 'Surname': 'Rizzatto', 'Name': 'Lorenzo', 'Email': 'sales@1000asa.com'}, {None: [''], 'Tel': '48132305', 'Surname': 'Santarelli', 'Name': 'Mirko', 'Email': 'info@1000asa.com'}])

    path = os.getcwd() + "/example/folders.csv"
    data = str(open(path).read())
    header = get_csv_header(data)
    assert(header == ['path', 'filename', 'id', 'title', 'description', 'content'])
    lines = get_csv_lines(data, header)
    assert(lines==[{'description': 'description', 'title': 'title', 'filename': 'filename', 'content': 'content', 'path': 'path', 'id': 'id'}, {'description': 'Desc', 'title': 'Theid', 'filename': 'rubrique_004.html', 'content': '<span><img alt="" border="0" height="281" src="travail.jpg" width="420"></span>', 'path': '/', 'id': 'theid'}])
