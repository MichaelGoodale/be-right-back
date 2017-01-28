var formidable = require('formidable');
var path = require('path');
var fs = require("fs");

module.exports.controller = function (objects) {
	objects.router.get('/data', function (req, res) {
		if (!req.isAuthenticated()) {
			return res.redirect('/');
		}

		return res.render('data', { user: req.user.toJSON() });
	});

	objects.router.post('/data/upload', function (req, res) {
		var form = new formidable.IncomingForm();

		form.on('file', function(field, file) {
			fs.rename(file.path, path.join(objects.APP_BASE_PATH, (new Date()).toString(), 'uploads',
				req.user.dataValues.facebook_id + file.name), function (err) {
					if (err) {
						console.error(err);
						res.send({ success: false, message: err });
					}

					res.send({ success: true, message: '' });
			});
		});

		form.on('error', function(err) {
			console.error(err);
			res.send({ success: false, message: err });
		});

		form.parse(req);

		// TODO: process file...
	});
};
