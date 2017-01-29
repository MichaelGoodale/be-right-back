var request = require('request');

module.exports.controller = function(objects) {
	objects.router.get('/messenger/webhook', function (req, res) {
		if (req.query['hub.mode'] === 'subscribe' && req.query['hub.verify_token'] === objects.appConfig["FACEBOOK_PAGE_ACCESS_TOKEN"]) {
			console.log('Validating webhook');
			res.status(200).send(req.query['hub.challenge']);
		} else {
			console.error("Failed validation. Make sure the validation tokens match.");
			res.sendStatus(403);
		}
	});


	objects.router.post('/messenger/webhook', function (req, res) {
		var data = req.body;

		function sendMessage (recipientId, messageText) {
			var messageData = {
				recipient: {
					id: recipientId
				},
				message: {
					text: messageText
				}
			};

			request({
				uri: 'https://graph.facebook.com/v2.8/me/messages',
				qs: { access_token: objects.appConfig['FACEBOOK_PAGE_ACCESS_TOKEN'] },
				method: 'POST',
				json: messageData
			}, function (err, response, body) {
				if (err || response.statusCode !== 200) {
					console.error(response);
					console.error(err);
				}

				// TODO: SUCCESS!
			});
		}

		function sendLogInMessage (recipientId) {
			request({
				uri: 'https://graph.facebook.com/v2.8/me/thread_settings',
				qs: { access_token: objects.appConfig['FACEBOOK_PAGE_ACCESS_TOKEN'] },
				method: 'POST',
				json: {
					setting_type : "account_linking",
					account_linking_url : "https://brb.dlougheed.com/auth/messenger?client_id=" + recipientId
				}
			}, function (err, response, body) {
				if (err || response.statusCode !== 200) {
					console.error(response);
					console.error(err);
				}

				console.log(body);

				var messageData = {
					recipient: {
						id: recipientId
					},
					message: {
						attachment: {
							type: 'template',
							payload: {
								template_type: 'button',
								text: 'Please log in to use the bot!',
								buttons: [
									{
										type: 'account_link',
										url: 'https://brb.dlougheed.com/auth/messenger'
									}
								]
							}
						}
					}
				};

				request({
					uri: 'https://graph.facebook.com/v2.8/me/messages',
					qs: { access_token: objects.appConfig['FACEBOOK_PAGE_ACCESS_TOKEN'] },
					method: 'POST',
					json: messageData
				}, function (err, response, body) {
					if (err || response.statusCode !== 200) {
						console.error(response);
						console.error(err);
					}

					console.log(body);
				});
			});
		}

		if (data.object === 'page') {
			//noinspection JSUnresolvedVariable
			data.entry.forEach(function (entry) {
				var pageID = entry.id;
				var timeOfEvent = entry.time;

				//noinspection JSUnresolvedVariable
				entry.messaging.forEach(function (event) {
					if (event.message) {
						// TODO: Recieved message 'event'
						console.log('Message data: ', event.message);
						// TODO: CHECK IF THEY HAVE AN ACCOUNT IN THE DB
						var senderId = event.sender.id;
						objects.models.User.findOne({ messenger_id: senderId }).then(function (user) {
							if (user) {
								// TODO: QUERY FOR A RESPONSE
								var response = 'backtalk';
								sendMessage(senderId, response);
							} else {
								sendLogInMessage(senderId);
							}
						});
					} else {
						console.log('Webhook received unknown event: ', event);
					}
				});
			});

			return res.sendStatus(200);
		}
	});
};