'use strict';


angular.module('AniTheme').controller(
    'LetterInboxCtrl',
    function ($scope,
              $translate,
              $q,
              $rootScope, $stateParams,
              $modal, $$$,
              $location,
              $http,
              shareService,
              shareServiceBool,
              LetterInboxService) {

        $scope.ComposeModal = {};
        $scope.prevLetterReplay = {};
        $scope.$on("ReplayTo", function (event, args) {
            $scope.prevLetterReplay = args.prevLetter;
            if ($scope.prevLetterReplay) {
                $scope.Compose();
            }
        });


        $scope.statics = {};
        $scope.$on("UpdateInboxStatics", function (event, args) {
            $scope.statics = args;
        });

        $rootScope.$broadcast("GetInboxStatic");

        $scope.GetDefaultDabir = function (items) {
            for (var i = 0; items.length > i; i++) {
                if (items[i].default) {
                    return items[i].name;
                }
            }

            return ""
        };

        ActivateSelectSec($scope, $http, $stateParams);

        //
        //$scope.Compose = function () {
        //    $scope.ComposeModal = $modal.open({
        //        animation: true,
        //        templateUrl: 'page/letter/compose',
        //        controller: 'LetterComposeCtrl',
        //        scope: $scope,
        //        size: '',
        //        resolve: {
        //            deps: ["$ocLazyLoad", function ($ocLazyLoad) {
        //                ////////console.log("perparing to get scripts");
        //                return $ocLazyLoad.load({
        //                    name: 'AniTheme.Compose',
        //                    files: [
        //                        '/static/angularThings/Letter/Compose/LetterComposeCtrl.js',
        //                        '/static/angularThings/Letter/Compose/LetterComposeService.js',
        //                        '/static/angularThings/Letter/Sidebar/Groups/classChart.js',
        //                        '/static/angularThings/Letter/Sidebar/Groups/classGroup.js',
        //                        '/static/angularThings/Letter/Sidebar/Groups/classMember.js',
        //                        '/static/angularThings/Letter/Sidebar/Groups/classZone.js'
        //                    ],
        //                    catch: true
        //                }).then(
        //                    function () {
        //                    }
        //                )
        //            }]
        //        }
        //    });
        //    $scope.ComposeModal.result.then(function (res) {
        //        growl.then("Successfully sent/saved !", {});
        //        //$scope.prevLetterReplay = {};
        //    }, function () {
        //        //$scope.prevLetterReplay = {};
        //    });
        //
        //};

        //setUpSideBar($scope, $http, $modal, $location, shareService, shareServiceBool, $$$);


//------------------------------- services
        var listLabel = function () {
            return $http.get("/api/v1/inboxLabels/")
        };
        var deleteLabel = function (id) {
            return $http.delete("/api/v1/inboxLabels/" + id + "/")

        };
        var listFolderTreeView = function () {
            return $http.get("/api/v1/inboxFolders/listFolderTreeView/")

        };
        var createFolder = function (folder) {
            if (folder.hasOwnProperty("id")) {
                return $http.patch("/api/v1/inboxFolders/" + folder.id + "/", folder)
            } else {
                return $http.post("/api/v1/inboxFolders/", folder)
            }
        };
        var listGroup = function () {
            return $http.get("/api/v1/inboxGroups/GetListForBar/")
        };
        var deleteFolder = function (id) {
            return $http.delete("/api/v1/inboxFolders/" + id + "/")

        };
        var deleteGroup = function (id) {
            return $http.delete("/api/v1/inboxGroups/" + id + "/")
        };
//----------------------------------- end service
        $scope.treedata = [];
        $scope.labels = {};
        $scope.listFolder = [];
//---------------------------------------
//----------------------------------------------------------------
//----------------------------------------------------------------
//--------- Labels ---------
        $scope.searchLabel = function (node) {
            ////////console.log(node);
            $scope.SelectedFolder = node;
            $rootScope.$broadcast("callInboxItemsWithTypeDynamicFolder", {
                itemType: -1,
                itemMode: -1,
                itemPlace: -1,
                SelectedLabel: node,
                SelectedFolder: {}
            });
        };
        $scope.newLabel = {};
        $scope.listLabel = function () {
            listLabel().then(function (data) {
                $scope.labels = data.data;
            }).catch(function (data) {

            });
        };
        $scope.createLabel = function () {
            var modalInstance = $modal.open({
                animation: true,
                templateUrl: 'LabelCreateModal',
                controller: 'ModalLabelCreateInstanceCtrl',
                size: '',
                resolve: {
                    oldLabel: function () {
                        return false;
                    }
                    ,
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'AniTheme.LabelModal',
                            files: [
                                '/static/angularThings/Letter/Sidebar/Labels/InboxLabelService.js',
                                '/static/angularThings/Letter/Sidebar/Labels/InboxLabelController.js'
                            ],
                            catch: true
                        }).then(
                            function () {
                            }
                        )
                    }]
                }
            });


            modalInstance.result.then(function (res) {
                swal('You add:', res.title, "success");
                $scope.listLabel();
            }, function () {

            });

        };
        $scope.editLabel = function (label) {
            var modalInstance = $modal.open({
                animation: true,
                templateUrl: 'LabelCreateModal',
                controller: 'ModalLabelCreateInstanceCtrl',
                size: '',
                resolve: {
                    oldLabel: function () {
                        return label;
                    },

                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        ////////console.log("perparing to get scripts");
                        return $ocLazyLoad.load({
                            name: 'AniTheme.ForgetPass',
                            files: [
                                '/static/angularThings/Letter/Sidebar/Labels/InboxLabelService.js',
                                '/static/angularThings/Letter/Sidebar/Labels/InboxLabelController.js',
                            ],
                            catch: true
                        }).then(
                            function () {
                            }
                        )
                    }]
                }
            });

            modalInstance.result.then(function (res) {
                swal('You edit:', res.title, "success");
                $scope.listLabel();
            }, function () {

            });

        };
        $scope.deleteLabel = function (obj) {
            swal({
                title: $$$("Are you sure?"),
                text: $$$("You will not be able to recover this imaginary file!"),
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: $$$("Yes, delete it!"),
                showLoaderOnConfirm: true,
                closeOnConfirm: false
            }, function () {

                deleteLabel(obj.id).then(function (data) {
                    swal($$$("Deleted!"), $$$("Your imaginary file has been deleted"), "success");
                    $scope.listLabel();

                });
            });
        };
        $scope.newObj = {};
