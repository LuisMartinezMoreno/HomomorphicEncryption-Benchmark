def checkSimilarity(message, decoded, threshold):
    """
    Checks the similarity between the original message and the decoded message.

    Parameters:
    - message (list or array): The original message, represented as a list of numbers.
    - decoded (list or array): The decoded message, represented as a list of complex numbers.
    - threshold (float): The threshold value for considering two elements as similar.

    Returns:
    - str or float: If the similarity between corresponding elements exceeds the threshold, returns "it is not similar".
                   Otherwise, returns the average similarity rate.

    Example:
    >>> checkSimilarity([1, 2, 3], [1.1+0.2j, 2.1-0.1j, 2.9+0.05j], 0.2)
    """
    # Extract the real parts of the decoded message
    realParts = [number.real for number in decoded]

    # Calculate the similarity rate for each element
    similarityRate = []
    for i in range(len(realParts)):
        if message[i] != 0:
            similarity = abs(realParts[i] - message[i])
            similarityRate.append(similarity)
            
            # Check if the similarity exceeds the threshold
            if similarity > threshold:
                return "it is not similar"

    # Calculate the average similarity rate
    average_similarity = sum(similarityRate) / len(similarityRate)

    return average_similarity
