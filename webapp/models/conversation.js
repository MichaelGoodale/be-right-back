// Models conversation data between a user of the web app and someone they talk to on Messenger.

module.exports = function (sequelize, Sequelize) {
	var Conversation = sequelize.define('Conversation', {
		messages: {type: Sequelize.JSON, allowNull: false},
		other_name: {type: Sequelize.STRING, allowNull: false}
	}, {
		classMethods: {
			associate: function (models) {
				Conversation.belongsTo(models.User, { as: 'Owner' })
			}
		}
	});
	return Conversation;
};
