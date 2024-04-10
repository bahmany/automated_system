'use strict';

angular.module('AniTheme').controller(
    'sahmCalcCtrl',
    function ($scope,
              //$translate,
              $q,
              $http,
              $location,
              $rootScope,
              $timeout) {

// $scope.dataTableOpt = {
//    //custom datatable options
//   // or load data through ajax call also
//   "aLengthMenu": [[10, 50, 100,-1], [10, 50, 100,'All']],
//   };
// });

        $scope.results = {};
        $scope.calculate = function () {
            $http.get("/Financial/api/v1/tashbasehamk/calculate/").then(function (data) {
                $scope.results = data.data;
            })
        }

        $scope.calculate();


    });
