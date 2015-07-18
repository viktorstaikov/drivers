angular
    .module('LogoutCtrl', [])
    .controller('LogoutController', ['$window', 'AuthenticationService', function ($window, AuthenticationService) {
        AuthenticationService.logout();
        $window.location.href = '/';
    }]);