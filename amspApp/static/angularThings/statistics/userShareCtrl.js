/**
 * Created by m on 8/16/2016.
 */
angular.module('AniTheme').controller(
    'UserShareCtrl',
    function ($scope,
              $translate,
              $http,
              $q,
              $rootScope,
              $stateParams,
              SettingsService,
              $modal, $timeout,
              $state) {


        $scope.staticTmpl = {};
        $scope.getTmpl = function () {
            $http.get("/api/v1/statistics/" + $stateParams.MSTemplateId + "/").then(function (data) {
                $scope.staticTmpl = data.data;
            })
        };

        $scope.updateTmpl = function () {
            $http.patch("/api/v1/statistics/" + $scope.staticTmpl.id + "/", $scope.staticTmpl).then(function (data) {
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


        // $scope.person = {};
        // $scope.GetDefaultCompany = function () {
        //     $http.get("/api/v1/companies/getDefault/").then(function (data) {
        //         $scope.Company = data;
        //         $scope.SelectedCompanyID = data.id;
        //         setUpMemberAutocomplement($scope.person, $scope.SelectedCompanyID, SettingsService);
        //         $scope.person.GetMembers();
        //     });
        // };

        $scope.getTmpl();


        $scope.removeUser = function (item) {
            var index = -1;
            // debugger;
            for (var i = 0; $scope.staticTmpl.publishedUsersDetail.length > i; i++) {
                if ($scope.staticTmpl.publishedUsersDetail[i].positionID == item.positionID) {
                    index = i;
                }
            }
            if (index != -1){
                $scope.staticTmpl.publishedUsersDetail.splice(index, 1)
            }

            index = -1;
            for (var i = 0; $scope.staticTmpl.publishedUsers.length > i; i++) {
                if ($scope.staticTmpl.publishedUsersDetail[i] == item.positionID) {
                    index = i;
                }
            }
            if (index != -1){
                $scope.staticTmpl.publishedUsers.splice(index, 1)
            }
        }
        $scope.addTo = function (person) {
            //converting positionID to positionDocInstance

            $http.get("/api/v1/statistics/getPosDoc/?q=" + person.selectedItem.value).then(function (data) {
                if ($scope.staticTmpl.publishedUsersDetail) {
                    for (var i = 0; $scope.staticTmpl.publishedUsersDetail.length > i; i++) {
                        if ($scope.staticTmpl.publishedUsersDetail[i].id == person.selectedItem.value) {
                            alert("این کاربر قبلا انتخاب شده است");
                            return
                        }
                    }
                } else {

                    $scope.staticTmpl.publishedUsersDetail = [];
                    $scope.staticTmpl.publishedUsers = [];
                }

                $scope.staticTmpl.publishedUsersDetail.push(data.data);
                $scope.staticTmpl.publishedUsers.push(data.data.id);
            });

        }


    });
