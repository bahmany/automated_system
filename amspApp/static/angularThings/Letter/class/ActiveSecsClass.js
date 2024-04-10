'use strict';


function ActivateSelectSec($scope, $http, $stateParams) {
    $scope.PermittedSecratraitsList = {};
    $scope.GetAllActiveSecratriat = function () {
        $http.get("/api/v1/companies/"+$stateParams.companyid+"/secretariats/GetAllPermitted/").then(function (data) {
            $scope.PermittedSecratraitsList = data.data;
        })
    };
    $scope.GetAllActiveSecratriat();
    $scope.ChangeDefaultSecratrait = function (item) {
        $http.post("/api/v1/companies/"+$stateParams.companyid+"/secretariats/ChangeDefault/", {
            secretariat_id: item.secretariat_id
        }).then(
            function (data) {
                $scope.GetAllActiveSecratriat();
                $http.get("UpdateStatics").then(function (data) {
                    location.reload(true);
                });
            }).catch(function (data) {

            });
    };
}