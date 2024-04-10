'use strict';
var globalxml = '';


angular.module('AniTheme')
    .controller('CompanyProcessCtrl', function ($scope, $http, $translate, $rootScope, $state, $stateParams, $modal, $location, bpmnService) {

        $scope.bpmns = {};
        $scope.bpmn = {};
        $scope.oldBpmn = {};
        $scope.timeouts = [];
        // $scope.currentPage = 1;
        // $scope.maxSize = 5;
        // $scope.itemsPerPage = 14;


        $scope.TableBpmns = {};
        $scope.Bpmn = {};
        $scope.TableBpmns.pagination = {};
        $scope.TableBpmns.pagination.size = 20;
        $scope.TableBpmns.pagination.total = 0;
        $scope.TableBpmns.isShow = false;
        $scope.BpmnsTableSearch = "";
        $scope.HandleBpmnsTablePagination = function () {
            if ($scope.TableBpmns.pagination.size == 40) {
                $scope.TableBpmns.pagination.size = 10;
            }
            $scope.TableBpmns.pagination.size = $scope.TableBpmns.pagination.size + 5;
            $scope.ListBpmns($scope.TableBpmns.pagination.size);
        };
        $scope.$watch("BpmnsTableSearch", function () {
            $scope.ListBpmns($scope.TableBpmns.pagination.size);
        });
        $scope.BpmnsTableGoToPage = function (url) {
            $scope.isSearchCallbackCompleted = false;
            $http.get(url).then(function (data) {
                $scope.isSearchCallbackCompleted = true;
                $scope.Bpmns = data.data;
            }).catch(function (data) {
                $scope.isSearchCallbackCompleted = true;
            });
        };

        $scope.isSearchCallbackCompleted = true;
        $scope.ListBpmns = function () {
            $scope.isSearchCallbackCompleted = false;
            $http.get('/api/v1/companies/' + $stateParams.companyid + '/process/listForEdit/?q=' + $scope.BpmnsTableSearch + "&page_size=" + $scope.TableBpmns.pagination.size).then(function (data) {
                $scope.Bpmns = data.data;
                $scope.isSearchCallbackCompleted = true;
            }).catch(function (data) {
                $scope.isSearchCallbackCompleted = false;
            });

            // bpmnService.listBpmns($stateParams.Bpmnid, $scope.currentPage, $scope.searchInput, $scope.itemsPerPage).then(function (data) {
            //     $scope.data = data;
            //     $scope.isSearchCallbackCompleted = true;
            // $scope.totalItems = data.count;
            // if (($scope.searchInput == undefined) || ($scope.searchInput == '')) {
            //     $scope.totalItemsCount = data.count;
            // }
            // $scope.itemsFrom = ($scope.currentPage - 1) * $scope.itemsPerPage;
            //
            // $scope.itemsFrom += 1;
            //
            // $scope.itemsTo = $scope.itemsFrom + $scope.itemsPerPage - 1;
            // if ($scope.itemsTo > $scope.totalItems) {
            //     $scope.itemsTo = $scope.totalItems;
            // }
            //
            // $scope.foundedItemsCount = data.count;
            // }).catch(function (data) {
            //     $scope.isSearchCallbackCompleted = false;
            // });
        };


        $('#newbpmn').click(function () {

        });
        // it's for get edit form field data
        $scope.createBpmn = function () {
            $rootScope.bpmnRoot = '';
            $rootScope.bpmnRoot = {};
            globalxml = '';
            $state.go("new-process", {companyid: $stateParams.companyid});
        };
        $scope.openbpmnPublish = function (id) {
            $rootScope.$broadcast("setSelectMemProp", {
                prevDivName: "divBpmn",
                currDivName: "divRec",
                thisListIsFor: 4, // bpmn
                letterID: id
            });
            if ($scope.bpmn.extra) {
                if ($scope.bpmn.extra.receiverListId) {
                    $rootScope.$broadcast("CallMembers", $scope.bpmn.extra.receiverListId);
                }
            }
            $("#divBpmn").fadeOut(function () {
                $("#divRec").fadeIn();
                $rootScope.$broadcast("CallMembersFromList", $scope.bpmn.publishedUsersDetail);
            });
        };
        $scope.bpmnPublish = function (id) {
            bpmnService.retrieveBpmn($stateParams.companyid, id).then(function (data) {
                $scope.bpmn = data.data;
                globalxml = data.data['xml'];
                $scope.openbpmnPublish(id);

            });
            //$state.go("Bpmn.process.new", {Bpmnid: $stateParams.Bpmnid});
        };
        $scope.retrieveBpmn = function (id) {
            bpmnService.retrieveBpmn($stateParams.companyid, id).then(function (data) {
                $scope.bpmn.name = data.data['name'];
                $scope.bpmn.xml = data.data['xml'];
                $scope.bpmn.description = data.data['description'];
                $scope.bpmn.id = data.data['id'];
                globalxml = data.data['xml'];
            });
        };
        $scope.bpmnEdit = function (id) {
            $state.go("edit-process", {Bpmnid: $stateParams.companyid, processId: id});

        };
        $scope.datamodel = function (id) {
            $state.go("datamodel-process", {Bpmnid: $stateParams.companyid, processId: id});

        };
        $scope.buildForm = function (id) {
            $rootScope.id = id;
            $state.go("setup-process", {Bpmnid: $stateParams.companyid, processId: id});

        };
        $scope.cpyyBpmnId = '';
        $scope.bpmnCopy = function (id) {
            $scope.cpyyBpmnId = id;
            swal({
                    title: "کپی فرایند",
                    text: "لطفا عنوان برای فرایند وارد کنید",
                    type: "input",
                    showCancelButton: true,
                    closeOnConfirm: false,
                    animation: "slide-from-top",
                    inputPlaceholder: "عنوان فرایند..."
                },
                function (inputValue) {
                    var data = {bpmnId: $scope.cpyyBpmnId, value: inputValue};
                    bpmnService.copyBpmn($stateParams.companyid, data).then(function (data) {
                        $scope.retrieveBpmn(data.data);
                        swal(
                            "تبریک!",
                            "فرایند با موفقیت ساخته شد.",
                            "success");
                    }).catch(function (data) {
                        swal.showInputError('نام نباید تکراری باشد.');
                    });
                });

        };
        $scope.bpmnDelete = function (id) {
            var modalInstance = $modal.open({
                animation: true,
                templateUrl: 'GenericModalAreYouSure.html',
                controller: 'ModalAreYouSureInstanceCtrl',
                size: '',
                resolve: {}
            });
            modalInstance.result.then(function (selectedItem) {
                bpmnService.bpmnDelete($stateParams.companyid, id).then(function (data) {

                    $scope.ListBpmns();
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

        $scope.bpmnValidate = function (id) {
            bpmnService.validateBpmn($stateParams.companyid, id).then(function (data) {
                var modalInstance = $modal.open({
                    animation: true,
                    controller: 'validateBpmnCtrl',
                    templateUrl: 'validateBpmnModal.html',
                    resolve: {
                        "data": function () {
                            return data.data;
                        }
                    }
                });
                modalInstance.result.then(function () {


                }, function () {
                });
            });
        };


        $scope.clearAllTimeouts = function () {
            for (var i = 0; i < $scope.timeouts.length; i++) {
                clearTimeout($scope.timeouts[i])
            }
        };
        //$('.sidenav-outer').perfectScrollbar();

        $scope.searchBpmn = function () {
            $scope.clearAllTimeouts();
            $scope.timeouts.push(
                setTimeout($scope.ListBpmnsList, 1500)
            );

        };
    });

angular.module('AniTheme')
    .controller('validateBpmnCtrl', function ($scope, $modalInstance, data) {
        $scope.allErrors = [];
        $scope.allErrors = data.data;
        $scope.ok = function () {
            //$modalInstance.dismiss('ok');

        };
    });