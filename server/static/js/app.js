var myApp = angular.module('vsmApp', []);

myApp.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('<[');
    $interpolateProvider.endSymbol(']>');
});

myApp.config(function($routeProvider) {
  $routeProvider
      .when('/',
      {
        templateUrl: 'static/partials/patient_index.html',
        controller: 'PatientListCtrl'
      })
      .otherwise(
      {
        redirectTo: "/"
      })
});

function AppController($scope) {

}

function PatientListCtrl($scope, $http){
  $http.get('/patients/').success(function(data) {
    $scope.patients = data.patients;
    console.log($scope.patients);
    for (var i = 0 ; i < $scope.patients.length ; i++) {
      $scope.patients[i].fullname = $scope.patients[i].firstname + $scope.patients[i].lastname;
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