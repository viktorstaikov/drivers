angular.module('appRoutes', []).config(['$routeProvider', '$locationProvider', function ($routeProvider, $locationProvider) {
	$routeProvider
		.when('/home', {
			templateUrl: '../static/home/home.html',
			controller: 'MainController'
		})
		.when('/new-driver', {
			templateUrl: '../static/drivers/new-driver.html',
			controller: 'NewDriverController'
		})
		.when('/list-all-drivers', {
			templateUrl: '../static/drivers/list-all-drivers.html',
			controller: 'ListDriversController'
		})
		.when('/signup', {
			templateUrl: '../static/drivers/new-driver.html',
			controller: 'NewDriverController'
		})
		.otherwise({
			redirectTo: '/home'
		});

	//$locationProvider.html5Mode(true); // fix url to not contain '#'
}])