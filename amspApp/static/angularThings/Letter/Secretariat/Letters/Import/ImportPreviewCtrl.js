'use strict';


angular.module('AniTheme').controller(
    'ImportPreviewCtrl',
    function ($scope,
              $translate,
              $q,
              $state,
              $stateParams,
              $rootScope,
              $modal,
              $compile,
              $timeout,
              $http) {

        $scope.Download = function (filename) {
            downloadURL("/api/v1/file/upload?q=" + filename.imgInf.orgname);
        };


        $scope.init = function () {
            if ($stateParams.importid) {
                $http.get("/api/v1/letter/sec/export-import/" + $stateParams.importid + "/get_prev/?id=" + $stateParams.importid).then(function (data) {
                    $scope.ImportLetter = data.data.letter;
                    $scope.ImportLetter.tags = data.data.tags;
                    $scope.UploadedFiles = $scope.ImportLetter.attachments;
                })
            } else {
                $scope.ImportLetter = {};
            }
        };


        $scope.Pending = false;
        $scope.init();

        TagClass($scope, $http, $q, 2);

    });