'use strict';


angular.module('AniTheme').controller(
    'ExportRecievedCtrl',
    function ($scope,
              $translate,
              $q,
              $rootScope,
              $stateParams,
              $modal,
              $location,
              $http) {

        $scope.Recieve = {};
        $scope.Post = function () {

            if (!$scope.Recieve.timeOf || !$scope.Recieve.reciever) {
                sweetAlert("Oops...", "Complete the requirements", "error");
                return
            }

            $scope.Recieve.inboxID = $stateParams.exportid;
            if ($scope.Recieve.id) {
                $http.patch("api/v1/letter/sec/recieved/" + $scope.Recieve.id + "/?id=" + $stateParams.exportid, $scope.Recieve).success(function (data) {
                    $scope.list();
                }).error(function (data) {
                    sweetAlert("Oops...", "Complete the requirements", "error");
                    return
                })
            } else {
                $http.post("api/v1/letter/sec/recieved/", $scope.Recieve).success(function (data) {
                    $scope.list();
                }).error(function (data) {
                    sweetAlert("Oops...", "Complete the requirements", "error");
                    return
                })
            }
        };

        $scope.Recieveds = {};

        $scope.edit = function (item) {
            $scope.Recieve = item;
        };


        $scope.Clear = function () {
            $scope.Recieve = {};
        };

        $scope.Delete = function () {
            swal({
                title: "Are you sure?",
                text: "You will not be able to recover this receiver file!",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "Yes, delete it!",
                closeOnConfirm: false,
                showLoaderOnConfirm: true
            }, function () {
                $http.delete("api/v1/letter/sec/recieved/" + $scope.Recieve.id + "/?id=" + $stateParams.exportid).success(function (data) {
                    $scope.list();
                    $scope.Clear();
                    swal("Deleted!", "Your receiver has been deleted.", "success");
                });
            });
        };

        $scope.list = function () {
            $http.get("api/v1/letter/sec/recieved/?id=" + $stateParams.exportid).success(function (data) {
                $scope.Recieveds = data;
            })
        };
        $scope.list();

    });