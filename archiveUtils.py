def read_text_file(fileName):
    file_name = fileName+".txt" 
    try:
        with open(file_name, "r") as file:
            lines = file.readlines()
            return lines
    except FileNotFoundError:
        print(f"The file '{file_name}' was not found.")
        return []

def returnArchiveASCII(fileName):
    lines = read_text_file(fileName)
    archiveASCII = []
    archive = []
    if lines:
        for i, line in enumerate(lines, 1):
            for char in line:
                unicodeValue = ord(char)
                archiveASCII.append(unicodeValue)
                archive.append(char)
    return archiveASCII, archive

def retrieveValuesFromASCII(result):
    deASCIIedResult = []
    for asciiValue in enumerate(result,1):
        deASCIIedResult.append(chr(int(asciiValue[1])))
    return deASCIIedResult