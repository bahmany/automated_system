/**
 * Created by m on 9/11/2016.
 */


angular.module('AniTheme').controller(
    'DataTablesCtrl',
    function ($scope,
              $translate,
              $http,
              $q, $mdDialog,
              $rootScope,
              $modal) {


        $scope.dataTables = {};
        $scope.filter = {};
        $scope.list = function () {
            var gt = $http.get("/api/v1/datatable/?q=" + $scope.filter.search);
            gt.then(function (data) {
                $scope.dataTables = data.data;
            })

        };

        var originatorEv;

        $scope.openMenu = function (mdMenu, event) {
            originatorEv = event;
            mdMenu.open(event);
        }

        $scope.delete = function (item) {

            swal({
                title: "حذف جدول",
                text: "آیا از حذف جدول انتخابی اطمینان دارید",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "بله",
                closeOnConfirm: false,
                showLoaderOnConfirm: true
            }, function () {
                $http.delete("/api/v1/datatable/" + item.id + "/").then(function (data) {
                    $scope.list();
                    swal("حذف شد!", "جدول مورد نظر از سیستم حذف گردید", "success");

                })
            });


        }


        $scope.$watch("filter.search", function () {
            $scope.list();
        })

        $scope.GoToPage = function (url) {
            var gt = $http.get(url);
            gt.then(function (data) {
                $scope.dataTables = data.data;
            })
        }


        $rootScope.$on("dataTableList", function () {
            $scope.list();
        })

    })