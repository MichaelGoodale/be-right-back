var formidable = require('formidable');
var path = require('path');
var fs = require('fs');
var unzip = require('unzip2');
var spawn = require('child_process').spawn;

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
						var parseMessages = spawn('python', ['../../parser/parser.py']);
						var conversationDataString = '';

						parseMessages.stdout.on('data', function (data) {
							conversationDataString += data.toString();
						});

						parseMessages.stdout.on('end', function () {
							var conversationData = JSON.parse(conversationDataString);
							for (var name in conversationData) {
								if (conversationData.hasOwnProperty(name)) {
									objects.models.Conversation.create({
										messages: conversationData,
										other_name: name
									}).then(function (conversation) {
										conversation.setOwner(req.user).then(function () {
											return res.send({success: true, message: ''});
										});
									});
								}
							}
						});

						var toSend = req.user.toJSON();
						toSend["path"] = path.join(objects.APP_BASE_PATH, 'uploads', 'output',
							newFileName.slice(0, -4), 'html', 'messages.htm');

						parseMessages.stdin.write(JSON.stringify(toSend));
						parseMessages.stdin.end();
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
