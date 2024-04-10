/**
 * Created by m on 9/11/2016.
 */


angular.module('AniTheme').controller(
    'ScriptDataTablesCtrl',
    function ($scope,
              $translate,
              $http,
              $q, $mdDialog,
              $rootScope,
              $stateParams,
              $modal) {


        $scope.dataTable = {};
        $scope.getDataTable = function () {
            $http.get("/api/v1/datatable/" + $stateParams.DataTableId + "/").then(function (data) {
                if (data.data.id) {
                    $scope.dataTable = data.data;
                } else {
                    $scope.dataTable = {};

                }
            })
        }
        $scope.getDataTable();

        $scope.updateDataTable = function () {
            $http.patch("/api/v1/datatable/" + $scope.dataTable.id + "/", $scope.dataTable).then(function (data) {
                $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
            })
        };

        $scope.editorOptionsPython = {
            lineWrapping: true,
            lineNumbers: true,
            // readOnly: 'nocursor',
            mode: 'python'
        };
    })