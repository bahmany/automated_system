'use strict';

angular
    .module('AniTheme')
    .service('SettingsService',
    ['$cookies', '$http', '$location',
        function ($cookies, $http, $location) {


            var urlCompnaies = "/api/v1/companies/";
            this.GetListCompanyByPager = function (addr) {
                return $http.get(addr);
            };
            this.GetCompanies = function (q, page_size) {
                return $http.get(urlCompnaies + "?q=" + q + "&page_size=" + page_size)
            };
            var urlMembers = "/api/v1/members-search/";
            this.GetMembersListByPager = function (addr) {
                return $http.get(addr);
            };
            this.GetMembersListByPager = function (addr) {
                return $http.get(addr);
            };
            this.GetMembers = function (q, page_size, companyID) {
                return $http.get(urlMembers + "?q=" + q + "&page_size=" + page_size+"&companyID="+companyID)
            };




        }]);






