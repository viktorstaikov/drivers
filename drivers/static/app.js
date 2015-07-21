angular.module('app', [
    'ngRoute',
    'LocalStorageModule',

    'DrvService',
    'AuthService',

    'appRoutes',
    'MainCtrl',
    'NewDriverCtrl',
    'ListDriversCtrl',
    'LoginCtrl',
    'LogoutCtrl',
    'EditDriverCtrl'
]);