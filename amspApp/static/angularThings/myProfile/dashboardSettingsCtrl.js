'use strict';

/**
 * @ngdoc function
 * @name AniTheme.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of AniTheme
 */
angular.module('AniTheme').controller(
    'DashboardSettingsCtrl',
    function ($scope,
              $injector,
              $timeout,
              $state,
              $translate,
              $$$, $q,
              $rootScope,
              $http,
              $mdToast,
              $interval) {

        $scope.DashSetting = {};
        $http.get("/api/v1/profile/getCurrentProfileInPositionDoc/").then(function (data) {
            $scope.DashSetting = data.data;
        });


        $scope.searchTerm;
        $scope.clearSearchTerm = function () {
            $scope.searchTerm = '';
        };

        $scope.StaticItems;

        $scope.sortup = function () {
            for (var i = 0; i < $scope.DashSetting.dashboard.length; i++) {
                $scope.DashSetting.dashboard[0].sort = i + 1;
            }
        }

        $scope.GetStaticItems = function () {
            $http.get("/api/v1/statistics/MSTemplateList/").then(function (data) {
                $scope.StaticItems = data.data;
                // $scope.sortup();


            })
        };
        $scope.GetStaticItems();


        $scope.AddDataCell = function (item) {
            if (!( Object.prototype.toString.call(item.data_id) === '[object Array]' )) {
                item.data_id = [];
            }
            item.data_id.push({
                static_id: null,
                static_color: 'black'
            })
        }

        $scope.AddOneRow = function () {
            if (!($scope.DashSetting.dashboard)){
                $scope.DashSetting.dashboard = [];
            }
            $scope.DashSetting.dashboard.push(
                {
                    type: 3,
                    sort: $scope.DashSetting.dashboard.length,
                    items: [
                        {
                            data_id: null,
                            name: null,
                            desc: null
                        }
                    ]
                }
            )
        }

        $scope.PostEditing = function ($event) {
            var defer = $q.defer();
            var elem = angular.element($event.target);
            elem.attr("disabled", true);
            var prevText = elem.text();
            elem.text("لطفا صبر کنید ...");
            var res = $http.post("/api/v1/forced/setDashboard/", $scope.DashSetting);
            res.then(function (data) {
                $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
                elem.text(prevText);
                elem.attr("disabled", false);
                return defer.resolve(res);
            }).catch(function (data) {
                data.message.forEach(function (err) {
                    swal(err.name, err.message, "error");
                });
                elem.text(prevText);
                elem.attr("disabled", false);
                return defer.reject(res);
            });
            return defer.promise;
        };

        $scope.MoveUp = function (item) {
            if (item.sort <= 1) {
                return
            }
            var newSortID = item.sort - 1;
            for (var i = 0; i < $scope.DashSetting.dashboard.length; i++) {
                if ($scope.DashSetting.dashboard[i].sort == newSortID) {
                    $scope.DashSetting.dashboard[i].sort = newSortID + 1;
                }
            }
            item.sort = newSortID;
        }

        $scope.MoveDown = function (item) {
            // if (item.sort == $scope.DashSetting.dashboard.length) {
            //     return
            // }
            // finding max sort
            var max = -1;
            for (var i = 0; i < $scope.DashSetting.dashboard.length; i++) {
                if ($scope.DashSetting.dashboard[i].sort >= max) {
                    max = $scope.DashSetting.dashboard[i].sort
                }

            }

            if (item.sort >= max) {
                return
            }
            var newSortID = item.sort + 1;
            for (var i = 0; i < $scope.DashSetting.dashboard.length; i++) {
                if ($scope.DashSetting.dashboard[i].sort == newSortID) {
                    $scope.DashSetting.dashboard[i].sort = newSortID - 1;
                }
            }
            item.sort = newSortID;
        }


        $scope.AddFourRow = function () {
            $scope.DashSetting.dashboard.push(
                {
                    type: 2,
                    sort: $scope.DashSetting.dashboard.length,
                    items: [
                        {
                            data_id: null,
                            name: null,
                            desc: null,
                            sort: 1,
                            backColor: "#00bcd4",
                            min: -1,
                            max: 1
                        },
                        {
                            data_id: null,
                            name: null,
                            desc: null,
                            sort: 2,
                            backColor: "#8bc34a",
                            min: -1,
                            max: 1
                        },
                        {
                            data_id: null,
                            name: null,
                            desc: null,
                            sort: 3,
                            backColor: "#ff9800",
                            min: -1,
                            max: 1
                        },
                        {
                            data_id: null,
                            name: null,
                            desc: null,
                            sort: 4,
                            backColor: "#607d8b",
                            min: -1,
                            max: 1
                        }
                    ]
                }
            )
        }


    });