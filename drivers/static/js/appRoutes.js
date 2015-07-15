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
			.otherwise({
				redirectTo: '/home'
			});

		//$locationProvider.html5Mode(true); // fix url to not contain '#'
	}])
	.run(function ($rootScope, $location) {
		$rootScope.$on('$routeChangeError', function (current, previous, rejection, message) {

			if (message === 'Not Authenticated') {
				$location.path('/login');
				$location.search('redirect_url', previous.$$route.originalPath);
			}
		})
	})