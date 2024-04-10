/**
 * Created by mohammad on 12/20/15.
 */
'use strict';

angular
    .module('AniTheme')
    .service('CompanyGroupsService',
    ['$cookies', '$http', '$location',
        function ($cookies, $http, $location) {

            var url = "/api/v1/letter/sec/company-group/";

            this.GetCompanyGroupsListByPager = function (addr) {
                return $http.get(addr);
            };
            this.GetCompanyGroups = function (q, page_size) {
                return $http.get(url + "?q=" + q+"&page_size="+page_size)
            };
            this.UpdateCompanyGroup = function (id, companyGroup) {
                return $http.put(url + id + "/", companyGroup)
            };
            this.PostCompanyGroup = function (companyGroup) {
                return $http.post(url , companyGroup)
            };
            this.RemoveCompanyGroup = function (id) {
                return $http.delete(url + id + "/");
            };

        }]);