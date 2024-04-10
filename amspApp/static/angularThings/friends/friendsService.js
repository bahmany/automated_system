'use strict';

angular
    .module('AniTheme')
    .service('FriendsService','$stateParams'
    ['$cookies', '$http', '$location',
        function ($stateParams, $cookies, $http, $location) {


            this.GetMemberInvitations = function (personID) {
                return $http.get("/api/v1/profile/GetMyInvitations/")
            };


            this.GetCompanyMembers = function (companyID) {
                return $http.get("/api/v1/profile/SearchProfiles/?page=1")
            };

            this.GetProfiles = function (q) {
                return $http.get("/api/v1/profile/SearchProfiles/" + "?q=" + q)
            };

            this.GetAllChartList = function (q) {
                return $http.get("/api/v1/companies/"+$stateParams.companyid+"/chart/GetAllCharts/" + "?q=" + q)

            }


            this.GetProfileListByPager = function (SearchProfileList, PagerUrl) {
                var qurl = PagerUrl + "&q=" + SearchProfileList;

                if (qurl.split("?").length == 1) {
                    qurl = qurl.replace("&", "?");
                }
                return $http.get(qurl);
            };
            this.GetChartListByPager = function (SearchChartList, PagerUrl) {
                var qurl = PagerUrl + "&q=" + SearchChartList;

                if (qurl.split("?").length == 1) {
                    qurl = qurl.replace("&", "?");
                }
                return $http.get(qurl);
            };
            this.ApproveInvitation = function (invitationID) {
                return $http.post("/api/v1/companies/"+$stateParams.companyid+"/invite/DoInvite/", {
                    invitationID: invitationID
                });
            };
            this.GetCompanyChartList = function (companyID) {
                return $http.get("/api/v1/companies/" + companyID + "/chart/")
            };

            this.GetUserInvitations = function (SelectedUserID, searchStr) {
                return $http.get("/api/v1/profile/" + SelectedUserID + "/GetUserInvitations/")
            };
            this.RemoveInvitation = function (SelectedUserID, invitaionID) {
                return $http.get("/api/v1/profile/" + SelectedUserID + "/RemoveInvitations/?q=" + invitaionID)
            };

            this.SelectDeselectChart = function (companyID, chartID, receiver, selected, isEmpty,positionID) {
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

        }]);






