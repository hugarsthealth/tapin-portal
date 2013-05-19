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
    $scope.query = {};
    if ($scope.searchBy === "fullname") {
      $scope.query.fullname = $scope.queryString;
    } else {
      $scope.query.nhi = $scope.queryString;
    }
    console.log($scope.query);
  };

  $scope.searchByChange = function () {
    $scope.searchBarChange();
  };

}
