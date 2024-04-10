'use strict';

angular.module('RahsoonApp').controller(
    'step10jobsCtrl',
    function ($scope,
              $translate,
              $q, $location,
              $http,
              $rootScope,
              $timeout) {

// getting all jobs available
        $scope.Jobs = [];
        $scope.GetAllJob = function () {
            $http.get("/reg/api/v1/login/get_all_jobs/").then(function (data) {
                $scope.Jobs = data.data;
            })
        }


        $scope.selectedJob = {};
        $scope.backToList = function () {
            $("#jobDetail").fadeOut(function () {
                $("#jobsList").fadeIn();
            });
        };

        $scope.GetJobDetail = function (jobID) {
            $http.get("/reg/api/v1/login/" + jobID + "/getJobDetail/").then(function (data) {
                if (data.data.answers) {
                    $scope.selectedJob.extraFields = data.data.answers;
                }
                if (data.data.requests) {
                    $scope.selectedJob.jobs = data.data.requests;
                }
            })
        };

        $scope.gotoJob = function (item) {
            $scope.selectedJob = item;
            $scope.GetJobDetail(item.id);
            $("#jobsList").fadeOut(function () {
                $("#jobDetail").fadeIn();
            });
            //$http.get("/home/profile/"+item.id+"/openJob/")
        };
        $scope.GetAllJob();


        $scope.PostCancelReq = function (item, index) {
            item.is_selected = false;
            $http.post("/reg/api/v1/login/" + $scope.selectedJob.id + "/answerReqs/", $scope.selectedJob.jobs).then(function () {
                            $rootScope.$broadcast("showToast", "اطلاعات شما با موفقیت ثبت شد");
            })
        }

        $scope.PostExtra = function (jobID, ans) {
            $http.post("/reg/api/v1/login/" + jobID + "/answerQustions/", ans).then(function () {
                $rootScope.$broadcast("showToast", "اطلاعات شما با موفقیت ثبت شد");
            })
        };
        $scope.PostReq = function (jobID, req, item) {
            item.is_selected = true;
            $http.post("/reg/api/v1/login/" + jobID + "/answerReqs/", req).then(function () {
                $rootScope.$broadcast("showToast", "اطلاعات شما با موفقیت ثبت شد");

            })
        };

    })