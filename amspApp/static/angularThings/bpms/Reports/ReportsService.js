'use strict';

angular
    .module('AniTheme')
    .service('ReportsService',
    ['$cookies', '$http', '$location',
        function ($cookies, $http, $location) {

            this.getListBpmns = function () {
                return $http.get("/api/v1/reports/BmnsList/");
            };
            this.getFieldsList = function (bpmnId) {
                return $http.get("/api/v1/reports/FieldsList/?bpmn=" + bpmnId);
            };
            this.getDataList = function (bpmnId, selectedIDs, srchQuery, page) {
                if (page == undefined) {
                    page = 1;
                }
                return $http.get("/api/v1/reports/DataList/?bpmn=" + bpmnId + '&fields=' + selectedIDs + '&toDate=' + srchQuery.toDate + '&fromDate=' + srchQuery.fromDate + '&isDone=' + srchQuery.isDone + '&starter=' + srchQuery.starter + '&page=' + page);
            };
            this.getXlsFile = function (bpmnId,selectedNames, selectedIDs, srchQuery) {
                location.href="/api/v1/reports/XLSDataFile/?bpmn=" + bpmnId + '&fields=' + selectedNames + '&fieldsIds=' + selectedIDs + '&toDate=' + srchQuery.toDate + '&fromDate=' + srchQuery.fromDate + '&isDone=' + srchQuery.isDone + '&starter=' + srchQuery.starter;

            };


        }]);






