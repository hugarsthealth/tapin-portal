define(['angular'], function (angular) {
  'use strict';

  return angular.module('tapin.services', [])

  .factory('Patient', function($resource) {
    return $resource('/patients/:nhi');
  })

  .factory('PatientSummary', function($resource) {
    return $resource('/patient_summaries/:nhi');
  })

  .factory('CheckIn', function($resource) {
    return $resource('/patients/:nhi/checkins/:checkin_id');
  })

  .factory('Department', function($resource) {
    return $resource('/departments/:department_id');
  })

  .factory('Appointment', function($resource) {
    return $resource('/appointments/:appointment_id');
  });
});
