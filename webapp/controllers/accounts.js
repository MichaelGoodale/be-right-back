module.exports.controller = function (objects) {
	objects.router.get('/auth/facebook', objects.passport.authenticate('facebook'));
	objects.router.get('/auth/facebook/callback', objects.passport.authenticate('facebook', { successRedirect: '/data',
			failureRedirect: '/' }));

	objects.router.get('/authenticated', function (req, res) {

	});
};
