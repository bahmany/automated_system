'use strict';


function PrepareServerTimes($scope, $http) {
    $scope.CurrentTime = "";
    $scope.GetDateTime = function () {
        $http.get("/api/v1/getcurrenttime/").then(function (data) {
            $scope.CurrentTime = data.data.currentDatetime
        });
    }
    $scope.GetDateTime();
}