'use strict';

angular
    .module('AniTheme')
    .service('dashService',
    ['$cookies', '$http', '$location',
        function ($cookies, $http, $location) {
            this.getMSBoxes = function () {
                return $http.get("/api/v1/statistics/GetCurrentBoxes/");
            };
            this.getMSTemplates = function () {
                return $http.get("/api/v1/statistics/MSTemplateList/");
            };
            this.changeMSBox = function (data) {
                return $http.post("/api/v1/statistics/ChangeMSBox/", data);
            };

        }]);





