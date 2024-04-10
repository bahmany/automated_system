'use strict';


function signBodyCtrl($scope,
                      $translate,
                      $q,
                      $http,
                      $timeout,
                      $rootScope, $$$,
                      $mdToast,
                      dataToSend,
                      $mdDialog) {

    $scope.sign = {};
    $scope.error = "";

    $scope.sendWithoutCell = function ($event) {
        angular.element($event.target).attr("disabled", true);
        $scope.error = "";
        dataToSend.withSMS = false;
        dataToSend.signpass = $scope.sign.signpass;
        dataToSend.comment = $scope.sign.comment;
        $http.post(dataToSend.httppost, dataToSend).then(function (data) {
            if (data.data.errcode) {
                angular.element($event.target).attr("disabled", false);
                $scope.error = data.data.msg;
            }
            if (data.data.id) {
                angular.element($event.target).attr("disabled", false);
                if (data.data.HavalehForooshApproveLink) {
                    if (data.data.whichStep === 5) {
                        $http.post("/api/v1/havakehForoosh/sendAutomated_tolid/", {dt: data.data});
                    }
                    if (data.data.whichStep === 7) {
                        $http.post("/api/v1/havakehForoosh/sendAutomated_foroosh/", {dt: data.data});
                    }
                }
                $mdDialog.hide();
            }
        })
    }

    $scope.sendWithCell = function ($event) {
        angular.element($event.target).attr("disabled", true);

        $scope.error = "";
        dataToSend.withSMS = true;
        dataToSend.signpass = $scope.sign.signpass;
        // dataToSend.cellno = $scope.sign.cellno;
        dataToSend.comment = $scope.sign.comment;
        $http.post(dataToSend.httppost, dataToSend).then(function (data) {
            if (data.data.errcode) {
                angular.element($event.target).attr("disabled", false);

                $scope.error = data.data.msg;
            }
            if (data.data.id) {
                angular.element($event.target).attr("disabled", false);

                $mdDialog.hide();
            }
        })
    }


}

