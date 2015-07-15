angular.module('NewDriverCtrl', []).controller('NewDriverController', ['$scope', '$location', 'DriversService', function ($scope, $location, driversService) {
    $scope.driver = {}
    $scope.errorMsg = '';

    $scope.submit = function () {

        driversService.submit($scope.driver)
            .success(function () {
                $scope.errorMsg = '';
                $location.path('/list-all-drivers');
            })
            .error(function (err) {
                $scope.errorMsg = err;
            });
    };
}]);