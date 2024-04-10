/**
 * Created by m on 9/11/2016.
 */


angular.module('AniTheme').controller(
    'EditDataTablesCtrl',
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
//DataTableId


        $scope.Companies = [];
        $scope.Company = {};
        $scope.SelectedCompanyID = null;
        $scope.person = {};
        $scope.successor = {};
        $scope.assistant = {};
        $scope.permission = {};

        $scope.GetDefaultCompany = function () {
            $scope.Companies = [];
            $scope.Company = {};
            $scope.SelectedCompanyID = null;
            $scope.person = {};
            $scope.successor = {};
            $scope.assistant = {};
            $scope.permission = {};
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


        // $scope.person = {};
        // $scope.GetDefaultCompany = function () {
        //     $http.get("/api/v1/companies/getDefault/").then(function (data) {
        //         $scope.Company = data;
        //         $scope.SelectedCompanyID = data.id;
        //         setUpMemberAutocomplement($scope.person, $scope.SelectedCompanyID, SettingsService);
        //         $scope.person.GetMembers();
        //     });
        // };

        $scope.reset = function () {
            $scope.dataTable = {};
            $scope.dataTable.publishedUsers = {};
            $scope.dataTable.publishedUsers.users = [];
            $scope.dataTable.fields = {};
            $scope.dataTable.fields.list = [];
        };
        $scope.reset();

        if ($stateParams.DataTableId != "0") {
            $http.get("/api/v1/datatable/" + $stateParams.DataTableId + "/").then(function (data) {
                $scope.dataTable = data.data;
            })
        }


        $scope.AddNewField = function () {
            $scope.dataTable.fields.list.push({})
        };


        $scope.RemoveField = function (index, item) {
            swal({
                title: "حذف فیلد",
                text: "آیا از حذف فیلد انتخابی اطمینان دارید",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "بله",
                closeOnConfirm: false
            }, function () {
                $scope.dataTable.fields.list.splice(index, 1);
                swal("حذف شد!", "جهت ثبت تغییرات دکمه ثبت را کلیک کنید در غیر اینصورت صفحه را ببندید", "success");
            });
        };


        $scope.list = function () {
            $rootScope.$broadcast("dataTableList");
        }


        $scope.post = function () {
            var pst = $http.post("/api/v1/datatable/", $scope.dataTable);
            pst.then(function (data) {
                if (data.data.id) {
                    $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
                    // ({DataTableId: data.data.id})
                    $state.go("value-datatables", {DataTableId: data.data.id});
                }

                // if ($stateParams.DataTableId == "0") {
                //     $scope.reset();
                // }
                // $scope.list();
            })
        };


        $scope.removeUser = function (parentIndex, parent, index, item) {
            var index = -1;

            for (var i = 0; $scope.dataTable.fields.list.length > i; i++) {
                if ($scope.dataTable.fields.list[i].sort == parent.sort) {
                    parentIndex = i
                }
            }
            // debugger;
            for (var i = 0; $scope.dataTable.fields.list[parentIndex].limitedUsers.length > i; i++) {
                if ($scope.dataTable.fields.list[parentIndex].limitedUsers[i].positionID == item.positionID) {
                    index = i;
                }
            }
            if (index != -1) {
                $scope.dataTable.fields.list[parentIndex].limitedUsers.splice(index, 1)
            }
        }
        $scope.addTo = function (index, item, person) {
            //converting positionID to positionDocInstance

            for (var i = 0; $scope.dataTable.fields.list.length > i; i++) {
                if ($scope.dataTable.fields.list[i].sort == item.sort) {
                    index = i
                }
            }

            if (!($scope.dataTable.fields.list[index].limitedUsers)) {
                $scope.dataTable.fields.list[index].limitedUsers = [];
            }
            var itms = $scope.dataTable.fields.list[index].limitedUsers;
            if (!(itms)) {
                $scope.dataTable.fields.list[index].limitedUsers = [];
                itms = []
            }

            $http.get("/api/v1/statistics/getPosDoc/?q=" + person.selectedItem.value).then(function (data) {
                if ($scope.dataTable.publishedUsers.users) {
                    for (var i = 0; $scope.dataTable.fields.list[index].limitedUsers.length > i; i++) {
                        if ($scope.dataTable.fields.list[index].limitedUsers[i].id == person.selectedItem.value) {
                            alert("این کاربر قبلا انتخاب شده است");
                            return
                        }
                    }
                } else {
                    // $scope.dataTable.publishedUsers = {};
                    // $scope.dataTable.publishedUsers.users = [];

                }

                // //console.log(itms);
                $scope.dataTable.fields.list[index].limitedUsers.push(data.data);


                $scope.GetDefaultCompany();
            });

        }
    });