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
	    var f21 = db.collection('f21')
	    f21.find({'_id' : o_id}).toArray(function(err, result) {
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
	    // db.close();
	  });

}

function createAccount(email, password, firstName, lastName, callback, res) {

	// Use connect method to connect to the Server
	MongoClient.connect(url, function (err, db) {
	  if (err) {
	    console.log('Unable to connect to the mongoDB server. Error:', err);
	  } else {
	    //HURRAY!! We are connected. :)
	    console.log('Database connection established');
		}


		 // do some work here with the database.
	    var userDB = db.collection('userDB')
	    //CHECK IF DB CONTAINS ACCOUNT WITH THAT EMAIL BEFORE CREATING NEW ACCOUNT

	    
	    var userJSON = {"email": email, "password": password, "firstName": firstName, "lastName": lastName, outfits: {}}
	    userDB.insert(userJSON, function(err, result) {
	    	if (err) {
	        	console.log(err);
	      } else {
	        	console.log(firstName + " added!")
	        	callback(res, email)
	        }
	    })

	    //Close connection
	    // db.close();
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
	    var f21 = db.collection('f21')
	    var queries = f21.find( {$text: {$search: query}}).toArray(function(err, result) {
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
	    // db.close();
	  });

}

function sendData(res, data) {
	if (data == 0) {
		res.send("error")
	}
	else res.send(data)
}

function redirectHome(res, email) {
	if (email == 0) {
		res.send("error") 
	}
	else {
		var link = "/home/" + email
		res.redirect(link)
	}
	
}


/* GET home page. */
router.get('/home/:account', function(req, res, next) {
	res.render('home');
});


router.get('/product/:productID', function(req, res, next) {
	res.render('product');
});

router.get('/product/:productID/data', function(req, res, next) {
	var productID = req.params.productID
	dbFetch(productID, sendData, res)
});

router.get('/search/:query/data', function(req, res, next) {
	var query = req.params.query
	dbSearch(query, sendData, res)

});

router.get('/search/:query', function(req, res, next) {
	res.render('search');
});

router.get('/search-static/:query', function(req, res, next) {
	res.render('search-static');
	res.render('search-static');
});

router.get('/', function(req, res, next) {
	res.render('landing');
});

router.get('/login', function(req, res, next) {
	res.render('login');
});

router.get('/login#', function(req, res, next) {
	res.render('login');
});

router.get('/create_account', function(req, res, next) {
	res.render('create_account');
});

router.get('/create_account/:email/:password/:firstName/:lastName', function(req, res, next) {
	var email = req.params.email
	var password = req.params.password
	var firstName = req.params.firstName
	var lastName = req.params.lastName
	createAccount(email, password, firstName, lastName, redirectHome, res)
});


module.exports = router;
