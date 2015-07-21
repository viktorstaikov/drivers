angular
    .module('AuthService', ['LocalStorageModule'])
    .factory('AuthenticationService', ['$http', '$location', '$q', 'localStorageService', 'DriversService', function ($http, $location, q, localStorageService, DriversService) {
        var $cookies = localStorageService.cookie;

        function setUser(user) {
            $cookies.set('user', JSON.stringify(user));
        }

        function getUser() {
            return $cookies.get('user');
        }

        return {
            login: function (email, password, success, error) {
                $http
                    .post('/accounts/login/', {
                        username: email,
                        password: password
                    })
                    .success(function (user, status, headers, config) {
                        setUser(user);
                        success(user);
                    }).error(function (data, status, headers, config) {
                        error(data);
                    });
            },
            logout: function (done) {
                $http
                    .get('/accounts/logout/')
                    .success(function () {
                        setUser(null);
                        done();
                    });
            },
            getMe: function () {
                return getUser();
            },
            isAdmin: function () {
                var user = getUser();
                if (!user || user.is_admin == false) {
                    return q.reject('Not Authenticated');
                }
                return true;
            }
        }
    }]);