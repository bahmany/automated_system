'use strict';

angular
    .module('AniTheme')
    .service('DMSManagementService',
    ['$cookies', '$http', '$location',
        function ($cookies, $http, $location) {

            this.getFile = function (companyId, fileId) {
                return $http.get("/api/v1/companies/" + companyId + "/dms/" + fileId + "/fileDet/");
            };
            this.getDMS = function (companyId, id) {
                return $http.get("/api/v1/companies/" + companyId + "/dms/" + id + "/");
            };

            this.getDMSlist = function (companyId) {
                return $http.get("/api/v1/companies/" + companyId + "/dms/InboxList/");
            };
            this.getDMSListForUser = function (page) {
                return $http.get("/api/v1/companies/0/dms/DMSListForUser/?page=" + page);
            };
            this.getDMSSettings = function (companyId) {
                return $http.get("/api/v1/companies/" + companyId + "/dms/getDMSSettings/");
            };

            this.createDMS = function (companyId, obj) {
                return $http.post('/api/v1/companies/' + companyId + '/dms/', obj);
            };

            this.updateDMS = function (companyId, id, obj) {
                return $http.put('/api/v1/companies/' + companyId + '/dms/' + id + '/', obj);
            };
            this.destroyDMS = function (companyId, id) {
                return $http.delete("/api/v1/companies/" + companyId + "/dms/" + id + "/");
            };
        }]);






