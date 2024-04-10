'use strict';


angular.module('AniTheme').controller(
    'tolidSaleConvSaleItemCtrl',
    function ($scope,
              $translate,
              $http, $filter, $state, $stateParams,
              $q, $mdDialog, $element,
              $rootScope, toastConfirm,
              $modal) {

        $scope.hot = {};
        $scope.setting = {
            formulas: true,
            colHeaders: true,
            rowHeaders: true,
            dropdownMenu: true,
            filters: true,
            licenseKey: 'non-commercial-and-evaluation',
            width: '100%',
            height: 320,
            colWidths: [45, 60, 60, 60, 60, 60, 60, 60, 60, 60, 110, 60, 60, 100, 250],
            manualColumnResize: true,
            minSpareRows: 1,
            contextMenu: true,
            manualRowResize: true,
            afterInit: function () {
                $scope.hot.instance = this;
                $scope.getcols();
            }
        }


        $scope.calcSums = function () {
            let colcount = $scope.hot.instance.countCols();
            let sums = {};
            let colHeader = $scope.hot.instance.getColHeader();
            let colData = $scope.hot.instance.getDataAtRow($scope.hot.instance.countRows() - 1);
            for (var i = 0; colHeader.length > i; i++) {
                sums[colHeader[i]] = colData[i];
            }
            return sums
        }

        $scope.list = {};
        $scope.org = {};

        $scope.getcols = function () {
            $http.get("/api/v1/materialconvsale/getColDefs/").then(function (data) {
                $scope.list.cols = data.data;
                $scope.getdata();
            })
        }

        $scope.getdata = function () {
            if ($stateParams.sale_item !== '0') {
                $http.get("/api/v1/materialconvsale/" + $stateParams.sale_item + "/").then(function (data) {
                    // $scope.colsdata = data.data.desc.details
                    $scope.org = data.data;
                    $scope.list.data = data.data.desc.details;
                })
            }
        }

        $scope.init = function () {

        }


        $scope.init();


        $scope.SaveChanges = function () {
            let newchanges = $scope.hot.instance.getData();
            $http.post('/api/v1/materialconvsale/' + $stateParams.sale_item + '/saveCovSale/', newchanges).then(function (data) {
                if ($stateParams.sale_item === '0') {
                    if (data.data.id) {
                        $state.go("material_tolid_sale_conv_sale_item", {sale_item: data.data.id})
                    }
                }

            })
        }

        $scope.CopyNew = function () {
            if ($stateParams.sale_item !== '0') {
                $http.get('/api/v1/materialconvsale/' + $stateParams.sale_item + '/CopyNew/').then(function (data) {
                    $state.go("material_tolid_sale_conv_sale_item", {sale_item: data.data.id})
                })
            }
        }


    });