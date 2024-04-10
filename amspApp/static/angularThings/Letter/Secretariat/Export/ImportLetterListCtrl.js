'use strict';


angular.module('AniTheme').controller(
    'ImportCtrl',
    function ($scope,
              $translate,
              $q,
              $state,
              $stateParams,
              $rootScope,
              $modal,
              $compile,
              $timeout,
              $http) {

        $scope.filter = {};

        $scope.filter.selectedCompanies = [];

        $scope.TableMembers = {};
        $scope.Members = [];
        $scope.Member = {};
        $scope.TableMembers.pagination = {};
        $scope.TableMembers.pagination.size = 10;
        $scope.TableMembers.pagination.total = 0;
        $scope.TableMembers.isShow = false;
        $scope.MembersTableSearch = "";


        $scope.Table = {};
        $scope.Table.pagination = {};
        $scope.Table.pagination.size = 10;
        $scope.Table.pagination.total = 0;
        $scope.Table.isShow = false;



        $scope.GetExportList();

        // $scope.previewLetter = function (item) {
        //
        // }

        $scope.Download = function (filename) {
            downloadURL(filename);
        }


        $scope.waitForLoading = false;

        $scope.GetExportList = function () {
            var filter = {};
            filter.companies = $scope.filter.selectedCompanies.map(function (node) {
                return node.id
            }).join("-");
            filter.el = $scope.filter.exportList;
            filter.edl = $scope.filter.exportDraftList;
            filter.il = $scope.filter.importList;
            filter.startdate = $scope.filter.startDate;
            filter.enddate = $scope.filter.endDate;
            filter.q2 = $scope.filter.searchString;
            var ss = "";
            if ($scope.filter.exportDraftList) {
                ss = "9"
            }
            if ($scope.filter.exportList) {
                if (ss != "") {
                    ss = ss + ";";
                }
                ss = ss + "5"
            }
            if ($scope.filter.importList) {
                if (ss != "") {
                    ss = ss + ";";
                }
                ss = ss + "10"
            }
            if (ss == "") {
                ss = "10"
            }
            filter.p = '-1,' + ss + ',-1';
            var filterResult = $.param(filter);
            $scope.waitForLoading = true;
            $http.get("api/v1/letter/sec/export/?" + filterResult).success(function (data) {
                $scope.ExportletterList = data;
                $scope.waitForLoading = false;

            }).error(function () {
                $scope.waitForLoading = false;
            });
        };

    })