'use strict';


angular.module('AniTheme').controller(
    'AccessToSecratariatCrtl',
    function ($scope,
              $translate,
              $q,
              $http,
              $timeout,
              $rootScope,
              $mdToast,
              $modal,
              SettingsService) {


        $scope.Companies = [];
        $scope.Company = {};
        $scope.SelectedCompanyID = null;
        $scope.person = {};
        $scope.successor = {};
        $scope.assistant = {};
        $scope.permission = {};


        $scope.GetDefaultCompany = function () {
            $http.get("/api/v1/companies/getDefault/").then(function (data) {
                $scope.Company = data.data;
                $scope.SelectedCompanyID = data.data.id;
            });
        };
        $timeout(function () {
            $scope.GetDefaultCompany();
        }, 0);
        $scope.$watch("SelectedCompanyID", function () {
            for (var i = 0; $scope.Companies.length > i; i++) {
                if ($scope.Companies[i].id == $scope.SelectedCompanyID) {
                    $scope.Company = $scope.Companies[i];
                }
            }
            setUpMemberAutocomplement($scope.person, $scope.SelectedCompanyID, SettingsService);
            setUpMemberAutocomplement($scope.successor, $scope.SelectedCompanyID, SettingsService);
            setUpMemberAutocomplement($scope.assistant, $scope.SelectedCompanyID, SettingsService);
            $scope.person.GetMembers();
        });

        $scope.OpenChangeCompany = function () {
            $("#divCurrentCompany").fadeOut(200, function () {
                $("#divSelectCompany").fadeIn(200);
            })
        };
        $scope.OpenCompanyShowDiv = function () {
            $("#divSelectCompany").fadeOut(200, function () {
                $("#divCurrentCompany").fadeIn(200);
            })
        };
        $scope.GetCompanies = function (pagingSize) {
            SettingsService.GetCompanies("", pagingSize).then(function (data) {
                $scope.Companies = data.data.results;
            });
        };

        function sanitizePosition() {
            var current = $scope.toastPosition;
            if (current.bottom && last.top) current.top = false;
            if (current.top && last.bottom) current.bottom = false;
            if (current.right && last.left) current.left = false;
            if (current.left && last.right) current.right = false;
            last = angular.extend({}, current);
        }

        var last = {
            bottom: false,
            top: true,
            left: false,
            right: true
        };
        $scope.toastPosition = angular.extend({}, last);
        $scope.getToastPosition = function () {
            sanitizePosition();
            return Object.keys($scope.toastPosition)
                .filter(function (pos) {
                    return $scope.toastPosition[pos];
                })
                .join(' ');
        };

        $scope.GetSecPermissions = function () {
            var objToPost = {};
            if (!$scope.person.selectedItem) {
                alert("Please select a person");
                return;
            }
            objToPost.person = $scope.person.selectedItem.value;
            $http.get("/api/v1/settings/secratariat/" + objToPost.person + "/?comid=" + $scope.SelectedCompanyID).then(function (data) {
                $scope.permission = data.data.automation.permission;
                $scope.successor =  data.data.automation.successor;
                $scope.assistant =  data.data.automation.assistant;
                setUpMemberAutocomplement($scope.successor, $scope.SelectedCompanyID, SettingsService);
                setUpMemberAutocomplement($scope.assistant, $scope.SelectedCompanyID, SettingsService);

            })
        };


        $scope.SetSecPermissions = function () {
            var objToPost = {};

            if (!$scope.person.selectedItem) {
                alert("Please select a person");
                return;
            }
            objToPost.desc = {};
            objToPost.desc.automation = {};
            objToPost.desc.automation.person = $scope.person.selectedItem.value;
            objToPost.desc.automation.successor = $scope.successor;
            objToPost.desc.automation.assistant = $scope.assistant;
            objToPost.desc.automation.permission = $scope.permission;
            objToPost.desc.automation.SelectedCompanyID = $scope.SelectedCompanyID;


            $http.patch("/api/v1/settings/secratariat/" + objToPost.desc.automation.person + "/", objToPost).then(function (data) {
                var toast = $mdToast.simple()
                    .textContent('Successfully Updated')
                    .action('OK')
                    .highlightAction(true)
                    .position($scope.getToastPosition());
                $mdToast.show(toast);
            }).catch(function (data) {
                var toast = $mdToast.simple()
                    .textContent('Error, edit info and post them again')
                    .action('OK')
                    .highlightAction(true)
                    .position($scope.getToastPosition());
                $mdToast.show(toast);

            });
        };

        function init() {
            setUpMemberAutocomplement($scope.person, $scope.SelectedCompanyID, SettingsService);
            setUpMemberAutocomplement($scope.successor, $scope.SelectedCompanyID, SettingsService);
            setUpMemberAutocomplement($scope.assistant, $scope.SelectedCompanyID, SettingsService);
        }


        $scope.SelectCompany = function (item) {
            $scope.SelectedCompany = item;
            $scope.person.GetMembers();
        }


    }
)
;

