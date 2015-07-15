angular.module('DrvService', []).factory('DriversService', ['$http', '$q', function ($http, $q) {

    return {
        get: function (id) {
            return $http.get('/api/driver/' + id + '/');
        },
        getAll: function () {
            return $http.get('/api/driver/');
        },
        update: function (id, driver) {
            return $http.put('/api/driver/' + id + '/', driver);
        },
        submit: function (driver) {
            return $http.post('/api/driver/', driver);
        },
        delete: function (id) {
            return $http.delete('/api/driver/' + id + '/');
        }
    }
}]);