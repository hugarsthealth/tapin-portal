define([
  'angular',
  'ngCookies',
  'ngResource',
  'services',
  'controllers'
  ], function (angular, filters, services, directives, controllers) {
    'use strict';

    return angular.module('tapin', ['tapin.controllers', 'tapin.services', 'ngCookies', 'ngResource']);
});
