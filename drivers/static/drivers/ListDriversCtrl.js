angular
    .module('ListDriversCtrl', ['angularFileUpload'])
    .controller('ListDriversController', ['$scope', '$route', '$http', 'DriversService', 'FileUploader', function ($scope, $route, $http, driversService, FileUploader) {
        $scope.errorMsg = '';

        $scope.uploader = new FileUploader();
        $scope.uploader.url = '/api/import/driver';
        $scope.uploader.queueLimit = 1;
        $scope.uploader.onSuccessItem = function () {
            $route.reload();
        }

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

        $scope.export = function () {
            window.open('/api/export/driver', '_blank', '');
        }

        $scope.import = function () {
            if ($scope.uploader.queue && $scope.uploader.queue.length > 0) {
                $scope.uploader.uploadAll();
            }
        }

        driversService.getAll()
            .success(function (response) {
                $scope.drivers = response.objects;
            });
    }]);