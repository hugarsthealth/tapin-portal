function AddCheckinCtrl ($scope, PatientSummary) {
  
  $scope.searchBy = "name";
  $scope.creatingPatient = false;

  $scope.searchBarChange = function() {
    if (!$scope.queryString) {
        // if there is no query, don't filter
        $scope.query = {};
        return;
    }

    $scope.query = {};
    if ($scope.searchBy === "name") {
        $scope.query.name = $scope.queryString;
    } else {
        $scope.query.nhi = $scope.queryString;
    }
  };

  $scope.searchByChange = function () {
    $scope.searchBarChange();
  };

  $scope.newPatient = function() {
    alert($scope.creatingPatient);
    $scope.creatingPatient = true;
  };

  $scope.patients = PatientSummary.query({}, function(patients) {});
}