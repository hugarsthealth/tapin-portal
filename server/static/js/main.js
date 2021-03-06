require.config({
    baseUrl: 'static/js',

    paths: {
        'angular': 'vendor/angular.min',
        'ngCookies': 'vendor/angular-cookies.min',
        'ngResource': 'vendor/angular-resource.min',
        'ngUIUtils': 'vendor/angular-ui-utils'
    },

    shim: {
        'angular' : {'exports' : 'angular'},
        'ngCookies' : {deps: ['angular']},
        'ngResource' : {deps: ['angular']},
        'ngUIUtils' : {deps: ['angular']},
        'angularMocks': {deps:['angular'], 'exports':'angular.mock'}
    },

    priority: [
        "angular"
    ]
});

require(['angular', 'app', 'routes'],
    function(angular, app, routes) {
        'use strict';
        angular.bootstrap(document, [app['name']]);
    }
);
