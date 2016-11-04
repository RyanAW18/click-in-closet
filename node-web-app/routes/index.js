var express = require('express');
var router = express.Router();

//lets require/import the mongodb native drivers.
var mongodb = require('mongodb');
var ObjectID = mongodb.ObjectID

//We need to work with "MongoClient" interface in order to connect to a mongodb server.
var MongoClient = mongodb.MongoClient;

// Connection URL. This is where your mongodb server is running.
var url = 'mongodb://trossi:1460@ds143707.mlab.com:43707/heroku_b37frt6h';
var ex;

function dbSearch(id) {

	var o_id = new ObjectID(id)
	// Use connect method to connect to the Server
	MongoClient.connect(url, function (err, db) {
	  if (err) {
	    console.log('Unable to connect to the mongoDB server. Error:', err);
	  } else {
	    //HURRAY!! We are connected. :)
	    console.log('Database connection established');
		}


		 // do some work here with the database.
	    var f21_dresses = db.collection('f21_dresses')
	    f21_dresses.find({'_id' : o_id}).toArray(function(err, result) {
	    	if (err) {
	        	console.log(err);
	      } else if (result.length) {
	        	console.log('Found ' + result.length + " item(s)")
	        	ex = result
	      } else {
	        	console.log('No document(s) found with defined "find" criteria!');
	        	ex = 0
	      }
	    })

	    //Close connection
	    db.close();
	  });
}

dbSearch("581bc7734d1c7bf095fa6926")

/* GET home page. */
router.get('/', function(req, res, next) {
	res.render('home');
});

/* GET product page. */
// router.get('/product', function(req, res, next) {
// 	res.render('product')
// });

router.get('/product/:productID', function(req, res, next) {
	res.render('product');
});

router.get('/product/:productID/data', function(req, res, next) {
	var productID = req.params.productID
	var dataJSON = ex[0]
	res.send(dataJSON)
});

module.exports = router;
