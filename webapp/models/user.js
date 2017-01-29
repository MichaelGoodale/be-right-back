// Models the user object for the web app; linked with Facebook.

module.exports = function (sequelize, Sequelize) {
	return sequelize.define('User', {
		facebook_id: {type: Sequelize.STRING, unique: true, allowNull: false},
		messenger_id: {type: Sequelize.String, uniquie: true},
		display_name: {type: Sequelize.STRING, allowNull: false}
	});
};
