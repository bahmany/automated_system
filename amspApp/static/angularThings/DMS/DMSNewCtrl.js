'use strict';

angular.module('AniTheme').controller('DMSNewCtrl', function ($q, $location, $http, $scope, $state, $stateParams, $rootScope, Upload, DMSManagementService) {
    $scope.newDMS = {};
    $scope.newDMS.allFiles = [];
    $scope.editDMS = {};
    $scope.listDMS = [];
    $scope.docdata = [];
    $scope.errors = [];
    $scope.createDMS = function () {
        DMSManagementService.createDMS($stateParams.companyid, $scope.newDMS).then(function (data) {
            swal("سند به سیستم اضافه شد!", "success");
            $state.go("dms", {companyid: $stateParams.companyid});
        }).catch(function (data) {
            $scope.errors = data.data.message;
        });
    };

    $scope.fixCheckCurr = function (dirName) {
        for (var i = 0; i < $scope.newDMS.allFiles.length; i++) {
            if ($scope.newDMS.allFiles[i].dir == dirName) {
                $scope.newDMS.allFiles[i].isCurr = true;
            } else {
                $scope.newDMS.allFiles[i].isCurr = false;
            }
        }
    };
    $scope.DMSSsettings = function () {
        DMSManagementService.getDMSSettings($stateParams.companyid).then(function (data) {
            $scope.docdata = data.data;

        }).catch(function (data) {

        });
    };

    $scope.addFileDetailToNew = function (companyid, fileID) {
        DMSManagementService.getFile(companyid, fileID).then(function (data) {
            $scope.newDMS.allFiles.push(data);
        });
    };
    $scope.pleaseWait = false;


    $scope.upload = function (files) {
        $scope.pleaseWait = true;
        Upload.upload({
            method: 'POST',
            data: {file: files[0]},
            file: files[0],
            headers: {'Content-Type': files[0].type},
            url: '/api/v1/file/upload'
        }).then(function (resp) {
            $scope.pleaseWait = false;

            $scope.addFileDetailToNew($stateParams.companyid, resp.data.name);
        }, function (resp) {
            $scope.pleaseWait = false;
            return 0;
        }, function (evt) {
            $scope.pleaseWait = false;
            return 0;
        });

    };
    $scope.DMSSsettings();
});

