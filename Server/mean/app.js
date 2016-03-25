var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');

var routes = require('./routes/index');
var users = require('./routes/users');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

var publicDir = path.join(__dirname, 'public');
app.use('/', routes);
app.get('/', function(req, res){
  res.sendFile(publicDir + '/index.html');
});

app.get('/authenticate', function(req, res){
  // check header or url parameters or post parameters for token
  var token = req.cookies['_xsrf'];
  // decode token
  if (token) {
    // verifies secret and checks exp
    jwt.verify(token, app.get('secret'), function(err, decoded) {
      if (err) {
        return res.json({ auth: 0 });
      } else {
        // if everything is good, save to request for use in other routes
        return res.json({auth: 1});
      }
    });
  } else {
    return res.json({auth: 0});
  }
});

app.get('/partials/:name', function(req, res){
  var name = req.params.name;
  res.render(name);
});

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
  app.use(function(err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
      message: err.message,
      error: err
    });
  });
}

// production error handler
// no stacktraces leaked to user
app.use(function(err, req, res, next) {
  res.status(err.status || 500);
  res.render('error', {
    message: err.message,
    error: {}
  });
});


module.exports = app;
