'use strict';

angular.module('AniTheme').controller(
    'EmzaKonandehaCtrl',
    function ($scope,
              $translate,
              $q, $http,
              $rootScope,
              $modal) {

        $scope.members = [];
        $scope.get_members = function () {
            $http.get("/api/v1/companies/700/members/getListJustHasPos/?q=").then(function (data) {
                $scope.members = data.data;
            });
        }

        $scope.get_members();


        $scope.ChangeCell = function (item) {
            let a = prompt('موبایل جدید را وارد کنید مثلا : 09121234567');
            if (a) {
                $http.post("/api/v1/companies/" + $scope.SelectedCompanyID + "/chart/" + item.positionID + "/ChangeCell/", {
                    newCell: a
                }).then(function (data) {
                    $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
                    $scope.get_members();
                })
            }
        }

        $scope.ChangePersCode = function (item) {
            let a = prompt('کد پرسنلی را وارد نمایید مثلا 1234');
            if (a) {
                $http.post("/api/v1/companies/" + $scope.SelectedCompanyID + "/chart/" + item.positionID + "/ChangePersCode/", {
                    newCell: a
                }).then(function (data) {
                    $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
                    $scope.get_members();
                })
            }
        }


        $scope.get_personnel_name_from_code = function (member, _typeof, numm) {
            member['desc']['taeed'][_typeof][numm + '_name'] = 'درحال جستجو...'
            $http.get("/api/v1/companies/700/members/get_position_from_personnel_code_req/?q=" + member['desc']['taeed'][_typeof][numm]).then(function (data) {
                if (data.data.userID) {
                    member['desc']['taeed'][_typeof][numm + '_name'] = data.data.profileName
                } else {
                    member['desc']['taeed'][_typeof][numm + '_name'] = 'یافت نشد'
                }
            }).catch(function (data) {
                member['desc']['taeed'][_typeof][numm + '_name'] = 'یافت نشد'

            });
        }


        $scope.save_mojavez_grid = function (member) {

            $http.post("/api/v1/companies/700/members/update_emzaha/", member).then(function (data) {
                $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");

            })
        }


    });





