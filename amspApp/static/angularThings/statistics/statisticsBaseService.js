'use strict';

angular
    .module('AniTheme')
    .service('statisticsBaseService',
    ['$cookies', '$http', '$location',
        function ($cookies, $http, $location) {

            this.getCurrent = function (returnWithDetails) {
                return $http.get("/getCurrent?position=" + returnWithDetails);
            };
            this.createStatisticTemplate = function (data) {
                return $http.post("/api/v1/statistics/", data);
            };

            this.createMSData = function (data) {
                return $http.post("/api/v1/dataForMS/", data);
            };
            this.deleteTemplate = function (objId) {
                return $http.delete("/api/v1/statistics/" + objId + '/');
            };
            this.deleteData= function (objId) {
                return $http.delete("/api/v1/dataForMS/" + objId + '/');
            };

            this.retrieveMSTemplate = function (objId) {
                return $http.get("/api/v1/statistics/" + objId + '/');
            };
            this.updateMSTemplate = function (objId, data) {
                return $http.put("/api/v1/statistics/" + objId + '/', data);
            };
            this.retrieveMSData = function (objId) {
                return $http.get("/api/v1/dataForMS/" + objId + '/');
            };
            this.updateMSData = function (objId, data) {
                return $http.put("/api/v1/dataForMS/" + objId + '/', data);
            };

            this.listStatisticsTemplates = function (currentPage, searchInput, itemsPerPage) {
                if (currentPage == undefined) {
                    currentPage = 1;
                }
                return $http.get('/api/v1/statistics/?page=' + currentPage + '&query=' + searchInput + '&itemPerPage=' + itemsPerPage);
            };
            this.listStatisticsData = function (tempId, currentPage, searchInput, itemsPerPage) {
                if (currentPage == undefined) {
                    currentPage = 1;
                }
                return $http.get('/api/v1/dataForMS/?tempId=' + tempId + '&page=' + currentPage + '&query=' + searchInput + '&itemPerPage=' + itemsPerPage);
            };
            this.DataPageTo = function (url) {
                return $http.get(url);
            };

        }]);






