/**
 * Created by mohammad on 12/20/15.
 */
'use strict';

angular
    .module('AniTheme')
    .service('SecSideService',
    ['$cookies', '$http', '$location',
        function ($cookies, $http, $location) {

            //var PagerUrl = "/search/inbox/";
            //
            //this.GetCompanyGroupsListByPager = function (addr) {
            //    return $http.get(addr);
            //};
            //
            //this.GetCompanyGroups = function (q, page_size) {
            //    return $http.get("/api/v1/letterSec/secretariat/" + "?q=" + q+"&page_size="+page_size)
            //};

        }]);