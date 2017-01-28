module.exports.controller = function (objects) {
	objects.router.get('/', function (req, res) {
		return res.render('index');
	});
};
