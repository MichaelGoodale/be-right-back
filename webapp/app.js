var http = require('http');
var fs = require('fs');

var express = require('express');
var pug = require('pug');

var passport = require('passport');
var passportFacebook = require('passport-facebook');

const APP_BASE_PATH = __dirname;
var CONTROLLER_PATH = APP_BASE_PATH + '/controllers';

var DB_CONFIG = require(APP_BASE_PATH + '/config/config.json')[process.env.NODE_ENV];

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
var appRouter = express.Router();

// Set up views.
app.set('view engine', 'pug');
app.set('views', APP_BASE_PATH + '/views');

app.use('/', appRouter);

// Load all JavaScript files in the controller directory as controller objects.
fs.readdirSync(CONTROLLER_PATH).filter(function (file) {
	return (file.indexOf('.') !== 0) && (file.substr(-3) === '.js');
}).forEach(function (file) {
	var route = require(CONTROLLER_PATH + '/' + file);
	// Pass an object containing shared instances needed for site function to each controller.
	route.controller({
		router: appRouter,
		passport: passport,
		models: models,
		dbConfig: DB_CONFIG
	});
});

// Start the server.
models.sequelize.sync().then(function () {
	// Once models are synced, server can be started!
	var server = appServer.listen(8080, 'localhost', function () {
		console.log('App running on ' + server.address().port);
	});
});
