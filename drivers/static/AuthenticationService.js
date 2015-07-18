angular.module('AuthService', ['LocalStorageModule']).factory('AuthenticationService', ['$http', 'localStorageService', '$q', function ($http, localStorageService, $q) {
    var $cookies = localStorageService.cookie;

    function setUser(user) {
        $cookies.set('user', JSON.stringify(user));
    }

    function setToken(token) {
        $cookies.set('token', JSON.stringify(token));
    }

    return {
        login: function (email, password, success, error) {
            $http.post('/accounts/login/', {
                    email: email,
                    password: password
                })
                .success(function (data, status, headers, config) {
                    setUser(data.user);
                    setToken(data.token);

                    success();
                }).error(function (data, status, headers, config) {
                    error(data);
                });
        },
        logout: function () {
            setUser(null);
            setToken(null);
            console.log("logout");
        }
    }
}]);