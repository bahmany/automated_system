'use strict';


angular.module('AniTheme').controller(
    'ExportPreviewCtrl',
    function ($scope,
              $translate,
              $q,
              $rootScope,
              $stateParams,
              $modal,
              $location,
              $http,
              ExportPreviewService) {
        $scope.ExportLetter = {};
        $scope.UploadedFiles = {};
        $scope.Openletter = function () {
            $http.get("/api/v1/letter/sec/export/" + $stateParams.exportid + "/get_prev/?id=" + $stateParams.exportid).then(function (data) {
                $scope.ExportLetter = data.data;
                $scope.UploadedFiles = {};
                if ($scope.ExportLetter.attachments) {
                    $scope.UploadedFiles.files = $scope.ExportLetter.attachments;
                }
            })
        };
        $scope.Openletter();
        $scope.prepareDownloadUrl = function (url) {
            return url.replace("thmum50_", "");
        }

    });