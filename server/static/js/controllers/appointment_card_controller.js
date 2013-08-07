function AppointmentCardCtrl ($scope) {
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
