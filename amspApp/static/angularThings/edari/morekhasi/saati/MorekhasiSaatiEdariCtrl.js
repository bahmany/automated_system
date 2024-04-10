'use strict';


angular.module('AniTheme').controller(
    'MorekhasiSaatiEdariCtrl',
    function ($scope,
              $translate,
              $http,
              $q, $mdDialog,
              $rootScope,
              $modal) {


        $scope.result = [];
        $scope.dateofmorekhasi = "";

        $scope.getlist = function () {
            $http.get('/api/v1/morekhasi_saati/get_edari/?dt=' + $scope.dateofmorekhasi).then(function (data) {
                $scope.result = data.data;
            })
        }

        $scope.updatekaraweb = function (idofinatance, id, event) {
            angular.element(event.target).attr("disabled", true);
            $http.get('/api/v1/morekhasi_saati/make_change/?ins=' + idofinatance + '&dt=' + id).then(function (data) {
                angular.element(event.target).css("display", 'none');
            })
        }
        $scope.delupdatekaraweb = function (idofinatance, id, event) {
            angular.element(event.target).attr("disabled", true);
            $http.get('/api/v1/morekhasi_saati/make_unchange/?ins=' + idofinatance + '&dt=' + id).then(function (data) {
                $scope.getlist();
            })
        }

        $scope.showline = function (item, Id) {
            if (item.exp['karaweb_approves']) {
                for (var i = 0; item.exp.karaweb_approves.length > i; i++) {
                    if (item.exp.karaweb_approves[i]['id'] === Id) {
                        return false
                    }
                }
            }
            return true
        }


        $scope.getlist();


    });