'use strict';

angular.module('AniTheme').controller(
    'profilePrevWithCommentCtrl',
    function ($scope,
              $translate,
              $q, $location,
              $http, $stateParams,
              $rootScope,
              $timeout) {

        $scope.prev = {};
        $scope.GetAll = function () {
            $http.get("/reg/api/v1/login/" + $stateParams.profileID + "/get_prev_with_edit/").then(function (data) {
                $scope.prev = data.data;
            })
        };
        $scope.GetAll();


        $scope.downloadResume = function (str) {
            downloadURL('/api/v1/file/upload?q=' + $scope.prev.Resume.resume);
        };


        $scope.comment = {};
        $scope.PostComment = function () {
            $http.post("/reg/api/v1/login/" + $stateParams.profileID + "/post_resume_comments/", $scope.comment).then(function (data) {
                $scope.GetComments();
            });
        };

        $scope.commentList = [];

        $scope.GetComments = function () {
            $http.get("/reg/api/v1/login/" + $stateParams.profileID + "/get_resume_comments/").then(function (data) {
                $scope.commentList = data.data;
            });
        };

        $scope.GetComments();

    });