function PatientCardCtrl ($scope) {
  $scope.expandedPatients = [];

  $scope.expandPatient = function(nhi) {
    $scope.expandedPatients.push(nhi);
  };

  $scope.retractPatient = function(nhi) {
    var patientIndex = $scope.expandedPatients.indexOf(nhi);

    if (patientIndex > -1) {
      $scope.expandedPatients.splice(patientIndex, 1);
    }
  };
}
