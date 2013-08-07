function AddCheckinCtrl ($scope, PatientSummary, $http) {
  
  $scope.searchBy = "name";
  $scope.creatingPatient = false;
  $scope.makingCheckin = false;
  $scope.patientNHI;

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

  $scope.displayCheckinCreate = function(nhi) {
    // Get the patient and their lastest checkin. use it to populate the form
    var url = '/patients/' + nhi.toString();
    $http.get(url).success(function(data, status, headers, config) {
      $scope.patientNHI = data.nhi;
      $scope.checkin = create_checkin(data.latest_checkin);
      console.log($scope.checkin);
      $scope.makingCheckin = true;
    });
  }

  var create_checkin = function(checkin) {
    if (checkin !== null) {
      delete checkin.patient_nhi;
      delete checkin.checkin_id;
      return checkin;
    }

    return create_empty_checkin();
  }

  var create_empty_checkin = function() {
    return {
        "drinker": false,
        "occupation": "",
        "citizen_resident": false,
        "contact_num": "",
        "checkin_time": "",
        "allergies": [
            ""
        ],
        "overseas_dests": [
            "",
        ],
        "location": "",
        "blood_type": "",
        "weight_unit": "",
        "firstname": "",
        "lastname": "",
        "height_value": 0,
        "family_hist": [
            ""
        ],
        "height_unit": "",
        "weight_value": 0,
        "overseas_recently": false,
        "dob": "",
        "gender": "",
        "smoker": false,
        "medical_conditions": [
            ""
        ]
    }
  }

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

  $scope.createPatient = function(nhi) {
    var data = {"nhi": nhi};
    var url = "/patients"
    $http.post(url, data).success(function(data, status, headers, config) {
      $scope.displayCheckinCreate(nhi)
    });
  }
}