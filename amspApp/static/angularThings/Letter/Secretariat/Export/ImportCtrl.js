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
              ExportService) {


        $scope.TableCompanies = {};
        $scope.Company = {};
        $scope.TableCompanies.pagination = {};
        $scope.TableCompanies.pagination.size = 10;
        $scope.TableCompanies.pagination.total = 0;
        $scope.TableCompanies.isShow = false;
        $scope.CompnaiesTableSearch = "";


        $scope.OpenSelectCompanyModal = function () {
            $scope.GetCompanies(15)
            $("#modal_select_imported_companies").modal('show');
        }

        $scope.OpenRecPositionModal = function () {
            $scope.GetCompanies(15)
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
            SecCompaniesService.GetListByPager(url).success(function (data) {
                $scope.isSearchCallbackCompleted = true;
                $scope.Companies = data;
            }).error(function (data) {
                $scope.isSearchCallbackCompleted = true;
            });
        };
        $scope.isLoading = false;
        $scope.GetCompanies = function (pagingSize) {
            $scope.isLoading = true;
            SecCompaniesService.Get($scope.CompnaiesTableSearch, pagingSize).success(function (data) {
                $scope.isLoading = false;
                $scope.Companies = data;
            }).error(function (data) {
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

            $scope.SelectedCompnaies.push(item)
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
        $scope.$watch("MembersNewInpTableSearch", function () {
            $scope.GetMembers($scope.TableCompanies.pagination.size);
        });
        $scope.membersTableGoToPage = function (url) {
            ExportService.GetMembersListByPager(url).success(function (data) {
                $scope.Members = data;
            }).error(function (data) {
            });
        };
        $scope.GetMembers = function (pagingSize) {
            $scope.isSearchCallbackCompleted = true;

            ExportService.GetMembers($scope.MembersNewInpTableSearch, pagingSize).success(function (data) {
                $scope.isSearchCallbackCompleted = false;

                $scope.Members = data;
            }).error(function () {
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
            $http.post("api/v1/letter/sec/export-import/", $scope.ImportLetter).success(function (data) {
                $scope.isPosting = false;
                $scope.ImportLetter = {};
                $scope.sentLetter = data;
            }).error(function () {
                $scope.isPosting = false;
            })
        };


        //$scope.$root.$on("UpdateFiles", function (event, args) {
        //    $scope.UploadedFiles = args;
        //});
        //$scope.PrepareToSend = function (letterType) {
        //    //var sss = angular.copy($scope.ImportLetter);
        //    //$scope.ImportLetter.recievers = $scope.SelectedMemebrs; // roonevesht recievers
        //    if ($scope.UploadedFiles) {
        //        $scope.ImportLetter.attachments = $scope.UploadedFiles.files;
        //    }
        //    $scope.ImportLetter.letterType = letterType;
        //    return $scope.ImportLetter
        //};

        //$scope.Save = function () {
        //    if ($scope.ImportLetter.hasOwnProperty("id")) {
        //        delete $scope.ImportLetter["id"];
        //    }
        //
        //    $scope.PostImportLetterAsNew($scope.PrepareToSend(2)).success(function (data) {
        //        $rootScope.$broadcast("RefreshExportList");
        //        sweetAlert("Good job!", "Successfully Sent", "success");
        //    }).error(function (data) {
        //        sweetAlert("Complete the letter", data, "error");
        //    });
        //};
        //
        //$scope.Save = function () {
        //    if ($scope.ImportLetter.hasOwnProperty("id")) {
        //        delete $scope.ImportLetter["id"];
        //    }
        //    $scope.PostImportLetterAsNew($scope.PrepareToSend(2)).success(function (data) {
        //        $rootScope.$broadcast("RefreshExportList");
        //        sweetAlert("Good job!", "Successfully Sent", "success");
        //        $state.go("letter.export");
        //    }).error(function (data) {
        //        sweetAlert("Complete the letter", data, "error");
        //    });
        //};
        //$scope.SaveRemoveDraft = function () {
        //
        //    if ($scope.ImportLetter.hasOwnProperty("id")) {
        //        delete $scope.ImportLetter["id"];
        //    }
        //    $scope.PostImportLetterAsNew($scope.PrepareToSend(2)).success(function (data) {
        //        $rootScope.$broadcast("RefreshExportList");
        //        sweetAlert("Good job!", "Successfully Sent", "success");
        //        $http.delete("api/v1/letter/sec/export/" + $stateParams.exportid + "/").success(function (data) {
        //            $state.go("letter.export");
        //        });
        //    }).error(function (data) {
        //        sweetAlert("Complete the letter", data, "error");
        //    });
        //};
        //$scope.SaveAsDraft = function () {
        //    $scope.PostImportLetter($scope.PrepareToSend(8)).success(function (data) {
        //        $rootScope.$broadcast("RefreshExportList");
        //        sweetAlert("Good job!", "Successfully Sent", "success");
        //    }).error(function (data) {
        //        sweetAlert("Complete the letter", data, "error");
        //    });
        //};
        //$scope.PostImportLetter = function (ImportLetter) {
        //    //////console.log("PostImportLetter");
        //    return $http.patch("api/v1/letter/sec/export/" + ImportLetter.id + "/", ImportLetter)
        //};
        //$scope.PostImportLetterAsNew = function (ImportLetter) {
        //    //////console.log("PostImportLetterAsNew");
        //    return $http.post("api/v1/letter/sec/export/", ImportLetter)
        //};
        $scope.init = function () {
            if ($stateParams.importid) {
                $http.get("api/v1/letter/sec/export-import/" + $stateParams.importid + "/get_prev/?id=" + $stateParams.importid).success(function (data) {
                    $scope.ImportLetter = data.letter;
                    $scope.UploadedFiles = $scope.ImportLetter.attachments;
                })
            } else {
                $scope.ImportLetter = {};
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

        function loadContacts() {
            return $scope.tagsResult.map(function (c, index) {
                var name = c.name;
                var id = c.id;
                var contact = {
                    name: name,
                    id: id
                };
                contact._lowername = contact.name.toLowerCase();
                return contact;
            });
        }


        var pendingSearch, cancelSearch = angular.noop;
        var lastSearch;


        $scope.AddNewTag = function () {
            swal({
                    title: "تگ جدید",
                    text: "لطفا عنوان تگ مورد نظر را وارد نمایید",
                    type: "input",
                    showCancelButton: true,
                    closeOnConfirm: false,
                    animation: "slide-from-top",
                    showLoaderOnConfirm: true,
                    inputPlaceholder: "عنوان تگ"
                },
                function (inputValue) {
                    if (inputValue === false) return false;

                    if (inputValue === "") {
                        swal.showInputError("نامی را وارد نمایید");
                        return false
                    }

                    $http.post("api/v1/letter/sec/tag/", {
                        "name": inputValue
                    }).success(function (data) {
                        swal("ثبت شد", "تک جدید شما :  " + inputValue, "success");
                    });

                });
        };


        $scope.allContacts = loadContacts;
        // $scope.contacts = [$scope.allContacts[0]];
        $scope.asyncContacts = [];
        $scope.filterSelected = true;

        $scope.querySearch = querySearch;
        $scope.delayedQuerySearch = delayedQuerySearch;

        $scope.tagsResult = [];

        /**
         * Search for contacts; use a random delay to simulate a remote call
         */
        function querySearch(criteria) {
            console.log("querySearch");
            return criteria ? $scope.allContacts().filter(createFilterFor(criteria)) : [];
        }

        /**
         * Async search for contacts
         * Also debounce the queries; since the md-contact-chips does not support this
         */
        function delayedQuerySearch(criteria) {
            // if (!pendingSearch || !debounceSearch()) {
            //     cancelSearch();

            return pendingSearch = $q(function (resolve, reject) {
                // Simulate async search... (after debouncing)
                cancelSearch = reject;

                $http.get("api/v1/letter/sec/tag/?q=" + criteria).success(function (data) {
                    var newN = [];
                    for (var i = 0; data.length > i; i++) {
                        newN.push({
                            "name": data[i]["name"] + " (" + data[i]["count"].toString() + ")",
                            "id": data[i]["id"]
                        });
                    }
                    $scope.tagsResult = newN;
                    resolve($scope.querySearch(criteria))
                });

            });


            return pendingSearch;
        }

        function refreshDebounce() {
            lastSearch = 0;
            pendingSearch = null;
            cancelSearch = angular.noop;
        }

        /**
         * Debounce if querying faster than 300ms
         */
        function debounceSearch() {
            var now = new Date().getMilliseconds();
            lastSearch = lastSearch || now;

            return ((now - lastSearch) < 300);
        }

        /**
         * Create filter function for a query string
         */
        function createFilterFor(query) {
            console.log("createFilterFor(" + query + ")");

            var lowercaseQuery = angular.lowercase(query);

            return function filterFn(contact) {
                return (contact._lowername.indexOf(lowercaseQuery) != -1);
            };

        }


    }
);