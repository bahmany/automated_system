'use strict';
angular.module('AniTheme')
    .controller('HamkarijobsCtrl', function ($scope, $http, $translate, $rootScope, $stateParams, $location, $window, $$$, $filter) {


            var GetMemberInvitations = function (personID) {
                return $http.get("/api/v1/profile/GetMyInvitations/")
            };


            var GetCompanyMembers = function (companyID) {
                return $http.get("/api/v1/profile/SearchProfiles/?page=1")
            };

            var GetProfiles = function (q) {
                return $http.get("/api/v1/profile/SearchProfiles/" + "?q=" + q)
            };

            var GetAllChartList = function (q) {
                return $http.get("/api/v1/companies/" + $stateParams.companyid + "/chart/GetAllCharts/" + "?q=" + q)

            }


            var GetProfileListByPager = function (SearchProfileList, PagerUrl) {
                var qurl = PagerUrl + "&q=" + SearchProfileList;

                if (qurl.split("?").length == 1) {
                    qurl = qurl.replace("&", "?");
                }
                return $http.get(qurl);
            };
            var GetChartListByPager = function (SearchChartList, PagerUrl) {
                var qurl = PagerUrl + "&q=" + SearchChartList;

                if (qurl.split("?").length == 1) {
                    qurl = qurl.replace("&", "?");
                }
                return $http.get(qurl);
            };
            var ApproveInvitation = function (invitationID) {
                return $http.post("/api/v1/companies/" + $stateParams.companyid + "/invite/DoInvite/", {
                    invitationID: invitationID
                });
            };
            var GetCompanyChartList = function (companyID) {
                return $http.get("/api/v1/companies/" + companyID + "/chart/")
            };

            var GetUserInvitations = function (SelectedUserID, searchStr) {
                return $http.get("/api/v1/profile/" + SelectedUserID + "/GetUserInvitations/")
            };
            var RemoveInvitation = function (SelectedUserID, invitaionID) {
                return $http.get("/api/v1/profile/" + SelectedUserID + "/RemoveInvitations/?q=" + invitaionID)
            };

            var SelectDeselectChart = function (companyID, chartID, receiver, selected, isEmpty, positionID) {
                return $http.post("/api/v1/companies/" + companyID + "/invite/", {
                    company: companyID,
                    chart: chartID,
                    receiver: receiver,
                    selected: selected,
                    seen: false,
                    isEmpty: isEmpty,
                    positionID: positionID
                })
            };


            ////console.log($stateParams);

            $scope.leftMenu = [];
            $scope.GetLeftMenu = function () {
                $http.get("/api/v1/companies/" + $stateParams.companyid + "/hamkarijobs/makeLeftMenuWithStatics/").then(function (data) {
                    $scope.leftMenu = data.data;
                });
            }
            //$scope.GetProfiles();
            $scope.sortOrder = ["کاردانی",
                "کارشناسی",
                "کارشناسی ارشد",
                "دکتری",
                "حوزوی",
                "پزشکی"];
            $scope.GetLeftMenu();


            $scope.Filters = [];
            $scope.FilterStr = "";
            $scope.AddToFilters = function (item, parent) {
                $scope.Filters.push({
                    title: parent.name,
                    name: parent.fieldName,
                    value: item._id
                });
                $scope.FilterStr = "";
                for (var i = 0; $scope.Filters.length > i; i++) {
                    $scope.FilterStr = $scope.FilterStr + "978547" + $scope.Filters[i].name + "798745" + $scope.Filters[i].value;
                }

            };


            $scope.searchFilterString = "";
            $scope.searchFilterToText = function () {
                $scope.searchFilterString = "";
                if ($scope.searchFilter.Name) {
                    $scope.searchFilterString = $scope.searchFilterString + "___" + "Name"
                }
                if ($scope.searchFilter.Family) {
                    $scope.searchFilterString = $scope.searchFilterString + "___" + "Family"
                }
                if ($scope.searchFilter.BirthDate) {
                    $scope.searchFilterString = $scope.searchFilterString + "___" + "BirthDate"
                }
                if ($scope.searchFilter.BirthPlace) {
                    $scope.searchFilterString = $scope.searchFilterString + "___" + "BirthPlace"
                }
                if ($scope.searchFilter.InternationalCode) {
                    $scope.searchFilterString = $scope.searchFilterString + "___" + "InternationalCode"
                }
                if ($scope.searchFilter.Mobile) {
                    $scope.searchFilterString = $scope.searchFilterString + "___" + "Mobile"
                }
                if ($scope.searchFilter.OstanHome) {
                    $scope.searchFilterString = $scope.searchFilterString + "___" + "OstanHome"
                }
                if ($scope.searchFilter.CityHome) {
                    $scope.searchFilterString = $scope.searchFilterString + "___" + "CityHome"
                }
                if ($scope.searchFilter.HomeAddress) {
                    $scope.searchFilterString = $scope.searchFilterString + "___" + "HomeAddress"
                }
            };
            $scope.removeFilter = function ($index) {
                $scope.Filters.splice($index, 1);
                $scope.FilterStr = "";
                for (var i = 0; $scope.Filters.length > i; i++) {
                    $scope.FilterStr = $scope.FilterStr + "978547" + $scope.Filters[i].name + "798745" + $scope.Filters[i].value;
                }
            }

            $scope.addPersonToNewPosition = function (profileID) {
                // debugger;
                $http.post("/api/v1/companies/" + $stateParams.companyid + "/chart/addPersonToNewPosition/", {
                    selected: true,
                    isEmpty: false,
                    receiver: profileID,
                    chart: $scope.SelectedChartID
                }).then(function (data) {
                    // debugger;
                    if (typeof data.data == 'object') {
                        $rootScope.$broadcast("UpdateProfiles");
                        $scope.GetProfileList($scope.SelectedChartID);
                        $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
                    } else {
                        swal("Error!", "این شخص قبلا سمت دهی شده است", "error");

                    }
                }).catch(function (data) {
                    swal("Error!", "این شخص قبلا سمت دهی شده است", "error");

                })
            }


            $scope.list = [];
            $rootScope.$on("UpdateProfiles", function (data) {
                $scope.GetProfiles();
            })

            $scope.GetProfiles = function () {
                $scope.searchFilterToText();
                $http.get("/api/v1/companies/" + $stateParams.companyid + "/hamkarijobs/?q=" + $scope.listSearch + "&s=" + $scope.searchFilterString + "&f=" + $scope.FilterStr).then(function (data) {
                    $scope.list = data.data;
                });
            };


            $scope.DeleteAccount = function (item) {
                swal({
                    title: "آیا اطمینان دارید",
                    text: "آیا اطمینان دارید می خواهید این شخص را حذف کنید ؟",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#DD6B55",
                    confirmButtonText: "بله",
                    closeOnConfirm: false,
                    showLoaderOnConfirm: true
                }, function () {
                    $scope.SelectedPerson = item;

                    $http.post("/api/v1/companies/" + $stateParams.companyid + "/chart/0/DeleteAccount/", item
                    ).then(function (data) {
                        $rootScope.$broadcast("UpdateProfiles");
                        // $scope.GetMembers($stateParams.companyid);
                        $scope.GetProfileList($scope.SelectedChartID);
                        swal($$$("Removed"), "کاربر مورد نظر تعلیق گردید", "success");

                    });
                });
            }


            $scope.listSearch = "";
            $scope.Table = {};
            $scope.searchFilter = {};
            $scope.searchFilter.CheckAll = true;
            $scope.Table.pagination = {};
            $scope.Table.pagination.size = 10;
            $scope.Table.pagination.total = 0;
            $scope.Table.isShow = false;
            $scope.HandlelistPagination = function () {
                if ($scope.Table.pagination.size == 40) {
                    $scope.Table.pagination.size = 5;
                }
                $scope.Table.pagination.size = $scope.Table.pagination.size + 5;
            };


            $scope.listTableGoToPage = function (page) {
                $http.get(page).then(function (data) {
                    $scope.list = data.data;
                });
            };

            $scope.getImage = function (item) {
                //    "/api/v1/file/upload?q=thmum100_"+
                var extra = "/api/v1/file/upload?q=thmum100_";
                var res = "";
                if (item.extra.job) {
                    if (!(item.extra.job.Resume)) {
                        res = "" + item.extra.profileAvatar.url;
                    } else if (!(item.extra.job.Resume.pic)) {
                        res = item.extra.profileAvatar.url;
                    } else res = item.extra.job.Resume.pic;

                }
                // debugger;
                // debugger;

                if ((res.indexOf("api") == -1)) {
                    res = extra + res;
                }
                return res;
            }


            $scope.OpenChart = function (item) {
                $http.get("/api/v1/profile/getProfileByUserID/?q=" + item.userID).then(function (data) {
                    $scope.SelectedPerson = data.data;
                    $scope.GetUserInvitations();
                    $("#divList").fadeOut(function () {
                        $("#divCharts").fadeIn(function () {

                        })
                    })
                });


            };
            $scope.OpenChartBack = function () {
                $("#divCharts").fadeOut(function () {
                    $("#divList").fadeIn(function () {

                    })
                })
            };
            $scope.OpenResume = function (item) {
                //$http.get("/api/v1/companies/0/hamkarijobs/")
                $window.open("/#/dashboard/previewResume/" + item.id);

                //$location.url("/dashboard/previewResume/" + item.id);
            }
            $scope.getLicense = function (item) {
                if (item.extra.job) {
                    if (item.extra.job.Education) {
                        if (item.extra.job.Education.items) {
                            if (item.extra.job.Education.items.length == 1) {
                                //////console.log(item.extra.job.Education.items);
                                return item.extra.job.Education.items[0].Education + " <br> " + item.extra.job.Education.items[0].SelectedBranch + "<br> از " + item.extra.job.Education.items[0].EducationalPlaceName + item.extra.job.Education.items[0].EndYear;
                            }
                            if (item.extra.job.Education.items.length == 0) {
                                return item.extra.job.Education.EducationType + " <br> " + item.extra.job.Education.SelectedBranch + "<br> معدل " + item.extra.job.Education.AverageOfLicense + " سال اتمام " + item.extra.job.Education.EndYear;
                            }
                            if (item.extra.job.Education.items.length > 1) {
                                var sort = -1;
                                var final = {};
                                for (var i = 0; item.extra.job.Education.items.length > i; i++) {
                                    for (var c = 0; $scope.sortOrder.length > c; c++) {
                                        if (item.extra.job.Education.items[i].Education == $scope.sortOrder[c]) {
                                            if (c >= sort) {
                                                sort = c;
                                                final = item.extra.job.Education.items[i];

                                            }
                                        }

                                        //item.extra.job.Education.items[i]
                                    }
                                }
                                return final.Education + " * <br> " + final.SelectedBranch + "<br> از " + final.EducationalPlaceName + " " + final.EndYear;

                            }

                        }
                    }
                }

                return "اطلاعات تحصیلی ثبت نشده"
            }

            //---------------------------------------------------------
            //---------------------------------------------------------
            //---------------------------------------------------------
            //---------------------------------------------------------
            //---------------------------------------------------------
            //---------------------------------------------------------
            //---------------------------------------------------------

            $scope.SelectedPerson = {};
            $scope.OpenInviteModal = function (person) {


                $scope.SelectedPerson = person;
                // here i have some points
                // when i click on a user
                // i can see all of my invitations !!
                // so invitations is not company based
                GetMemberInvitations(person.id).then(function (data) {
                    $("#profileList").removeClass("col-md-12").addClass("col-md-7");
                    $("#invList").removeClass("hide").addClass("show");
                    $scope.GetUserInvitations();
                })
            };
            $scope.SearchPersons = {};
            $scope.GetCompanyMembers = function (companyID) {
                GetCompanyMembers(companyID).then(function (data) {
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

                GetAllChartList($scope.ChartSearch).then(function (data) {
                    $scope.ChartSimpleList = data.data;
                });
            };
            $scope.GetCompanyChartList();
            $scope.ChartPageTo = function (PageUrl) {
                GetChartListByPager($scope.ChartSearch, PageUrl).then(function (data) {
                    $scope.ChartSimpleList = data.data;
                });
            };
            $scope.OpenCompanyMembers = function (item) {
                $scope.SelectedCompanyID = item;
                $scope.GetCompanyMembers(item);
                $scope.GetCompanyChartList(item);
            };
            $scope.SearchChart = "";
            $scope.GetUserInvitations = function (searchStr) {
                GetUserInvitations(
                    $scope.SelectedPerson.id, $scope.InvitationsSearch
                ).then(function (data) {
                    $scope.Invitations = data.data;
                    if (!($scope.SelectedPerson.id)) {
                        return
                    }

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
                    RemoveInvitation($scope.SelectedPerson.id, inv.id).then(function (data) {
                        $scope.GetUserInvitations();
                        swal("Deleted!", "Your imaginary file has been deleted.", "success");

                    });
                });

            };
            $scope.SelectedChart = {};
            $scope.SelectDeselectChart = function (chart) {
                $scope.SelectedChart = chart;
                $scope.InvitationsSearch = "";
                SelectDeselectChart(
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
                ApproveInvitation(
                    invitation.id
                ).then(function (data) {
                    $scope.GetUserInvitations();
                    $scope.GetCompanyChartList();
                    $scope.GetProfiles();
                    $scope.OpenChartBack();
                    swal("Updated", "Completed..", "success");
                }).catch(function (data) {
                    swal("Error", data.message, "error");
                });
            };
            //---------------------------------------------------------
            //---------------------------------------------------------
            //---------------------------------------------------------
            //---------------------------------------------------------
            //---------------------------------------------------------
            //---------------------------------------------------------
            //---------------------------------------------------------
            //---------------------------------------------------------
            //---------------------------------------------------------

            $scope.$watch("searchFilter.CheckAll", function () {
                $scope.searchFilter.Name = $scope.searchFilter.CheckAll;
                $scope.searchFilter.Family = $scope.searchFilter.CheckAll;
                $scope.searchFilter.BirthDate = $scope.searchFilter.CheckAll;
                $scope.searchFilter.BirthPlace = $scope.searchFilter.CheckAll;
                $scope.searchFilter.InternationalCode = $scope.searchFilter.CheckAll;
                $scope.searchFilter.Mobile = $scope.searchFilter.CheckAll;
                $scope.searchFilter.OstanHome = $scope.searchFilter.CheckAll;
                $scope.searchFilter.CityHome = $scope.searchFilter.CheckAll;
                $scope.searchFilter.HomeAddress = $scope.searchFilter.CheckAll;
            });
            $scope.$watch("ChartSearch", function () {
                $scope.GetCompanyChartList();
            });
            $scope.$watch("InvitationsSearch", function () {
                $scope.GetUserInvitations();
            });
            $scope.$watchGroup(['listSearch', 'FilterStr'], function () {
                $scope.GetProfiles();
            });
        }
    )
;
