'use strict';
angular.module('AniTheme')
    .controller('CompanyMembersCtrl', function ($scope,$stateParams, $http, $translate, $rootScope, $location, $modal, companiesManagmentService) {

        $scope.SelectedPerson = {};
        $scope.OpenInviteModal = function (person) {
            $scope.SelectedPerson = person;
            // here i have some points
            // when i click on a user
            // i can see all of my invitations !!
            // so invitations is not company based
            companiesManagmentService.GetMemberInvitations(person.id).then(function (data) {
                $scope.GetUserInvitations();

            })
        };
        $scope.SearchPersons = [];
        $scope.GetCompanyMembers = function (companyID) {
            companiesManagmentService.GetCompanyMembers(companyID).then(function (data) {
                $scope.SearchPersons = data.data.results;


            });
        };
        $scope.ChartSimpleList = [];
        $scope.GetCompanyChartList = function (companyID) {
            companiesManagmentService.GetCompanyChartList(companyID).then(function (data) {
                $scope.ChartSimpleList = data.data;
            });
        };
        $scope.OpenCompanyMembers = function (item) {

            $scope.SelectedCompanyID = item;
            $scope.GetCompanyMembers(item);
            $scope.GetCompanyChartList(item);
        };
        $scope.OpenCompanyMembers($stateParams.companyid);
        $scope.SearchChart = "";
        $scope.$watch("SearchChart", function () {
            ////console.log("Hiiii");
        });
        $scope.GetUserInvitations = function (searchStr) {
            companiesManagmentService.GetUserInvitations(
                $scope.SelectedPerson.id, searchStr
            ).then(function (data) {
                    $scope.Invitations = data.data;
                    for (var j = 0; j < $scope.ChartSimpleList.results.length; j++) {
                        $scope.ChartSimpleList.results[j].selected = false;
                    }
                    for (var i = 0; i < data.data.results.length; i++) {

                        for (var j = 0; j < $scope.ChartSimpleList.results.length; j++) {
                            if (data.data.results[i].chart == $scope.ChartSimpleList.results[j].id) {
                                $scope.ChartSimpleList.results[j].selected = true;

                            }
                        }
                    }

                })
        };
        $scope.Invitations = [];
        $scope.RemoveInvitation = function (inv) {
            companiesManagmentService.RemoveInvitation($scope.SelectedPerson.id, inv.id).then(function (data) {
                $scope.GetUserInvitations();
            });
        };
        $scope.SelectDeselectChart = function (chart) {
            companiesManagmentService.SelectDeselectChart(
                $scope.SelectedCompanyID,
                chart.id,
                $scope.SelectedPerson.id,
                chart.selected
            ).then(function (data) {
                    $scope.GetUserInvitations();
                    //$scope.SearchPersons = data.results;
                });
        };


    });
