var http = require('http');
var fs = require('fs');
var path = require('path');

var express = require('express');
var pug = require('pug');

var session = require('express-session');

var passport = require('passport');
var passportFacebook = require('passport-facebook');

const APP_BASE_PATH = __dirname;
var CONTROLLER_PATH = APP_BASE_PATH + '/controllers';

var DB_CONFIG = require(APP_BASE_PATH + '/config/config.json')[process.env.NODE_ENV];
var APP_CONFIG = require(APP_BASE_PATH + '/config/app.json');

var models = require('./models');

// Set up authentication.
passport.use(new passportFacebook.Strategy({
	clientID: APP_CONFIG["FACEBOOK_APP_ID"],
	clientSecret: APP_CONFIG["FACEBOOK_APP_SECRET"],
	callbackURL: '/auth/facebook/callback'
}, function (accessToken, refreshToken, profile, done) {
	console.log({where: {facebook_id: profile.id}, defaults: {display_name: profile.displayName}}.where);
	//noinspection JSUnresolvedFunction,JSUnresolvedVariable
	models.User.findOrCreate({where: {facebook_id: profile.id}, defaults: {display_name: profile.displayName}}).spread(function (user) {
		done(null, user)
	});
	// FIND OR CREATE USER!!!
}));

var app = express();
var appServer = http.createServer(app);
var appRouter = express.Router();

var sessionMiddleware = session({
	secret: APP_CONFIG["SESSION_SECRET"],
	resave: false,
	saveUninitialized: false
});

// Set up views.
app.set('view engine', 'pug');
app.set('views', path.join(APP_BASE_PATH, 'views'));

app.use(sessionMiddleware);
app.use(passport.initialize());
app.use(passport.session());

app.use('/bower_components', express.static(path.join(APP_BASE_PATH, 'bower_components')));
app.use(express.static(path.join(APP_BASE_PATH, 'public')));
app.use('/', appRouter);

// Convert a user object to its serialized form.
passport.serializeUser(function (user, done) {
	done(null, user.id);
});
// Convert a user's serialized form to an object.
passport.deserializeUser(function (id, done) {
	models.User.findOne({ where: { id: id }}).then(function (user) {
		done(null, user);
	});
});

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
		dbConfig: DB_CONFIG,
		appConfig: APP_CONFIG,
		APP_BASE_PATH: APP_BASE_PATH
	});
});

// Start the server.
models.sequelize.sync({ force: true }).then(function () {
	// Once models are synced, server can be started!
	var server = appServer.listen(8080, 'localhost', function () {
		console.log('App running on ' + server.address().port);
	});
});
