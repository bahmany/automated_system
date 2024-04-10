'use strict';
angular.module('AniTheme')
    .controller(
        'PishfactorBaseCtrl',
        function ($scope, $window, $http,
                  $mdDialog,
                  $translate, $rootScope, $stateParams, $location, $$$, $filter) {


            $scope.pish = {};
                $scope.get_pish = function (){
                        $http.get('/api/v1/hamkaranKhorooj/'+$stateParams.pishID+'/pishfatorget/').then(function (data){
                            $scope.pish = data.data;
                        })
                }

                $scope.get_pish();


        });



