var myApp = angular.module('vsmApp', ['ngCookies']);

myApp.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('<[');
    $interpolateProvider.endSymbol(']>');
});

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
      .when('/patients/:nhi/vitalinfos', {
        redirectTo: "/patients/:nhi"
      })
      .when('/patients/:nhi/vitalinfos/:vital_info_id',
      {
        templateUrl: 'static/partials/vital_info.html',
        controller: 'VitalInfoCtrl'
      })
      .otherwise(
      {
        redirectTo: "/"
      });
});
