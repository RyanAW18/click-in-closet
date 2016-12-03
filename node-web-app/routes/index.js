var express = require('express');
var router = express.Router();
var async = require('async');
var http = require('http');
var httpReq = require('httpReq.js');


//lets require/import the mongodb native drivers.
var mongodb = require('mongodb');
var ObjectID = mongodb.ObjectID

//We need to work with "MongoClient" interface in order to connect to a mongodb server.
var MongoClient = mongodb.MongoClient;

// Connection URL. This is where your mongodb server is running.
var url = 'mongodb://trossi:1460@ds143707.mlab.com:43707/heroku_b37frt6h';

function productFetch(id, callback, res) {

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
	    var products = db.collection('productsMen')
	    products.find({'_id' : o_id}).toArray(function(err, result) {
	    	if (err) {
	        	console.log(err);
	      } else if (result.length) {
	        	console.log('Found ' + result.length + " item(s)")
	        	callback(res, result[0])
	      } else {
	        	console.log('No document(s) found with defined "find" criteria!');
	        	callback(res, 0)
	      }
	    })

	    //Close connection
	    // db.close();
	  });

}

function userFetch(account, callback, res) {

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
	    userDB.find({'email' : account}).toArray(function(err, result) {
	    	if (err) {
	        	console.log(err);
	      } else if (result.length) {
	        	console.log("Found account" + account)
	        	callback(res, result[0])
	      } else {
	        	console.log('No document(s) found with defined "find" criteria!');
	        	callback(res, 0)
	      }
	    })

	    //Close connection
	    // db.close();
	  });

}

function createAccount(email, password, firstName, lastName, callbackSucc, callbackFail, res) {

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
	    userDB.find({'email' : email}).toArray(function(err, result) {
	    	if (err) {
	        	console.log(err);
	      } else if (result.length) {
	        	callbackFail(res)
	      } else {
	      	    var userJSON = {"email": email, "password": password, "firstName": firstName, "lastName": lastName, "outfits": []}
	        	userDB.insert(userJSON, function(err, result) {
	    			if (err) {
	        			console.log(err);
	      				} else {
	        				console.log(firstName + " added!")
	        				callbackSucc(res, email)
	       				}
	    			})
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
	    var products = db.collection('productsMen')
	    var queries = products.find( {$text: {$search: query}}).toArray(function(err, result) {
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

function loginAccount(email, password, callbackSucc, callbackFail, res) {

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
	    userDB.find({'email' : email}).toArray(function(err, result) {
	    	if (err) {
	        	console.log(err);
	      } else if (result.length) {
	      		if (password != result[0]["password"]) {
	      			callbackFail(res)
	      		}
	      		else callbackSucc(res, email)
	        	
	      } else {
	        	callbackFail(res)
	     		}
	    	})

	    //Close connection
	    // db.close();
	  });

}

function checkLoginStatus(req) {
	var cookie = req.cookies;
	if (cookie["user_email"] == undefined) return false
	if (cookie["user_email"].length == 0) return false
	else return true
}

function sendData(res, data) {
	if (data == 0) {
		res.send("error")
	}
	else res.send(data)
}

function redirectHome(res, email) {
	if (email.length == 0) {
		res.send("error") 
	}
	else {
		var cookie = "user_email=" + email + ";"
		res.cookie(cookie);
		res.redirect("/home")
	}
}

function redirectEmailCollision(res) {
	var link = "/create_account%"
	res.redirect(link)
}

function redirectWrongPassword(res) {
	var link = "/login#"
	res.redirect(link)
}

function addOutfit(req, name) {
	var cookie = req.cookies;
	if (cookie["user_email"] == undefined) return null
	if (cookie["user_email"].length == 0) return null
	else {
		var email = cookie["user_email"]
		var newOutfitJSON = {"name": name, "price": "$0.00", "items": []}
		var outfitArray = JSON.parse(cookie["outfits"])
		var contains = false;
		for (var i = 0; i < outfitArray.length; i++) {
			if (outfitArray[i]["name"] == name) {
				contains = true
				break
			}
		}
		if (!contains) {
			outfitArray.push(newOutfitJSON)
			console.log("outfit length: " + outfitArray.length)
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
			    userDB.update(
			    	{'email' : email},
			    	{
	        		"$set": {
			            "outfits": outfitArray
	        		}
	        		}
	       		)
			    //Close connection
			    // db.close();
			  });
		}
	}
}

function addItemToOutfit_User(req, productID, index, callback_prod, callback_up) {
	console.log("Add item --> user level")
	console.log("index: " + index)
	var cookie = req.cookies;
	if (cookie["user_email"] == undefined) return null
	if (cookie["user_email"].length == 0) return null
	else {
		var email = cookie["user_email"]

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
		    userDB.find({'email' : email}).toArray(function(err, result) {
		    	if (err) {
		        	console.log(err);
		      } else if (result.length) {
		        	console.log("Found account" + email)
		        	callback_prod(result[0], productID, index, callback_up, email, db)
		      } else {
		        	console.log('No document(s) found with defined "find" criteria!');
		        	return 0
		      }
		    })

		    //Close connection
		    // db.close();
		  });
	}
}



