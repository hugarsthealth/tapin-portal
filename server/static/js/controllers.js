// Controls the logining in and out of the application
function LoginCtrl ($scope, $cookies, $location, $route, Department) {
  $scope.departments = Department.query();

  $scope.enter = function() {
    if ($scope.department) {
      $cookies.department = $scope.department.department_name;
      document.location = '/';  // screw it
    } else {
      toastr.warning("Please select a department");
    }
  };

  if ('department' in $cookies) {
    $location.path('/patients');
  }
}

// controls the display and editing of a vital info
function VitalInfoCtrl ($scope, $routeParams, $cookies, $location, $route, Patient, VitalInfo) {
  if (!('department' in $cookies)) {
    $location.path('/');
  }
  $scope.currentlyEditing = false;
  $scope.editingList = null;
  $scope.editingPos = null;

  $scope.editVitalInfo = function () {
    $scope.currentlyEditing = true;
  };

  $scope.saveChanges = function () {
    // Need all these checks to delete empty fields from the list
    if ($scope.vitalinfo.overseas_dests[$scope.vitalinfo.overseas_dests.length-1] === "") {
      $scope.vitalinfo.overseas_dests.splice($scope.vitalinfo.overseas_dests.length-1,1);
    }
    if ($scope.vitalinfo.allergies[$scope.vitalinfo.allergies.length-1] === "") {
      $scope.vitalinfo.allergies.splice($scope.vitalinfo.allergies.length-1,1);
    }
    if ($scope.vitalinfo.medical_conditions[$scope.vitalinfo.medical_conditions.length-1] === "") {
      $scope.vitalinfo.medical_conditions.splice($scope.vitalinfo.medical_conditions.length-1,1);
    }
    if ($scope.vitalinfo.family_hist[$scope.vitalinfo.family_hist.length-1] === "") {
      $scope.vitalinfo.family_hist.splice($scope.vitalinfo.family_hist.length-1,1);
    }

    // Gotta save that stuff
    $scope.currentlyEditing = false;
    $scope.vitalinfo.$save({"nhi": $routeParams.nhi, "vital_info_id": $routeParams.vital_info_id},
      function() {
        toastr.success("Saved changes");
        $route.reload();
      },
      function() {
        toastr.error("Failed to save changes");
      });
  };

  $scope.cancelEditing = function () {
    $route.reload();
  };

  $scope.saveChangeIntoList = function (element) {
    $scope.editingList[$scope.editingPos] = element;

    console.log(element);
    $scope.editingList = null;
    $scope.editingPos = null;
  };

  $scope.prepareChangeIntoList = function (element, viList) {
    $scope.editingList = viList;
    $scope.editingPos = viList.indexOf(element);
    console.log("preparing edit for " + element + " at " + viList.indexOf(element));
  };

  $scope.deleteFromList = function(element, elements) {
    var index = elements.indexOf(element);
    elements.splice(index, 1);
  };

  $scope.addToList = function(viList) {
    console.log(viList);
    for (var i = 0; i< viList.length ; i++) {
      if (viList[i] === "") {
        toastr.error("Can not create another blank entry.");
        return;
      }
    }
    viList.push("");
  };

  $scope.patient = Patient.get({"nhi": $routeParams.nhi});
  $scope.vitalinfo = VitalInfo.get({"nhi": $routeParams.nhi, "vital_info_id": $routeParams.vital_info_id});
}

// Controller for viewing a single patient
function PatientCtrl($scope, $routeParams, $cookies, $location, Patient, VitalInfo) {
  if (!('department' in $cookies)) {
    $location.path('/');
  }

  $scope.patient = Patient.get({"nhi": $routeParams.nhi});
  $scope.vitalinfos = VitalInfo.query({"nhi": $routeParams.nhi});

  $scope.deletePatient = function(index) {
    if(!confirm("Are you sure you wish to delete " + $scope.patient.latest_vitalinfo.firstname + " " + $scope.patient.latest_vitalinfo.lastname + "?"))
      return;

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

// Controller for the entire list of patients
function PatientListCtrl($scope, $cookies, $location, Patient){
  if (!('department' in $cookies)) {
    $location.path('/');
  }

  $scope.deletePatient = function(index) {
    var deleted = $scope.patients.splice(index, 1)[0];

    if(!confirm("Are you sure you wish to delete " + deleted.latest_vitalinfo.firstname + " " + deleted.latest_vitalinfo.lastname + "?")) {
      $scope.patients.splice(index, 0, deleted);
      return;
    }

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

// Controller for the nav bar
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

// Controller for the breadcrumbs
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
