'use strict';

angular
    .module('AniTheme')
    .service('generalService',
    ['$cookies', '$http', '$location',
        function ($cookies, $http, $location) {


            this.getStatistics = function (statistics) {
                return $http.post("getStatistcs", statistics);
            };

            this.getInboxStatistics = function (statistics) {
                return $http.post("getInboxStatistics", statistics);
            };
            this.getFirstTimeInboxStatistics = function () {
                return $http.post("getFirstTimeInboxStatistics", {});
            };

            //this.getUserInfo = function () {
            //    return $http.get("/api/v1/users/GetUserInfo/");
            //};
            this.getMSBoxes = function () {
                return $http.get("/api/v1/statistics/GetCurrentBoxes/");
            };
            this.changeMSBox = function (data) {
                return $http.post("/api/v1/statistics/ChangeMSBox/",data);
            };


        }]);






