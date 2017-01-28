var formidable = require('formidable');
var path = require('path');
var fs = require('fs');
var unzip = require('unzip2');

module.exports.controller = function (objects) {
	objects.router.get('/data', function (req, res) {
		if (!req.isAuthenticated()) {
			return res.redirect('/');
		}

		return res.render('data', { user: req.user.toJSON() });
	});

	objects.router.post('/data/upload', function (req, res) {
		var form = new formidable.IncomingForm();
		form.parse(req);

		form.on('fileBegin', function (field, file) {
			var extension = path.extname(file.name).toLowerCase();
			if (extension !== '.zip') {
				return res.send({ success: false, message: 'bad_extension' });
			}
		});

		form.on('file', function(field, file) {
			var newFileName = req.user.dataValues.facebook_id + '-' + ((new Date()).getTime()).toString() + '-' + file.name;
			fs.rename(file.path, path.join(objects.APP_BASE_PATH, 'uploads', newFileName),
				function (err) {
					if (err) {
						console.error(err);
						return res.send({success: false, message: err});
					}

					// Unzip the uploaded file.
					fs.createReadStream(path.join(objects.APP_BASE_PATH, 'uploads', newFileName)).pipe(unzip.Extract({
						path: path.join(objects.APP_BASE_PATH, 'uploads', 'output', newFileName.slice(0, -4))
					})).on('close', function () {
						return res.send({success: true, message: ''});
					});
				}
			);
		});

		form.on('error', function(err) {
			console.error(err);
			return res.send({ success: false, message: err });
		});

		// TODO: process file...
	});
};
