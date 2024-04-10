'use strict';

angular
    .module('AniTheme')
    .service('LunchedProcessService',
    ['$cookies', '$http', '$location',
        function ($cookies, $http, $location) {

            this.listUsers = function (companyId, chartId) {
                return $http.get("/api/v1/companies/" + companyId + "/chart/" + chartId + "/PositionsList/");
            };
            this.listCharts = function (companyId) {
                return $http.get("/api/v1/companies/" + companyId + "/chart/");
            };
            this.retrieveProcess = function (id, processType) {
                return $http.get("/api/v1/" + processType + "/" + id + "/");
            };
            this.retrieveLunchedArchiveTrackData= function (id) {
                return $http.get("/api/v1/LunchedProcessArchive/" + id + "/LPATrack/");
            };
            this.retrieveDoneArchiveTrackData= function (id) {
                return $http.get("/api/v1/DoneProcessArchive/" + id + "/DPATrack/");
            };
            this.retrieveLunchedProcess = function (id) {
                return $http.get("/api/v1/LunchedProcess/" + id + "/");
            };
            this.retrieveSearchBar = function () {
                return $http.get("/api/v1/LunchedProcessArchive/SearchBar/");
            };
            this.listLunchedArchive = function (query) {
                return $http.get("/api/v1/LunchedProcessArchive/ListArchive/?" + query);
            };
            this.retrieveLunchedProcessDiagram = function (id) {
                return $http.get("/api/v1/LunchedProcess/" + id + "/Diagram/");
            };
            this.hideLunchedProcess = function (id) {
                return $http.delete("/api/v1/LunchedProcess/" + id + "/HideLunchedProcess/");
            };
            this.hideLunchedProcessArchive = function (id) {
                return $http.delete("/api/v1/LunchedProcessArchive/" + id + "/HideLunchedProcess/");
            };
            this.hideDoneProcess = function (id) {
                return $http.delete("/api/v1/DoneProcessArchive/" + id + "/HideLunchedProcess/");
            };
            this.listLunchedProcess = function (currentPage, searchInput, itemsPerPage, listUrl) {
                if (listUrl == undefined) {
                    listUrl = '';
                }
                return $http.get('/api/v1/LunchedProcess/' + listUrl + '/?page=' + currentPage + '&query=' + searchInput + '&itemPerPage=' + itemsPerPage);
            };
            this.listLunchedProcessArchive = function (currentPage, searchInput, itemsPerPage, query, listUrl) {
                if (listUrl == undefined) {
                    listUrl = '';
                }
                return $http.get('/api/v1/LunchedProcessArchive/' + listUrl + '/?bpmn=' + query.bpmn +'&name='+ query.name+'&receive='+ query.receive+'&starter='+ query.starter+'&fromDate='+ query.fromDate+'&toDate='+ query.toDate + '&page=' + currentPage + '&query=' + searchInput + '&itemPerPage=' + itemsPerPage);
            };
            this.listDoneProcessArchive = function (currentPage, searchInput, itemsPerPage, query, listUrl) {
                if (listUrl == undefined) {
                    listUrl = '';
                }
                return $http.get('/api/v1/DoneProcessArchive/' + listUrl + '/?bpmn=' + query.bpmn +'&name='+ query.name+'&receive='+ query.receive+'&starter='+ query.starter+'&fromDate='+ query.fromDate+'&toDate='+ query.toDate + '&page=' + currentPage + '&query=' + searchInput + '&itemPerPage=' + itemsPerPage);
            };
            this.createLunchedProcess = function (obj) {
                return $http.post('/api/v1/LunchedProcess/', obj);
            };
            this.updateLunchedProcess = function (id, obj) {
                return $http.put('/api/v1/LunchedProcess/' + id + '/', obj);
            };
            this.completeJob = function (id, obj) {
                return $http.patch('/api/v1/LunchedProcess/' + id + '/CompleteJob/', obj);
            };
            this.justSaveJob = function (id, obj) {
                return $http.patch('/api/v1/LunchedProcess/' + id + '/JustSaveIt/', obj);
            };
            this.deleteLunchedProcess = function (id) {
                return $http.delete('/api/v1/LunchedProcess/' + id + '/');
            };

        }]);






