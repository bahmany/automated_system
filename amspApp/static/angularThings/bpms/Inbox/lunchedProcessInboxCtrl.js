'use strict';
var globalxml = '';


angular.module('AniTheme')
    .controller('lunchedProcessInboxCtrl', function ($scope, $$$, $http,
                                                     $translate, $state,
                                                     $rootScope,
                                                     $modal, $location, LunchedProcessService, bpmnService) {

        $scope.bpmns = {};
        $scope.globalpos = '';
        $scope.current = {};
        $scope.bpmn = {};
        $scope.oldBpmn = {};
        $scope.timeouts = [];
        $scope.currentPage = 1;
        $scope.maxSize = 5;
        $scope.itemsPerPage = 14;
        $scope.lunchedProcess = {};


        $rootScope.$on('newNotification', function () {
            $scope.getLunchedProcessList();
        });

        // it's for get edit form field data
        $scope.createLunchedProcess = function () {
            $('#newJob').addClass('disabled').html('صبر کنید...');
            LunchedProcessService.createLunchedProcess($scope.lunchedProcess).then(function (dataAA) {
                // return
                if (dataAA.data.id) {
                    // debugger;
                    $('#newJob').removeClass('disabled').html('شروع فرایند');
                    $rootScope.$broadcast('UpdateLPList');
                    ////console.log(dataAA);
                    $scope.doJob(dataAA.data.id, dataAA.data);
                }


                //bpmnService.getCurrent(0).then(function (data) {
                //    $scope.current = data;
                //    $scope.listBpmns(data);v
                //});
            }).catch(function (data) {
                $('#newJob').removeClass('disabled').html('شروع فرایند');
                $scope.errors = data.data.message;
            });

        };

        $scope.destroyDoneProcess = function (LunchedProcessObj) {

            //swal({
            //    title: "Are you sure?",
            //    text: "You will not be able to recover this imaginary file!",
            //    type: "warning",
            //    showCancelButton: true,
            //    confirmButtonColor: "#DD6B55",
            //    confirmButtonText: "Yes, delete it!",
            //    showLoaderOnConfirm: true,
            //    closeOnConfirm: false
            //}, function () {
            //    bpmnService.getCurrent(0).then(function (res) {
            //        $scope.current = res;
            //        if (res.positionDocument == LunchedProcessObj.position_id) {
            //            LunchedProcessService.hideDoneProcess(LunchedProcessObj.id).then(function (data) {
            //
            //                swal("Deleted!", "Your imaginary file has been deleted.", "success");
            //                $scope.DoneProcessArchiveList();
            //            });
            //        } else {
            //            swal("Permission!", "You're nor be able to delete this process.", "error");
            //
            //        }
            //    });
            //
            //});

        };

        $scope.saveLunchedProcess = function () {
            LunchedProcessService.createLunchedProcess($scope.lunchedProcess).then(function (data) {
                $modalInstance.close($$$('u did it with success'));
            }).catch(function (data) {
                $scope.errors = data.data.message;
            });
        };

        $scope.listBpmns = function (current) {
            bpmnService.listForStart(current.company, 1, undefined, 99).then(function (data) {
                $scope.bpmns = data.data['results'];

            });
        };


        bpmnService.getCurrent(0).then(function (data) {
            $scope.current = data.data;
            $scope.listBpmns(data.data);
        });
        //

        $scope.selectedLunchedProcessId = "";


        $scope.inboxBAMDanger = function (date) {
            //1==zaman gozashte
            //2==yani 7sa2 moonde
            //3==yani 2sa2 moonde
            //0==koli moonde
            if (date == -1) {
                return 0;
            }
            date = new Date(date);

            var CurrentDate = moment();
            var NEwdate = moment(date);
            if (NEwdate >= CurrentDate) {
                var durSecs = moment.duration(NEwdate - CurrentDate);
                if ((durSecs.years() == 0) && (durSecs.days() == 0)) {
                    if (durSecs.hours() <= 7) {
                        if (durSecs.hours() <= 2) {
                            return 3;
                        } else {
                            return 2;
                        }
                    } else {
                        return 0;
                    }
                } else {
                    return 0;
                }
            } else {
                return 1;
            }
        };


        $scope.doJob = function (LunchedProcessId, item) {
            // debugger;
            if (item.hasOwnProperty("seen")) {
                item.seen = 1;
            }
            $scope.selectedLunchedProcessId = LunchedProcessId;
            // debugger;

            $state.go("inbox-process-do", {lunchedProcessId: LunchedProcessId});


        };

        $scope.viewBpmnDiagram = function (LunchedProcessId, item) {
            $scope.selectedLunchedProcessId = LunchedProcessId;
            $state.go("inbox-process-diagram", {lunchedProcessId: LunchedProcessId});
        };

        $scope.destroyProcess = function (LunchedProcessObj) {
            swal({
                title: "آیا به حذف این فرایند مطمئن هستید؟ ",
                text: "این فرایند از سیستم حذف خواهد شد, وقابل بازگرداندن نخواهد بود. ",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: $$$("Yes, delete it"),
                showLoaderOnConfirm: true,
                closeOnConfirm: false
            }, function () {
                bpmnService.getCurrent(0).then(function (res) {
                    $scope.current = res.data;
                    if (res.positionDocument == LunchedProcessObj.position_id) {
                        LunchedProcessService.hideLunchedProcess(LunchedProcessObj.id).then(function (data) {

                            swal("خذف شد!", "فرایند از سیستم حذف شد.", "success");
                            $scope.getLunchedProcessList();
                            $state.go("inbox-process-dashboard");
                        });
                    } else {
                        swal("دسترسی!", "شما اجازه دسترسی به حذف این فرایند ندارید.", "error");

                    }
                });


            });

        };


        $scope.retrieveLunchedProcess = function (id) {
            bpmnService.retrieveLunchedProcess(id).then(function (data) {
                $scope.bpmn.name = data.data['name'];
                $scope.bpmn.xml = data.data['xml'];
                $scope.bpmn.description = data.data['description'];
                $scope.bpmn.id = data.data['id'];
                $scope.bpmn.currentTaskID = data.data.curAndPrevSteps.taskId;
                globalxml = data.data['xml'];
            });
        };

        $scope.buildForm = function (id) {
            $rootScope.id = id;
            $location.url('/dashboard/buildForm');
        };
        $scope.lunchedProcessDelete = function (id) {
            var modalInstance = $modal.open({
                animation: true,
                templateUrl: 'GenericModalAreYouSure.html',
                controller: 'ModalAreYouSureInstanceCtrl',
                size: '',
                resolve: {}
            });
            modalInstance.result.then(function (selectedItem) {
                bpmnService.lunchedProcessDelete(id).then(function (data) {

                    $scope.getLunchedProcessList();
                }).catch(function (data) {
                    var modalInstance = $modal.open({
                        animation: true,
                        templateUrl: 'GenericModalPermissionDenied.html',
                        controller: 'ModalPermissionDeniedInstanceCtrl',
                        size: '',
                        resolve: {}
                    });
                });

            }, function () {
            });

        };
        $scope.getLunchedProcessList = function () {
            bpmnService.getCurrent(0).then(function (res) {
                $scope.globalposid = res.data.positionDocument;
                LunchedProcessService.listLunchedProcess($scope.currentPage, $scope.searchInput, $scope.itemsPerPage, "Inbox").then(function (data) {
                    $scope.data = data.data;
                    $scope.totalItems = data.data.count;
                    if (($scope.searchInput == undefined) || ($scope.searchInput == '')) {
                        $scope.totalItemsCount = data.data.count;
                    }
                    $scope.itemsFrom = ($scope.currentPage - 1) * $scope.itemsPerPage;

                    $scope.itemsFrom += 1;

                    $scope.itemsTo = $scope.itemsFrom + $scope.itemsPerPage - 1;
                    if ($scope.itemsTo > $scope.totalItems) {
                        $scope.itemsTo = $scope.totalItems;
                    }

                    $scope.foundedItemsCount = data.data.count;
                });
            });

        };
        $scope.getLunchedProcessList();
        $scope.$on("UpdateLPList", function (event, args) {
            $scope.getLunchedProcessList();
        });
        $scope.$on("RemoveFromList", function (event, args) {
            $scope.removeFromList(args.ProcessID);
        });
        $scope.removeFromList = function (processID) {
            //////console.log(processID);
            //
            for (var i = 0; $scope.data.results.length; i++) {

                if ($scope.data.results[i].id == processID) {
                    //
                    $scope.data.results.splice(i, 1);
                    return
                }
            }
        };
        $scope.clearAllTimeouts = function () {
            for (var i = 0; i < $scope.timeouts.length; i++) {
                clearTimeout($scope.timeouts[i])
            }
        };


    });

