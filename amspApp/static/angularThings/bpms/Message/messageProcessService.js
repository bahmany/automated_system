'use strict';

angular
    .module('AniTheme')
    .service('messageProcessService',
    ['$cookies', '$http', '$location',
        function ($cookies, $http, $location) {

            this.listMessages = function (currentPage, searchInput, itemsPerPage, listUrl) {
                if (listUrl == undefined) {
                    listUrl = '';
                }
                return $http.get('/api/v1/MessageProcess/' + listUrl + '/?page=' + currentPage + '&query=' + searchInput + '&itemPerPage=' + itemsPerPage);
            };
            this.retrieveMessageProcess = function (id) {
                return $http.get("/api/v1/MessageProcess/" + id + "/");
            };
            this.seenMessage = function (id, obj) {
                return $http.patch('/api/v1/MessageProcess/' + id + '/SeenMessage/', obj);
            };
            this.destroyMessage = function (id) {
                return $http.delete('/api/v1/MessageProcess/' + id + '/');
            };
        }]);






