'use strict';


angular.module('AniTheme').controller(
    'QCFindingPostCtrl',
    function ($scope,
              $translate, $filter,
              $http, Upload, $stateParams, $state, SettingsService,
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


                    })
                }
            }
        };
        $scope.getForEdit();


        $scope.post = function () {

            if ($scope.finding.id) {
                // it is remained .....
                //$scope.finding.followUpPosID = $scope.person.selectedItem.value;
                $http.patch("/api/v1/qcfinding/" + $scope.finding.id + "/", $scope.finding).then(function (data) {
                    // $scope.list();
                    $state.go('QCFindingList')
                })
            } else {
                $scope.finding.followUpPosID = $scope.person.selectedItem.value;
                $http.post("/api/v1/qcfinding/", $scope.finding).then(function (data) {
                    $state.go('QCFindingList')
                })
            }

        };
        $timeout(function () {
            $('#txtDateOf').datepicker({
                dateFormat: 'yy/mm/dd'
            });
            $('#txtauditFrom').datepicker({
                dateFormat: 'yy/mm/dd'
            });
            $('#txtauditTo').datepicker({
                dateFormat: 'yy/mm/dd'
            });
        }, 0);

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

        setupfileUploader($scope, $http, Upload, $scope.finding, "/api/v1/qcfinding/");

        $scope.person = {};
        setUpMemberAutocomplement($scope.person, $rootScope.currentCompany.id, SettingsService);
        $scope.person.GetMembers();

    });