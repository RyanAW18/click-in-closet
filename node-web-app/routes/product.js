//lets require/import the mongodb native drivers.
var mongodb = require('mongodb');

//We need to work with "MongoClient" interface in order to connect to a mongodb server.
var MongoClient = mongodb.MongoClient;

function dbRender(productID) {
	// Connection URL. This is where your mongodb server is running
	var url = 'mongodb://trossi:1460@ds143707.mlab.com:43707/heroku_b37frt6h';
	var db = dbConnect(url)
	if (db != 0) {
		var f21_dresses = db.collection('f21_dresses')
		dbClose()
		return "connected to f21 dresses!"
	}

}




function dbConnect(url) {
	MongoClient.connect(url, function (err, db) {
		if (err) {
			console.log('Unable to connect to the mongoDB server. Error:', err);
			return 0
		} 
		else {
			//HURRAY!! We are connected. :)
			console.log('Connection established to', url);
			return db
		}
	});
}

function dbClose() {
	db.close();
}