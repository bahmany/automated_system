/**
 * Created by mohammad on 12/20/15.
 */
'use strict';

angular
    .module('AniTheme')
    .service('SecCompaniesService',
    ['$cookies', '$http', '$location',
        function ($cookies, $http, $location) {

            var url = "/api/v1/letter/sec/company/";
            this.GetListByPager = function (addr) {
                return $http.get(addr);
            };
            this.Get = function (q, page_size) {
                return $http.get(url + "?q=" + q+"&page_size="+page_size)
            };
            this.Update = function (id, item) {
                return $http.put(url + id + "/", item)
            };
            this.Post = function (item) {
                return $http.post(url , item)
            };
            this.Remove = function (id) {
                return $http.delete(url + id + "/");
            };

        }]);