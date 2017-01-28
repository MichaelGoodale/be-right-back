var http = require('http');
var express = require('express');

var passport = require('passport');
var passportFacebook = require('passport-facebook');

const APP_BASE_PATH = __dirname;

var models = require('./models');

passport.use(new passportFacebook.Strategy({
	clientID: 'todo',
	clientSecret: 'todo',
	callbackURL: 'todo'
}, function (accessToken, refreshToken, profile, done) {
	// FIND OR CREATE USER!!!
}));

var app = express();
var appServer = http.createServer(app);

models.sequelize.sync().then(function () {
	// Once models are synced, server can be started!
	var server = appServer.listen(8080, 'localhost', function () {
		console.log('App running on ' + server.address().port);
	});
});
