'use strict';

angular
    .module('AniTheme')
    .service('bamService',
    ['$cookies', '$http', '$location',
        function ($cookies, $http, $location) {

            var current = this;

            current.getCurrent = function (returnWithDetails) {
                return $http.get("/getCurrent?position=" + returnWithDetails)
            };
            //
            current.allRunningReport = function (companyId) {
                return $http.get("/api/v1/companies/" + companyId + "/BAM/AllRunningReport/");
            };
            current.allDoneReport = function (companyId) {
                return $http.get("/api/v1/companies/" + companyId + "/BAM/AllDoneReport/");
            };
            current.getBpmns = function (companyId) {
                return $http.get("/api/v1/companies/" + companyId + "/BAM/GetBpmns/");
            };
            current.getSteps = function (companyId, bpmnId) {
                return $http.get("/api/v1/companies/" + companyId + "/BAM/" + bpmnId + "/GetSteps/");
            };
            current.hideShakhes = function (companyId, shakhesObj) {
                return $http.delete("/api/v1/companies/" + companyId + "/BAM/" + shakhesObj + "/");
            };
            current.shakhesReport = function (companyId, shakhesId) {
                return $http.get("/api/v1/companies/" + companyId + "/BAM/" + shakhesId + "/ShakhesReport/");
            };
            current.listShakhes = function (companyId) {
                return $http.get("/api/v1/companies/" + companyId + "/BAM/");
            };
            current.bamCreate = function (companyId, data) {
                return $http.post("/api/v1/companies/" + companyId + "/BAM/", data);
            };
            current.bamUpdate = function (companyId, shakhesId, data) {
                return $http.put("/api/v1/companies/" + companyId + "/BAM/" + shakhesId + "/", data);
            };
            current.getShakhes = function (companyId, shakhesId) {
                return $http.get("/api/v1/companies/" + companyId + "/BAM/" + shakhesId + "/");
            };
            //current.listCharts = function (companyId) {
            //    return $http.get("/api/v1/companies/" + companyId + "/chart/");
            //};
            //current.listChartsWithoutPage = function (companyId) {
            //    return $http.get("/api/v1/companies/" + companyId + "/chart/PositionsWhitoutPageList/");
            //};
            //current.retrieveBpmn = function (companyId, id) {
            //    return $http.get("/api/v1/companies/" + companyId + "/process/" + id + "/");
            //};
            //current.copyBpmn = function (companyId, data) {
            //    return $http.post('/api/v1/companies/' + companyId + '/process/CopyBpmn/', data);
            //};
            //current.listBpmns = function (companyId, currentPage, searchInput, itemsPerPage) {
            //    return $http.get('/api/v1/companies/' + companyId + '/process/?page=' + currentPage + '&query=' + searchInput + '&itemPerPage=' + itemsPerPage);
            //};
            //
            //current.listForStart = function (companyId, currentPage, searchInput, itemsPerPage) {
            //    return $http.get('/api/v1/companies/' + companyId + '/process/listForStart/?page=' + currentPage + '&query=' + searchInput + '&itemPerPage=' + itemsPerPage);
            //};
            //current.bpmnCreate = function (companyId, obj) {
            //    return $http.post('/api/v1/companies/' + companyId + '/process/', obj);
            //};
            //current.bpmnUpdate = function (companyId, id, obj) {
            //    return $http.put('/api/v1/companies/' + companyId + '/process/' + id + '/', obj);
            //};
            //current.bpmnUpdateCallActivity = function (companyId, id, obj) {
            //    return $http.patch('/api/v1/companies/' + companyId + '/process/' + id + '/UpdateCallActivity/', obj);
            //};
            //current.bpmnPublish = function (companyId, id, obj) {
            //    return $http.patch('/api/v1/companies/' + companyId + '/process/' + id + '/PublishBpmn/', obj);
            //};
            //current.bpmnDelete = function (companyId, id) {
            //    return $http.delete('/api/v1/companies/' + companyId + '/process/' + id + '/');
            //};
            //current.validateBpmn = function (companyId, id) {
            //    return $http.get('/api/v1/companies/' + companyId + '/process/' + id + '/validateBpmn/');
            //};

        }]);






