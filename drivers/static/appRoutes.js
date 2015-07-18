angular.module('appRoutes', [])
	.config(['$routeProvider', '$locationProvider', function ($routeProvider, $locationProvider) {
		$routeProvider
			.when('/home', {
				templateUrl: '../static/home/home.html',
				controller: 'MainController'
			})
			.when('/new-driver', {
				templateUrl: '../static/drivers/new-driver.html',
				controller: 'NewDriverController',
				resolve: {
					//This function is injected with the AuthService where you'll put your authentication logic
					'auth': function (DriversService) {
						return false;
						// return DriversService.getMe();
					}
				}
			})
			.when('/list-all-drivers', {
				templateUrl: '../static/drivers/list-all-drivers.html',
				controller: 'ListDriversController',
				resolve: {
					//This function is injected with the AuthService where you'll put your authentication logic
					'auth': function (DriversService) {
						return false;
						// return DriversService.getMe();
					}
				}
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
	.run(function ($rootScope, $location) {
		$rootScope.$on('$routeChangeError', function (current, previous, rejection, message) {

			if (message === 'Not Authenticated') {
				$location.path('/login');
				$location.search('next', previous.$$route.originalPath);
			}
		})
	})