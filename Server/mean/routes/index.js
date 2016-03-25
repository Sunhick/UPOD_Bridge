var express = require('express');
var users = require('../users');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
    res.render('index', { title: 'Express' });
});

router.post('/login', function(req, res, next){
    // res.write('something...');
    var secret = req.app.get('secret');
    users.getUser(req.body.params.username, req.body.params.password, secret, function(data){
	if(data["auth"] == 1) {
	    //res.cookie('_xsrf', data['token']);
	}
	res.json(data);
	res.end();
    });
});

module.exports = router;
