/**
 * Created by mohammad on 12/20/15.
 */


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
              Upload,
              $http,
              SecCompaniesService,
              ImportService) {


        $scope.TableCompanies = {};
        $scope.Company = {};
        $scope.TableCompanies.pagination = {};
        $scope.TableCompanies.pagination.size = 10;
        $scope.TableCompanies.pagination.total = 0;
        $scope.TableCompanies.isShow = false;
        $scope.CompnaiesTableSearch = "";


        $scope.OpenSelectCompanyModal = function () {
            $scope.GetCompanies(15);
            $("#modal_select_imported_companies").modal('show');
        }

        $scope.OpenRecPositionModal = function () {
            $scope.GetCompanies(15);
            $("#modal_select_imported_positions").modal('show');
        }


        loadUploader($scope, $http, Upload);


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
        $scope.isLoading = false;
        $scope.GetCompanies = function (pagingSize) {
            $scope.isLoading = true;
            SecCompaniesService.Get($scope.CompnaiesTableSearch, pagingSize).then(function (data) {
                $scope.isLoading = false;
                $scope.Companies = data.data;
            }).catch(function (data) {
                $scope.isLoading = false;
            });

        };
        $scope.Pending = false;
        //-----------------
        //Company Select funcs
        $scope.SelectedCompnaies = [];
        $scope.SelectCompanyToImported = function (item) {

            if (!($scope.ImportLetter.exp)) {
                $scope.ImportLetter.exp = {}
            }
            if (!($scope.ImportLetter.exp.export)) {
                $scope.ImportLetter.exp.export = {}
            }
            if (!($scope.ImportLetter.exp.export.companyRecievers)) {
                $scope.ImportLetter.exp.export.companyRecievers = []
            }
            $scope.ImportLetter.exp.export.companyRecievers = [];
            $scope.SelectedCompnaies = [];

            $scope.SelectedCompnaies.push(item);
            $scope.ImportLetter.exp.export.companyRecievers.push(item);


        };
        $scope.RemoveCompany = function (index) {
            $scope.ImportLetter.exp.export.companyRecievers.splice(index, 1);
        };
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
            $scope.GetMembers($scope.TableCompanies.pagination.size);
        });
        $scope.membersTableGoToPage = function (url) {
            ImportService.GetMembersListByPager(url).then(function (data) {
                $scope.Members = data.data;
            }).catch(function (data) {
            });
        };
        $scope.GetMembers = function (pagingSize) {
            $scope.isSearchCallbackCompleted = true;

            ImportService.GetMembers($scope.MembersTableSearch, pagingSize).then(function (data) {
                $scope.isSearchCallbackCompleted = false;

                $scope.Members = data.data;
            }).catch(function () {
                $scope.isSearchCallbackCompleted = false;

            });
        };
        //-----------------
        $scope.SelectedMemebrs = [];
        $scope.SelectPerson = function (item) {

            if (!($scope.ImportLetter.exp)) {
                $scope.ImportLetter.exp = {}
            }
            if (!($scope.ImportLetter.exp.export)) {
                $scope.ImportLetter.exp.export = {}
            }
            if (!($scope.ImportLetter.exp.export.hameshRecievers)) {
                $scope.ImportLetter.exp.export.hameshRecievers = []
            }
            $scope.ImportLetter.exp.export.hameshRecievers.push(item);
        };
        $scope.RemoveMember = function (index) {
            $scope.ImportLetter.exp.export.hameshRecievers.splice(index, 1);
        };
        $scope.prepareDownloadUrl = function (url) {
            return url.replace("thmum50_", "");
        };
        //-----------------


        //-----------------
        // fileUploader
        // $scope.UploadedFiles stores uploaded files


        //loadFileUploader($scope, Upload, $http);
        $scope.loadPanel = function (panelName) {
            $(".hideIt").hide();
            $("#" + panelName).show();

        };
        $scope.SelectAttachments = function () {
            $scope.loadPanel("div_uploader");
        };
        $scope.CancelAttachments = function () {
            $scope.loadPanel("div_accepted_atts");
        };
        $scope.AcceptAtts = function () {
            $scope.loadPanel("div_accepted_atts");
        };
        //--------------------------------------

        // Import Letter Operations

        $scope.ImportLetter = {};
        $scope.ImportLetter.exp = {};
        $scope.isPosting = false;

        $scope.Post = function () {
            //debugger;

            // checking if uploaded coverpage
            if (!($scope.ImportLetter.exp.cover)) {
                sweetAlert("اخطار", "لطفا کاور نامه ی وارده را آپلود نمایید");
                return;

            }
            if (!($scope.ImportLetter.exp.export)) {
                sweetAlert("اخطار", "لطفا شرکتی را بعنوان صادر کننده ی نامه انتخاب نمایید");
                return;
            }

            if (!($scope.ImportLetter.exp.export.companyRecievers)) {
                sweetAlert("اخطار", "لطفا شرکتی را بعنوان صادر کننده ی نامه انتخاب نمایید");
                return;
            }

            if ($scope.ImportLetter.exp.export.companyRecievers.length == 0) {
                sweetAlert("اخطار", "لطفا شرکتی را بعنوان صادر کننده ی نامه انتخاب نمایید");
                return;
            }


            if ($scope.UploadedFiles) {
                $scope.ImportLetter.attachments = $scope.UploadedFiles;
            }

            $scope.isPosting = true;
            $scope.ImportLetter.tags = $scope.asyncContacts;
            $scope.sentLetter = {};
            $http.post("/api/v1/letter/sec/export-import/", $scope.ImportLetter).then(function (data) {
                $scope.isPosting = false;
                $scope.ImportLetter = {};
                $scope.ImportLetter.exp = {};
                $scope.sentLetter = data.data;
            }).catch(function () {
                $scope.isPosting = false;
            })
        };


        $scope.init = function () {
            if ($stateParams.importid) {
                $http.get("/api/v1/letter/sec/export-import/" + $stateParams.importid + "/get_prev/?id=" + $stateParams.importid).then(function (data) {
                    $scope.ImportLetter = data.data.letter;
                    $scope.UploadedFiles = $scope.ImportLetter.attachments;
                })
            } else {
                $scope.ImportLetter = {};
                $scope.ImportLetter.exp = {};
            }

        };


        $scope.Pending = false;
        $scope.init();

        $timeout(function () {
            $('#txt_dateOfSent').datepicker({
                dateFormat: 'yy/mm/dd'
            });
        }, 0);


        //------------------------------
        //------------------------------
        //------------------------------

        TagClass($scope, $http, $q, 2);


    }
);