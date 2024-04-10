'use strict';


angular.module('AniTheme').controller(
    'ExportTemplateCtrl',
    function ($scope,
              $translate,
              $q,
              $rootScope,
              $stateParams,
              $modal,
              $location,
              $http, Upload) {


        $scope.Templates = {};

        $scope.GetTemplates = function () {
            $http.get("api/v1/letter/sec/export-templates/?id=" + $stateParams.exportid).success(function (data) {
                $scope.Templates = data;
            });
        };

        $scope.DownloadOriginal = function () {

        }

        $scope.GetTemplates();


        $scope.UploadedFile = {};


        $scope.upload = function (files) {
            Upload.upload({
                method: 'POST',
                data: {file: files[0]},
                file: files[0],
                headers: {'Content-Type': files[0].type},
                url: 'api/v1/file/upload'
            }).then(function (resp) {
                $scope.UploadedFile = resp.data;

            }, function (resp) {
                return 0;
            }, function (evt) {
                return 0;
            });

        };

        $scope.Template = {};

        $scope.Post = function () {
            if (!($scope.UploadedFile.name)) {
                sweetAlert("Oops...", "upload a template file", "error");
                return
            }
            if (!($scope.Template.name)) {
                sweetAlert("Oops...", "template name is require", "error");
                return
            }
            $scope.Template.fileAddr = $scope.UploadedFile.name;
            $http.post("api/v1/letter/sec/export-templates/", $scope.Template).success(function (data) {
                $scope.Clear();
                $scope.GetTemplates();
            });
        };


        $scope.Edit = function (item) {
            $scope.Template = item;
            $scope.UploadedFile.name = $scope.Template.fileAddr;
        };

        $scope.Clear = function () {
            $scope.Template = {};
            $scope.UploadedFile = {};
        };
        $scope.Delete = function (item) {
            swal({
                title: "Are you sure?",
                text: "You will not be able to recover this template file!",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "Yes, delete it!",
                closeOnConfirm: false,
                showLoaderOnConfirm: true
            }, function () {
                $http.delete("api/v1/letter/sec/export-templates/" + item.id + "/").success(function (data) {
                    $scope.GetTemplates();
                    $scope.Clear();
                    swal("Deleted!", "Your template has been deleted.", "success");
                });
            });
        };

        $scope.Preview = function (item) {
            $http.get("api/v1/letter/sec/export-templates/" + $stateParams.exportid + "/Preview/?id=" + item.id).success(function (data) {
                downloadURL(data.addr);
            })
        };

        $scope.PreviewDefs = function (item) {
            $http.get("api/v1/letter/sec/export-templates/" + $stateParams.exportid + "/Preview/?id=" + item).success(function (data) {
                downloadURL(data.addr);
            })
        };


        $scope.Download = function (filename) {
            $http.get("api/v1/letter/sec/export-templates/" + filename + "/Download/").success(function (data) {
                downloadURL(data.addr);
            })
        }
    });