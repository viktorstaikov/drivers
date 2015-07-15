angular.module('ListDriversCtrl', []).controller('ListDriversController', ['$scope', '$route', 'DriversService', function ($scope, $route, driversService) {
    $scope.errorMsg = '';


    $scope.statusToText = function (driver) {
        switch (driver.status) {
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

    $scope.remove = function (driver, index) {
        $scope.drivers.splice(index, 1);
        driversService.delete(driver.id);
    }

    $scope.edit = function (driver) {
        console.log(driver);
    }

    driversService.getAll()
        .success(function (response) {
            $scope.drivers = response.objects;
        });
}]);