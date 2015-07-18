angular.module('MainCtrl', []).controller('MainController', ['$scope', 'DriversService', function ($scope, DriversService) {
    $scope.driver = {}
    $scope.statusToText = function () {
        switch ($scope.driver.status) {
        case 1:
            return 'clean';
            break;
        case 2:
            return 'discrepancy in docs';
            break;
        case 3:
            return 'fake documents';
            break;
        default:
            return 'not checked';
            break;
        }
    }

    DriversService.getMe()
        .success(function (user) {
            $scope.driver = user
            console.log(user)
        })
        .error(function () {
            console.log('User has not logged in properly.')
        })
}]);