angular.module('DrvService', []).factory('DriversService', ['$http', '$q', function ($http, $q) {

    return {
        register: function (driver) {
            return $http.post('/api/signup/', driver);
        },
        //admin permissions required
        submit: function (driver) {
            return $http.post('/api/driver/', driver);
        },
        get: function (id) {
            return $http.get('/api/driver/' + id + '/');
        },
        getAll: function () {
            return $http.get('/api/driver/');
        },
        getMe: function () {
            return $http.get('/api/me/');
        },
        update: function (id, driver) {
            return $http.put('/api/driver/' + id + '/', driver);
        },
        delete: function (id) {
            return $http.delete('/api/driver/' + id + '/');
        }
    }
}]);