'use strict';

angular.module('AniTheme')
    .controller('DoLunchedProcessCtrl', function (
        $scope, $http, $translate, $rootScope, $stateParams,
        $state, $modal, $location, $q,
        LunchedProcessService, bpmnService) {
        $scope.sendingData = {};
        $scope.current = {};
        $scope.userOptions = [];
        $scope.chartOptions = [];
        $scope.chartSelected = [];
        $scope.userSelected = [];
        $scope.lunchedPData = {};

        $scope.listCharts = function (companyId) {
            bpmnService.listChartsWithoutPage(companyId).then(function (data) {
                $scope.sendingData.formData.chartOptions = data.data.results;
                $scope.sendingData.formData.chartOptions.shift();
            });

        };

        $scope.listUsers = function (companyId, chartId) {
            if (!((companyId == undefined) || (chartId == undefined))) {
                bpmnService.listUsers(companyId, chartId).then(function (data) {
                    $scope.sendingData.formData.userOptions = data.data.results;
                });
            }
        };


        $scope.processPrint = function (element, json) {
            // get from big archive
            $http.get("/api/v1/reports/" + json.id + "/getBigArchiveHistory/").then(function (data) {
                PrintElem('#DoLunchedProcessCtrl', json, data.data);

            });


        }

        $scope.initUsers = function () {
            bpmnService.getCurrent(0).then(function (data) {
                $scope.current = data.data;
                $scope.listCharts($scope.current.company);

            });
        };
        $scope.$watch("sendingData.formData.chartSelected", function (newVal, oldVal) {
            $scope.listUsers($scope.current.company, newVal);
        });

        $scope.completeIt = function (myForm) {
            if (myForm.$invalid) {
                swal({
                    title: "Invalid data",
                    text: "Please fill the form ",
                    type: "error"
                });
                return;

            }


            $scope.sendingData.taskID = $scope.lunchedPData.curAndPrevSteps.taskId;
            $('#sendjob').attr('disabled', 'disabled').html('صبر کنید...').removeClass('fa').removeClass('fa-send');
            LunchedProcessService.completeJob($stateParams.lunchedProcessId, $scope.sendingData).then(function (data) {
                if (data.data.id) {
                    $rootScope.$broadcast('UpdateLPList');
                    swal({
                        title: "فعالیت مذکور انجام به مرحله ی بعد ارسال شد",
                        text: "این کار در قسمت پایش کار یا بایگانی قابل پیگیری است",
                        type: "success"
                    }, function () {
                        //$rootScope.$broadcast("RemoveFromList", {"ProcessID": $stateParams.lunchedProcessId});
                        $state.go("inbox-process-dashboard");
                    });
                } else {
                    alert("ارسال نشد - لطفا دیباگر را کنترل کنید")
                }
            });

        };
        $scope.justSaveIt = function () {
////debugger;
            LunchedProcessService.justSaveJob($stateParams.lunchedProcessId, $scope.sendingData).then(function (data) {

                swal({
                    title: "ذخیره شد",
                    text: "فرآیند مورد نظر با موفقیت ذخیره شد",
                    type: "success"
                }, function () {
                    //$state.go("process.inbox");
                });

            });
        };


        $scope.HandleTables = function (process) {
            angular.forEach(process.formSchema.fields, function (value, key) {
                if (value.tableId) {

                }

            })
        };

        $scope.current = {};
        $scope.bpmn = {};
        $scope.pleasewaitform = true;
        $scope.renderForm = function () {
            $scope.pleasewaitform = true;

            LunchedProcessService.retrieveLunchedProcess($stateParams.lunchedProcessId).then(function (data) {
                $scope.lunchedPData = data.data;
                bpmnService.getCurrent(0).then(function (dataCurrnet) {
                    //console.log("-------------------------");
                    //console.log(data);
                    //console.log("-------------------------");
                    $scope.current = dataCurrnet.data;
                    $scope.HandleTables(data.data);
                    //$scope.bpmn = data['bpmn'];
                    $scope.formSchema = data.data.formSchema;

                    $scope.sendingData.formData = data.data.formData;
                    $scope.sendingData.formSchema = data.data.formSchema;
                    if (!($scope.sendingData.formData.chartSelected)) {
                        $scope.initUsers();
                    }
                    $scope.pleasewaitform = false;

                });

            });
        };


        $scope.renderForm();


    });

