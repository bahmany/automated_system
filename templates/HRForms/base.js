'use strict';


angular.module('AniTheme').controller(
    "HRForms", ['$scope', '$http', 'Upload', function ($scope, $http, Upload) {

        $scope.HRForms = {};
        $scope.Table = [];
        $scope.One = {};
        $scope.IsUploading = false;
        $scope.UploadedFiles = [];


        $scope.GetTable = function () {
            $http.post("/dms/hr/get-table/", {}).success(function (data) {
                $scope.Table = data;
                console.log($scope.Table);
            });
        };

        $scope.AddNewFile = function () {
            $("#id_fileAddress").click();

        }

        $scope.GetOne = function (data) {
            $http.post("/dms/hr/get-one/", {}).success(function (data) {
                $scope.One = data;
            });
        };

        $scope.DownloadPDF = function (item) {
            window.location.href = "/files/" + item.latestFile;
        }

        $scope.Post = function () {
            if ($scope.IsUploading) {
                alert("لطفا صبر کنید تا فایل آپلود شود");
                return;
            }

            $scope.One.UploadedFiles = $scope.UploadedFiles;
            $http.post("/dms/hr/post/", $scope.One).success(function (data) {
//            debugger;
                if (data.messageType == "Succ") {
                    showSmallMessageSucc("ایول", data.messageText);
                    $scope.GetTable();
                    $("#addNewForm").modal("hide");
                } else {
                    showSmallMessage("ارور روی سیستمی", data.messageText)
                    return
                }

            }).error(function (data) {
                showSmallMessage("ارور خیلی بد از توی سیستم", "اگه فایلی رو آپلود نکردید تورو خدا آپلود کنید - خدا خیرتون بده")
                return
            })
        };

        $scope.ToggleForm = function (item) {
            // changing visibility of
            $http.post("/dms/hr/toggle/", item).success(function (data) {
                item.visible = data.visible;
            })
        };


        $scope.$watch("One.fileAddress", function () {
            $scope.upload($scope.One.fileAddress);
        });

        $scope.$watch("IsUploading", function () {
            if ($scope.IsUploading == true) {
                $("div#mask").css(
                    "display", "inline"
                );
            } else {
                $("div#mask").css(
                    "display", "none"
                );

            }
        });

        $scope.ItemEnableCheckedClicked = function (item) {
            for (var i = 0; $scope.UploadedFiles.length > i; i++) {
                $scope.UploadedFiles[i].default = false;
            }
            item.default = true;
        }

        $scope.upload = function (files) {
            if (files && files.length) {
                for (var i = 0; i < files.length; i++) {
                    var file = files[i];
                    $scope.IsUploading = true;

                    Upload.upload({
                        url: '/dms/upload-file/',
//                    fields: {'username': $scope.username},
                        file: file
                    }).progress(function (evt) {
                        var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
                        console.log('progress: ' + progressPercentage + '% ' + evt.config.file.name);
                    }).success(function (data, status, headers, config) {
//                    debugger;
                        $scope.One.File = data.id;
                        $scope.IsUploading = false;
                        // getting file infos after upload completed
                        $http.post("/dms/get-file-info-hr/", {"fileID": $scope.One.File}).success(function (data) {
                            $scope.UploadedFiles.push(data);
                        });

                        console.log('file ' + $scope.One.File);
                    });
                }
            }
        };


        $scope.DeleteFile = function (item) {
            if (confirm("واقعا می خوایی پاکش کنی ؟؟؟")) {
                $scope.UploadedFiles.splice(item, 1);
            }
        };

        $scope.Edit = function (item) {
            $http.post("/dms/hr/get-one/", item).success(function (data) {

                $scope.One = data;
                $scope.UploadedFiles = data.UploadedFiles;
                $("#addNewForm").modal();

            })

        };

        $scope.Remove = function (item) {
            if (confirm("واقعا مطمئن هستی که می خوایی حذفش کنی")) {
                if (confirm("در صورت حذف شدن این سند تمام فایل های آپلود شده با آن نیز حذف میشه")) {
                    $http.post("/dms/hr/remove/", item).success(function (data) {
                        $scope.GetTable();
                        showSmallMessageSucc("ایول", data.messageText);
                    })
                }
            }
        };
        $scope.Disable = function (item) {
        };
        $scope.GetTable();

    }]);