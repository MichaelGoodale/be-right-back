module.exports.controller = function (objects) {
	objects.router.get('/', function (req, res) {
		if (req.isAuthenticated()) {
			return res.redirect('/data');
		}

		return res.render('index');
	});
};
