'use strict';


angular.module('AniTheme').controller(
    'QCOpenFindingCtrl',
    function ($scope,
              $translate, $filter,
              $http, Upload, $stateParams, $state,
              $q, $mdDialog, $timeout, $location,
              $rootScope,
              $modal) {


        $scope.finding = {};
        $scope.getForEdit = function () {
            if ($stateParams.findingID) {
                if ($stateParams.findingID.length > 2) {
                    $http.get("/api/v1/qcfinding/" + $stateParams.findingID + "/").then(function (data) {


                        $scope.finding = data.data;
                        if ($scope.finding.dueDateStart) {
                            $scope.finding.dueDateStart = $filter('jalaliDate')($scope.finding.dueDateStart, 'jYYYY/jMM/jDD');
                        }
                        if ($scope.finding.dueDateEnd) {
                            $scope.finding.dueDateEnd = $filter('jalaliDate')($scope.finding.dueDateEnd, 'jYYYY/jMM/jDD');
                        }
                        if ($scope.finding.desc.dateOf) {
                            $scope.finding.desc.dateOf = $filter('jalaliDate')($scope.finding.desc.dateOf, 'jYYYY/jMM/jDD');
                        }


                        if (!($scope.finding.rootCause)) {
                            $scope.finding.rootCause = {}
                        }
                        if (!($scope.finding.rootCause.files)) {
                            $scope.finding.rootCause.files = {}
                        }

                        setupfileUploader($scope, $http, Upload, $scope.finding.rootCause.files, "/api/v1/qcfinding/");


                        $('#qrcode1').qrcode({
                            text: data.data.id,
                            width: 75, height: 75
                        });


                    })
                }
            }
        };
        $scope.getForEdit();


// --------------------------------------------------
// --------------------------------------------------
// --------------------------------------------------
// --------------------------------------------------
// --------------------------------------------------
// --------------------------------------------------
        function setupfileUploader($scope, $http, Upload, modelName, apiUrl) {
            $scope.UploadedFiles = [];
            $scope.Scans = {};
            $scope.Scan = {};
            loadUploader($scope, $http, Upload);
            $scope.showUploader = function () {
                $("#divFiles").fadeOut(function () {
                    $("#divUploader").fadeIn();
                });
            };
            $scope.cancelFiles = function () {

                $("#divUploader").fadeOut(function () {
                    $("#divFiles").fadeIn();
                });

            }
            $scope.RemoveFromUploaded = function (ev, index) {

                var confirm = $mdDialog.confirm()
                    .title('حذف فایل')
                    .textContent('فایل مورد نظر حذف شود ؟')
                    .ariaLabel('حذف فایل')
                    .targetEvent(ev)
                    .ok('حذف شود')
                    .cancel('انصراف');

                $mdDialog.show(confirm).then(function (result) {

                    $scope.finding.Files.uploaded.splice(index, 1);

                    // $http.patch(apiUrl + $scope.currentConv.id + "/", {
                    //     Files: {
                    //         uploaded: modelName.Files.uploaded
                    //     }
                    // }).then(function () {
                    //
                    // })
                }, function () {
                    $scope.status = 'You didn\'t name your dog.';
                });


            }
            $scope.saveFiles = function () {
                var final = [];
                angular.forEach($scope.UploadedFiles, function (value, key) {
                    final.push(value);
                });
                final = angular.copy($scope.UploadedFiles);
                if (modelName.Files) {
                    if (modelName.Files.uploaded) {
                        for (var i = 0; modelName.Files.uploaded.length > i; i++) {
                            final.push(modelName.Files.uploaded[i]);
                        }
                    }
                }


                // $http.patch(apiUrl + modelName.id + "/", {
                //     Files: {
                //         uploaded: final
                //     }
                // }).then(function () {
                //
                // })
                modelName.Files = {};
                modelName.Files.uploaded = final;
                $("#divUploader").fadeOut(function () {
                    $("#divFiles").fadeIn();
                });
            };
        }

// --------------------------------------------------
// --------------------------------------------------
// --------------------------------------------------
        $scope.postCause = function () {
            $scope.finding.type = 3;
            $http.patch("/api/v1/qcfinding/" + $scope.finding.id + "/", {
                rootCause: $scope.finding.rootCause,
                type: 3,
                currentPerformerPositionID: $scope.finding.rootCause.position.positionID
            }).then(function (data) {
                $scope.finding = data.data;
            })
        };
// --------------------------------------------------
// --------------------------------------------------
// --------------------------------------------------
// --------------------------------------------------
// --------------------------------------------------
        $scope.accept = function () {
            $scope.finding.type = 4;
            var flu = $scope.finding.followUp;
            $http.patch("/api/v1/qcfinding/" + $scope.finding.id + "/", {
                type: 4,
                followUp: flu,
                currentPerformerPositionID: 1

            }).then(function (data) {
                $scope.finding = data.data;
            })
        };
        $scope.reject = function () {
            $scope.finding.type = 2;
            var flu = $scope.finding.followUp;
            $http.patch("/api/v1/qcfinding/" + $scope.finding.id + "/", {
                type: 2,
                followUp: flu,
                currentPerformerPositionID: $scope.finding.followUp.position.positionID

            }).then(function (data) {
                $scope.finding = data.data;
            })
        };

// --------------------------------------------------
// --------------------------------------------------
// --------------------------------------------------
// --------------------------------------------------
// --------------------------------------------------


    });