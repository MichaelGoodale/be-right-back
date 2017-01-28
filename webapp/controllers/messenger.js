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

		if (data.object === 'page') {
			//noinspection JSUnresolvedVariable
			data.entry.forEach(function (entry) {
				var pageID = entry.id;
				var timeOfEvent = entry.time;
				var message = event.message;

				//noinspection JSUnresolvedVariable
				entry.messaging.forEach(function (event) {
					if (event.message) {
						// TODO: Recieved message 'event'
						console.log('Message data: ', event.message);
					} else {
						console.log('Webhook received unknown event: ', event);
					}
				});
			});

			res.sendStatus(200);
		}
	});
};