//----------------------------------------------------------------
//----------------------------------------------------------------
//--------- Folders ---------
        $scope.listFolder = [];
        $scope.InboxFoldersStatics = [];
        $scope.FolderFiles = [];
        $scope.SelectFolder = function (node) {
            $scope.SelectedFolder = node;

            //$scope.GetInboxList();
            $rootScope.$broadcast("callInboxItemsWithTypeDynamicFolder", {
                itemType: -1,
                itemMode: -1,
                itemPlace: -1,
                SelectedFolder: node,
                SelectedLabel: {}

            });
            //$location.path("dashboard/Letter/list");

        };
        $scope.$on("callInboxFoldersStatics", function (event, args) {
            $scope.getFoldersCount();
        });
        $scope.getFoldersCount = function () {
            $http.get("getInboxFoldersStatistics").then(function (data) {
                $scope.InboxFoldersStatics = data.data;
            });
        };
        $scope.getFoldersCount();
        $scope.listFolderTreeView = function () {
            listFolderTreeView().then(function (data) {
                $scope.treedata = data.data;
                $http.get("getInboxFoldersStatistics").then(function (data) {
                    $scope.InboxFoldersStatics = data.data;
                    //
                    //for (var y = 0; $scope.treedata.length > y; y++) {
                    //    for (var i = 0; $scope.InboxFoldersStatics.length > i; i++) {
                    //        if ($scope.treedata[y].id == $scope.InboxFoldersStatics[i].id) {
                    //            ////////console.log($scope.InboxFoldersStatics[i].count);
                    //            $scope.treedata.count =  $scope.InboxFoldersStatics[i].count;
                    //        }
                    //    }
                    //}
                    //$scope.$apply();
                })

            }).catch(function (data) {

            });

        };
        $scope.openFolderModal = function (folder) {
            var modalInstance = $modal.open({
                animation: true,
                templateUrl: 'FolderModal',
                controller: 'FolderEditModalInstanceCtrl',
                size: '',

                resolve: {
                    oldFolder: function () {
                        return folder;
                    },

                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        ////////console.log("perparing to get scripts");
                        return $ocLazyLoad.load({
                            name: 'AniTheme.ForgetPass',
                            files: [
                                '/static/angularThings/Letter/Sidebar/Folders/InboxFolderService.js',
                                '/static/angularThings/Letter/Sidebar/Folders/InboxFolderController.js',
                            ],
                            catch: true
                        }).then(
                            function () {
                            }
                        )
                    }]
                }
            });
            modalInstance.result.then(function (res) {
                $scope.listFolderTreeView();
            }, function () {
            });
        };
        $scope.editFolderModal = function (folder) {
            $scope.openFolderModal(folder);
        };
        $scope.newFolder = function (parentObj) {
            if (parentObj) {
                var newObj = {"title": $scope.newObj.title, "parentID": parentObj.id, positionID: 1, "children": []};
            } else {
                var newObj = {"title": "", positionID: 1, "children": []};
            }
            swal({
                title: $$$("New Group"),
                text: $$$("Enter new group name"),
                type: "input",
                inputValue: $scope.newObj.title,
                showCancelButton: true,
                closeOnConfirm: false,
                animation: "slide-from-top",
                inputPlaceholder: $$$("Write something")
            }, function (inputValue) {
                if (inputValue === false) return false;
                if (inputValue === "") {
                    swal.showInputError($$$("You need to write something!"));
                    return false
                }
                newObj.title = inputValue;
                createFolder(newObj).then(function (data) {
                    swal($$$("Nice!"), $$$("You added") + ": " + data.data.title, "success");
                    $scope.listFolderTreeView();
                }).catch(function (data) {
                    swal('title', data.data.title, "error");
                });
            });
        };
        $scope.deleteFolder = function (obj) {
            swal({
                title: $$$("Are you sure?"),
                text: $$$("You will not be ble to recover this imaginary file!"),
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: $$$("Yes, delete it!"),
                showLoaderOnConfirm: true,
                closeOnConfirm: false
            }, function () {
                if (obj.children.length != 0) {

                    swal($$$("Error"), $$$("you should delete children first"), "error");
                    return false
                }
                deleteFolder(obj.id).then(function (data) {
                    swal($$$("Deleted!"), $$$("Your imaginary file has been deleted"), "success");
                    $scope.listFolderTreeView();

                });
            });
        };
