var http = require('http');
var express = require('express');
var pug = require('pug');

var passport = require('passport');
var passportFacebook = require('passport-facebook');

const APP_BASE_PATH = __dirname;

var models = require('./models');

// Set up authentication.
passport.use(new passportFacebook.Strategy({
	clientID: 'todo',
	clientSecret: 'todo',
	callbackURL: 'todo'
}, function (accessToken, refreshToken, profile, done) {
	// FIND OR CREATE USER!!!
}));

var app = express();
var appServer = http.createServer(app);

// Set up views.
app.set('view engine', 'pug');
app.set('views', APP_BASE_PATH + '/views');

// Start the server.
models.sequelize.sync().then(function () {
	// Once models are synced, server can be started!
	var server = appServer.listen(8080, 'localhost', function () {
		console.log('App running on ' + server.address().port);
	});
});
