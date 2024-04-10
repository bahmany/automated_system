'use strict';


angular.module('AniTheme').controller(
    'LetterForwardCtrl',
    function ($scope,
              $translate,
              $timeout,
              $q,
              $rootScope,
              $http,
              LetterForwardService) {

        $scope.selects = {};
        $scope.CurrentLetter = {};

        $scope.$on("SetCurrentLetterForForward", function (event, args) {
            $scope.CurrentLetter = args.CurrentLetter;
        });

        $scope.loadRecieverPanel = function () {
            memberInbox($scope, $http);
            chartInbox($scope, $http);
            zoneInbox($scope, $http);
            groupInbox($scope, $http);
        };

        $scope.loadRecieverPanel();
        // overding exiting func for special uses
        $scope.handleSelect = function () {
            if ($scope.selects.length == 0){
                alert("Please select at least one person");
                return;
            }
            LetterForwardService.ForwardTo($scope.CurrentLetter.id, $scope.selects).then(function (data) {
                $scope.forwardModelInstance.close();
            }).catch(function (data) {
                alert("Please choose appropriate users ...")
            })
        };

        $scope.cancelSelect = function () {
            $scope.forwardModelInstance.dismiss("cancel");
        }
    });