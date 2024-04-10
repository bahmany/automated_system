'use strict';


angular.module('AniTheme').controller(
    'ContactsCtrl',
    function ($scope,
              $translate,
              $http,
              $q, $mdDialog,
              $rootScope,
              $modal) {

        $scope.Contacts = [];
        $scope.Contact = {};
        $scope.selectedContact = {};

        var originatorEv;
        $scope.openMenu = function ($mdOpenMenu, ev) {
            originatorEv = ev;
            $mdOpenMenu(ev);
        };


        $scope.AddContact = function () {
            $scope.selectedContact = null;
            var modalInstance = $modal.open({
                animation: true,
                templateUrl: 'page/edit-contact',
                controller: "ContactModalCtrl",
                size: '',
                resolve: {
                    oldItem: function () {
                        return null;
                    },
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'AniTheme.contact',
                            files: [
                                '/static/angularThings/contacts/editContactCtrl.js'
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

            }, function () {
            });
        };
        $scope.$root.$on("GetSelectedContact", function () {
            $rootScope.$broadcast("SetCurrentContact", $scope.selectedContact);
        });
        $scope.$root.$on("reloadContacts", function () {
            $scope.GetContacts();
        });
        $scope.EditContact = function (item) {
            $scope.selectedContact = item;
            var modalInstance = $modal.open({
                animation: true,
                templateUrl: 'page/edit-contact',
                controller: "ContactModalCtrl",
                size: '',
                resolve: {
                    oldItem: function () {
                        return angular.copy(item);
                    },
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'AniTheme.contact',
                            files: [
                                '/static/angularThings/contacts/editContactCtrl.js'
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

            }, function () {
            });
        };
        $scope.GetRow1 = function (item) {
            if (item.fields.length > 0) {
                return item.fields[0].fieldValue
            }
        };
        $scope.GetRow2 = function (item) {
            if (item.fields.length > 1) {
                return item.fields[1].fieldValue
            }
        };
        $scope.GetRow3 = function (item) {
            if (item.fields.length > 2) {
                return item.fields[2].fieldValue
            }
        };
        $scope.ChangeStar = function (item) {
            item.extra.starred = !((item.extra.starred) == true);
            $http.patch("/api/v1/contacts/" + item.id + "/", item).then(function (data) {
                $scope.GetStarredContacts();

            });
        }
        $scope.checkForDefaultAvatar = function (item) {
            if (!(item.extra.avatar)) {
                item.extra.avatar = "/static/images/default-avatar-contact.jpg";
            }
        };
        $scope.RemoveContact = function (item) {

            swal({
                title: "Are you sure?",
                text: "You will not be able to recover this imaginary file!",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "Yes, delete it!",
                closeOnConfirm: false,
                showLoaderOnConfirm: true
            }, function () {
                $http.delete("/api/v1/contacts/" + item.id + "/").then(function (data) {
                    $scope.GetContacts();
                    swal("Deleted!", "Your imaginary file has been deleted.", "success");

                })
            });


        };
        $scope.StarredContacts = {};

        $scope.GetStarredContacts = function () {
            $http.get("/api/v1/contacts/?starred=0&group_id=" + $scope.FilteredGroupID + "&q=" + $scope.SearchText + "&starred=1").then(function (data) {
                $scope.StarredContacts = data.data;
            });
        };


        $scope.GetContacts = function () {
            $http.get("/api/v1/contacts/?starred=0&group_id=" + $scope.FilteredGroupID + "&q=" + $scope.SearchText).then(function (data) {
                $scope.Contacts = data.data;
            });
            $scope.GetStarredContacts();

        };


        $scope.ContactsPageTo = function (page) {
            $http.get(page).then(function (data) {
                $scope.Contacts = data.data;
            });
        }


        $scope.GetItemSelected = function (item) {
            if (item.id == $scope.FilteredGroupID) {
                return false;
            }
            return true;
        };

        $scope.EditGroup = function (item) {
            var newName = prompt("Please enter new name");
            if (newName) {
                $http.patch("/api/v1/groups-contacts/" + item.id + "/", {
                    name: newName
                }).then(function (data) {
                    $scope.GetGroups();
                    alert("Updated");
                }).catch(function (data) {
                    alert("error");
                })
            }
        };

        $scope.RemoveGroup = function (item) {
            if (confirm("Are you ready ?")) {
                $http.delete("/api/v1/groups-contacts/" + item.id + "/").then(function (data) {
                    $scope.GetGroups();
                    alert("Deleted");
                })
            }
        };

        $scope.ContactGroups = {};
        $scope.FilteredGroupID = "";
        $scope.SearchText = "";

        $scope.GetGroups = function () {
            $http.get("/api/v1/groups-contacts/").then(function (data) {
                $scope.ContactGroups = data.data;
            })
        };
        $scope.GetGroups();

        $scope.FilterContacts = function (groupID) {
            $scope.FilteredGroupID = groupID;
            $scope.GetContacts();
        };
        $scope.AllContacts = function () {
            $scope.FilteredGroupID = "";
            $scope.SearchText = "";
            $scope.GetContacts();

        };

        $scope.$watch("SearchText", function () {
            $scope.GetContacts();
        });


        $scope.ContactsClickedGroups = {};
        $scope.AddNewGroup = function () {
            var b = prompt("Please enter new group name");
            if (b) {
                $http.post("/api/v1/groups-contacts/", {
                    name: b
                }).then(function (data) {
                    $scope.GetGroups();
                })


            }

        };
        $scope.ContactsClickedGroupsIsLoading = false;
        $scope.GetGroupsList = function (item) {
            $scope.ContactsClickedGroupsIsLoading = true;
            $http.get("/api/v1/groups-contacts/" + item.id + "/getGroups/").then(function (data) {
                $scope.ContactsClickedGroups = data.data;
                $scope.ContactsClickedGroupsIsLoading = false;
            }).catch(function (data) {
                $scope.ContactsClickedGroupsIsLoading = false;

            })
        };
        $scope.AddMemberToGroup = function (contactID, GroupID, itemChecked) {
            itemChecked.checked = !(itemChecked.checked);
            $http.post("/api/v1/items-groups-contacts/", {
                group: GroupID,
                member: contactID,
                checked: itemChecked.checked
            }).then(function (data) {

            })
        }

    });

