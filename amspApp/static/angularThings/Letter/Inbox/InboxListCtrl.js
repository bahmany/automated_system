'use strict';


angular.module('AniTheme').controller(
    'InboxListCtrl',
    function ($scope,
              $translate,
              $location,
              $q,
              $state,
              $timeout,
              $rootScope,
              $modal, $$$,
              $http,
              shareService, $mdSidenav,
              InboxListService,
              shareServiceBool) {


        $rootScope.$on("hideInboxLeft", function (ev, args) {
            angular.element(document.getElementById("divList")).css("margin-right", "0");
            // angular.element(document.getElementById("rightInboxList")).css("display", "none");
            angular.element(document.getElementById("btnInboxShowRightMenu")).text("نمایش منو");
            $mdSidenav("rightInboxList").close();
        });


        $scope.showNotShow = function () {

            if ($mdSidenav("rightInboxList").isOpen()) {
                angular.element(document.getElementById("divList")).css("margin-right", "0");

                angular.element(document.getElementById("btnInboxShowRightMenu")).text("نمایش منو");
                // angular.element(document.getElementById("sidebar-right-container")).css("display", "block");
                // angular.element(document.getElementById("div_maincontent")).css("right", "250px");

            } else {
                angular.element(document.getElementById("divList")).css("margin-right", "250px");
                angular.element(document.getElementById("btnInboxShowRightMenu")).text("بستن منو");
                // angular.element(document.getElementById("sidebar-right-container")).css("display", "none");
                // angular.element(document.getElementById("div_maincontent")).css("right", "0");

            }


            $mdSidenav("rightInboxList").toggle()
        }


        $scope.callInboxList = function () {
            $rootScope.$broadcast("callInboxItemsWithType", {
                itemType: -1,
                itemMode: 1,
                itemPlace: 1
            });
        }


        $scope.createNewElastic = function () {
            $http.get("/api/v1/inbox/StartConverting/").then(function (data) {

            });
        }


        $scope.HandleItem = function (item) {
            var itemType = item.itemType;
            var itemMode = item.itemMode;
            var itemPlace = item.itemPlace;
            var icon = "";
            var text = "";
            var txtItemMode = "";
            switch (itemMode) {
                case 1 :
                    txtItemMode = " نامه داخلی ";
                    break;
                case 2 :
                    txtItemMode = " رونوشت صادره ";
                    break;
                case 3 :
                    txtItemMode = " رونوشت وارده ";
                    break;
                case 4 :
                    txtItemMode = " پیش نویس ";
                    break;
                case 5 :
                    txtItemMode = " پیش نویس صادره ";
                    break;
                case 6 :
                    txtItemMode = " پیش نویس وارده ";
                    break;
                case 7 :
                    txtItemMode = " اولین ارسال نامه داخلی ";
                    break;
                case 8 :
                    txtItemMode = " ارجای نامه داخلی ";
                    break;
                case 9 :
                    txtItemMode = " صادره ";
                    break;
                case 10 :
                    txtItemMode = " وارده ";
                    break;
                case 11 :
                    txtItemMode = " تمپلیت صادره ";
                    break;
                case 12 :
                    txtItemMode = " تمپلیت وارده ";
                    break;
                default:
                    txtItemMode = "ناشناس";
            }

            var txtItemType = "";
            switch (itemType) {
                case 1 :
                    txtItemType = " دریافت شده از طریق ارسال ";
                    break;
                case 2 :
                    txtItemType = " ارسال شده ";
                    break;
                case 3 :
                    txtItemType = " دریافت شده از طریق ارجاع ";
                    break;
                case 4 :
                    txtItemType = " دریافت شده از طریق پاسخ ";
                    break;
                case 5 :
                    txtItemType = " دریافت شده از طریق رونوشت خودکار ";
                    break;
                case 6 :
                    txtItemType = " اولین ارسال ";
                    break;
                case 7 :
                    txtItemType = " بدون عملیات ";
                    break;
                case 8 :
                    txtItemType = " دریافت شده از طریق ارجاع ";
                    break;
                case 9 :
                    txtItemType = " توسط شما ";
                    break;
                case 10 :
                    txtItemType = " دریافت شده از طریق ارجاع ";
                    break;
                default:
                    txtItemType = "ناشناس";

            }

            return txtItemMode + txtItemType;

        };


        $scope.ListTitle = "";
        $scope.HandleListTitle = function (item) {

            if (item == "-1,1,1") {
                $scope.ListTitle = "کارتابل";
            }
            if (item == "6,7,1") {
                $scope.ListTitle = "ارسال شده ها";
            }
            if (item == "9,-1,-1") {
                $scope.ListTitle = "ارجاعیات";
            }
            if (item == "-1,4,1") {
                $scope.ListTitle = "پیش نویس";
            }
            if (item == "5,1,1") {
                $scope.ListTitle = "رونوشت خودکار";
            }
            if (item == "-1,-1,2") {
                $scope.ListTitle = "آرشیو";
            }
            if (item == "-1,-1,3") {
                $scope.ListTitle = "حذف شده ها";
            }
            if (item == "-1,-1,-1") {
                $scope.ListTitle = "پوشه یا برچسب";
            }
        }


        $scope.demo = {};
        $scope.demo.hidden = false;
        $scope.demo.isOpen = false;
        $scope.demo.hover = false;
        $scope.$watch('demo.isOpen', function (isOpen) {
            if (isOpen) {
                $timeout(function () {
                    $scope.tooltipVisible = self.isOpen;
                }, 600);
            } else {
                $scope.tooltipVisible = self.isOpen;
            }
        });


        $scope.ShowFilter = function () {
            $scope.ShowSearchPanel = !$scope.ShowSearchPanel;
        }

        $scope.ShowSearchPanel = false;
        $scope.InboxList = {};
        $scope.itemType = -1;
        $scope.itemMode = 1;
        $scope.itemPlace = 1;
        $scope.currentSelected = {};
        /*
         here we have letter Type and letter Mode and its differences are listed bellow
         itemType:
         1 = this inbox item received and sent by some one else as usual inside letter
         2 = this inbox item is sent to a user and an inbox item listed in send letters
         3 = this inbox item forwarded
         4 = this inbox item is replied one, i mean this letter is a replay letter
         5 = this inbox item is auto send inbox as rooneveshte khodkar
         6 = this inbox item is first sent of a user for showing it in sent items

         itemMode :
         1 = dakheli
         2 = rooneveshte sadereh
         3 = rooneveshte varedeh
         4 = draft
         5 = draft sadere
         6 = draft varedeh

         */


        $scope.filter = {};

        $scope.$watchGroup(["filter.q1", "filter.q2", "filter.q3", "filter.q4", "filter.startdate", "filter.enddate"], function () {
            //if (shareServiceBool.get() == true) {
            //    return
            //}
            $scope.GetInboxList();
        }, true);

        $rootScope.$on("newNotification", function () {
            $http.get("/api/v1/inbox/GetLastInboxID/").then(function (data) {
                if (data.data.r != 0) {
                    var result = $scope.GenerateFilterForRequests();
                    InboxListService.GetInboxList(
                        result.q,
                        result.itemTypes
                    ).then(function (data) {
                        if (data.data.results) {
                            if (len(data.data.results) > 0) {
                                $scope.GetInboxList();
                            }
                        }
                    }).catch(function (data) {
                    });

                    // if ($scope.InboxList.results[0].id != data.r) {
                    //     $scope.GetInboxList();
                    // }
                }
            })
        });

        $scope.ForwardSelected = function () {
            ////console.log("ForwardSelected");
            $rootScope.$broadcast("setSelectMemProp", {
                prevDivName: "divList",
                currDivName: "divFor",
                thisListIsFor: 2,
                selectedInbox: GetSelected()
            });
            $("#divList").fadeOut(function () {
                $("#divFor").fadeIn();
            });
        };
        $scope.ForwardSelectedArchve = function () {
            ////console.log("ForwardSelected");
            $rootScope.$broadcast("setSelectMemProp", {
                prevDivName: "divList",
                currDivName: "divFor",
                thisListIsFor: 6,
                selectedInbox: GetSelected()
            });
            $("#divList").fadeOut(function () {
                $("#divFor").fadeIn();
            });
        };
        $scope.TrashSelected = function () {
            swal({
                title: $$$("Are you sure?"),
                text: $$$("Selected letter move to your trash!"),
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: $$$("Yes, remove it!"),
                cancelButtonText: $$$("No, cancel plx!"),
                closeOnConfirm: false,
                closeOnCancel: false,
                showLoaderOnConfirm: true
            }, function (isConfirm) {
                if (isConfirm) {
                    $http.post("/api/v1/inbox/MoveSelectedToTrash/", GetSelected()).then(function (data) {
                        $rootScope.GetIntimeNotification();
                        swal($$$("Removed!"), $$$("Selected letter successfully removed to trash ."), "success");
                        $timeout(function () {
                            $scope.GetInboxList();
                        }, 2000);
                    });
                } else {
                    swal($$$("Cancelled", $$$("Operation canceled", "error")));
                }
            });
        };

        function GetSelected() {
            var selectedInboxID = [];
            for (var i = 0; $scope.InboxList.results.length > i; i++) {
                if ($scope.InboxList.results[i].selected) {
                    selectedInboxID.push($scope.InboxList.results[i].id)
                }
            }
            return selectedInboxID
        }

        $scope.MoveToArchive = function () {
            $http.post("/api/v1/inbox/MoveSelectedToArchive/", GetSelected()).then(function (data) {
                $timeout(function () {
                    $scope.GetInboxList();
                    $rootScope.GetIntimeNotification();
                }, 1000);
            }).catch(function () {

            });
        };
        $scope.ListSelectAll = false;
        $scope.CheckSelections = function () {
            for (var i = 0; $scope.InboxList.results.length > i; i++) {
                if ($scope.InboxList.results[i].selected) {
                    $scope.InboxList.selected = true;
                    return
                }
            }
            $scope.InboxList.selected = false;
        };
        $scope.ToggleSelected = function () {
            for (var i = 0; $scope.InboxList.results.length > i; i++) {
                $scope.InboxList.results[i].selected = !$scope.ListSelectAll;
            }
            $scope.CheckSelections();
        };
        $scope.OpenSearchMenu = function () {
            $("#navbarCollapseSearchList").toggleClass('slide-show', 'slide-hide');
        };

        // $scope.$on("callInboxItems", function (event, args) {
        //     $scope.GetInboxList($scope.LetterType);
        // });
        $rootScope.$on("callInboxItems", function (event, args) {
            $scope.GetInboxList($scope.LetterType);

        });
        $scope.dynamicFoldersStatic = [];
        $scope.GetInboxDynamicFoldersCount = function () {
            $http.get("getInboxFoldersStatistics").then(function (data) {
                $scope.dynamicFoldersStatic = data.data;
                for (var i = 0; $scope.dynamicFoldersStatic.length > i; i++) {
                    $("#inbox_dyna_" + $scope.dynamicFoldersStatic[i].id).text($scope.dynamicFoldersStatic[i].count);
                }
            });
        };
        $timeout(function () {
            $scope.GetInboxDynamicFoldersCount();
        }, 0);
        $scope.$on("GetInboxDynamicFoldersCount", function (event, args) {
            $scope.GetInboxDynamicFoldersCount();
        });
        $scope.$on("GetInboxDynamicLabelsCount", function (event, args) {
            $scope.GetInboxDynamicLabelsCount();
        });
        $scope.dynamicLabelsStatic = [];
        $scope.GetInboxDynamicLabelsCount = function () {
            $http.get("getInboxLabelsStatistics").then(function (data) {
                $scope.dynamicLabelsStatic = data.data;
                for (var i = 0; $scope.dynamicLabelsStatic.length > i; i++) {
                    $("#inbox_dyna_lbl_" + $scope.dynamicLabelsStatic[i].id).text($scope.dynamicLabelsStatic[i].count);
                }
            });
        };
        $timeout(function () {
            $scope.GetInboxDynamicLabelsCount();
        }, 0);
        $scope.ChangeStar = function (item) {
            item.star = !item.star;
            $http.post("/api/v1/inbox/ChangeStar/", item).then(function (data) {

            })
        }
        // it support both labels and folders
        $scope.dropCallbackAddToFolder = function (event, ui, inbox, hhh) {
            var zzz = this.dndDragItem;
            if (zzz.bgcolor) {
                var q = {
                    inboxID: this.item.id,
                    labelID: this.dndDragItem.id
                };
                $http.post("/api/v1/inboxLabels/AddLetterTo/", q).then(function (data) {
                    $rootScope.GetIntimeNotification();
                    //$scope.getFoldersCount();
                    if (inbox.labels == undefined) {
                        inbox.labels = [];
                    }
                    if (inbox.labels == null) {
                        inbox.labels = [];
                    }
                    if (getClass(inbox.labels) == "Object") {
                        inbox.labels = [];
                    }
                    inbox.labels.push(zzz);
                    //
                    $scope.GetInboxDynamicLabelsCount();
                });
            } else {
                var q = {
                    inboxID: this.item.id,
                    folderID: this.dndDragItem.id
                };
                $http.post("/api/v1/inboxFolders/AddLetterTo/", q).then(function (data) {
                    $rootScope.GetIntimeNotification();
                    //$scope.getFoldersCount();
                    if (inbox.folders == undefined) {
                        inbox.folders = [];
                    }
                    if (inbox.folders == null) {
                        inbox.folders = [];
                    }
                    if (getClass(inbox.folders) == "Object") {
                        inbox.folders = [];
                    }
                    inbox.folders.push(zzz);
                    //
                    $scope.GetInboxDynamicFoldersCount();
                });
            }
        };
        $scope.backFromPrev = false;
        $scope.$root.$on("transferList", function (event, args) {
            $scope.backFromPrev = true;
            ////////console.log(args);
            $scope.InboxList = args;

        });

        //shareServiceBool.set(false); // for handling back from prev

        $scope.$on("callInboxItemsWithType", function (event, args) {
            ////////console.log(args);
            $scope.itemType = args.itemType;
            $scope.itemMode = args.itemMode;
            $scope.itemPlace = args.itemPlace;
            $scope.GetInboxList();
        });
        $scope.$on("callInboxItemsWithTypeDynamicFolder", function (event, args) {
            ////////console.log(args);
            $scope.itemType = args.itemType;
            $scope.itemMode = args.itemMode;
            $scope.itemPlace = args.itemPlace;
            $scope.SelectedFolder = (args.hasOwnProperty("SelectedFolder")) ? args.SelectedFolder : $scope.SelectedFolder;
            $scope.SelectedLabel = (args.hasOwnProperty("SelectedLabel")) ? args.SelectedLabel : $scope.SelectedLabel;
            $scope.GetInboxList();
            //$scope.GetInboxListByFolderOrLabel();
        });
        $scope.SelectAllItems = function () {
            var count = $scope.InboxList.results.length;
            for (var i = 0; count > i; i++) {
                $scope.InboxList.results[i].selected = true;
            }
        };
        $scope.UnSelectAllItems = function () {
            var count = $scope.InboxList.results.length;
            for (var i = 0; count > i; i++) {
                $scope.InboxList.results[i].selected = false;
            }
        };
        $scope.SelectedFolder = {};
        $scope.SelectedLabel = {};
        //$scope.GetInboxListByFolderOrLabel = function () {
        //
        //    //////debugger;
        //    InboxListService.GetInboxListBy(
        //        $scope.InboxSearchText,
        //        $scope.SelectedFolder.id,
        //        $scope.SelectedLabel.id).then(function (data) {
        //            $scope.InboxList = data;
        //            ////////console.log($scope.InboxList);
        //            $scope.isSearchCallbackCompleted = true;
        //        }).catch(function (data) {
        //            $scope.isSearchCallbackCompleted = true;
        //        });
        //}
        $timeout(function () {
            if (typeof($(".picker").datepicker) !== 'function'){
                return
            }
            $(".picker").datepicker({
                showOn: 'button',
                buttonImage: 'static/images/open-iconic-master/png/calendar-2x.png',
                buttonImageOnly: true,
                dateFormat: 'yy/mm/dd'
            });
        }, 0);

        $scope.removeFolderFilter = function () {
            $scope.SelectedFolder = {};
            $scope.filter.fi = null;
            $scope.GetInboxList();
        };
        $scope.removeLabelFilter = function () {
            $scope.SelectedLabel = {};
            $scope.filter.li = null;
            $scope.GetInboxList();
        };

        $scope.filter.r = 1;
        $scope.filter.s = 1;

        $scope.ChangeReadUnread = function () {
            if ($scope.filter.r == 1) {
                $scope.filter.r = 2; // just unread
                $scope.GetInboxList();
                return
            }
            if ($scope.filter.r == 2) {
                $scope.filter.r = 3;// just read
                $scope.GetInboxList();

                return
            }
            $scope.filter.r = 1; // all
            $scope.GetInboxList();

        };

        $scope.ChangeListStar = function () {
            if ($scope.filter.s == 1) {
                $scope.filter.s = 2;
                $scope.GetInboxList();
                return
            }
            $scope.filter.s = 1;
            $scope.GetInboxList();
        };

        $scope.GenerateFilterForRequests = function () {
            $scope.isSearchCallbackCompleted = false;
            $scope.filter.fi = $scope.SelectedFolder.id;
            $scope.filter.li = $scope.SelectedLabel.id;
            $scope.HandleListTitle([$scope.itemType, $scope.itemMode, $scope.itemPlace].join(","));
            var q = $.param($scope.filter);
            return {
                q: q,
                itemTypes: [$scope.itemType,
                    $scope.itemMode,
                    $scope.itemPlace]
            }

        }

        $scope.GetInboxList = function () {
            if (shareServiceBool.get() == true) {
                $scope.InboxList = shareService.get();
                shareServiceBool.set(false); // for handling back from prev
                return
            }

            var result = $scope.GenerateFilterForRequests();
            $rootScope.$broadcast("UpdateActiveListStyle", [$scope.itemType, $scope.itemMode, $scope.itemPlace].join(","));


            InboxListService.GetInboxList(
                result.q,
                result.itemTypes
            ).then(function (data) {
                shareService.set(data.data);
                if ($rootScope.$broadcast) {
                    $rootScope.$broadcast("ShareServiceUpdated");
                }
                $scope.InboxList = shareService.get();
                $scope.isSearchCallbackCompleted = true;
            }).catch(function (data) {
                $scope.isSearchCallbackCompleted = true;
            });
        };


        $scope.init = function () {
            if (!shareService.get().results) {
                $scope.GetInboxList();
            }
        };
        $scope.init();
        $scope.isSearchCallbackCompleted = true;
        $scope.InboxPageTo = function (PagedUrl) {
            $scope.isSearchCallbackCompleted = false;
            InboxListService.GetInboxListByPager(PagedUrl).then(function (data) {
                $scope.isSearchCallbackCompleted = true;
                $scope.InboxList = data.data;
            }).catch(function (data) {
                $scope.isSearchCallbackCompleted = true;
            });
        };
        $scope.MakeLetterRead = function (inboxID) {
            InboxListService.MakeLetterRead(inboxID).then(function (data) {
                $rootScope.GetIntimeNotification();
            })
        };
        $scope.OpenLetter = function (inboxItem, index, $event) {

            //$scope.MakeLetterRead(inboxItem.id);
            $scope.currentSelected = inboxItem;
            //debugger;
            $scope.InboxList.results[index].seen = true;
            var t = $scope.InboxList;
            shareService.set(t);
            ////////console.log(inboxItem);
            //if (inboxItem.itemMode == 4) {
            //    $location.path('/dashboard/Letter/' + inboxItem.letter.id + '/compose');
            //    return
            //}
            $location.path('/dashboard/Letter/Inbox/' + inboxItem.id + '/Preview');
            inboxItem.seen = true;
        };
        $scope.loadingComposeLetter = false;

        // $rootScope.$on("makeNewLetter", function () {
        //     $scope.NewLetter();
        // });





    });






