angular.module('MainCtrl', []).controller('MainController', ['$scope', '$route', 'AuthenticationService', function ($scope, $route, AuthenticationService) {
    $scope.statusToText = function () {
        if (!$scope.driver) {
            return '';
        }
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


    $scope.driver = AuthenticationService.getMe()
        // $route.reload();
}]);