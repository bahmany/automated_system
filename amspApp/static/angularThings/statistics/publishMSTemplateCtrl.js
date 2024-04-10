'use strict';
angular.module('AniTheme')
    .controller('publishMSTemplateCtrl', function ($scope, $modalInstance, $http, oldUsers,oldUsersDetail) {
        $scope.selects = [];
        $scope.finalList = [];
        $scope.paramOfSend = {};
        $scope.letter = {};

        $scope.loadRecieverPanel = function () {
            memberInbox($scope, $http);
            chartInbox($scope, $http);
            zoneInbox($scope, $http);
            groupInbox($scope, $http);
        };

        $scope.loadRecieverPanel();
        if (oldUsersDetail != undefined) {
            $scope.selects = oldUsersDetail;
        }
        $scope.resList = [];
        $scope.finalRes = [];
        $scope.saveGroup = function () {
            var i = 0;
            for (i = 0; i < $scope.selects.length; i++) {
                $scope.resList.push($scope.selects[i].id);
            }
            $scope.finalRes.push($scope.resList);
            $scope.finalRes.push($scope.selects);
            $modalInstance.close($scope.finalRes);
        }


    });
