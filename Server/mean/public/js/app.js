"use strict"

angular.module('YPOD', ['ui.bootstrap', 'ui.router', 'ngCookies'])
.config(['$urlRouterProvider', '$stateProvider', function($urlRouterProvider, $stateProvider){
  $urlRouterProvider.otherwise('/');
  $stateProvider.state('index', {
    url: '/',
    views: {
      '': {
        templateUrl: '/partials/landingpage',
        controller: 'MainController',
        controllerAs: 'ctrl'
      },
      'login': {
        templateUrl: 'partials/loginbutton',
        controller: 'MainController',
        controllerAs: 'ctrl'
      }
    }
  })
  .state('loggedin', {
    url: '/',
    views: {
      '': {
        templateUrl: '/partials/home',
        controller: 'MainController',
        controllerAs: 'ctrl'
      },
      'login': {
        templateUrl: 'partials/loggedin',
        controller: 'MainController',
        controllerAs: 'ctrl'
      }
    }
  });
}]);
