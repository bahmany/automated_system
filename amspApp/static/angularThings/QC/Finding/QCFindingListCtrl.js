'use strict';


angular.module('AniTheme').controller(
    'QCFindingListCtrl',
    function ($scope,
              $translate, $state,
              $http, Upload, ExportService,
              $q, $mdDialog, $timeout,
              $rootScope,
              $modal) {


        $scope.finding = {};
        $scope.findings = {};
        $scope.currentFinding = {};
        $scope.sendType = 0;

// -----------------------------------------
// -----------------------------------------
// -----------------------------------------
        $scope.openFinding = function (item, ev) {
            if (item.currentPerformerPositionID) {
                $state.go("QCFindingOpen", {findingID: item.id});

            } else {
                $mdDialog.show(
                    $mdDialog.alert()
                        .parent(angular.element(document.querySelector('#popupContainer')))
                        .clickOutsideToClose(true)
                        .title('قبل از ارسال نمی توانید وارد این صفحه شوید')
                        .textContent('ابتدا این یافته را ارجاع دهید و سپس وارد یافته شوید')
                        .ariaLabel('Alert Dialog Demo')
                        .ok('تایید')
                        .targetEvent(ev)
                );
            }

        }

// -----------------------------------------
// -----------------------------------------
// -----------------------------------------
// -----------------------------------------
// -----------------------------------------
        //-----------------
        // Member select funcs
        $scope.TableMembers = {};
        $scope.Members = [];
        $scope.Member = {};
        $scope.TableMembers.pagination = {};
        $scope.TableMembers.pagination.size = 10;
        $scope.TableMembers.pagination.total = 0;
        $scope.TableMembers.isShow = false;
        $scope.MembersTableSearch = "";
        $scope.$watch("MembersTableSearch", function () {
            $scope.GetMembers($scope.TableMembers.pagination.size);
        });
        $scope.membersTableGoToPage = function (url) {
            $scope.isSearchCallbackCompleted = false;
            ExportService.GetMembersListByPager(url).then(function (data) {
                $scope.isSearchCallbackCompleted = true;
                $scope.Members = data.data;
            }).catch(function (data) {
                $scope.isSearchCallbackCompleted = true;
            });
        };
        $scope.GetMembers = function (pagingSize) {
            ExportService.GetMembers($scope.MembersTableSearch, pagingSize).then(function (data) {
                $scope.Members = data.data;
            });
        };


        $scope.SendRootCause = function (item) {
            $scope.GetMembers(20);
            $scope.currentFinding = item;
            $scope.sendType = 2; //
            $("#modal_select_imported_positions").modal('show');
        };
        $scope.SelectPersonAA = function (item) {

            var dt = {
                findingID: $scope.currentFinding.id,
                typeOf: $scope.sendType,
                recPositionID: item.id,
                currentPerformerPositionID: item.positionID
            };


            $http.post("/api/v1/qcfinding/sendFinding/", dt).then(function (data) {
                if (data.data.msg) {
                    $("#modal_select_imported_positions").modal('hide');
                    $scope.list();
                }
            });
        };

        //-----------------
        //-----------------
        //-----------------
        //-----------------


// -----------------------------------------
// -----------------------------------------
// -----------------------------------------
// -----------------------------------------
        $scope.page = 1;

        $scope.getCurrentPerformer = function (finding) {
            if (finding.performers) {
                if (finding.performers.recievers) {
                    if (finding.performers.recievers.length > 0) {
                        var pr = finding.performers.recievers[finding.performers.recievers.length - 1].position;
                        return pr
                    }
                }
            }
            return {}

        }


        $scope.list = function () {
            $scope.wait = true;
            $http.get("/api/v1/qcfinding/?search=" + $scope.findingsSearchText + "&page=" + $scope.page.toString() + "&page_size=20").then(function (data) {
                $scope.findings = data.data;
                $scope.wait = false;
            })
        };

        $scope.list();

        $scope.findingsSearchText = "";
        $scope.$watch("findingsSearchText", function () {
            $scope.list();
        });

        $scope.wait = false;
        $scope.findingsPageTo = function (page) {
            $scope.wait = true;
            if (page) {
                $http.get(page).then(function (data) {
                    $scope.wait = false;
                    $scope.findings = data.data;
                }).catch(function () {
                    $scope.wait = false;
                });
            }
        };

        $scope.delete = function (ev, item) {
            var confirm = $mdDialog.confirm()
                .title('حذف یافته')
                .textContent('یافته مورد نظر حذف شود ؟')
                .ariaLabel('حذف یافته')
                .targetEvent(ev)
                .ok('حذف شود')
                .cancel('انصراف');

            $mdDialog.show(confirm).then(function (result) {
                $http.delete("/api/v1/qcfinding/" + item.id + "/").then(function () {
                    $scope.list();
                })
            }, function () {
                $scope.status = 'You didn\'t name your dog.';
            });

        };


    });