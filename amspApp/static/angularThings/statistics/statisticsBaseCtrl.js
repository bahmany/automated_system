'use strict';


angular.module('AniTheme').controller(
    'statisticsBaseCtrl',
    function ($scope,
              $translate,
              $q,
              $rootScope,
              $modal,
              statisticsBaseService) {

        $scope.selectedStatisticTemplateId = "";
        $scope.showStatisticData = function (StatisticTemplateId) {
            $scope.selectedStatisticTemplateId = StatisticTemplateId;
            $state.go("data-statistics", {statisticTemplateId: StatisticTemplateId});
        };

        $scope.statisticsTemplates = function () {
            statisticsBaseService.listStatisticsTemplates($scope.currentPage, $scope.searchInput, $scope.itemsPerPage).then(function (data) {
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
            });
        };
        $scope.statisticsTemplates();

        $scope.destroyTemplate = function (tempObj) {
            swal({
                title: "Are you sure?",
                text: "You will not be able to recover this imaginary file!",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "Yes, delete it!",
                showLoaderOnConfirm: true,
                closeOnConfirm: false
            }, function () {
                statisticsBaseService.deleteTemplate(tempObj.id).then(function (data) {
                    swal("Deleted!", "Your imaginary file has been deleted.", "success");
                    $scope.statisticsTemplates();
                });


            });

        };
        $scope.$on("UpdateMSTemplateList", function (event, args) {
            $scope.statisticsTemplates();
        });
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

