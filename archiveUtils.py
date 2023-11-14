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
    archive = []
    if lines:
        for i, line in enumerate(lines, 1):
            for char in line:
                unicodeValue = ord(char)
                archive.append(unicodeValue)
    return archive, lines

def retrieveValuesFromASCII(result):
    deASCIIedResult = []
    for asciiValue in enumerate(result,1):
        deASCIIedResult.append(chr(int(asciiValue[1])))
    return deASCIIedResult