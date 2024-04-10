'use strict';


angular.module('AniTheme')
    .controller('CompanyMembersCtrl', function ($scope,
                                                $http,$$$,
                                                $stateParams,
                                                $translate,
                                                $rootScope,
                                                $location,
                                                $modal,
                                                CompanyMembersService
                                                // FriendsService
    ) {

        $scope.Members = [];
        $scope.MemberSearchText = '';
        $scope.SelectedPersonID = "";
        $scope.ChartCompanyID = $stateParams.companyid;
        $scope.ChartSimpleList = [];
        $scope.SearchChartList = "";
        $scope.SelectedPerson = {};
        $scope.SelectedNewChart = {};
        $scope.isSearchCallbackCompleted = true;
        $scope.GetMembers = function (companyId) {
            // debugger;
            $scope.isSearchCallbackCompleted = false;
            CompanyMembersService.searchMembers(companyId, $scope.MemberSearchText).then(function (data) {
                $scope.Members = data.data;
                $scope.isSearchCallbackCompleted = true;
            }).catch(function (data) {
                $scope.isSearchCallbackCompleted = true;

            });
        };

        $scope.MemberPageTo = function (pageUrl) {
            $http.get(pageUrl).then(function (data) {
                $scope.Members = data.data;
            })
        }
        $scope.$watch("MemberSearchText", function () {
            $scope.GetMembers($stateParams.companyid);
        });
        $scope.GetMembers($stateParams.companyid);

        $scope.ForceOut = function (item) {

            swal({
                title: $$$("Are you sure?"),
                text: $$$("This user access to his inbox will be lost"),
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: $$$("Yes, remove it"),
                closeOnConfirm: false,
                showLoaderOnConfirm: true
            }, function () {
                $scope.SelectedPerson = item;
                CompanyMembersService.ForceOutSrv($stateParams.companyid, {
                    profileID: $scope.SelectedPerson.id,
                    chartID: $scope.SelectedPerson.chartID,
                    userID: $scope.SelectedPerson.userID,
                    positionID: $scope.SelectedPerson.positionID,
                    companyID: $scope.SelectedPerson.companyID
                }).then(function (data) {
                    $scope.GetMembers($stateParams.companyid);
                    swal($$$("Removed"), $$$("Selected users removed from the selected chart"), "success");
                });
            });
        };
        $scope.RemoveInbox = function (item) {
            swal({
                title: "Danger!!",
                text: "By removing this, old letter in the inbox will be gone forever",
                type: "warning",
                showCancelButton: true,
                closeOnConfirm: false,
                showLoaderOnConfirm: true
            }, function () {
                ////console.log(item);
                CompanyMembersService.RemoveFromInbox($stateParams.companyid, item).then(function () {
                    $scope.GetMembers($stateParams.companyid);
                    swal("Removed!", "Successfully removed", "success");

                })


            });
        }
        //----------------------------------------------------------------------------------
        // $scope.GetCompanyChartList = function (companyID, searchStr) {
        //     $scope.isSearchCallbackCompleted = false;
        //     CompanyMembersService.GetCompanyChartList(companyID, searchStr, 1).then(function (data) {
        //         $scope.isSearchCallbackCompleted = true;
        //         $scope.ChartSimpleList = data;
        //     }).catch(function () {
        //         $scope.isSearchCallbackCompleted = true;
        //     });
        // };
        // $scope.$watch("SearchChartList", function () {
        //     $scope.GetCompanyChartList($scope.ChartCompanyID, $scope.SearchChartList)
        // });
        // $scope.ChartPageTo = function (PageUrl) {
        //     CompanyMembersService.GetCompanyChartListByPager($scope.SearchChartList, PageUrl).then(function (data) {
        //         $scope.ChartSimpleList = data;
        //         for (var i = 0; $scope.ChartSimpleList.results.length > i; i++) {
        //             if ($scope.ChartSimpleList.results[i].id == $scope.SelectedPerson.chartID &&
        //                 $scope.ChartSimpleList.results[i].isEmpty != $scope.SelectedPerson.isEmpty
        //             ) {
        //                 $scope.ChartSimpleList.results[i].selected = true;
        //
        //             } else {
        //                 $scope.ChartSimpleList.results[i].selected = false;
        //             }
        //         }
        //     });
        // };
        // $scope.SelectDeselectChart = function (chart) {
        //     if (chart.selected) {
        //         $scope.SelectedNewChart = chart;
        //     } else {
        //         $scope.SelectedNewChart.selected = false;
        //     }
        //     for (var i = 0; $scope.ChartSimpleList.results.length > i; i++) {
        //         if ($scope.ChartSimpleList.results[i].id != chart.id) {
        //             $scope.ChartSimpleList.results[i].selected = false;
        //         }
        //     }
        // };
        // $scope.LoadChart = function (person) {
        //     $scope.SelectedPerson = person;
        //     CompanyMembersService.GetCompanyChartList($scope.ChartCompanyID, "", 1).then(function (data) {
        //         $scope.ChartSimpleList = data;
        //         for (var i = 0; $scope.ChartSimpleList.results.length > i; i++) {
        //             if ($scope.ChartSimpleList.results[i].id == $scope.SelectedPerson.chartID) {
        //                 $scope.ChartSimpleList.results[i].selected = true;
        //
        //             } else {
        //                 $scope.ChartSimpleList.results[i].selected = false;
        //             }
        //         }
        //         $("#memList").show();
        //         $("#invList").hide();
        //     });
        // };
        // $scope.PostPostionSelect = function () {
        //     if ($scope.SelectedNewChart.selected == false) {
        //         swal("Not Selected", "Please Select a chart item to apply", "error");
        //         return;
        //     }
        //     swal({
        //         title: "Are ready ?",
        //         text: "After changing position, previous account will not be able to see this charts letter",
        //         type: "info",
        //         showCancelButton: true,
        //         closeOnConfirm: false,
        //         showLoaderOnConfirm: true
        //     }, function () {
        //         CompanyMembersService.UpdatePosition(
        //             $scope.ChartCompanyID,
        //             $scope.SelectedPerson.userID,
        //             $scope.SelectedNewChart.id,
        //             $scope.SelectedPerson.chartID,
        //             $scope.SelectedPerson.id
        //         ).then(function (data) {
        //                 $scope.GetMembers($scope.ChartCompanyID);
        //                 swal("Updated", "success", "success");
        //                 $("#memList").fadeOut(100)
        //             });
        //     });
        // };
        // $scope.CancelPostionSelect = function () {
        //     $("#memList").fadeOut(100);
        // };
        //----------------------------------------------------------------------------------


        // ---------------------------------------------------------------------------
        // ---------------------------------------------------------------------------
        // ---------------------------------------------------------------------------
        // ---------------------------------------------------------------------------
        // ---------------------------------------------------------------------------
        // ---------------------------------------------------------------------------

        // $scope.GetProfiles = function () {
        //     $scope.isSearchCallbackCompleted = false;
        //     FriendsService.GetProfiles($scope.ProfileSearchText).then(function (data) {
        //         $scope.SearchPersons = data;
        //         $scope.isSearchCallbackCompleted = true;
        //     }).catch(function (data) {
        //         $scope.isSearchCallbackCompleted = true;
        //     })
        // };
        // $scope.ProfileSearch = "";
        // $scope.ProfilePageTo = function (PageUrl) {
        //     $scope.isSearchCallbackCompleted = false;
        //
        //     FriendsService.GetProfileListByPager($scope.ProfileSearch, PageUrl).then(function (data) {
        //         $scope.isSearchCallbackCompleted = true;
        //         $scope.SearchPersons = data;
        //     }).catch(function (data) {
        //         $scope.isSearchCallbackCompleted = true;
        //     });
        // };
        // $scope.GetProfiles();
        // $scope.isSearchCallbackCompleted = true;
        // $scope.$watch("ProfileSearchText", function () {
        //     $scope.GetProfiles();
        // });
        // $scope.SelectedPerson = {};
        // $scope.OpenInviteModal = function (person) {
        //     $scope.SelectedPerson = person;
        //     // here i have some points
        //     // when i click on a user
        //     // i can see all of my invitations !!
        //     // so invitations is not company based
        //     FriendsService.GetMemberInvitations(person.profileID).then(function (data) {
        //         //$("#profileList").removeClass("col-md-12").addClass("col-md-7");
        //         //$("#invList").removeClass("hide").addClass("show");
        //         $("#memList").hide();
        //         $("#invList").show();
        //         $scope.GetUserInvitations();
        //     })
        // };
        // $scope.SearchPersons = {};
        // $scope.GetCompanyMembers = function (companyID) {
        //     FriendsService.GetCompanyMembers(companyID).then(function (data) {
        //         $scope.SearchPersons = data.results;
        //     });
        // };
        // $scope.CloseInvModal = function () {
        //     $("#invList").removeClass("show").addClass("hide");
        //     $("#profileList").removeClass("col-md-7").addClass("col-md-12");
        // }
        // $scope.ChartSimpleList = {};
        // $scope.ChartSearch = "";
        // $scope.GetCompanyChartList = function () {
        //     FriendsService.GetAllChartList($scope.ChartSearch).then(function (data) {
        //         $scope.ChartSimpleList = data;
        //     });
        // };
        // $scope.$watch("ChartSearch", function () {
        //     $scope.GetCompanyChartList();
        // });
        // $scope.GetCompanyChartList();
        // $scope.ChartPageTo = function (PageUrl) {
        //     FriendsService.GetChartListByPager($scope.ChartSearch, PageUrl).then(function (data) {
        //         $scope.ChartSimpleList = data;
        //     });
        // };
        // $scope.OpenCompanyMembers = function (item) {
        //     $scope.SelectedCompanyID = item;
        //     $scope.GetCompanyMembers(item);
        //     $scope.GetCompanyChartList(item);
        // };
        // $scope.SearchChart = "";
        // $scope.$watch("InvitationsSearch", function () {
        //     $scope.GetUserInvitations();
        // });
        // $scope.GetUserInvitations = function (searchStr) {
        //     FriendsService.GetUserInvitations(
        //         $scope.SelectedPerson.profileID, $scope.InvitationsSearch
        //     ).then(function (data) {
        //             $scope.Invitations = data;
        //
        //             for (var j = 0; j < $scope.ChartSimpleList.results.length; j++) {
        //                 $scope.ChartSimpleList.results[j].selected = false;
        //             }
        //
        //
        //             for (var i = 0; i < data.results.length; i++) {
        //                 for (var j = 0; j < $scope.ChartSimpleList.results.length; j++) {
        //                     if (
        //                         data.results[i].chart == $scope.ChartSimpleList.results[j].id
        //                     ) {
        //                         if (
        //                             data.results[i].isEmpty == $scope.ChartSimpleList.results[j].isEmpty &&
        //                             data.results[i].positionID == $scope.ChartSimpleList.results[j].positionID
        //                         ) {
        //                             $scope.ChartSimpleList.results[j].selected = true;
        //                         } else {
        //                             if
        //                             (data.results[i].positionID == undefined) {
        //                                 $scope.ChartSimpleList.results[j].selected = true;
        //                             }
        //                         }
        //                     }
        //                 }
        //             }
        //
        //         })
        // };
        // $scope.Invitations = [];
        // $scope.RemoveInvitation = function (inv) {
        //     swal({
        //         title: "Are you sure?",
        //         text: "Are you ready to remove this invitation ?",
        //         type: "warning",
        //         showCancelButton: true,
        //         confirmButtonColor: "#DD6B55",
        //         confirmButtonText: "Yes, delete it!",
        //         closeOnConfirm: false, showLoaderOnConfirm: true
        //     }, function () {
        //         FriendsService.RemoveInvitation($scope.SelectedPerson.id, inv.id).then(function (data) {
        //             $scope.GetUserInvitations();
        //             swal("Deleted!", "Your imaginary file has been deleted.", "success");
        //
        //         });
        //     });
        //
        // };
        // $scope.SelectedChart = {};
        // $scope.SelectDeselectChart = function (chart) {
        //     $scope.SelectedChart = chart;
        //     $scope.InvitationsSearch = "";
        //     FriendsService.SelectDeselectChart(
        //         parseInt(chart.CompanyID),
        //         chart.id,
        //         $scope.SelectedPerson.profileID,
        //         chart.selected,
        //         chart.isEmpty,
        //         chart.positionID
        //     ).then(function (data) {
        //             $scope.GetUserInvitations();
        //         });
        // };



        $scope.SuspendJob = function (item) {
            $http.post("/api/v1/companies/"+$stateParams.companyid+"/invite/suspend/", {
                positionID: item.id
            }).then(function (data) {

            })
        }

        $scope.ApproveInvitation = function (invitation) {
            FriendsService.ApproveInvitation(
                invitation.id
            ).then(function (data) {
                    $scope.GetUserInvitations();
                    $scope.GetCompanyChartList();
                    swal("Updated", "Completed..", "success");
                }).catch(function (data) {
                    swal("Error", data.message, "error");
                });
        };


    }
);
