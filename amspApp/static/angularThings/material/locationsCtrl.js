'use strict';


angular.module('AniTheme').controller(
    'MaterialLocationsCtrl',
    function ($scope,
              $translate,
              $http,
              $q, $mdDialog,
              $rootScope,
              $modal) {

        $scope.locations = [];

        $scope.init = function () {
            // $http.get("/api/v1/barcodes/getDatatableCols/")
            $http.get("/api/v1/warehouse/list_warehouses/").then(function (data) {
                $scope.locations = data.data;
            })
        }


        $scope.add = function () {
            $scope.locations.push({});
        }





        $scope.init();


        $scope.postShelf = function (item) {
            $http.post("/api/v1/warehouse/post_shelf/", item).then(function (data) {
                $scope.init()
            })

        }


        $scope.MaterialHamkaranTafzilList = [{}];

        $scope.getMaterialHamkaranTafzilList = function () {
            $http.get("/api/v1/warehouse/get_material_hamkaran_tafzil_list/").then(function (data) {
                $scope.MaterialHamkaranTafzilList = data.data;
            })
        }

        $scope.getMaterialHamkaranTafzilList();

        $scope.updatehamktafzcon = function (item, $index) {

            $http.post("/api/v1/warehouse/update_material_hamkaran_tafzil/", item).then(function (data) {
                item = data.data;
            })
        }

        $scope.delhamktafzcon = function (item, $index) {
            if (confirm('آیا اطمینان دارید ؟')) {
                $scope.MaterialHamkaranTafzilList.splice($index, 1);
                $http.post("/api/v1/warehouse/delete_material_hamkaran_tafzil/", item).then(function (data) {
                    // $scope.MaterialHamkaranTafzilList = data.data;
                })

            }

        }


    });