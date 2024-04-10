/**
 * Created by m on 9/11/2016.
 */


angular.module('AniTheme').controller(
    'ShareDataTablesCtrl',
    function ($scope,
              $translate,
              $http,
              $timeout,
              $q,
              $state,
              $stateParams,
              SettingsService,
              $mdDialog,
              $rootScope,
              $modal) {


   
        
        $scope.dataTable = {};
        $scope.getDataTable = function () {
            $http.get("/api/v1/datatable/" + $stateParams.DataTableId + "/").then(function (data) {
                $scope.dataTable = data.data;
            })
        };

        $scope.updateDataTable = function () {
            $http.patch("/api/v1/datatable/" + $scope.dataTable.id + "/", $scope.dataTable).then(function (data) {
                $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
            })
        };


        $scope.Companies = [];
        $scope.Company = {};
        $scope.SelectedCompanyID = null;
        $scope.person = {};
        $scope.successor = {};
        $scope.assistant = {};
        $scope.permission = {};

        $scope.GetDefaultCompany = function () {
            $http.get("/api/v1/companies/getDefault/").then(function (data) {
                $scope.Company = data.data;
                $scope.SelectedCompanyID = data.data.id;
                setUpMemberAutocomplement($scope.person, $scope.SelectedCompanyID, SettingsService);
                $scope.person.GetMembers();

            });
        };
        $timeout(function () {
            $scope.GetDefaultCompany();
        }, 0);



        $scope.getDataTable();


        $scope.removeUser = function (item) {
            var index = -1;
            // debugger;
            for (var i = 0; $scope.dataTable.publishedUsers.list.length > i; i++) {
                if ($scope.dataTable.publishedUsers.list[i].positionID == item.positionID) {
                    index = i;
                }
            }
            if (index != -1){
                $scope.dataTable.publishedUsers.list.splice(index, 1)
            }

            index = -1;
            for (var i = 0; $scope.dataTable.publishedUsers.list.length > i; i++) {
                if ($scope.dataTable.publishedUsers.list[i] == item.positionID) {
                    index = i;
                }
            }
            if (index != -1){
                $scope.dataTable.publishedUsers.list.splice(index, 1)
            }
        }
        $scope.addTo = function (person) {
            //converting positionID to positionDocInstance

            $http.get("/api/v1/statistics/getPosDoc/?q=" + person.selectedItem.value).then(function (data) {
                if ($scope.dataTable.publishedUsers.list) {
                    for (var i = 0; $scope.dataTable.publishedUsers.list.length > i; i++) {
                        if ($scope.dataTable.publishedUsers.list[i].id == person.selectedItem.value) {
                            alert("این کاربر قبلا انتخاب شده است");
                            return
                        }
                    }
                } else {
                    $scope.dataTable.publishedUsers.list = [];
                }

                $scope.dataTable.publishedUsers.list.push(data.data);
            });

        }



    });