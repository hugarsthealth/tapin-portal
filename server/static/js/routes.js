define(['angular', 'app'], function(angular, app) {
  'use strict';

  app.config(function($routeProvider) {
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
      .otherwise(
      {
        redirectTo: "/"
      });
  });

  // Need to use different symbols as flask uses {{ and }}
  app.config(function($interpolateProvider) {
      $interpolateProvider.startSymbol('<[');
      $interpolateProvider.endSymbol(']>');
  });
});
