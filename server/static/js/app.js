var myApp = angular.module('vsmApp', [], function($interpolateProvider) {
    $interpolateProvider.startSymbol('<[');
    $interpolateProvider.endSymbol(']>');
});

function PatientListCtrl($scope, $http){
  $http.get('/patients/').success(function(data) {
    $scope.patients = data.patients;
    for (var i = 0 ; i < $scope.patients.length ; i++) {
      $scope.patients[i].fullname = $scope.patients[i].firstname + $scope.patients[i].lastname;
    }
  });

  $scope.orderProp = 'patient_id';
}

