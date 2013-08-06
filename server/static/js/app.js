// Declares the modules that our app is going to use
var myApp = angular.module('vsmApp', ['ngCookies', 'ngResource', 'ui.utils']);

// Need to use different symbols as flask uses {{ and }}
myApp.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('<[');
    $interpolateProvider.endSymbol(']>');
});

// Routes for out application
myApp.config(function($routeProvider) {
  $routeProvider
      .when('/',
      {
        templateUrl: 'static/partials/login.html',
        controller: 'LoginCtrl'
      })
      .when('/patients',
      {
        templateUrl: 'static/partials/patient_index.html',
        controller: 'PatientListCtrl'
      })
      .when('/patients/:nhi',
      {
        templateUrl: 'static/partials/patient.html',
        controller:'PatientCtrl'
      })
      .when('/patients/:nhi/checkins', {
        redirectTo: "/patients/:nhi"
      })
      .when('/patients/:nhi/checkins/:checkin_id',
      {
        templateUrl: 'static/partials/checkin.html',
        controller: 'CheckInCtrl'
      })
      .when('/add_checkin', 
      {
        templateUrl: 'static/partials/add_checkin.html',
        controller: 'AddCheckinCtrl'
      })
      .otherwise(
      {
        redirectTo: "/"
      });
});

// These are the resources that we are getting from the web app
// Helps us update models from the api
myApp.factory('Patient', function($resource) {
  return $resource('/patients/:nhi');
});

myApp.factory('CheckIn', function($resource) {
  return $resource('/patients/:nhi/checkins/:checkin_id');
});

myApp.factory('Department', function($resource) {
  return $resource('/departments/:department_id');
});
