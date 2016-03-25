angular.module('YPOD')
.controller('MainController', ['$uibModal', '$cookies', '$http', '$state', function($modal, $cookies, $http, $state){
  var self = this;
  // Authenticate
  $http.get('/authenticate')
  .success(function(data){
    if(data["auth"] == 1) {
      //authenticated
      $state.go('loggedin');
    }
  });
  self.openLoginDialog = function() {
    var modalInstance = $modal.open({
      templateUrl: 'templates/login-modal.html',
      controller: 'LoginModalInstanceCtrl as ctrl',
      backdrop: 'static'
    });
    modalInstance.result.then(function(data){
      // Set token on scope
      self.token = data.token;
      $state.go('loggedin');
    });
  };
}]);
