define([
  'angular',
  'ngCookies',
  'ngResource',
  'ngUIUtils',
  'services',
  'controllers'
  ], function (angular, filters, services, directives, controllers) {
    'use strict';

    return angular.module('tapin', ['tapin.controllers', 'tapin.services', 'ngCookies', 'ngResource', 'ui.utils']);
});