//################################################################
//################################################################
//----------------------------------------------------------------
//----------------------------------------------------------------
//---------------Groups---------------------------------------
        $scope.group = {};
        $scope.groups = [];
        $scope.listGroup = function () {
            listGroup().then(function (data) {
                $scope.groups = data.data;
            }).catch(function (data) {

            });
        };
        $scope.createGroup = function () {
            swal({
                title: $$$("New Group"),
                text: $$$("Enter new group name"),
                type: "input",
                inputValue: $scope.group.title,
                showCancelButton: true,
                closeOnConfirm: false,
                animation: "slide-from-top",
                inputPlaceholder: $$$("Write something")
            }, function (inputValue) {
                if (inputValue === false) return false;
                if (inputValue === "") {
                    swal.showInputError($$$("You need to write something"));
                    return false
                }
                $scope.group.title = inputValue;
                $scope.group.positionID = 2;
                $http.post("/api/v1/inboxGroups/", $scope.group).then(function (data) {
                    swal($$$("Nice"), $$$("You added") + " :" + data.data.title, "success");
                    $scope.listGroup();
                }).catch(function (data) {
                    swal('title', $$$(data.data.title), "error");
                });
            });
        };
        $scope.editGroup = function (group) {
            var modalInstance = $modal.open({
                animation: true,
                templateUrl: 'GroupEditModal',
                controller: 'GroupEditModalInstanceCtrl',
                size: '',
                resolve: {
                    oldGroup: function () {
                        return group;
                    },

                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        ////////console.log("perparing to get scripts");
                        return $ocLazyLoad.load({
                            name: 'AniTheme.ForgetPass',
                            files: [
                                '/static/angularThings/Letter/Sidebar/Groups/InboxGroupService.js',
                                '/static/angularThings/Letter/Sidebar/Groups/InboxGroupController.js',
                                '/static/angularThings/Letter/Sidebar/Groups/classChart.js',
                                '/static/angularThings/Letter/Sidebar/Groups/classGroup.js',
                                '/static/angularThings/Letter/Sidebar/Groups/classMember.js',
                                '/static/angularThings/Letter/Sidebar/Groups/classZone.js'
                            ],
                            catch: true
                        }).then(
                            function () {
                            }
                        )
                    }]
                }
            });

            modalInstance.result.then(function (res) {
                swal('You edit:', res.title, "success");
                $scope.listGroup();
            }, function () {

            });

        };
        $scope.deleteGroup = function (obj) {
            swal({
                title: $$$("Are you sure ?"),
                text: $$$("You will not be able to recover this imaginary file!"),
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: $$$("Yes, delete it!"),
                showLoaderOnConfirm: true,
                closeOnConfirm: false
            }, function () {

                deleteGroup(obj.id).then(function (data) {
                    swal($$$("Deleted!"), $$$("Your imaginary file has been deleted"), "success");
                    $scope.listGroup();

                });
            });
        };
//################################################################
//################################################################
        $scope.listGroup();
        $scope.listLabel();
        $scope.listFolderTreeView();
        $scope.$on('ngRepeatFinished', function (ngRepeatFinishedEvent) {
            $(".inbox-dynamic-items").hover(function () {
                $(this).find(".btnss").fadeIn(70);
            }, function () {
                $(this).find(".btnss").fadeOut(20);
            });
        });

        $scope.itemType = 1;
        $scope.itemMode = 1;
        $scope.itemPlace = 1;
        $scope.ss = {};

        $scope.$root.$on("ShareServiceUpdated", function (event, args) {
            $scope.ss = shareService.get();
        });


        $scope.ListPosition = "";
        $rootScope.$on("UpdateActiveListStyle", function (event, args) {
            $scope.ListPosition = args;
        });


        $scope.callInboxList = function (itemType, itemMode, itemPlace) {
            //debugger;

            $scope.itemType = itemType;
            $scope.itemMode = itemMode;
            $scope.itemPlace = itemPlace;
            $rootScope.$broadcast("callInboxItemsWithType", {
                itemType: itemType,
                itemMode: itemMode,
                itemPlace: itemPlace
            });
            $location.path("dashboard/Letter/Inbox/List");

        }


    });






