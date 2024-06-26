'use strict';


angular.module('AniTheme').controller(
    'FriendsCtrl',
    function ($scope,
              $translate,
              $q,
              $rootScope,
              $modal,
              FriendsService) {


        $scope.GetProfiles = function () {
            $scope.isSearchCallbackCompleted = false;
            FriendsService.GetProfiles($scope.ProfileSearchText).then(function (data) {
                $scope.SearchPersons = data.data;
                $scope.isSearchCallbackCompleted = true;
            }).catch(function (data) {
                $scope.isSearchCallbackCompleted = true;
            })
        };
        $scope.ProfileSearch = "";
        $scope.ProfilePageTo = function (PageUrl) {
            $scope.isSearchCallbackCompleted = false;

            FriendsService.GetProfileListByPager($scope.ProfileSearch, PageUrl).then(function (data) {
                $scope.isSearchCallbackCompleted = true;
                $scope.SearchPersons = data.data;
            }).catch(function (data) {
                $scope.isSearchCallbackCompleted = true;
            });
        };
        $scope.GetProfiles();
        $scope.isSearchCallbackCompleted = true;
        $scope.$watch("ProfileSearchText", function () {
            $scope.GetProfiles();
        });
        $scope.SelectedPerson = {};
        $scope.OpenInviteModal = function (person) {
            $scope.SelectedPerson = person;
            // here i have some points
            // when i click on a user
            // i can see all of my invitations !!
            // so invitations is not company based
            FriendsService.GetMemberInvitations(person.id).then(function (data) {
                $("#profileList").removeClass("col-md-12").addClass("col-md-7");
                $("#invList").removeClass("hide").addClass("show");
                $scope.GetUserInvitations();
            })
        };
        $scope.SearchPersons = {};
        $scope.GetCompanyMembers = function (companyID) {
            FriendsService.GetCompanyMembers(companyID).then(function (data) {
                $scope.SearchPersons = data.data.results;
            });
        };
        $scope.CloseInvModal = function () {
            $("#invList").removeClass("show").addClass("hide");
            $("#profileList").removeClass("col-md-7").addClass("col-md-12");
        }
        $scope.ChartSimpleList = {};
        $scope.ChartSearch = "";
        $scope.GetCompanyChartList = function () {
            FriendsService.GetAllChartList($scope.ChartSearch).then(function (data) {
                $scope.ChartSimpleList = data.data;
            });
        };
        $scope.$watch("ChartSearch", function () {
            $scope.GetCompanyChartList();
        });
        $scope.GetCompanyChartList();
        $scope.ChartPageTo = function (PageUrl) {
            FriendsService.GetChartListByPager($scope.ChartSearch, PageUrl).then(function (data) {
                $scope.ChartSimpleList = data.data;
            });
        };
        $scope.OpenCompanyMembers = function (item) {
            $scope.SelectedCompanyID = item;
            $scope.GetCompanyMembers(item);
            $scope.GetCompanyChartList(item);
        };
        $scope.SearchChart = "";
        $scope.$watch("InvitationsSearch", function () {
            $scope.GetUserInvitations();
        });
        $scope.GetUserInvitations = function (searchStr) {
            FriendsService.GetUserInvitations(
                $scope.SelectedPerson.id, $scope.InvitationsSearch
            ).then(function (data) {
                    $scope.Invitations = data.data;

                    for (var j = 0; j < $scope.ChartSimpleList.results.length; j++) {
                        $scope.ChartSimpleList.results[j].selected = false;
                    }


                    for (var i = 0; i < data.data.results.length; i++) {
                        for (var j = 0; j < $scope.ChartSimpleList.results.length; j++) {
                            if (
                                data.data.results[i].chart == $scope.ChartSimpleList.results[j].id
                            ) {
                                if (
                                    data.data.results[i].isEmpty == $scope.ChartSimpleList.results[j].isEmpty &&
                                    data.data.results[i].positionID == $scope.ChartSimpleList.results[j].positionID
                                ) {
                                    $scope.ChartSimpleList.results[j].selected = true;
                                } else {
                                    if
                                    (data.data.results[i].positionID == undefined) {
                                        $scope.ChartSimpleList.results[j].selected = true;
                                    }
                                }
                            }
                        }
                    }

                })
        };
        $scope.Invitations = [];
        $scope.RemoveInvitation = function (inv) {
            swal({
                title: "Are you sure?",
                text: "Are you ready to remove this invitation ?",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "Yes, delete it!",
                closeOnConfirm: false, showLoaderOnConfirm: true
            }, function () {
                FriendsService.RemoveInvitation($scope.SelectedPerson.id, inv.id).then(function (data) {
                    $scope.GetUserInvitations();
                    swal("Deleted!", "Your imaginary file has been deleted.", "success");

                });
            });

        };
        $scope.SelectedChart = {};
        $scope.SelectDeselectChart = function (chart) {
            $scope.SelectedChart = chart;
            $scope.InvitationsSearch = "";
            FriendsService.SelectDeselectChart(
                parseInt(chart.CompanyID),
                chart.id,
                $scope.SelectedPerson.id,
                chart.selected,
                chart.isEmpty,
                chart.positionID
            ).then(function (data) {
                    $scope.GetUserInvitations();
                });
        };
        $scope.ApproveInvitation = function (invitation) {
            FriendsService.ApproveInvitation(
                invitation.id
            ).then(function (data) {
                    $scope.GetUserInvitations();
                    $scope.GetCompanyChartList()
                    swal("Updated", "Completed..", "success");
                }).catch(function (data) {
                    swal("Error", data.message, "error");
                });
        };


    });