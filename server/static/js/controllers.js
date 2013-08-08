// Controls the logining in and out of the application
define(['angular', 'services'], function (angular) {
  'use strict';
  return angular.module('tapin.controllers', ['tapin.services'])

  .controller('LoginCtrl', ['$scope', '$cookies', '$location', '$route', 'Department',
    function ($scope, $cookies, $location, $route, Department) {
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
  ])

  .controller('CheckInCtrl', ['$scope', '$routeParams', '$cookies', '$location', '$route', 'Patient', 'CheckIn',
    function ($scope, $routeParams, $cookies, $location, $route, Patient, CheckIn) {
      if (!('department' in $cookies)) {
        $location.path('/');
      }
      $scope.currentlyEditing = false;
      $scope.editingList = null;
      $scope.editingPos = null;

      $scope.editCheckIn = function () {
        $scope.currentlyEditing = true;
      };

      $scope.saveChanges = function () {
        // Need all these checks to delete empty fields from the list
        if ($scope.checkin.overseas_dests[$scope.checkin.overseas_dests.length-1] === "") {
          $scope.checkin.overseas_dests.splice($scope.checkin.overseas_dests.length-1,1);
        }
        if ($scope.checkin.allergies[$scope.checkin.allergies.length-1] === "") {
          $scope.checkin.allergies.splice($scope.checkin.allergies.length-1,1);
        }
        if ($scope.checkin.medical_conditions[$scope.checkin.medical_conditions.length-1] === "") {
          $scope.checkin.medical_conditions.splice($scope.checkin.medical_conditions.length-1,1);
        }
        if ($scope.checkin.family_hist[$scope.checkin.family_hist.length-1] === "") {
          $scope.checkin.family_hist.splice($scope.checkin.family_hist.length-1,1);
        }

        // Gotta save that stuff
        $scope.currentlyEditing = false;
        $scope.checkin.$save({"nhi": $routeParams.nhi, "checkin_id": $routeParams.checkin_id},
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
      $scope.checkin = CheckIn.get({"nhi": $routeParams.nhi, "checkin_id": $routeParams.checkin_id});
    }
  ])

  .controller('PatientCtrl', ['$scope', '$routeParams', '$cookies', '$location', 'Patient', 'CheckIn',
    function ($scope, $routeParams, $cookies, $location, Patient, CheckIn) {
      if (!('department' in $cookies)) {
        $location.path('/');
      }

      $scope.patient = Patient.get({"nhi": $routeParams.nhi});
      $scope.checkins = CheckIn.query({"nhi": $routeParams.nhi});

      $scope.deletePatient = function(index) {
        if(!confirm("Are you sure you wish to delete " + $scope.patient.latest_checkin.firstname + " " + $scope.patient.latest_checkin.lastname + "?"))
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
        if ($scope.sortBy === "latest_checkin_time") {
          $scope.reverseCheckIns = true;
        }  else {
          $scope.reverseCheckIns = false;
        }
      };

      $scope.sortBy = "latest_checkin_time";
      $scope.reverseCheckIns = true;
    }
  ])

  .controller('PatientCardCtrl', ['$scope',
    function ($scope) {
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
  ])

  .controller('AppointmentCardCtrl', ['$scope',
    function ($scope) {
      $scope.expandedAppointments = [];
      $scope.patient = $scope.appointment.patient;

      $scope.expandAppointment = function(appointment_id) {
        $scope.expandedAppointments.push(appointment_id);
      };

      $scope.retractAppointment = function(appointment_id) {
        var appointmentIndex = $scope.expandedAppointments.indexOf(appointment_id);

        if (appointmentIndex > -1) {
          $scope.expandedAppointments.splice(appointmentIndex, 1);
        }
      };
    }
  ])

  .controller('PatientListCtrl', ['$scope', '$cookies', '$location', 'Patient', 'Appointment',
    // Controller for the entire list of patients
    function ($scope, $cookies, $location, Patient, Appointment){
      if (!('department' in $cookies)) {
        $location.path('/');
      }

      $scope.patients = Patient.query({}, function(patients) {
        patients.forEach(function(p) {
          p.fullname = p.latest_checkin.firstname + " " + p.latest_checkin.lastname;
        });
      });

      $scope.appointments = Appointment.query({});

      $scope.orderProp = 'patient_id';
      $scope.searchBy = "fullname";

      $scope.deletePatient = function(index) {
        var deleted = $scope.patients.splice(index, 1)[0];

        if(!confirm("Are you sure you wish to delete " + deleted.latest_checkin.firstname + " " + deleted.latest_checkin.lastname + "?")) {
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
          }
        );
      };

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
  ])

  .controller('NavBarCtrl', ['$scope', '$cookies', '$location',
    // Controller for the nav bar
    function ($scope, $cookies, $location){
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
  ])

  .controller('BreadCrumbsCtrl', ['$scope', '$location', '$route',
    // Controller for the breadcrumbs
    function ($scope, $location, $route){
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
  ])

  .controller('AddCheckinCtrl', ['$scope', 'PatientSummary', '$http',
    function ($scope, PatientSummary, $http) {

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
      };

      var create_checkin = function(checkin) {
        if (checkin !== null) {
          delete checkin.patient_nhi;
          delete checkin.checkin_id;
          return checkin;
        }

        return create_empty_checkin();
      };

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
        };
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

      $scope.createPatient = function(nhi) {
        var data = {"nhi": nhi};
        var url = "/patients";
        $http.post(url, data).success(function(data, status, headers, config) {
          $scope.displayCheckinCreate(nhi);
        });
      };
    }
  ]);
});
