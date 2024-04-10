'use strict';


angular.module('AniTheme').controller(
    'statisticsNewCtrl',
    function ($scope,
              $translate,
              $q,
              $rootScope,
              $modal,
              $state,
              statisticsBaseService) {

        $scope.statisticTemplate = {};
        $scope.errors = {};
        $scope.createStatisticTemplate = function () {
            $scope.statisticTemplate.icon = "fa fa-statics";
            statisticsBaseService.createStatisticTemplate($scope.statisticTemplate).then(function (data) {
                $rootScope.$broadcast("UpdateMSTemplateList");
            }).catch(function (data) {
                $scope.errors = data.message;
            });
        };
        $scope.publishTemplate = function () {


            var modalInstance = $modal.open({
                animation: true,
                templateUrl: 'page/statistics/publish',
                controller: 'publishMSTemplateCtrl',
                size: '',
                resolve: {
                    oldUsers: function () {
                        return $scope.statisticTemplate.publishedUsers;
                    },
                    oldUsersDetail: function () {
                        return $scope.statisticTemplate.publishedUsersDetail;
                    },

                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        //////console.log("perparing to get scripts");
                        return $ocLazyLoad.load({
                            name: 'AniTheme.publishMSTemplateCtrl',
                            files: [
                                '/static/angularThings/statistics/publishMSTemplateCtrl.js',
                                '/static/angularThings/Letter/Sidebar/Groups/classChart.js',
                                '/static/angularThings/Letter/Sidebar/Groups/classGroup.js',
                                '/static/angularThings/Letter/Sidebar/Groups/classMember.js',
                                '/static/angularThings/Letter/Sidebar/Groups/classZone.js'

                            ],
                            catch: true
                        }).then(
                            function () {
                            }
                        )
                    }]

                }
            });
            modalInstance.result.then(function (res) {
                //debugger;
                $scope.statisticTemplate.publishedUsers = res[0];
                $scope.statisticTemplate.publishedUsersDetail = res[1];
            }, function () {


            });
        };

    });

