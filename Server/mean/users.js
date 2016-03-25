exports.getUser = function( username, password, secret, callback ) {
    var data = {};
    data.username = username;
    data.password = password;
    data["auth"] = 1;
    callback(data);
}
