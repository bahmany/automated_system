'use strict';

angular.module('AniTheme').controller('DMSManagementCtrl', function ($q, $location, $http, $scope, $state, $stateParams, $rootScope, Upload, DMSManagementService) {
    $scope.newDMS = {};
    $scope.newDMS.allFiles = [];
    $scope.editDMS = {};
    $scope.listDMS = [];
    $scope.docdata = [];
    $scope.getlistDMS = function () {
        DMSManagementService.getDMSlist($stateParams.companyid).then(function (data) {
            $scope.listDMS = data.data;

        }).catch(function (data) {

        });
    };
    $scope.pleaseWait = false;

    $scope.createDMS = function () {

        $scope.pleaseWait = true;
        DMSManagementService.createDMS($stateParams.companyid, $scope.newDMS).then(function (data) {
            $scope.getlistDMS();
                $scope.pleaseWait = false;
            swal("سند به سیستم اضافه شد!", "success");
            $state.go("dms", {companyid: $stateParams.companyid});
        }).catch(function (data) {

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

    $scope.prepareEditDMS = function (id) {
        $scope.selectedDMS = id;
        $state.go("edit-dms", {companyid: $stateParams.companyid, DMSId: id});

    };

    $scope.updateDMS = function (id) {
        DMSManagementService.updateDMS($stateParams.companyid, id, $scope.editDMS).then(function (data) {
            $scope.getlistDMS();
            $state.go("dms", {companyid: $stateParams.companyid});

        }).catch(function (data) {

        });
    };

    $scope.destroyDoc = function (id) {
        swal({
            title: "آیا به حذف این سند مطمئن هستید؟ ",
            text: "این سند از سیستم حذف خواهد شد, وقابل بازگرداندن نخواهد بود. ",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "بله!",
            showLoaderOnConfirm: true,
            closeOnConfirm: true
        }, function () {
            DMSManagementService.destroyDMS($stateParams.companyid, id).then(function () {
                $scope.getlistDMS();
                swal("خذف شد!", "سند از سیستم حذف شد.", "success");
                $state.go("dms", {companyid: $stateParams.companyid});
            }).catch(function (data) {
                swal("دسترسی!", "شما اجازه دسترسی به حذف این فرایند ندارید.", "error");
            });

        });

    };
    $rootScope.$on('$locationChangeSuccess', function (e, newUrl, oldUrl) {
        // debugger;
        if (((oldUrl.split('/#/dashboard/')[1].split('/dms/')[1].split('/')[0] == 'new') || (oldUrl.split('/#/dashboard/')[1].split('/dms/')[1].split('/')[0] == 'edit')) && (newUrl.split('/#/dashboard/')[1].split('/dms')[1] == '')) {
            $scope.getlistDMS();

        }
    });
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
            return 0;
        }, function (evt) {
            return 0;
        });

    };
    $scope.getlistDMS();
    $scope.DMSSsettings();
});

