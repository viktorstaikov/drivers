angular.module('LoginCtrl', []).controller('LoginController', ['$scope', '$window', '$route', 'AuthenticationService', function ($scope, $window, $route, AuthService) {

    // $scope.errorMsg = '';

    $scope.email = '';
    $scope.password = '';

    $scope.login = function () {
        AuthService.login($scope.email, $scope.password, function () {
            // $location.path(url);
            $window.location.href = '/';
        }, function (err) {
            // $scope.errorMsg = err;
        });
    };
}]);