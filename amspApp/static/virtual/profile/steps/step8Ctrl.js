'use strict';

angular.module('RahsoonApp').controller(
    'step8Ctrl',
    function ($scope,
              $translate,
              $q, $location,
              $http,
              $rootScope,
              $timeout) {


        var model_name = "Resume";
        var model_id = "8";

        $scope[model_name] = {};
        $scope[model_name].items = [];
        $scope[model_name + "Item"] = {};
        LoadSteps($rootScope, $scope, $http, $location);
        $scope.Get(model_id, model_name);
        $scope.AddToList = function (item) {
            if (!($scope[model_name].hasOwnProperty("items"))) {
                $scope[model_name].items = [];
            }
            $scope[model_name].items.push(item);
            $scope[model_name + "Item"] = {};
        };
        $scope.itemEdit = function (item, index) {
            $scope[model_name + "Item"] = item;
            $scope[model_name].items.splice(index, 1);
        };


        $scope.downloadResume = function () {
            downloadURL('/api/v1/file/upload?q=' + $scope.Resume.resume);
        }

        $scope.uploadImageClick = function () {
            $("#filePicProfile").click();
        }

        $scope.uploadResumeClick = function () {
            $("#fileResume").click();
        }


        //$scope.Get = function () {
        //    $http.get("/reg/api/v1/login/8/get_step/").then(function (data) {
        //        $scope.Resume = data;
        //    })
        //}

        //$scope.Get();

        $scope.removeProfilePic = function () {
            delete $scope.Resume.pic;
            $("#secPicProfile").html("جهت آپلود عکس کلیک کنید");
            $("#secPicProfile").css({
                "background-image": "inherit",
                'background-size': '50%',
                'background-repeat': 'no-repeat',
                'background-position': 'center center'
            });
        }

        $scope.removeResule = function () {
            delete $scope.Resume.resume;
            $("#secResumeProfile").html(
                'جهت آپلود رزومه کلیک کنید'
            )
        }

        $scope.$watch("[Resume.pic,Resume.resume]", function () {
            if ($scope.Resume.pic) {
                $("#secPicProfile").html("");
                $("#secPicProfile").css({
                    "background-image": "url('/api/v1/file/upload?q=" + $scope.Resume.pic + "')",
                    'background-size': '50%',
                    'background-repeat': 'no-repeat',
                    'background-position': 'center center'
                });
            }
            if ($scope.Resume.resume) {
                $("#secResumeProfile").html(
                    '<br><br><span class="fa-stack fa-lg">' +
                    '<i class="fa fa-file-o fa-5x"></i>' +
                    '<i class="fa fa-check fa-3x fa-stack-3x text-success"></i></span>'
                )
            }
        })


        $("#filePicProfile").change(function () {
            if ($("#filePicProfile").val()) {
                var frmData = new FormData();
                frmData.append("pic", filePicProfile.files[0]);
                $("#secPicProfile").html("<i class='fa fa-refresh fa-5x fa-spin'></i> ");
                $.ajax({
                    url: '/api/v1/file/upload/',
                    type: 'POST',
                    data: frmData,
                    contentType: false,
                    processData: false,
                    success: function (data) {
                        $scope.Resume.pic = data.name;
                        $("#secPicProfile").html("");
                        $("#secPicProfile").css({
                            "background-image": "url('/api/v1/file/upload?q=" + data.name + "')",
                            'background-size': '50%',
                            'background-repeat': 'no-repeat',
                            'background-position': 'center center'
                        });
                        $scope.$apply();

                    },
                    error: function (data) {
                        swal("خطا", "لطفا عکس دیگری را انتخاب نمایید", "error")
                    }
                });
            }
        });
        $scope.uploadedImage = "";
        $("#fileResume").change(function () {
            if ($("#fileResume").val()) {
                var frmData = new FormData();
                frmData.append("pic", fileResume.files[0]);
                $("#secResumeProfile").html("<i class='fa fa-refresh fa-5x fa-spin'></i> ");
                $.ajax({
                    url: '/api/v1/file/upload/',
                    type: 'POST',
                    data: frmData,
                    contentType: false,
                    processData: false,
                    success: function (data) {
                        $scope.Resume.resume = data.name;
                        $scope.uploadedImage = "/api/v1/file/upload?q=thmum200_"+data.name;
                        $scope.$apply();
                        $("#secResumeProfile").html(
                            '<img style="height: 170px;" src="'+$scope.uploadedImage+'">' +
                            '<i class="fa fa-check fa-3x fa-stack-3x text-success"></i></span>'
                        )
                    },
                    error: function (data) {
                        swal("خطا", "لطفا رزومه ی دیگری را انتخاب نمایید", "error")
                    }
                });
            }
        });
    });