angular.module('NewDriverCtrl', []).controller('NewDriverController', ['$scope', '$location', 'DriversService', function ($scope, $location, driversService) {
    $scope.driver = {
        // initialize the not required fields
        telnumber: '',
        address: '',
        car: ''
    }
    $scope.errorMsg = '';

    $scope.submit = function () {
        $scope.driver.username = $scope.driver.email;

        driversService.register($scope.driver)
            .success(function () {
                $scope.errorMsg = '';
                $location.path('/list-all-drivers');
            })
            .error(function (err) {
                // $scope.errorMsg = err;
            });
    };
}]);