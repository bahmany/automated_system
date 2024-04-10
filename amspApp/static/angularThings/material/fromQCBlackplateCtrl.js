'use strict';


angular.module('AniTheme').controller(
    'fromQCBlackplateCtrl',
    function ($scope,
              $translate,
              $http, $filter,
              $q, $mdDialog, $element,
              $rootScope, toastConfirm,
              $modal) {


        $scope.qcList = {};

        $scope.list = function () {
            $http.get('/api/v1/barcodes/getQCBLProblems/').then(function (data) {
                $scope.qcList = data.data;
            })
        }

        $scope.init = function () {
            $scope.list();
        }

        $scope.init();


        $scope.updateqc = function (item) {
            $http.post('/api/v1/barcodes/postqcbp/', item).then(function (data) {
                // if (data.data.id) {
                    $scope.list();

                // }
            })
        }
        $scope.convertToScrap = function (item, $index) {
            $scope.selectedItem = item;
            $scope.selectedIndex = item;
            toastConfirm.showConfirm("آیا شما اطمینان دارید ؟").then(function () {
                $http.post('/api/v1/barcodes/convertToScrap/', $scope.selectedItem).then(function (data) {
                    if (data.data.id) {
                        $scope.qcList.splice($scope.selectedIndex, 1);
                    }
                })
            }).catch(function (error) {
                // pass the error to the error service
                return error;
            })


        }

    });