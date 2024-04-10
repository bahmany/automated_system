'use strict';


angular.module('AniTheme').controller(
    'ExportScanCtrl',
    function ($scope,
              $translate,
              $q,
              $rootScope,
              $stateParams,
              $modal,
              $location,
              $http, Upload) {


        $scope.UploadedFiles = [];
        $scope.Scans = {};
        $scope.Scan = {};
        loadUploader($scope, $http, Upload);
        $scope.Recieve = {};


        $scope.Post = function () {
            $scope.Scan.fileAddr = $scope.UploadedFiles;
            ////console.log($scope.UploadedFiles);
            $scope.Scan.inboxID = $stateParams.exportid;
            $http.post("api/v1/letter/sec/export-scan/", $scope.Scan).success(function (data) {
                $scope.list();
                $scope.Clear();
            }).error(function (data) {
                sweetAlert("Oops...", "Complete the requirements", "error");
                return
            })

        };

        $scope.Recieveds = {};


        $scope.Clear = function () {
            $scope.Scan = {};
            $scope.UploadedFiles = [];
        };

        $scope.list = function () {
            $http.get("api/v1/letter/sec/export-scan/?id=" + $stateParams.exportid).success(function (data) {
                $scope.Scans = data;
            })
        };
        $scope.list();

    });