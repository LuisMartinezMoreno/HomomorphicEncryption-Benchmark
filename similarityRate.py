def checkSimilarity(message, decoded, threshold):
    realParts = [number.real for number in decoded]
    similarityRate = []
    for i in range(len(realParts)):
        if(message[i]!=0):
            similarity = abs(realParts[i]- message[i])
            similarityRate.append(similarity)
            if similarity > threshold:
                return("it is not similar")
    media =  sum(similarityRate) / len(similarityRate)
    return media