function addItemToOutfit_Product(userJSON, productID, index, callback, email, db) {
	console.log("Add item --> product level")
	console.log("Product ID: " + productID)
	var outfitArray = userJSON["outfits"]
	var outfitJSON = outfitArray[index];
	console.log(outfitJSON)

	var o_id = new ObjectID(productID)

	var productDB = db.collection('productsMen')
	productDB.find({'_id' : o_id}).toArray(function(err, result) {
	    	if (err) {
	        	console.log(err);
	      } else if (result.length) {
	        	console.log('Found ' + result.length + " item(s)")
	        	callback(result[0], outfitJSON, outfitArray, index, email, db)
	      } else {
	        	console.log('No document(s) found with defined "find" criteria!');
	      }
	    })

	    //Close connection
	    // db.close();
}

function addItemToOutfit_Update(productJSON, outfitJSON, outfitArray, index, email, db) {
	console.log("Add item --> update level")
	var itemArray = outfitJSON["items"];
	itemArray.push(productJSON)
	outfitArray[index] = outfitJSON;
	console.log("outfit length: " + outfitArray.length)
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
	    userDB.update(
	    	{'email' : email},
	    	{
    		"$set": {
	            "outfits": outfitArray
    		}
    		}
   		)
	    //Close connection
	    // db.close();
	  });
}


/* GET home page. */
router.get('/home', function(req, res, next) {
	var loggedIn = checkLoginStatus(req);
	if (loggedIn) res.render('home');
	else res.redirect("/");
});

router.get('/:email/data', function(req, res, next) {
	var loggedIn = checkLoginStatus(req);
	if (loggedIn) {
		var email = req.params.email
		userFetch(email, sendData, res)
	}
	else res.redirect("/");
	
});


router.get('/outfits', function(req, res, next) {
	var loggedIn = checkLoginStatus(req);
	if (loggedIn) res.render('outfits');
	else res.redirect("/");
});

router.get('/outfits/add/:name', function(req, res, next) {
	var name = req.params.name
	var loggedIn = checkLoginStatus(req);
	if (loggedIn) {
		addOutfit(req, name)
		res.redirect("/outfits")
	}
	else res.redirect("/");
});

router.get('/outfits/add_item/:productID', function(req, res, next) {
	var loggedIn = checkLoginStatus(req);
	if (loggedIn) {
		res.render("outfit_add_item")
	}
	else res.redirect("/");
});

router.get('/outfits/:index/:name', function(req, res, next) {
	var loggedIn = checkLoginStatus(req);
	if (loggedIn) {
		res.render("outfit_page")
	}
	else res.redirect("/");
});

router.get('/outfits/add_item/:productID/:index', function(req, res, next) {
	var productID = req.params.productID
	console.log("Product ID: " + productID)
	var index = req.params.index
	console.log(index)
	var loggedIn = checkLoginStatus(req);
	if (loggedIn) {
		addItemToOutfit_User(req, productID, index, addItemToOutfit_Product, addItemToOutfit_Update)
		res.redirect("/outfits")
	}
	else res.redirect("/");
});


router.get('/product/:productID', function(req, res, next) {
	var loggedIn = checkLoginStatus(req);
	if (loggedIn) {
		res.render('product');
	}
	else res.redirect("/");
});

router.get('/product/:productID/data', function(req, res, next) {
	var loggedIn = checkLoginStatus(req);
	if (loggedIn) {
		var productID = req.params.productID
		productFetch(productID, sendData, res)
	}
	else res.redirect("/");
	
});

router.get('/search/:query/data', function(req, res, next) {
	var loggedIn = checkLoginStatus(req);
	if (loggedIn) {
		var query = req.params.query
		dbSearch(query, sendData, res)
	}
	else res.redirect("/");
	

});

router.get('/search/:query', function(req, res, next) {
	var loggedIn = checkLoginStatus(req);
	if (loggedIn) {
		res.render('search');
	}
	else res.redirect("/");
	
});


router.get('/', function(req, res, next) {
	var loggedIn = checkLoginStatus(req);
	if (loggedIn) res.redirect('/home');
	else res.render('landing');
});

router.get('/!', function(req, res, next) {
	res.cookie("user_email=; expires=Thu, 01 Jan 1970 00:00:00 UTC")
	res.redirect("/")
});

router.get('/login', function(req, res, next) {
	res.render('login');
});

router.get('/login#', function(req, res, next) {
	res.render('login');
});

router.get('/login%', function(req, res, next) {
	res.render('login');
});


router.get('/login/:email/:password', function(req, res, next) {
	var email = req.params.email
	var password = req.params.password
	loginAccount(email, password, redirectHome, redirectWrongPassword, res)
});

router.get('/create_account', function(req, res, next) {
	res.render('create_account');
});

router.get('/create_account#', function(req, res, next) {
	res.render('create_account');
});

router.get('/create_account%', function(req, res, next) {
	res.render('create_account');
});

router.get('/create_account&', function(req, res, next) {
	res.render('create_account');
});

router.get('/create_account/:email/:password/:firstName/:lastName', function(req, res, next) {
	var email = req.params.email
	var password = req.params.password
	var firstName = req.params.firstName
	var lastName = req.params.lastName
	createAccount(email, password, firstName, lastName, redirectHome, redirectEmailCollision, res)
});


module.exports = router;