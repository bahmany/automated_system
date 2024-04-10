/**
 * Created by mohammad on 12/20/15.
 */


'use strict';


angular.module('AniTheme').controller(
    'SecretariatCtrl',
    function ($scope,
              $translate,
              $stateParams,
              $q,$state,
              $rootScope,
              $modal,
              $http) {
        $scope.GetDefaultDabir = function (items) {
            for (var i = 0; items.length > i; i++) {
                if (items[i].default) {
                    return items[i].name;
                }
            }
            return ""
        };
        $scope.ExportLetter = {};
        $scope.PrepareToSend = function (letterType) {
            //var sss = angular.copy($scope.ExportLetter);
            //$scope.ExportLetter.recievers = $scope.SelectedMemebrs; // roonevesht recievers
            if ($scope.UploadedFiles) {
                $scope.ExportLetter.attachments = $scope.UploadedFiles.files;
            }
            $scope.ExportLetter.letterType = letterType;
            return $scope.ExportLetter
        };

        $scope.NewExport = function () {
            $scope.ExportLetter = $scope.PrepareToSend(8);
            $http.post('/api/v1/letter/sec/export/',$scope.ExportLetter).then(function (data) {
                $state.go("exportNew", {exportid: data.data.exp.baseInbox});
            });
        };

        ActivateSelectSec($scope, $http, $stateParams);

    });


