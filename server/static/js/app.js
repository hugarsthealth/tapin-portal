var myApp = angular.module('vsmApp', ['ngCookies', 'ngBreadcrumbs']);

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

function LoginCtrl ($scope, $cookies, $location) {
  if ('department' in $cookies) {
    $location.path('/patients');
  }
}

function VitalInfoCtrl ($scope, $http, $routeParams) {
  $http.get('/patients/' + $routeParams.nhi).success(function(data) {
    console.log(data);
    $scope.patient = data.patient;
  });
  $http.get('/patients/' + $routeParams.nhi + '/vitalinfos/' + $routeParams.vital_info_id).success(function(data) {
    console.log(data);
    $scope.vitalinfo = data.vitalinfo;
  });
  //Works but throws errors in console
  //Returns true which is used with ng-show to show the overseas recently div if the overseas_recently parameter is true
  $scope.ShowOverseasRecentlyDiv = function(){
    console.log(String($scope.vitalinfo.overseas_recently)=="true");
    return String($scope.vitalinfo.overseas_recently)=="true";
  };
}

function PatientCtrl($scope, $http, $routeParams) {
  $http.get('/patients/' + $routeParams.nhi).success(function(data) {
    $scope.patient = data.patient;
    console.log($scope.patient);
  });
  $http.get('/patients/' + $routeParams.nhi + '/vitalinfos').success(function(data) {
    console.log(data);
    $scope.vitalinfos = data.vitalinfos;
  });

  $scope.sortByChange = function() {
    if ($scope.sortBy === "check_in_time") {
      $scope.reverseCheckIns = true;
    }  else {
      $scope.reverseCheckIns = false;
    }
  };

  $scope.sortBy = "check_in_time";
  $scope.reverseCheckIns = true;
}

function PatientListCtrl($scope, $http){
  $http.get('/patients/').success(function(data) {
    $scope.patients = data.patients;
    console.log($scope.patients);
    for (var i = 0 ; i < $scope.patients.length ; i++) {
      $scope.patients[i].fullname = $scope.patients[i].latest_vitalinfo.firstname + " " + $scope.patients[i].latest_vitalinfo.lastname;
    }
  });

  $scope.orderProp = 'patient_id';
  $scope.searchBy = "fullname";

  $scope.searchBarChange = function() {
    if (!$scope.queryString) {
      // if there is no query, don't filter
      $scope.query = true;
      return;
    }

    $scope.query = {};
    if ($scope.searchBy === "fullname") {
      $scope.query.fullname = $scope.queryString;
    } else {
      $scope.query.nhi = $scope.queryString;
    }
  };

  $scope.searchByChange = function () {
    $scope.searchBarChange();
  };
}

angular.module('ngBreadcrumbs', []).factory('BreadCrumbsService', function($rootScope, $log) {
    var data = {};
    var ensureIdIsRegistered = function(id) {
        if (angular.isUndefined(data[id])) {
            data[id] = [];
        }
    };
    return {
        push: function(id, item) {
            ensureIdIsRegistered(id);
            data[id].push(item);
            $log.log( "$broadcast" );
            $rootScope.$broadcast( 'breadcrumbsRefresh' );
        },
        get: function(id) {
            ensureIdIsRegistered(id);
            return angular.copy(data[id]);
        },
        setLastIndex: function( id, idx ) {
            ensureIdIsRegistered(id);
            if ( data[id].length > 1+idx ) {
                data[id].splice( 1+idx, data[id].length - idx );
            }
        }
    };
}).directive('breadCrumbs', function($log, BreadCrumbsService) {
    return {
        restrict: 'A',
        template: '<ul class="breadcrumb"><li ng-repeat=\'bc in breadcrumbs\' ng-class="{\'active\': {{$last}} }"><a ng-click="unregisterBreadCrumb( $index )" ng-href="{{bc.href}}">{{bc.label}}</a><span class="divider" ng-show="! $last">|</span></li></ul>',
        replace: true,
        compile: function(tElement, tAttrs) {
            return function($scope, $elem, $attr) {
                var bc_id = $attr['id'],
                    resetCrumbs = function() {
                        $scope.breadcrumbs = [];
                        angular.forEach(BreadCrumbsService.get(bc_id), function(v) {
                            $scope.breadcrumbs.push(v);
                        });
                    };
                resetCrumbs();
                $scope.unregisterBreadCrumb = function( index ) {
                    BreadCrumbsService.setLastIndex( bc_id, index );
                    resetCrumbs();
                };
                $scope.$on( 'breadcrumbsRefresh', function() {
                    $log.log( "$on" );
                    resetCrumbs();
                } );
            };
        }
    };

});

function breadCrumbsCtrl($scope, BreadCrumbsService){
  $scope.pushIndex = function() {
    console.log('Add patient index');
    BreadCrumbsService.push( 'myBreadCrumbs', {
        href: '#/',
        label: 'Patient Index'
    });
  };
  $scope.pushPatientCrumb = function() {
    console.log('Add patient crumb');
    BreadCrumbsService.push( 'myBreadCrumbs', {
      href: '#/patients/'+$scope.patient.nhi,
      label: 'Patient ' +$scope.patient.nhi
    });
  };
}