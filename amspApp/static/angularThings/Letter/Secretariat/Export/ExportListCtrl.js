'use strict';


angular.module('AniTheme').controller(
    'ExportListCtrl',
    function ($scope,
              $translate,
              $q,
              $rootScope,
              $modal,
              $location, $stateParams,
              $http, $$$,
              $state,
              debounce) {


        $scope.urlMember = "api/v1/members-search/";
        $scope.__GetMembersListByPager = function (addr) {
            return $http.get(addr);
        };
        $scope.__GetMembers = function (q, page_size) {
            return $http.get($scope.urlMember + "?q=" + q + "&page_size=" + page_size)
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
        $scope.filterSendAgain = {};
        $scope.filterSendAgain.MembersTableSearch = "";


        $scope.Table = {};
        $scope.Table.pagination = {};
        $scope.Table.pagination.size = 10;
        $scope.Table.pagination.total = 0;
        $scope.Table.isShow = false;


        $scope.SendItAgain = function () {
            var dtToSend = {
                "selectedLetter": $scope.currentSelectLetter,
                "persons": $scope.SelectedMembers
            }

            $http.post("api/v1/letter/sec/export-import/resend/", dtToSend).success(function (data) {

            })
        }

        $scope.HandleImportTablePagination = function () {
            if ($scope.Table.pagination.size == 40) {
                $scope.Table.pagination.size = 5;
            }
            $scope.Table.pagination.size = $scope.Table.pagination.size + 5;
            $scope.GetExportList();
        };


        $scope.ChangeStar = function (item) {
            item.star = !item.star;
            $http.post("api/v1/inbox/ChangeStar/", item).success(function (data) {

            })
        }


        $scope.$watchCollection("filterSendAgain", function () {
            $scope.GetMembers(15);
        });


        $scope.SelectedMembers = [];

        $scope.SelectPersonToSendAgain = function (item) {
            $scope.SelectedMembers.push(item)
        }

        $scope.RemoveFromSelectedSendAgain = function ($index) {
            $scope.SelectedMembers.splice($index)
        }

        $scope.membersTableGoToPage = function (url) {
            $scope.__GetMembersListByPager(url).success(function (data) {
                $scope.Members = data;
            });
        };

        $scope.ChangeFilterStar = function () {
            $scope.filter.starred = !$scope.filter.starred;
        }

        $scope.GetMembers = function (pagingSize) {
            $scope.isSearchCallbackCompleted = false;
            $scope.__GetMembers($scope.filterSendAgain.MembersTableSearch, pagingSize).success(function (data) {
                $scope.isSearchCallbackCompleted = true;
                $scope.Members = data;
            }).error(function () {
                $scope.isSearchCallbackCompleted = true;
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


        $scope.ExportletterList = {};
        $scope.filter = {};
        $scope.filter.starred = false;


        $scope.filtershow = function () {
            $("#filtershow").toggleClass("hide");
        };

        $scope.$root.$on("RefreshExportList", function (args, event) {
            $scope.GetExportList();
        });
        var originatorEv;
        $scope.openMenu = function ($mdOpenMenu, ev) {
            originatorEv = ev;
            $mdOpenMenu(ev);
        };
        $scope.prepareNew = function (obj) {
            $state.go("letter.export.new");
        };
        $scope.prepareDraft = function (obj) {
            $state.go("letter.export.new", {exportid: obj.id});
        };
        $scope.prepareTemplate = function (obj) {
            $state.go("letter.export.new", {exportid: obj.id});
        };
        $scope.previewExport = function (obj) {
            $state.go("letter.export.preview", {exportid: obj.id});
        };
        $scope.previewImport = function (obj) {
            //////console.log(obj);
            $state.go("letter.export.import", {importid: obj.id});
        };
        $scope.PrePreview = function (obj) {
            if (!obj) {
                $scope.prepareNew();
            } else if (obj.itemMode == 5) {
                $scope.prepareDraft(obj);
            } else if (obj.itemMode == 11) {
                $scope.prepareTemplate(obj);
            } else if (obj.itemMode == 10) {
                $scope.previewImport(obj);
            } else if (obj.itemMode == 9) {
                $scope.previewExport(obj);
            }
        };


        $scope.GoToPage = function (url) {
            $http.get(url).success(function (data) {
                $scope.ExportletterList = data;
            })
        };
        //$scope.GetExportList();


//----------------- this is for selecting compnay ...
        $scope.selectedCompanies = [];
        $scope.autocompleteDemoRequireMatch = true;
        $scope.CompaniesToSearch = {};
        $scope.searchCompanyText = "";
        $scope.searchCompanyItem = {};
        $scope.filter.selectedCompanies = [];
        $scope.transformCompanyChip = function (chip) {
            if (angular.isObject(chip)) {
                return chip;
            }
            return {name: chip.name, type: 'new'}
        };
        $scope.queryCompanySearch = function (query) {
            var defer = $q.defer();
            var ss = $http.get("api/v1/letter/sec/company/?q=" + query + "&page_size=20");
            ss.success(function (data) {
                return defer.resolve(data.data.results);
            });
            return defer.promise;
        };
//-----------------

        $scope.filter = {};
        $scope.filter.exportList = true;
        $scope.filter.exportDraftList = true;
        $scope.filter.importList = true;
        $scope.filter.startDate = "";
        $scope.filter.endDate = "";
        $scope.filter.selectedCompanies = [];
        $scope.filter.searchString = "";


        $scope.SuspendIt = function (item) {
            ////console.log(item);
            var updated = !(Boolean(item.extra.is_export_suspended));
            item.extra.is_export_suspended = updated;
            $http.post("api/v1/letter/sec/export/" + item.letter.id + "/changeSuspend/",
                {
                    'is_export_suspended': updated
                });
        };

        $scope.Preview = function (item) {
            $state.go("letter.export.templates", {exportid: item.id});
        };


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
            filter.page_size = $scope.Table.pagination.size;
            filter.starred = $scope.filter.starred;


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
                ss = "9;5;10"
            }
            filter.p = '-1,' + ss + ',-1';
            var filterResult = $.param(filter);

            //////console.log(filterRes);
            $scope.waitForLoading = true;
            $http.get("api/v1/letter/sec/export/?" + filterResult).success(function (data) {
                $scope.waitForLoading = false;

                $scope.ExportletterList = data;
            }).error(function () {
                $scope.waitForLoading = false;

            });
        };

        $scope.Download = function (filename) {
            downloadURL(filename);
        };

        $scope.SendAgainImported = function (item) {
            $scope.currentSelectLetter = item;
            $("#modal_select_imported_positions_send_again").modal("show");
        };


        $scope.RemoveExportDraft = function (item) {
            swal({
                title: $$$("Are you sure?"),
                text: $$$("You will not be able to recover this draft letter file"),
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: $$$("Yes"),
                closeOnConfirm: false,
                showLoaderOnConfirm: true
            }, function () {
                $http.delete("api/v1/letter/sec/export/" + item.id + "/").success(function (data) {
                    $scope.GetExportList();
                    swal($$$("Deleted"), $$$("Your draft letter file has been deleted"), "success");
                })
            });
        };


        $scope.Recieved = function (item) {
            $state.go("letter.export.recieved", {exportid: item.id});
        };

        $scope.Scan = function (item) {
            $state.go("letter.export.scan", {exportid: item.id});
        };


        $scope.$watchCollection('filter',
            debounce(function () {
                $scope.GetExportList();
            }, 300), true);

        $scope.$watchCollection('filter.selectedCompanies',
            debounce(function () {
                $scope.GetExportList();
            }, 300), true);

        $scope.GetDefaultDabir = function (items) {
            for (var i = 0; items.length > i; i++) {
                if (items[i].default) {
                    return items[i].name;
                }
            }
            return ""
        };

        ActivateSelectSec($scope, $http, $stateParams);

    });