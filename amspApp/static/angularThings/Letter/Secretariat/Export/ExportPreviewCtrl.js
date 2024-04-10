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
            $http.get("api/v1/letter/sec/export/" + $stateParams.exportid + "/get_prev/?id=" + $stateParams.exportid).success(function (data) {
                $scope.ExportLetter = data;
                $scope.UploadedFiles.files = data.letter.attachments;
            })
        };
        $scope.Openletter();
        $scope.prepareDownloadUrl = function (url) {
            return url.replace("thmum50_", "");
        }

    });