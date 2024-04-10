'use strict';


function LoadSteps($rootScope, $scope, $http, $location) {
    $scope.Get = function (step, jsonObjStr) {
        $http.get("/reg/api/v1/login/" + step + "/getstep/").then(function (data) {
            $scope[jsonObjStr] = data.data;


        })
    };

    //$scope.Get(currentStep, jsonObjStr);

    $scope.Post = function (step, jsonObj) {
        $http.post("/reg/api/v1/login/" + step + "/step/", jsonObj).then(function (data) {
            $rootScope.$broadcast("showToast", "اطلاعات شما با موفقیت ثبت شد");
            $location.url("/home/profile/step" + (parseInt(step) + 1).toString());

        })
    }
}