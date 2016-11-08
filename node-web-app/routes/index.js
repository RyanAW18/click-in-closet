var express = require('express');
var router = express.Router();
var async = require('async');

//lets require/import the mongodb native drivers.
var mongodb = require('mongodb');
var ObjectID = mongodb.ObjectID

//We need to work with "MongoClient" interface in order to connect to a mongodb server.
var MongoClient = mongodb.MongoClient;

// Connection URL. This is where your mongodb server is running.
var url = 'mongodb://trossi:1460@ds143707.mlab.com:43707/heroku_b37frt6h';

var ex;

function dbFetch(id, callback, res) {

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
	        	callback(res, ex[0])
	      } else {
	        	console.log('No document(s) found with defined "find" criteria!');
	        	ex = 0
	        	callback(res, 0)
	      }
	    })

	    //Close connection
	    //db.close();
	  });

}

function dbSearch(query, callback, res) {

	query = query.replace('\"', '\\\"')
	console.log(query)
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
	    var queries = f21_dresses.find( {$text: {$search: query}}).toArray(function(err, result) {
	    	if (err) {
	        	console.log(err);
	      } else if (result.length) {
	        	console.log('Found ' + result.length + " item(s)")
	        	callback(res, result)
	      } else {
	        	console.log('No document(s) found with defined "find" criteria!');
	        	callback(res, 0)
	      }
	    })

	    //Close connection
	    //db.close();
	  });

}

function sendData(res, data) {
	if (data == 0) {
		res.send("error")
	}
	else res.send(data)
}


/* GET home page. */
router.get('/', function(req, res, next) {
	res.render('home');
});


router.get('/product/:productID', function(req, res, next) {
	res.render('product');
});

router.get('/product/:productID/data', function(req, res, next) {
	var productID = req.params.productID
	dbFetch(productID, sendData, res)
});

router.get('/search/test/:query', function(req, res, next) {
	dbSearch("off the shoulder", sendData, res)
});

module.exports = router;
