module.exports.controller = function (objects) {
	objects.router.get('/data', function (req, res) {
		return res.render('data');
	});

	objects.router.post('/data/upload', function (req, res) {
		// TODO
	});
};
