'use strict';


angular.module('AniTheme').controller(
    'statisticsDataCtrl',
    function ($scope,
              $translate,
              $q,
              $filter,
              $http,
              $rootScope,
              $modal, $state, $stateParams,
              statisticsBaseService) {
        $scope.errors = {};
        $scope.selectedStatisticDataId = "";
        $scope.statisticData = {};

        $scope.statisticsDataList = function () {
            statisticsBaseService.listStatisticsData($stateParams.MSTemplateId, $scope.currentPage, $scope.searchInput, $scope.itemsPerPage).then(function (data) {
                $scope.data = data.data;
                $scope.totalItems = data.data.count;
                if (($scope.searchInput == undefined) || ($scope.searchInput == '')) {
                    $scope.totalItemsCount = data.data.count;
                }
                $scope.itemsFrom = ($scope.currentPage - 1) * $scope.itemsPerPage;

                $scope.itemsFrom += 1;

                $scope.itemsTo = $scope.itemsFrom + $scope.itemsPerPage - 1;
                if ($scope.itemsTo > $scope.totalItems) {
                    $scope.itemsTo = $scope.totalItems;
                }

                $scope.foundedItemsCount = data.data.count;
                $scope.GetSmallStaticsOf($stateParams.MSTemplateId)
            });
        };

        $scope.DataPageTo = function (url) {
            statisticsBaseService.DataPageTo(url).then(function (data) {
                $scope.data = data.data;
            })
        };

        $scope.getCurrentDate = function () {
            return $filter('jalaliDate')(currentDatetime(), 'jYYYY/jMM/jDD HH:mm');
        };


        $scope.getMSData = function (StatisticDataId) {
            statisticsBaseService.retrieveMSData(StatisticDataId).then(function (data) {
                $scope.statisticData.value = parseFloat(data.data.value);
                //$scope.statisticData.entryDate = data.entryDate;
                // debugger;
                $scope.statisticData.entryDate = $filter('jalaliDate')(data.data.entryDate, 'jYYYY/jMM/jDD HH:mm');
            });
        };
        $scope.saveMSData = function () {
            $scope.statisticData.template_id = $stateParams.MSTemplateId;

            statisticsBaseService.updateMSData($scope.statisticData.id, $scope.statisticData).then(function (data) {
                $scope.statisticsDataList();

            }).catch(function (data) {
                $scope.errors = data.data.message;
            });
        };

        $scope.currentSmallStatic = {};
        $scope.GetSmallStaticsOf = function (id) {
            $http.get("/api/v1/statistics/" + id + "/GetSmallStatic/").then(function (data) {
                $scope.currentSmallStatic = data.data;
            })
        };

        $scope.createStatisticDate = function () {
            $scope.statisticData.template_id = $stateParams.MSTemplateId;

            statisticsBaseService.createMSData($scope.statisticData).then(function (data) {
                $scope.statisticData.value = "";
                $scope.statisticData.entryDate = $filter('jalaliDate')($scope.getCurrentDate(), 'jYYYY/jMM/jDD HH:mm');
                $scope.statisticsDataList();

            }).catch(function (data) {
                $scope.errors = data.message;
            });
        };


        $scope.destroyData = function (dataObj) {
            swal({
                title: "حذف ",
                text: "پس از حذف دیگر به این داده دسترسی نخواهید داشت",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "بله حذف شود",
                showLoaderOnConfirm: true,
                closeOnConfirm: false
            }, function () {
                statisticsBaseService.deleteData(dataObj.id).then(function (data) {

                    swal("حذف شد", "داده آماری شما حذف شد", "success");
                    $scope.statisticsDataList();
                });
            });

        };
        $scope.updateOrCreate = function () {
            if ($scope.statisticData.id == undefined) {
                $scope.createStatisticDate();

            } else {
                $scope.saveMSData();
            }
        };
        $scope.statisticsDataList();
        $scope.removeFromList = function (processID) {
            for (var i = 0; $scope.data.results.length; i++) {

                if ($scope.data.results[i].id == processID) {
                    //
                    $scope.data.results.splice(i, 1);
                    return
                }
            }
        };
        $scope.clearAllTimeouts = function () {
            for (var i = 0; i < $scope.timeouts.length; i++) {
                clearTimeout($scope.timeouts[i])
            }
        };
    });

