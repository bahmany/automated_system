/**
 * Created by mohammad on 12/20/15.
 */
'use strict';

angular
    .module('AniTheme')
    .service('ImportService',
    ['$cookies', '$http', '$location',
        function ($cookies, $http, $location) {



            var urlMember = "/api/v1/members-search/";
            this.GetMembersListByPager = function (addr) {
                return $http.get(addr);
            };
            this.GetMembers = function (q, page_size) {
                return $http.get(urlMember + "?q=" + q + "&page_size=" + page_size)
            };


        }]);