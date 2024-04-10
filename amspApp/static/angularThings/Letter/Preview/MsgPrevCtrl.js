'use strict';


angular.module('AniTheme').controller(
    'MsgPrevCtrl',
    function ($scope,
              $translate,
              $timeout,
              $q,
              $rootScope,
              $location,
              $stateParams,
              $modal,
              $$$,
              $filter,
              $mdToast,
              $http) {


        $scope.msgs = {};
        $scope.getMsgList = function () {
            var userID = $stateParams.userID;
            $http.get("/api/v1/inbox-social/" + userID + "/get_msg_list/").then(function (data) {
                $scope.msgs = data.data;
            })
        }

        $scope.getMsgList();


        $scope.getMsgPrev = function(msg){
            $http.get("/api/v1/inbox-social/" + msg._id + "/get_msg_prev/").then(function (data) {
                msg.inf = data.data;
            })
        }


    }
);

