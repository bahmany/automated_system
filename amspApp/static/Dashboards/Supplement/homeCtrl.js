'use strict';

angular.module('Supplement').controller(
    'homeCtrl',
    function ($scope,
              $q,
              $http,
              $state,
              $location,
              $rootScope,
              $timeout) {


        $scope.getUerType = function () {
            $http.get("/dashboards/api/v1/firstreg/getUserType/").then(function (data) {
                var stype;
                stype = data.data.type;
                if (stype === 2) {
                    location.href = "/dashboards/#!/secondReg";
                }
            })
        };
        $scope.getUerType();
        $scope.utype = -1;

        $scope.CreateIt = function(ev){
            $http.get("/api/v1/adminTaminDakheli/createSuppCats/");
        }

        $scope.StartIt = function (ev) {
            $http.get("/dashboards/api/v1/firstreg/getUserType/").then(function (data) {
                $scope.utype = data.data.type;
                if ($scope.utype === 4) {
                    $state.go("s1")
                }
                if ($scope.utype === 5) {
                    $state.go("s2")
                }
                if ($scope.utype === 6) {
                    $state.go("s3")
                }
            });
        }


    });