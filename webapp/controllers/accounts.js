module.exports.controller = function (objects) {
	objects.router.get('/auth/facebook', objects.passport.authenticate('facebook'));
	objects.router.get('/auth/facebook/callback', objects.passport.authenticate('facebook', { successRedirect: '/data',
			failureRedirect: '/' }));

	objects.router.get('/oauth', function (req, res) {
		return res.json({

		});
	});

	objects.router.get('/authenticated', function (req, res) {

	});

	objects.router.get('/sign_out', function (req, res) {
		req.logout();
		res.redirect('/');
	});
};
