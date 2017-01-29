module.exports.controller = function (objects) {
	objects.router.get('/auth/facebook', function (req, res, next) {
		console.log(req.query);
		var callbackURL = '/auth/facebook/callback';

		if (req.query.account_linking_token) {
			objects.passport.authenticate('facebook', function (err, user, info) {
				if (err) { return next(err); }
				if (!user) {
					if (req.query.redirect_uri) {
						// Failure + auth from messenger
						return res.redirect(req.query.redirect_uri);
					} else {
						return res.redirect('/');
					}
				}

				req.logIn(user, function(err) {
					if (err) { return next(err); }

					// Success!

					if (req.query.redirect_uri) {
						request({
							uri: 'https://graph.facebook.com/v2.8/me',
							qs: {
								access_token: objects.appConfig['FACEBOOK_PAGE_ACCESS_TOKEN'],
								fields: 'recipient',
								account_linking_token: req.query.account_linking_token
							},
							method: 'POST'
						}, function (err, response, body) {
							if (err || response.statusCode !== 200) {
								console.error(response);
								console.error(err);
							}

							req.user.messenger_id = body.recipient;
							req.user.save();

							return res.redirect(req.query.redirect_uri + '&authorization_code=y');
						});
					} else {
						return res.redirect('/data');
					}
				});
			});
		} else {
			objects.passport.authenticate('facebook', { callbackURL: callbackURL })(req, res, next);
		}
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
