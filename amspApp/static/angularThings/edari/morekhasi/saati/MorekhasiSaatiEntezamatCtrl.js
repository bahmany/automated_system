'use strict';


angular.module('AniTheme').controller(
    'MorekhasiSaatiEntezamatCtrl',
    function ($scope,
              $translate,
              $http,
              $q, $mdDialog,
              $rootScope,
              $modal) {


        $scope.result = [];
        $scope.dateofmorekhasi = "";
        $scope.getlist = function () {
            $http.get('/api/v1/morekhasi_saati/get_entezamat/?dt=' + $scope.dateofmorekhasi).then(function (data) {
                $scope.result = data.data;
            })
        }

        $scope.getlist();


        $scope.entezamat_btn = function (item, _typeof, index) {
            $http.post('/api/v1/morekhasi_saati/post_entezamat/', {
                id: item.id,
                typeof: _typeof,
            }).then(function (data) {
                $scope.result[index] = data.data;
            })
        }


    });