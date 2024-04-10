'use strict';


angular.module('AniTheme').controller(
    'SecCompaniesCtrl',
    function ($scope,
              $translate,
              $q,
              $rootScope,
              $modal,
              $http,
              SecCompaniesService,
              CompanyGroupsService) {

        $scope.CompanyGroup = {};
        $scope.Companies = {};
        $scope.SelectedCompanyGroup = {};
        $scope.CompanyGroups = [];

        $scope.TableSearchString = "";
        $scope.Table = {};
        $scope.Table.pagination = {};
        $scope.Table.pagination.size = 10;
        $scope.Table.pagination.total = 0;
        $scope.Table.isShow = false;
        $scope.HandleTablePagination = function () {
            if ($scope.Table.pagination.size == 40) {
                $scope.Table.pagination.size = 5;
            }
            $scope.Table.pagination.size = $scope.Table.pagination.size + 5;
            $scope.GetCompanyGroups($scope.Table.pagination.size);
        };
        $scope.TableGoToPage = function (url) {
            url = url + "&page_size=" + $scope.Table.pagination.size.toString();
            $http.get(url).then(function (data) {
                $scope.CompanyGroups = data.data;
            });
        };


        $scope.ShowNewCompany = function () {
            $scope.Company = {};
            $("#modal_sec_newedit_company").modal("show");
        };


        $scope.ShowHideDropDown = function () {
            $(".search-drop-down").toggleClass("hide", "show");
            $scope.Table.isShow = !$scope.Table.isShow;
        };
        $scope.DropTableSelected = function (item) {
            $scope.SelectedCompanyGroup = item;
            $scope.ShowHideDropDown();
        };
        $scope.$watch("TableSearchString", function () {
            $scope.isSearchCallbackCompleted = false;
            CompanyGroupsService.GetCompanyGroups(
                $scope.TableSearchString,
                $scope.Table.pagination.size).then(function (data) {
                $scope.CompanyGroups = data.data;
                $scope.isSearchCallbackCompleted = true;
            }).catch(function (data) {
                $scope.isSearchCallbackCompleted = true;
            });
            //$scope.GetCompanyGroups($scope.Table.pagination.size);
        });
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
            $scope.GetCompanyGroups($scope.Table.pagination.size);
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


        // Companies Table defs
        $scope.TableCompanies = {};
        $scope.Company = {};
        $scope.TableCompanies.pagination = {};
        $scope.TableCompanies.pagination.size = 10;
        $scope.TableCompanies.pagination.total = 0;
        $scope.TableCompanies.isShow = false;
        $scope.CompnaiesTableSearch = "";
        $scope.HandleCompaniesTablePagination = function () {
            if ($scope.TableCompanies.pagination.size == 40) {
                $scope.TableCompanies.pagination.size = 5;
            }
            $scope.TableCompanies.pagination.size = $scope.TableCompanies.pagination.size + 5;
            $scope.GetCompanies($scope.TableCompanies.pagination.size);
        };
        $scope.$watch("CompnaiesTableSearch", function () {
            $scope.GetCompanies($scope.TableCompanies.pagination.size);
        });
        $scope.companiesTableGoToPage = function (url) {
            $scope.isSearchCallbackCompleted = false;
            SecCompaniesService.GetListByPager(url).then(function (data) {
                $scope.isSearchCallbackCompleted = true;
                $scope.Companies = data.data;
            }).catch(function (data) {
                $scope.isSearchCallbackCompleted = true;
            });
        };
        $scope.GetCompanies = function (pagingSize) {
            SecCompaniesService.Get($scope.CompnaiesTableSearch, pagingSize).then(function (data) {
                $scope.Companies = data.data;
            });

        };


        $scope.PostCompany = function () {
            $scope.Company.group = $scope.SelectedCompanyGroup.id;
            $scope.Company.groupname = $scope.SelectedCompanyGroup.name;
            if ($scope.Company.hasOwnProperty("id")) {
                SecCompaniesService.Update($scope.Company.id, $scope.Company).then(function (data) {
                    $scope.Company = data.data;
                    // $scope.GetCompanies($scope.TableCompanies.pagination.size);
                }).catch(function () {
                    sweetAlert("Oops...", "Do not left empty or enter unique value", "error");
                });
            } else {
                SecCompaniesService.Post($scope.Company).then(function (data) {
                    $scope.GetCompanies($scope.TableCompanies.pagination.size);
                }).catch(function () {
                    sweetAlert("Oops...", "Do not left empty or enter unique value", "error");
                });
            }

        };
        $scope.EditCompany = function (item) {
            $scope.Company = item;
            $scope.SelectedCompanyGroup = $scope.Company.group;

            $("#modal_sec_newedit_company").modal("show");
            //$scope.Company.group = $scope.SelectedCompanyGroup.id;
            //$scope.Company.groupname = $scope.SelectedCompanyGroup.name;
            //SecCompaniesService.Post($scope.Company).then(function (data) {
            //    $scope.GetCompanies($scope.TableCompanies.pagination.size);
            //});
        };
        $scope.DeleteCompany = function (item) {
            swal({
                title: "اخطار",
                text: "آیا اطمینان دارید می خواهید شرکت انتخاب شده را حذف کنید ؟",
                type: "warning",
                showCancelButton: true,
                closeOnConfirm: false,
                showLoaderOnConfirm: true
            }, function () {
                SecCompaniesService.Remove(item.id).then(function () {
                    swal("موفقیت", "شرکت مورد نظر حذف شد", "success");
                    $scope.GetCompanies($scope.TableCompanies.pagination.size);
                }).catch(function () {
                    sweetAlert("اخطار", "شرکت انتخاب شده حذف نشد", "error");
                })
            });
        };
        //-----------------

    });