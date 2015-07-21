angular.module('EditDriverCtrl', []).controller('EditDriverController', ['$scope', '$location', '$route', 'DriversService', function ($scope, $location, $route, driversService) {
    var id = $route.current.params.id;

    $scope.update = function () {
        console.log('updating here');
        console.log($scope.driver);

        driversService.update(id, $scope.driver)
            .success(function () {
                $scope.errorMsg = '';
                $location.path('/list-all-drivers');
            })
            .error(function (err) {
                $scope.errorMsg = err.error;
            });
    };

    $scope.log = function () {
        console.log($scope.driver);
    }
    $scope.forceapply = function () {
        $scope.$apply();
    }

    $scope.driver = {};
    driversService.get(id)
        .success(function (driver) {
            $scope.driver = driver;
            $scope.errorMsg = '';
        });
}]);