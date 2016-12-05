import json

from pymongo import MongoClient
client = MongoClient('mongodb://trossi:1460@ds143707.mlab.com:43707/heroku_b37frt6h')
db = client.heroku_b37frt6h
productsMen = db.productsMen


def getRecommendations(prod, products, productsMen):
	print "getting recs for " + str(prod["_id"])

	recShirts = [None, None, None]
	recPants = [None, None, None]
	recOuter = [None, None, None]
	recShoes = [None, None, None]

	topShirtScores = [-1, -1, -1]
	topPantsScores = [-1, -1, -1]
	topOuterScores = [-1, -1, -1]
	topShoeScores = [-1, -1, -1]

	categMap = {u'Shirts' : [topShirtScores, recShirts], u'Pants & Shorts' : [topPantsScores, recPants], 
	u'Jackets, Sweaters, & Outerwear' : [topOuterScores, recOuter], u'Shoes & Other Footwear': [topShoeScores, recShoes]}


	keyTerms = prod["key terms"]

	i = 0
	while i < products.count():
		othProd = products[i]
		if str(prod["_id"]) != str(othProd["_id"]):
			othTerms = othProd["key terms"]
			score = getScore(keyTerms, othTerms, prod, othProd)
			category = othProd["category"]
			if category != u'Other' and category != u'Shirt':
				# if category == u'Shirt':
				# 	print prod
				recArrays = categMap[category]
				topScores = recArrays[0]
				recItems = recArrays[1]
				updateRecs(topScores, recItems, score, othProd, prod)
		i = i + 1

	key = {'description' : prod["description"]}
	productsMen.update_one(key, {'$set' : {u'rec shirts': recShirts, "rec pants": recPants, "rec outer": recOuter, "rec shoes": recShoes}})





def getScore(keyTerms, othTerms, prod, othProd):
	keyTermsLength = len(keyTerms)
	count = 0
	for term in othTerms:
		if term in keyTerms:
			count = count + 1

	numerator = float(count)
	denom = float(keyTermsLength)

	score = numerator / denom
	if prod["brand"] != othProd["brand"]:
		score = 1.1 * score
	
	return score

def updateRecs(topScores, recItems, score, othProd, prod):
	if str(prod["_id"]) == str(othProd["_id"]):
		return
	if score > topScores[0]:
		topScores[2] = topScores[1]
		topScores[1] = topScores[0]
		topScores[0] = score

		recItems[2] = recItems[1]
		recItems[1] = recItems[0]
		recItems[0] = str(othProd["_id"])

	elif score == topScores[0]:
		if prod["brand"] != othProd["brand"]:
			topScores[2] = topScores[1]
			topScores[1] = topScores[0]
			topScores[0] = score

			recItems[2] = recItems[1]
			recItems[1] = recItems[0]
			recItems[0] = str(othProd["_id"])

		else:
			topScores[2] = topScores[1]
			topScores[1] = score

			recItems[2] = recItems[1]
			recItems[1] = str(othProd["_id"])


	elif score > topScores[1]:
		topScores[2] = topScores[1]
		topScores[1] = str(othProd["_id"])

		recItems[2] = recItems[1]
		recItems[1] = str(othProd["_id"])

	elif score == topScores[1]:
		if prod["brand"] != othProd["brand"]:
			topScores[2] = topScores[1]
			topScores[1] = score

			recItems[2] = recItems[1]
			recItems[1] = str(othProd["_id"])
		else:
			topScores[2] = score

			recItems[2] = str(othProd["_id"])

	elif score > topScores[2]:
		topScores[2] = score
		recItems[2] = str(othProd["_id"])

	elif score == topScores[2]:
		if prod["brand"] != othProd["brand"]:
			topScores[2] = score
			recItems[2] = str(othProd["_id"])


#RUN RECOMMEND

products = productsMen.find({})

i = 0
while i < products.count():
	getRecommendations(products[i], products, productsMen)
	i = i + 1

print "total products visited: " + str(i)


