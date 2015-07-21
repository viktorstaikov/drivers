angular
    .module('LogoutCtrl', [])
    .controller('LogoutController', ['$window', 'AuthenticationService', function ($window, AuthenticationService) {
        AuthenticationService.logout(function () {
            $window.location.href = '/';
        });
    }]);