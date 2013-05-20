function LoginCtrl ($scope, $cookies, $location) {
  if ('department' in $cookies) {
    $location.path('/patients');
  }

  if ('no_auth' in $cookies) {
    $scope.no_auth = true;
    delete $cookies.no_auth;
    console.log("no auth should have been deleted");
  } 

}

function VitalInfoCtrl ($scope, $http, $routeParams, $cookies, $location) {
  if (!('department' in $cookies)) {
    $location.path('/');
    $cookies.no_auth = true;
  }

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

function PatientCtrl($scope, $http, $routeParams, $cookies, $location) {
  if (!('department' in $cookies)) {
    $location.path('/');
    $cookies.no_auth = true;
  }

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

function PatientListCtrl($scope, $http, $cookies, $location){
  if (!('department' in $cookies)) {
    $location.path('/');
    console.log("got here");
    $cookies.no_auth = "true";
  }

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

function NavBarCtrl($scope, $cookies, $location){
  if ('department' in $cookies) {
    $scope.logged_in = true;
    $scope.department = $cookies.department;
  }

  $scope.signOut = function() {
    console.log("Deleting cookie")
    delete $cookies.department;
    $location.path('/');
    $scope.logged_in = false;
  }
}
