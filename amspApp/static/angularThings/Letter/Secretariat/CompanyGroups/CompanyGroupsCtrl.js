'use strict';


angular.module('AniTheme').controller(
    'CompanyGroupsCtrl',
    function ($scope,
              $translate,
              $q,
              $rootScope,
              $modal,
              CompanyGroupsService) {
        $scope.CompanyGroup = {};
        $scope.SelectedCompanyGroup = {};
        $scope.CompanyGroups = [];
        $scope.CompanyGroupsSearchText = "";
        $scope.TableSearchString = "";

        $scope.TableCompanyGroups = {};
        $scope.TableCompanyGroups.pagination = {};
        $scope.TableCompanyGroups.pagination.size = 10;
        $scope.TableCompanyGroups.pagination.total = 0;
        $scope.TableCompanyGroups.isShow = false;

        $scope.ShowNewCompanyGroup = function () {
            $scope.CompanyGroup = {};
            $("#modal_sec_newedit_companygroup").modal("show");
        }

        $scope.PostCompanyGroup = function () {
            if ($scope.CompanyGroup.hasOwnProperty("id")) {
                CompanyGroupsService.UpdateCompanyGroup($scope.CompanyGroup.id, $scope.CompanyGroup).then(function () {
                    $scope.CompanyGroup = {};
                    $scope.GetCompanyGroups();
                }).catch(function (data) {
                    sweetAlert("Oops...", "Do not left empty or enter unique value", "error");
                });
            } else {
                CompanyGroupsService.PostCompanyGroup($scope.CompanyGroup).then(function () {
                    $scope.CompanyGroup = {};
                    $scope.GetCompanyGroups();
                }).catch(function (data) {
                    sweetAlert("Oops...", "Do not left empty or enter unique value", "error");
                });
            }
        };
        $scope.EditCompanyGroup = function (item) {
            $scope.CompanyGroup = item;
            $("#modal_sec_newedit_companygroup").modal("show");
        };
        $scope.CancelCompanyGroup = function (item) {
            $scope.CompanyGroup = {};
        };

        $scope.RemoveCompanyGroup = function (item) {
            swal({
                title: "اخطار",
                text: "آیا اطمینان دارید می خواهید ",
                type: "warning",
                showCancelButton: true,
                closeOnConfirm: false,
                showLoaderOnConfirm: true
            }, function () {
                CompanyGroupsService.RemoveCompanyGroup(item.id).then(function () {
                    swal("با موفقیت", "گروه شرکت انتخابی حذف شد", "success");
                    $scope.GetCompanyGroups();
                }).catch(function () {
                    sweetAlert("خطا", "گروه شرکت مورد نظر حذف نشد", "error");
                })
            });
        };
        $scope.HandleCompaniesGroupTablePagination = function () {
            if ($scope.TableCompanyGroups.pagination.size == 40) {
                $scope.TableCompanyGroups.pagination.size = 5;
            }
            $scope.TableCompanyGroups.pagination.size = $scope.TableCompanyGroups.pagination.size + 5;
            $scope.GetCompanyGroups($scope.TableCompanyGroups.pagination.size);
        };

        $scope.GetCompanyGroups = function (pagingSize) {
            $scope.isSearchCallbackCompleted = false;
            CompanyGroupsService.GetCompanyGroups($scope.CompanyGroupsSearchText, pagingSize).then(function (data) {
                $scope.CompanyGroups = data.data;
                $scope.isSearchCallbackCompleted = true;
            }).catch(function (data) {
                $scope.isSearchCallbackCompleted = true;
            });
        };
        $scope.$watch("CompanyGroupsSearchText", function () {
            $scope.GetCompanyGroups(10);
        });

        $scope.isSearchCallbackCompleted = true;
        $scope.CompanyGroupsPageTo = function (PagedUrl) {
            $scope.isSearchCallbackCompleted = false;
            CompanyGroupsService.GetCompanyGroupsListByPager(PagedUrl).then(function (data) {
                $scope.isSearchCallbackCompleted = true;
                $scope.CompanyGroups = data.data;
            }).catch(function (data) {
                $scope.isSearchCallbackCompleted = true;
            });
        };

    });