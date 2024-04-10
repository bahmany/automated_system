'use strict';

angular.module('AniTheme').controller('DMSEditCtrl', function ($q, $location, $http, $scope, $state, $stateParams, $rootScope, Upload, DMSManagementService) {
    $scope.newDMS = {};
    $scope.newDMS.allFiles = [];
    $scope.editDMS = {};
    $scope.listDMS = [];
    $scope.docdata = [];
    $scope.errors = [];

    $scope.fixCheckCurr = function (dirName) {
        for (var i = 0; i < $scope.editDMS.allFiles.length; i++) {
            if ($scope.editDMS.allFiles[i].dir == dirName) {
                $scope.editDMS.allFiles[i].isCurr = true;
            } else {
                $scope.editDMS.allFiles[i].isCurr = false;
            }
        }
    };

    $scope.prepareEditDMS = function () {
        DMSManagementService.getDMS($stateParams.companyid, $stateParams.DMSId).then(function (data) {
            $scope.editDMS = data.data;
            $scope.editDMS.docType = data.data.docTypeRead;
            $scope.editDMS.docZone = data.data.docZoneRead;
            $scope.editDMS.docModel = data.data.docModelRead;
            $scope.editDMS.docFormat = data.data.docFormatRead;
            $scope.editDMS.docRelated = data.data.docRelatedRead;
            $scope.editDMS.id = $stateParams.DMSId;
        });

    };
    $scope.prepareEditDMS();
    $scope.updateDMS = function (id) {
        DMSManagementService.updateDMS($stateParams.companyid, id, $scope.editDMS).then(function (data) {
            $state.go("dms", {companyid: $stateParams.companyid});
            // $scope.listDMS();

        }).catch(function (data) {
            $scope.errors = data.data;

        });
    };

    $scope.DMSSsettings = function () {
        DMSManagementService.getDMSSettings($stateParams.companyid).then(function (data) {
            $scope.docdata = data.data;

        }).catch(function (data) {

        });
    };

    $scope.addFileDetailToNew = function (companyid, fileID) {
        DMSManagementService.getFile(companyid, fileID).then(function (data) {
            $scope.editDMS.allFiles.push(data.data);
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

