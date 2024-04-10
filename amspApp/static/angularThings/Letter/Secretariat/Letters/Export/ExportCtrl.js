/**
 * Created by mohammad on 12/20/15.
 */


'use strict';


angular.module('AniTheme').controller(
    'ExportCtrl',
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
              ExportService) {

        loadUploader($scope, $http, Upload);


        $scope.editorOptions = {
            language: 'fa',
            toolbar: [
                {
                    name: 'document',
                    items: ['Source', '-', 'Save', 'NewPage', 'DocProps', 'Preview', 'Print', '-', 'Templates']
                },
                {name: 'clipboard', items: ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
                {name: 'editing', items: ['Find', 'Replace', '-', 'SelectAll', '-', 'SpellChecker', 'Scayt']},
                {
                    name: 'forms',
                    items: ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                        'HiddenField']
                },
                '/',
                {
                    name: 'basicstyles',
                    items: ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']
                },
                {
                    name: 'paragraph',
                    items: ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv',
                        '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl']
                },
                {name: 'links', items: ['Link', 'Unlink', 'Anchor']},
                {
                    name: 'insert',
                    items: ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']
                },
                '/',
                {name: 'styles', items: ['Styles', 'Format', 'Font', 'FontSize']},
                {name: 'colors', items: ['TextColor', 'BGColor']},
                {name: 'tools', items: ['Maximize', 'ShowBlocks', '-', 'About']}

            ],
            extraPlugins: 'lineutils,notification,uploadwidget,uploadimage',
            removePlugins: 'sourcearea',
            filebrowserUploadUrl: '/api/v1/file/upload',
            resize_maxHeight: 900,
            height: 600

        };


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
        $scope.Pending = false;
        //-----------------
        //Company Select funcs
        $scope.SelectedCompnaies = [];
        $scope.SelectCompany = function (item) {
            if (!($scope.ExportLetter.exp)) {
                $scope.ExportLetter.exp = {};
            }
            if (!($scope.ExportLetter.exp.export)) {
                $scope.ExportLetter.exp.export = {};
            }
            if (!($scope.ExportLetter.exp.export.companyRecievers)) {
                $scope.ExportLetter.exp.export.companyRecievers = [];
            }
            $scope.ExportLetter.exp.export.companyRecievers.push(item);
        };
        $scope.RemoveCompany = function (index) {
            $scope.ExportLetter.exp.export.companyRecievers.splice(index, 1);
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
        //-----------------
        $scope.SelectedMemebrs = [];
        $scope.SelectPerson = function (item) {

            if (!($scope.ExportLetter.exp)) {
                $scope.ExportLetter.exp = {}
            }
            if (!($scope.ExportLetter.exp.export)) {
                $scope.ExportLetter.exp.export = {}
            }
            if (!($scope.ExportLetter.exp.export.hameshRecievers)) {
                $scope.ExportLetter.exp.export.hameshRecievers = []
            }
            $scope.ExportLetter.exp.export.hameshRecievers.push(item);
        };
        $scope.RemoveMember = function (index) {
            $scope.ExportLetter.exp.export.hameshRecievers.splice(index, 1);
        };
        $scope.prepareDownloadUrl = function (url) {
            return url.replace("thmum50_", "");
        };
        //-----------------
        $scope.ExportLetter = {};

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

        // Export Letter Operations

        $scope.$root.$on("UpdateFiles", function (event, args) {
            $scope.UploadedFiles = args;
        });
        $scope.PrepareToSend = function (letterType) {
            $scope.ExportLetter.tags = $scope.asyncContacts;

            //var sss = angular.copy($scope.ExportLetter);
            //$scope.ExportLetter.recievers = $scope.SelectedMemebrs; // roonevesht recievers
            if ($scope.UploadedFiles) {
                $scope.ExportLetter.attachments = $scope.UploadedFiles.files;
            }
            $scope.ExportLetter.letterType = letterType;
            return $scope.ExportLetter
        };
        //$scope.Save = function () {
        //    if ($scope.ExportLetter.hasOwnProperty("id")) {
        //        delete $scope.ExportLetter["id"];
        //    }
        //
        //    $scope.PostExportLetterAsNew($scope.PrepareToSend(2)).then(function (data) {
        //        $rootScope.$broadcast("RefreshExportList");
        //        sweetAlert("Good job!", "Successfully Sent", "success");
        //    }).catch(function (data) {
        //        sweetAlert("Complete the letter", data, "error");
        //    });
        //};
        //
        $scope.Save = function () {
            $scope.ExportLetter.tags = $scope.asyncContacts;

            if ($scope.ExportLetter.hasOwnProperty("id")) {
                delete $scope.ExportLetter["id"];
            }
            $scope.PostExportLetterAsNew($scope.PrepareToSend(2)).then(function (data) {
                $rootScope.$broadcast("RefreshExportList");
                sweetAlert("ثبت شد", "نامه ی صادره با موفقیت ثبت شد", "success");
                $state.go("exportList");
            }).catch(function (data) {
                sweetAlert("لطفا اطلاعات خواسته شده را صحیح تکمیل نمایید", data, "error");
            });
        };
        $scope.SaveRemoveDraft = function () {
            $scope.ExportLetter.tags = $scope.asyncContacts;

            if ($scope.ExportLetter.hasOwnProperty("id")) {
                delete $scope.ExportLetter["id"];
            }
            $scope.PostExportLetterAsNew($scope.PrepareToSend(2)).then(function (data) {
                if (data.data.id) {
                    $rootScope.$broadcast("RefreshExportList");
                    sweetAlert("ثبت شد", "نامه ی صادره شما با موفقیت ثبت شد", "success");
                    $http.delete("/api/v1/letter/sec/export/" + $stateParams.exportid + "/").then(function (data) {
                        $state.go("exportList");
                    });
                } else {
                    sweetAlert("اطلاعات خواسته شده را به درستی تکمیل نمایید", data.data.body, "error");
                }
            }).catch(function (data) {
                sweetAlert("اطلاعات خواسته شده را به درستی تکمیل نمایید", data.data.body, "error");
            });
        };

        $scope.SaveAsDraft = function () {
            $scope.ExportLetter.tags = $scope.asyncContacts;

            $scope.PostExportLetter($scope.PrepareToSend(8)).then(function (data) {
                $rootScope.$broadcast("RefreshExportList");
                sweetAlert("ثبت شد", "نامه ی مد نظر شما با موفقیت در پیش نویس های صادره ثبت شد", "success");
            }).catch(function (data) {
                sweetAlert("اطلاعات خواسته شده را به درستی تکمیل نمایید", data, "error");
            });
        };


        $scope.OpenSelectCompanyModal = function () {
            $scope.GetCompanies(15);
            $("#modal_select_imported_companies").modal('show');
        }

        $scope.OpenRecPositionModal = function () {
            $scope.GetCompanies(15);
            $("#modal_select_imported_positions").modal('show');
        }


        $scope.PostExportLetter = function (ExportLetter) {
            //////console.log("PostExportLetter");
            return $http.patch("/api/v1/letter/sec/export/" + ExportLetter.id + "/", ExportLetter)
        };
        $scope.PostExportLetterAsNew = function (ExportLetter) {
            //////console.log("PostExportLetterAsNew");
            return $http.post("/api/v1/letter/sec/export/", ExportLetter)
        };
        $scope.init = function () {
            $timeout(function () {
                $('#txt_dateOfSent').datepicker({
                    dateFormat: 'yy/mm/dd'
                });
            }, 10);
            //////console.log("loadedd");
            $scope.ExportLetter = {};
            if ($stateParams.exportid == "") {
                $scope.PostExportLetterAsNew($scope.PrepareToSend(8)).then(function (data) {
                    $state.go("exportNew", {exportid: data.data.exp.baseInbox});
                    $scope.ExportLetter = data.data;
                    $scope.UploadedFiles = $scope.ExportLetter.attachments;
                });
            } else {
                $http.get("/api/v1/letter/sec/export/" + $stateParams.exportid + "/get_prev/?id=" + $stateParams.exportid).then(function (data) {
                    $scope.ExportLetter = data.data.letter;
                    // $scope.UploadedFiles = {};
                    // $scope.UploadedFiles.files = [];
                    // $scope.UploadedFiles.files = data.letter.attachments;
                    $scope.UploadedFiles = $scope.ExportLetter.attachments;

                    $scope.Pending = false;
                    $rootScope.$broadcast("RefreshExportList");

                });
            }
        };
        $scope.Pending = true;
        $scope.init();


        ///----------------------------
        ///----------------------------
        ///----------------------------

        TagClass($scope, $http, $q, 1);


        ///----------------------------
        ///----------------------------
        ///----------------------------


    });