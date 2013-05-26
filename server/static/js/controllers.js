function LoginCtrl ($scope, $cookies, $location, Department) {
  $scope.departments = Department.query({}, function(ds) {
    $scope.department = ds[0];
  });

  if ('department' in $cookies) {
    $location.path('/patients');
  }
}

function VitalInfoCtrl ($scope, $routeParams, $cookies, $location, Patient, VitalInfo) {
  if (!('department' in $cookies)) {
    $location.path('/');
  }

  $scope.patient = Patient.get({"nhi": $routeParams.nhi});
  $scope.vitalinfo = VitalInfo.get({"nhi": $routeParams.nhi, "vital_info_id": $routeParams.vital_info_id});
}

function PatientCtrl($scope, $routeParams, $cookies, $location, Patient, VitalInfo) {
  if (!('department' in $cookies)) {
    $location.path('/');
  }

  $scope.patient = Patient.get({"nhi": $routeParams.nhi});
  $scope.vitalinfos = VitalInfo.query({"nhi": $routeParams.nhi});

  $scope.deletePatient = function(index) {
    $scope.patient.$delete({"nhi": $scope.patient.nhi},
      function() {
        toastr.success('Successfully deleted', $scope.patient.nhi);
        $location.path('/patients');
      },
      function() {
        toastr.error('Could not be deleted', $scope.patient.nhi);
      });
  };

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

function PatientListCtrl($scope, $cookies, $location, Patient){
  if (!('department' in $cookies)) {
    $location.path('/');
  }

  $scope.deletePatient = function(index) {
    var deleted = $scope.patients.splice(index, 1)[0];

    deleted.$delete({"nhi": deleted.nhi},
      function() {
        toastr.success('Successfully deleted', deleted.nhi);
      },
      function() {
        toastr.error('Could not be deleted', deleted.nhi);
        $scope.patients.splice(index, 0, deleted);
      });
  };

  $scope.patients = Patient.query({}, function(patients) {
    patients.forEach(function(p) {
      p.fullname = p.latest_vitalinfo.firstname + " " + p.latest_vitalinfo.lastname;
    });
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

function NavBarCtrl($scope, $cookies, $location){
  if ('department' in $cookies) {
    $scope.logged_in = true;
    $scope.department = $cookies.department;
  }

  $scope.signOut = function() {
    //console.log("Deleting cookie")
    delete $cookies.department;
    $location.path('/');
    $scope.logged_in = false;
  };
}

function BreadCrumbsCtrl($scope, $location, $route){
  $scope.$on('$routeChangeSuccess', function() {

    var path = $location.path();
    $scope.bcs = path === "/" ? [] : path.split('/').slice(1);
    $scope.paths = {};
    $scope.show = false;

    $scope.bcs.forEach(function(bc) {
      $scope.show = true;

      // dat oneliner. forEach and indexOf only supported in IE9+
      $scope.paths[bc] = this.bcs.slice(0, this.bcs.indexOf(bc) + 1).join('/');
    }.bind($scope));
  });
}
