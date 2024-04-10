'use strict';
angular.module('AniTheme')
    .controller(
        'HavalehForooshChangeCtrl',
        function ($scope, $window, $mdMenu, $http, $translate, $rootScope, $stateParams, $state , $location, $$$, $filter) {


            $scope.approve = {};
            $scope.firstData = {};

            $scope.goback = function () {
                $state.go('HavalehForooshDetails',{hfdid:$scope.approve.havalehForooshLink})
            }

            $scope.get = function () {
                $http.get("/api/v1/havakehForoosh/getDetailsApprove/?ai=" + $stateParams.ApproveID + "&s=" + $stateParams.Step).then(function (data) {
                    $scope.approve = data.data;


                    for (var i = 0; $scope.approve.item.items.length > i; i++) {
                        $scope.approve.item.items[i].AQty = 0;
                    }


                });


            };

            $scope.get();


            $scope.save = function ($event) {
                // controlling
                // controlling mandeh kol vs meghdare pishnahadi
        angular.element($event.target).attr("disabled",true);

                $http.post("/api/v1/havakehForoosh/saveApprove/?ai=" + $stateParams.ApproveID + "&s=" + $stateParams.Step, $scope.approve).then(function (data) {
                            angular.element($event.target).attr("disabled",false);

                            $scope.goback();
                })


            }

        });