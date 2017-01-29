module.exports.controller = function (objects) {
	objects.router.get('/auth/facebook', function (req, res, next) {
		console.log(req.query);
		var callbackURL = '/auth/facebook/callback';

		if (req.query.account_linking_token) {
			callbackURL += '?redirect_uri=' + req.query.redirect_uri;
		}
		objects.passport.authenticate('facebook', { callbackURL: callbackURL })(req, res, next);
	});
	objects.router.get('/auth/facebook/callback', objects.passport.authenticate('facebook', { successRedirect: '/data', failureRedirect: '/' }));

	objects.router.get('/auth/messenger', function (req, res) {
		if (req.isAuthenticated()) {

		} else {
			console.log('no auth!!!!');
			// return res.sendStatus(200);
			return res.redirect(req.query.redirect_uri);
		}
	});

	objects.router.get('/auth/messenger/callback', function (req, res) {
		console.log(req.query);
		if (req.query.authorization_code) {
			// SUCCESS!
			return res.json({

			});
		} else {

		}
	});

	objects.router.get('/authenticated', function (req, res) {

	});

	objects.router.get('/sign_out', function (req, res) {
		req.logout();
		res.redirect('/');
	});
};
