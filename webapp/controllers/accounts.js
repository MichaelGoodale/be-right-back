module.exports.controller = function (objects) {
	objects.router.get('/auth/facebook', objects.passport.authenticate('facebook'));
	objects.router.get('/auth/facebook/callback', objects.passport.authenticate('facebook', { successRedirect: '/data',
			failureRedirect: '/' }));

	objects.router.get('/auth/messenger', objects.passport.authenticate('facebook'), function (req, res) {
		if (req.isAuthenticated()) {
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

				console.log(req.query);
				return res.redirect(req.query.redirect_uri + '&authorization_code=y');
			});
		} else {
			console.log(req.query);
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
