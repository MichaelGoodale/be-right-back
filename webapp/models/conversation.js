// Models conversation data between a user of the web app and someone they talk to on Messenger.

module.exports = function (sequelize, Sequelize) {
	var Conversation = sequelize.define('Conversation', {
		messages: Sequelize.JSON
	}, {
		classMethods: {
			associate: function (models) {
				Conversation.belongsTo(models.User, { as: 'Owner' })
			}
		}
	});
	return Conversation;
};
