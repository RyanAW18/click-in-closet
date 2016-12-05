

def getCommonWords():

	commonWords = ['the', 'in', 'and', 'with', 'for', 'on', 'this', 'that', 'an', 'it', 'anything', 'to', 'a', 'its', 'these', 'give', 'gives', 
	'look', 'looks', 'like', 'of', 'any', 'but', 'where', 'when', 'wear', 'made', 'thanks', 'you', 'yours', 'your', 'is', 'as', 'just', 'from', 'our', 'at', 
	'there\'s', 'something', 'so', 'call', 'was', 'great', 'they', 'by', ]

	titleWords = []

	for word in commonWords:
		titleWords.append(word.title())

	commonWords = commonWords + titleWords

	return commonWords

