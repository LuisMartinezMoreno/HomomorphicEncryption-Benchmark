def read_text_file(fileName):
    """
    Reads the content of a text file and returns a list of lines.

    Parameters:
    - fileName (str): The name of the text file (without the file extension).

    Returns:
    - list: A list of strings, where each string represents a line from the text file.

    Example:
    >>> read_text_file("example_file")
    """
    file_name = fileName + ".txt"
    try:
        with open(file_name, "r") as file:
            lines = file.readlines()
            return lines
    except FileNotFoundError:
        print(f"The file '{file_name}' was not found.")
        return []

def returnArchiveASCII(fileName):
    """
    Reads a text file and returns two lists: one with ASCII values of each character and one with characters.

    Parameters:
    - fileName (str): The name of the text file (without the file extension).

    Returns:
    - tuple: A tuple containing two lists - the first list contains ASCII values, and the second list contains characters.

    Example:
    >>> returnArchiveASCII("example_file")
    """
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
    """
    Converts a list of ASCII values back to a list of characters.

    Parameters:
    - result (list): A list of ASCII values.

    Returns:
    - list: A list of characters obtained by converting each ASCII value.

    Example:
    >>> retrieveValuesFromASCII([72, 101, 108, 108, 111])
    """
    deASCIIedResult = []
    for asciiValue in enumerate(result, 1):
        deASCIIedResult.append(chr(int(asciiValue[1])))
    return deASCIIedResult
