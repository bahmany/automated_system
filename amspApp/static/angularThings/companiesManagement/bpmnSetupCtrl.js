'use strict';
var amftest;
angular.module('AniTheme')
    .controller('bpmnSetupCtrl', function ($scope, $http, $q, $translate, $rootScope, $state, $stateParams, $location, $modal, bpmnService, $timeout) {
        $scope.bpmn = {};
        $scope.processObjs = [];
        $scope.bindingResults = [];
        $scope.parentToChild = [];
        $scope.childToParent = [];
        $scope.parentProcessData = [];
        $scope.childProcessData = [];
        $scope.formsForCopy = [];
        $scope.selectedFormForCopy = '';
        $scope.charts = [];
        $scope.users = [];
        $scope.chartSelected = '';
        $scope.userSelected = '';
        $scope.form = {};
        $scope.usertask = {};
        $scope.lastSelected = {};
        $scope.properties = {};
        $scope.properties.convdive = '';
        $scope.activeElement = {};
        $scope.activeElementIsDef = '';
        $scope.companyId = $stateParams.companyid;
        //$scope.processId= $stateParams.processId;


        self.hhhhe = "that's it";
        $scope.hhhhe = "that's it";

        var viewer;
        viewer = new BpmnModule({container: '#bpmn-viewer'});
        $scope.showBpmn = function () {
            bpmnService.retrieveBpmn($stateParams.companyid, $stateParams.processId).then(function (data) {
                $scope.bpmn = data.data;
                $scope.processObjs = $scope.bpmn.processObjs;
                $scope.parentProcessData = $scope.bpmn.processObjs;
                $scope.listFormsForCopy();
                viewer.importXML($scope.bpmn.xml, function (err) {
                    $("#bpmn-viewer").fadeIn(150);
                    if (err) {
                        ////console.log('error rendering', err);
                    }
                });
            });
        };


        $scope.getListBpmns = function (current) {
            $scope.listBpmns = function (current) {
                bpmnService.listBpmns(current.company, 1, undefined, 99).then(function (data) {
                    $scope.bpmns = data.data['results'];

                });
            };
            bpmnService.getCurrent(0).then(function (data) {
                $scope.listBpmns(data.data);
            });
        };
        $scope.getDataLayer = function (selectedBpmn) {
            $scope.bpmnDataLayer = function (current) {
                bpmnService.retrieveBpmn(current.company, selectedBpmn).then(function (data) {
                    $scope.childProcessData = data.data.processObjs;
                });
            };
            bpmnService.getCurrent(0).then(function (data) {
                $scope.bpmnDataLayer(data.data);
            });
        };
        $scope.$watch("bpmnSelected", function (newVal, oldVal) {
            // //console.log($scope.bpmnSelected)
            if (newVal != undefined) {
                if (newVal != "") {
                    $scope.getDataLayer(newVal);

                }

            }
        });
        $scope.listCharts = function (companyId) {
            var defer = $q.defer();
            var ss = bpmnService.listChartsWithoutPage(companyId);
            ss.then(function (data) {
                $scope.charts = data.data;
                $scope.charts.results.shift();
                return defer.resolve(ss);
            }).catch(function (data) {
                return defer.reject("");
            });
            return defer.promise;
        };
        $scope.onDropOnChild = function (arg1, arg2) {
            var from, to, res;
            from = $(arg2.draggable[0]);
            to = $(arg1.toElement);
            res = {
                fromBpmn: $scope.bpmn.id,
                toBpmn: $scope.bpmnSelected,
                fromId: $scope.parentProcessData[parseInt(from.attr('id'))].name,
                fromName: $scope.parentProcessData[parseInt(from.attr('id'))].displayName,
                toId: $scope.childProcessData[parseInt(to.attr('id'))].name,
                toName: $scope.childProcessData[parseInt(to.attr('id'))].displayName
            };
            if ($scope.bindingResults == undefined) {

                $scope.bindingResults = [];
                $scope.bindingResults.push(res);
            } else {
                $scope.bindingResults.push(res);
            }
        };
        $scope.onDropOnParent = function (arg1, arg2) {
            var from, to, res;
            from = $(arg2.draggable[0]);
            to = $(arg1.toElement);
            res = {
                fromBpmn: $scope.bpmnSelected,
                toBpmn: $scope.bpmn.id,
                fromId: $scope.childProcessData[parseInt(from.attr('id'))].name,
                fromName: $scope.childProcessData[parseInt(from.attr('id'))].displayName,
                toId: $scope.parentProcessData[parseInt(to.attr('id'))].name,
                toName: $scope.parentProcessData[parseInt(to.attr('id'))].displayName
            };
            if ($scope.bindingResults == undefined) {

                $scope.bindingResults = [];
                $scope.bindingResults.push(res);
            } else {
                $scope.bindingResults.push(res);
            }
        };
        $scope.deleteBindedItm = function (itmIndex) {
            $scope.bindingResults.splice(itmIndex, 1);
        };
        $scope.listUsers = function (companyId, chartId) {
            bpmnService.listUsers(companyId, chartId).then(function (data) {
                $scope.users = data.data;
            });
        };

        $scope.$watch("chartSelected", function (newVal, oldVal) {
            // //console.log($scope.chartSelected);
            $scope.listUsers($scope.bpmn.company_id, newVal);
        });
        $scope.showBpmn();

        $scope.setupExclusive = function (exclusiveElement) {
            $scope.activeElement = exclusiveElement;
            amftest = $scope.activeElement;
            var moddle = new BpmnModdle();
            moddle.fromXML($scope.bpmn.xml, function (err, definitions) {
                definitions.get('rootElements')[definitions.get('rootElements').length - 1].flowElements.some(function (element, index, array) {
                    if (element.id == exclusiveElement.id) {
                        $scope.$apply(function () {
                            $scope.activeElementIsDef = element.default;
                            $scope.properties.convdive = element.get('gatewayDirection');
                            $scope.properties.outgoingSeq = element.outgoing;

                        });
                        $scope.properties.outgoingSeq.some(function (seq, index, array) {
                            if (seq.conditionExpression != undefined) {
                                $('#' + seq.id).val(seq.conditionExpression.body);
                            }
                        });
                        return true;
                    } else {
                        return false;
                    }
                });

                $("#bpmn-viewer").fadeOut(200);
                $('#exclusive-setup-div').fadeIn(200);
            });
        };
        $scope.setupCallActivity = function (callActivityElement) {
            $scope.activeElement = callActivityElement;
            if ($scope.bpmn.bindingMap[callActivityElement.id] != undefined) {

                $scope.bpmnSelected = $scope.bpmn.bindingMap[callActivityElement.id].bpmnSelected;
                $scope.bindingResults = $scope.bpmn.bindingMap[callActivityElement.id].fields;
            }

            amftest = $scope.activeElement;
            $("#bpmn-viewer").fadeOut(200);
            $('#callactivity-setup-div').fadeIn(200);
        };

        $scope.saveSetupExclusive = function () {
            var moddle = new BpmnModdle();

            moddle.fromXML($scope.bpmn.xml, function (err, definitions) {

                definitions.get('rootElements')[definitions.get('rootElements').length - 1].flowElements.some(function (element, index, array) {
                    $scope.properties.outgoingSeq.some(function (seq, index, array) {
                        if (element.id == seq.id) {
                            element.conditionExpression = moddle.create('bpmn:FormalExpression', {body: $('#' + seq.id).val()});
                            return true;
                        } else {
                            return false;
                        }
                    });

                    if ($scope.activeElement.id == element.id) {

                        element.set('default', $('#isdef option:selected').val());
                        element.set('gatewayDirection', $('#convdive option:selected').val());

                    }


                });
                moddle.toXML(definitions, function (err, xmlStrUpdated) {
                    $scope.bpmn.xml = xmlStrUpdated;
                });
                bpmnService.bpmnUpdate($stateParams.companyid, $scope.bpmn.id, $scope.bpmn).then(function (data) {
                    $scope.bpmn = data.data;

                    $('#exclusive-setup-div').fadeOut(200);
                    $("#bpmn-viewer").fadeIn(200);
                    viewer.importXML($scope.bpmn.xml, function (err) {

                        if (err) {
                            ////console.log('error rendering', err);
                        }
                    });
                });
            });
        };
        $scope.saveSetupCallActivity = function () {
            var moddle = new BpmnModdle();
            moddle.fromXML($scope.bpmn.xml, function (err, definitions) {

                definitions.get('rootElements')[definitions.get('rootElements').length - 1].flowElements.some(function (element, index, array) {
                    //if (element.id == $scope.activeElement.id) {
                    //    element.calledElement = moddle.create('bpmn:FormalExpression', {body: $('#' + seq.id).val()});
                    //    return true;
                    //} else {
                    //    return false;
                    //}
                    if ($scope.activeElement.id == element.id) {

                        element.set('calledElement', element.id);
                    }
                });
                moddle.toXML(definitions, function (err, xmlStrUpdated) {
                    $scope.bpmn.xml = xmlStrUpdated;
                });
                bpmnService.bpmnUpdate($stateParams.companyid, $scope.bpmn.id, $scope.bpmn).then(function (data) {
                    $scope.bpmn = data.data;
                    bpmnService.bpmnUpdateCallActivity($stateParams.companyid, $scope.bpmn.id, {
                        bindingMap: $scope.bindingResults,
                        stepId: $scope.activeElement.id,
                        bpmnSelected: $scope.bpmnSelected
                    }).then(function (data) {
                        $scope.bpmn.bindingMap = data.data;

                        $('#callactivity-setup-div').fadeOut(200);
                        $("#bpmn-viewer").fadeIn(200);
                    });
                    viewer.importXML($scope.bpmn.xml, function (err) {

                        if (err) {
                            ////console.log('error rendering', err);
                        }
                    });
                });
            });

        };

        $scope.setupParallel = function (parallelElement) {
            $scope.activeElement = parallelElement;

            $("#bpmn-viewer").fadeOut(200);
            $('#parallel-setup-div').fadeIn(200);
            var moddle = new BpmnModdle();
            moddle.fromXML($scope.bpmn.xml, function (err, definitions) {
                definitions.get('rootElements')[definitions.get('rootElements').length - 1].flowElements.some(function (element, index, array) {
                    if (element.id == parallelElement.id) {
                        $scope.properties.convdive = element.get('gatewayDirection');

                        return true;
                    } else {
                        return false;
                    }
                });
            });
        };
        $scope.saveSetupParallel = function () {
            var moddle = new BpmnModdle();
            moddle.fromXML($scope.bpmn.xml, function (err, definitions) {
                definitions.get('rootElements')[definitions.get('rootElements').length - 1].flowElements.some(function (element, index, array) {
                    if (element.id == $scope.activeElement.id) {
                        element.set('gatewayDirection', $('#convdive option:selected').val());
                        return true;
                    } else {
                        return false;
                    }
                });
                moddle.toXML(definitions, function (err, xmlStrUpdated) {
                    $scope.bpmn.xml = xmlStrUpdated;
                });
                bpmnService.bpmnUpdate($stateParams.companyid, $scope.bpmn.id, $scope.bpmn).then(function (data) {
                    $('#parallel-setup-div').fadeOut(200);
                    $("#bpmn-viewer").fadeIn(200);
                    viewer.importXML($scope.bpmn.xml, function (err) {

                        if (err) {
                            ////console.log('error rendering', err);
                        }
                    });
                });
            });

        };

        $scope.setupManualTask = function (manualTaskElement) {
            $scope.activeElement = manualTaskElement;

            var moddle = new BpmnModdle();
            moddle.fromXML($scope.bpmn.xml, function (err, definitions) {
                definitions.get('rootElements')[definitions.get('rootElements').length - 1].flowElements.some(function (element, index, array) {
                    if (element.id == $scope.activeElement.id) {
                        $scope.$apply(function () {
                            $scope.activeElement.isForCompensation = element.get('isForCompensation');
                        });
                        return true;
                    } else {
                        return false;
                    }
                });
            });


            var isExistFlag = 0;
            if ($scope.bpmn.form == null) {
                $scope.bpmn.form = [];
            }
            if ($scope.bpmn.processObjs == null) {
                $scope.bpmn.processObjs = [];
            }
            $scope.bpmn.form.some(function (element, index, array) {

                if (element["bpmnObjID"] == manualTaskElement.id) {
                    $scope.form = angular.copy(element);
                    isExistFlag = 1;
                    return true
                } else {
                    return false
                }
            });
            if (isExistFlag == 0) {
                $scope.form.bpmnID = $scope.bpmn.id;
                $scope.form.bpmnObjID = manualTaskElement.id;

                if ($scope.lastSelected != manualTaskElement) {
                    $scope.form.schema = {'fields': []};
                }
            }


            $("#bpmn-viewer").fadeOut(200);
            $('#manualtask-setup-div').fadeIn(200);

            $scope.$apply(function () {
                $scope.lastSelected = manualTaskElement;
            });
        };

        $scope.setupUserTask = function (userTaskElement) {
            $scope.activeElement = userTaskElement;
            if ($scope.bpmn.userTasks == null) {
                $scope.bpmn.userTasks = [];
            }
            $scope.bpmn.userTasks.forEach(function (element) {
                if (element.taskId == userTaskElement.id) {
                    $scope.chartSelected = element.chartPerformer;
                    $scope.userSelected = element.performer;
                    $scope.performerType = element.performerType;
                    $scope.selectedBAM = element.selectedBAM;
                    if ($scope.performerType == 6) {
                        $scope.prePerformer = element.performer;
                    }
                }
            });
            $scope.listCharts($scope.bpmn.company_id);

            var isExistFlag = 0;
            if ($scope.bpmn.form == null) {
                $scope.bpmn.form = [];
            }
            if ($scope.bpmn.processObjs == null) {
                $scope.bpmn.processObjs = [];
            }
            $scope.bpmn.form.some(function (element, index, array) {
                if (element["bpmnObjID"] == userTaskElement.id) {
                    $scope.form = angular.copy(element);
                    isExistFlag = 1;
                    return true
                } else {
                    return false
                }
            });
            if (isExistFlag == 0) {
                $scope.form.bpmnID = $scope.bpmn.id;
                $scope.form.bpmnObjID = userTaskElement.id;

                if ($scope.lastSelected != userTaskElement) {
                    $scope.form.schema = {'fields': []};
                }
            }
            // $scope.$apply(function () {
            $scope.lastSelected = userTaskElement;
            // });
            $timeout(function () {
                $("#bpmn-viewer").fadeOut(200);
                $('#usertask-setup-div').fadeIn(200);
            }, 100);
        };
        $scope.setupTask = function (task) {
            $scope.activeElement = task;
            if ($scope.bpmn.userTasks == null) {
                $scope.bpmn.userTasks = [];
            }
            $scope.bpmn.userTasks.forEach(function (element) {

                if (element.taskId == task.id) {
                    $scope.chartSelected = element.chartPerformer;
                    $scope.userSelected = element.performer;
                    $scope.performerType = element.performerType;
                    if ($scope.performerType == 6) {
                        $scope.prePerformer = element.performer;
                    }
                }
            });
            $scope.listCharts($scope.bpmn.company_id);
            var moddle = new BpmnModdle();
            var isExistFlag = 0;
            if ($scope.bpmn.form == null) {
                $scope.bpmn.form = [];
            }
            if ($scope.bpmn.processObjs == null) {
                $scope.bpmn.processObjs = [];
            }
            $scope.bpmn.form.some(function (element, index, array) {

                if (element["bpmnObjID"] == task.id) {
                    $scope.form = angular.copy(element);
                    isExistFlag = 1;
                    return true
                } else {
                    return false
                }
            });
            if (isExistFlag == 0) {
                $scope.form.bpmnID = $scope.bpmn.id;
                $scope.form.bpmnObjID = task.id;

                if ($scope.lastSelected != task) {
                    $scope.form.schema = {'fields': []};
                }
            }


            $("#bpmn-viewer").fadeOut(200);
            $('#task-setup-div').fadeIn(200);

            $scope.$apply(function () {

                $scope.lastSelected = task;
            });
        };
        //$scope.setupTask = function (taskElement) {
        //
        //    var isExistFlag = 0;
        //    if ($scope.bpmn.form == null) {
        //        $scope.bpmn.form = [];
        //    }
        //    if ($scope.bpmn.processObjs == null) {
        //        $scope.bpmn.processObjs = [];
        //    }
        //    $scope.bpmn.form.some(function (element, index, array) {
        //
        //        if (element["bpmnObjID"] == taskElement.id) {
        //            $scope.form = angular.copy(element);
        //            isExistFlag = 1;
        //            return true
        //        } else {
        //            return false
        //        }
        //    });
        //    if (isExistFlag == 0) {
        //        $scope.form.bpmnID = $scope.bpmn.id;
        //        $scope.form.bpmnObjID = taskElement.id;
        //
        //        if ($scope.lastSelected != taskElement) {
        //            $scope.form.schema = {'fields': []};
        //        }
        //    }
        //
        //
        //    $("#bpmn-viewer").fadeOut(200);
        //    $('#task-setup-div').fadeIn(200);
        //
        //    $scope.$apply(function () {
        //
        //        $scope.lastSelected = taskElement;
        //    });
        //};
        $scope.slctedRmPO = '';
        $scope.removeProcessObj = function (index) {
            $scope.slctedRmPO = index;
            swal({
                    title: "آیا به حذف این داده مطمئن هستید؟ ",
                    text: "این داده از تمام فرم ها حذف خواهد شد, وقابل بازگرداندن نخواهد بود. ",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#DD6B55",
                    confirmButtonText: "بله, خذف کن!",
                    showLoaderOnConfirm: true,
                    closeOnConfirm: false
                },
                function () {
                    var item = $scope.processObjs[$scope.slctedRmPO];

                    $scope.bpmn.form.forEach(function (form) {
                        form.schema.fields.forEach(function (field, index) {

                            if (field["name"] == item["name"]) {
                                form.schema.fields.splice(index, 1);
                            }
                        });

                    });
                    $scope.processObjs.splice($scope.slctedRmPO, 1);
                    $scope.bpmn.processObjs = $scope.processObjs;
                    bpmnService.bpmnUpdate($stateParams.companyid, $scope.bpmn.id, $scope.bpmn).then(function (data) {
                        $scope.bpmn = data.data;
                        swal("خذف شد!", "داده از فرایند حذف شد.", "success");

                    });

                });
        };

        $scope.toggleVisibleProcessObj = function (event) {

            $(event.target).parent().parent().find(".fg-field-inner").find('div').toggleClass("show")
        };
        //$scope.saveSetupManualTask = function () {
        //    if ($scope.processObjs == null) {
        //        $scope.processObjs = [];
        //    }
        //    var moddle = new BpmnModdle();
        //    moddle.fromXML($scope.bpmn.xml, function (err, definitions) {
        //        definitions.get('rootElements')[ definitions.get('rootElements').length-1].flowElements.some(function (element, index, array) {
        //            if (element.id == $scope.activeElement.id) {
        //                element.set('isForCompensation', $scope.activeElement.isForCompensation);
        //                return true;
        //            } else {
        //                return false;
        //            }
        //        });
        //        moddle.toXML(definitions, function (err, xmlStrUpdated) {
        //            $scope.bpmn.xml = xmlStrUpdated;
        //        });
        //        $scope.form.schema.fields.forEach(function (obj, index) {
        //
        //            var currentIndex;
        //            var searchableStr = '';
        //            //In this If else app add new form objects to $scope.processObjs
        //            if (obj.name.indexOf('__') != -1) {
        //                $scope.processObjs.forEach(function (obj2) {
        //                    if (obj2.hasOwnProperty('$_isDragging')) {
        //                        delete(obj2.$_isDragging);
        //                    }
        //                    searchableStr += JSON.stringify(obj2);
        //                });
        //                currentIndex = searchableStr.indexOf(obj.name);
        //                if (currentIndex == -1) {
        //                    $scope.processObjs.push(obj);
        //                }
        //            } else {
        //                obj.name = $scope.lastSelected.id + '__' + obj.name;
        //                searchableStr = '';
        //                $scope.processObjs.forEach(function (obj2) {
        //                    if (obj2.hasOwnProperty('$_isDragging')) {
        //                        delete(obj2.$_isDragging);
        //                    }
        //                    searchableStr += JSON.stringify(obj2);
        //                });
        //                currentIndex = searchableStr.indexOf(obj.name);
        //                if (currentIndex == -1) {
        //                    $scope.processObjs.push(obj);
        //                }
        //            }
        //            $scope.bpmn.processObjs = $scope.processObjs;
        //
        //        });
        //        var isUpdateFlag = 0;
        //        // In this if check if bpmn has any form then update bpmn.form with new data or add new form to it
        //        if ($scope.bpmn.form != null) {
        //            $scope.bpmn.form.some(function (element, index, array) {
        //                if (element["bpmnObjID"] == $scope.form.bpmnObjID) {
        //                    $scope.bpmn.form[index] = angular.copy($scope.form);
        //
        //                    isUpdateFlag = 1;
        //                    return true
        //                } else {
        //                    return false
        //                }
        //            });
        //        } else {
        //            $scope.bpmn.form = []
        //        }
        //        if (isUpdateFlag == 0) {
        //            $scope.bpmn.form.push($scope.form);
        //        }
        //        bpmnService.bpmnUpdate($stateParams.companyid, $scope.bpmn.id, $scope.bpmn).then(function (data) {
        //            $scope.bpmn = data;
        //            $('#manualtask-setup-div').fadeOut(200);
        //            $("#bpmn-viewer").fadeIn(200);
        //            viewer.importXML($scope.bpmn.xml, function (err) {
        //
        //                if (err) {
        //                    ////console.log('error rendering', err);
        //                }
        //            });
        //        });
        //    });
        //
        //};
        $scope.performerType = 1;
        $scope.selectedBAM = '';
        $scope.editorOptionsPython = {
            lineWrapping: true,
            lineNumbers: true,
            // readOnly: 'nocursor',
            mode: 'python'
        };

        $scope.saveSetupUserTask = function () {
            if ($scope.processObjs == null) {
                $scope.processObjs = [];
            }
            var moddle = new BpmnModdle();
            moddle.fromXML($scope.bpmn.xml, function (err, definitions) {
                moddle.toXML(definitions, function (err, xmlStrUpdated) {
                    $scope.bpmn.xml = xmlStrUpdated;

                });

                $scope.usertask.taskId = $scope.activeElement.id;
                $scope.usertask.performerType = $scope.performerType;
                $scope.usertask.chartPerformer = $scope.chartSelected;
                $scope.usertask.performer = $scope.userSelected;
                $scope.usertask.selectedBAM = $scope.selectedBAM;
                if ($scope.performerType == 6) {
                    $scope.usertask.performer = $scope.prePerformer;
                }

                if ($scope.bpmn.userTasks == null) {
                    $scope.bpmn.userTasks = [];
                }
                var upFlag = 0;
                $scope.bpmn.userTasks.some(function (element, index, array) {

                    if ($scope.usertask.taskId == element.taskId) {
                        upFlag = 1;
                        $scope.bpmn.userTasks[index] = angular.copy($scope.usertask);
                        $scope.usertask = {};
                        return true;
                    } else {
                        return false;
                    }
                });
                if (upFlag == 0) {
                    $scope.bpmn.userTasks.push($scope.usertask);
                }
                var isUpdateFlag = 0;


                $scope.form.schema.layout.forEach(function (layout, index) {
                    for (var kk = 1; 5 > kk; kk++) {
                        console.log(kk);
                        if (layout.layout["row" + kk.toString()]) {
                            if (layout.layout["row" + kk.toString()].name) {
                                if (layout.layout["row" + kk.toString()].name.indexOf("__") == -1) {
                                    layout.layout["row" + kk.toString()].name = $scope.lastSelected.id + '__' + layout.layout["row" + kk.toString()].name;
                                }
                            }
                        }
                    }
                });

                // debugger;


                $scope.form.schema.fields.forEach(function (obj, index) {
                        var currentIndex;
                        var searchableStr = '';
                        //In this If else app add new form objects to $scope.processObjs
                        if (obj.name.indexOf('__') != -1) {
                            $scope.processObjs.forEach(function (obj2, index) {
                                if (obj2.hasOwnProperty('$_isDragging')) {
                                    delete($scope.processObjs[index].$_isDragging);
                                }
                                searchableStr += JSON.stringify(obj2);
                            });
                            currentIndex = searchableStr.indexOf(obj.name);
                            if (currentIndex == -1) {
                                $scope.processObjs.push(obj);
                            }
                        }
                        else {
                            // debugger;
                            // updating layout

                            obj.name = $scope.lastSelected.id + '__' + obj.name;
                            searchableStr = '';
                            $scope.processObjs.forEach(function (obj2) {
                                searchableStr += JSON.stringify(obj2);
                            });
                            currentIndex = searchableStr.indexOf(obj.name);
                            if (currentIndex == -1) {
                                $scope.processObjs.push(obj);
                            }
                        }


                        $scope.bpmn.processObjs = $scope.processObjs;
                    }
                );
// In this if check if bpmn has any form then update bpmn.form with new data or add new form to it
                if ($scope.bpmn.form == null) {
                    $scope.bpmn.form = []
                }
                $scope.bpmn.form.some(function (element, index, array) {
                    if (element["bpmnObjID"] == $scope.form.bpmnObjID) {
                        $scope.bpmn.form[index] = angular.copy($scope.form);

                        isUpdateFlag = 1;
                        return true
                    } else {
                        return false
                    }
                });

                if (isUpdateFlag == 0) {
                    $scope.bpmn.form.push($scope.form);
                }
                bpmnService.bpmnUpdate($stateParams.companyid, $scope.bpmn.id, $scope.bpmn).then(function (data) {
                    $('#usertask-setup-div').fadeOut(200);
                    $("#bpmn-viewer").fadeIn(200);
                    $scope.bpmn = data.data;
                    viewer.importXML($scope.bpmn.xml, function (err) {
                        if (err) {
                            ////console.log('error rendering', err);
                        }
                    });
                });
            })
            ;

        }
        ;
        $scope.saveSetupTask = function () {
            if ($scope.processObjs == null) {
                $scope.processObjs = [];
            }
            var moddle = new BpmnModdle();
            moddle.fromXML($scope.bpmn.xml, function (err, definitions) {
                //definitions.get('rootElements')[ definitions.get('rootElements').length-1].flowElements.some(function (element, index, array) {
                //    if (element.id == $scope.activeElement.id) {
                //        element.set('isForCompensation', $scope.activeElement.isForCompensation);
                //
                //        return true;
                //    } else {
                //        return false;
                //    }
                //});
                moddle.toXML(definitions, function (err, xmlStrUpdated) {
                    $scope.bpmn.xml = xmlStrUpdated;

                });


                $scope.usertask.taskId = $scope.activeElement.id;
                $scope.usertask.performerType = $scope.performerType;
                $scope.usertask.chartPerformer = $scope.chartSelected;
                $scope.usertask.performer = $scope.userSelected;
                if ($scope.performerType == 6) {
                    $scope.usertask.performer = $scope.prePerformer;
                }
                if ($scope.bpmn.userTasks == null) {
                    $scope.bpmn.userTasks = [];
                }
                var upFlag = 0;
                $scope.bpmn.userTasks.some(function (element, index, array) {

                    if ($scope.usertask.taskId == element.taskId) {
                        upFlag = 1;
                        $scope.bpmn.userTasks[index] = angular.copy($scope.usertask);
                        $scope.usertask = {};
                        return true;
                    } else {
                        return false;
                    }
                });
                if (upFlag == 0) {
                    $scope.bpmn.userTasks.push($scope.usertask);
                }
                var isUpdateFlag = 0;
                $scope.form.schema.fields.forEach(function (obj, index) {


                    var currentIndex;
                    var searchableStr = '';
                    //In this If else app add new form objects to $scope.processObjs
                    if (obj.name.indexOf('__') != -1) {
                        $scope.processObjs.forEach(function (obj2, index) {
                            if (obj2.hasOwnProperty('$_isDragging')) {
                                delete($scope.processObjs[index].$_isDragging);
                            }
                            searchableStr += JSON.stringify(obj2);
                        });
                        currentIndex = searchableStr.indexOf(obj.name);
                        if (currentIndex == -1) {
                            $scope.processObjs.push(obj);
                        }
                    }
                    else {
                        obj.name = $scope.lastSelected.id + '__' + obj.name;
                        searchableStr = '';
                        $scope.processObjs.forEach(function (obj2) {
                            searchableStr += JSON.stringify(obj2);
                        });
                        currentIndex = searchableStr.indexOf(obj.name);
                        if (currentIndex == -1) {
                            $scope.processObjs.push(obj);
                        }
                    }


                    $scope.bpmn.processObjs = $scope.processObjs;

                });

                // In this if check if bpmn has any form then update bpmn.form with new data or add new form to it
                if ($scope.bpmn.form == null) {
                    $scope.bpmn.form = []
                }
                $scope.bpmn.form.some(function (element, index, array) {
                    if (element["bpmnObjID"] == $scope.form.bpmnObjID) {
                        $scope.bpmn.form[index] = angular.copy($scope.form);

                        isUpdateFlag = 1;
                        return true
                    } else {
                        return false
                    }
                });

                if (isUpdateFlag == 0) {
                    $scope.bpmn.form.push($scope.form);
                }
                bpmnService.bpmnUpdate($stateParams.companyid, $scope.bpmn.id, $scope.bpmn).then(function (data) {
                    $('#task-setup-div').fadeOut(200);
                    $("#bpmn-viewer").fadeIn(200);
                    $scope.bpmn = data.data;
                    viewer.importXML($scope.bpmn.xml, function (err) {
                        if (err) {
                            ////console.log('error rendering', err);
                        }
                    });
                });
            });

        };
//$scope.saveSetupTask = function () {
//    if ($scope.processObjs == null) {
//        $scope.processObjs = [];
//    }
//    var isUpdateFlag = 0;
//    $scope.form.schema.fields.forEach(function (obj, index) {
//        var currentIndex;
//        var searchableStr = '';
//        //In this If else app add new form objects to $scope.processObjs
//        if (obj.name.indexOf('__') != -1) {
//            $scope.processObjs.forEach(function (obj2) {
//                if (obj2.hasOwnProperty('$_isDragging')) {
//                    delete(obj2.$_isDragging);
//                }
//                searchableStr += JSON.stringify(obj2);
//            });
//            currentIndex = searchableStr.indexOf(obj.name);
//            if (currentIndex == -1) {
//                $scope.processObjs.push(obj);
//            }
//        } else {
//            obj.name = $scope.lastSelected.id + '__' + obj.name;
//            searchableStr = '';
//            $scope.processObjs.forEach(function (obj2) {
//                    if (obj2.hasOwnProperty('$_isDragging')) {
//                        delete(obj2.$_isDragging);
//                    }
//                    searchableStr += JSON.stringify(obj2);
//                }
//            )
//            ;
//            currentIndex = searchableStr.indexOf(obj.name);
//            if (currentIndex == -1) {
//                $scope.processObjs.push(obj);
//            }
//        }
//
//        // In this if check if bpmn has any form then update bpmn.form with new data or add new form to it
//
//
//        $scope.bpmn.processObjs = $scope.processObjs;
//
//    });
//    if ($scope.bpmn.form != null) {
//        $scope.bpmn.form.some(function (element, index, array) {
//            if (element["bpmnObjID"] == $scope.form.bpmnObjID) {
//                $scope.bpmn.form[index] = angular.copy($scope.form);
//                isUpdateFlag = 1;
//                return true
//            } else {
//                return false
//            }
//        });
//    } else {
//        $scope.bpmn.form = []
//    }
//    if (isUpdateFlag == 0) {
//        $scope.bpmn.form.push($scope.form);
//    }
//    bpmnService.bpmnUpdate($stateParams.companyid, $scope.bpmn.id, $scope.bpmn).then(function (data) {
//        $scope.bpmn = data;
//        $('#task-setup-div').fadeOut(200);
//        $("#bpmn-viewer").fadeIn(200);
//    });
//
//};

        $scope.cancelForm = function () {
            $('#task-setup-div').fadeOut(200);
            $("#bpmn-viewer").fadeIn(200);
        };

        $scope.cancelSetupParallel = function () {
            $('#parallel-setup-div').fadeOut(200);
            $("#bpmn-viewer").fadeIn(200);
        };
        $scope.cancelSetupManualTask = function () {
            $('#manualtask-setup-div').fadeOut(200);
            $("#bpmn-viewer").fadeIn(200);
        };

        $scope.cancelSetupUserTask = function () {
            $('#usertask-setup-div').fadeOut(200);
            $("#bpmn-viewer").fadeIn(200);
        };
        $scope.cancelSetupCallActivity = function () {
            $('#callactivity-setup-div').fadeOut(200);
            $("#bpmn-viewer").fadeIn(200);
        };
        $scope.cancelTask = function () {
            $('#task-setup-div').fadeOut(200);
            $("#bpmn-viewer").fadeIn(200);
        };

        $scope.cancelSetupExclusive = function () {
            $('#exclusive-setup-div').fadeOut(200);
            $("#bpmn-viewer").fadeIn(200);
        };

        $scope.resetForm = function () {
            $scope.form.schema = {'fields': []};
        };

        $scope.listFormsForCopy = function () {
            var moddle = new BpmnModdle();
            moddle.fromXML($scope.bpmn.xml, function (err, definitions) {
                definitions.get('rootElements')[definitions.get('rootElements').length - 1].flowElements.some(function (element, index, array) {
                    if ((element.$type == "bpmn:UserTask") || (element.$type == "bpmn:Task")) {
                        $scope.formsForCopy.push({id: element.id, name: element.name});
                    }
                });
            });

        };

        $scope.pasteForm = function () {

            $scope.bpmn.form.some(function (element, index, array) {
                if (element.bpmnObjID == $scope.selectedFormForCopy) {
                    $scope.form.schema = angular.copy(element.schema);

                    return true;
                }
            });
        };
        $scope.readonlyAll = function () {

            $scope.form.schema.fields.some(function (element, index, array) {
                if (element.validation != undefined) {
                    element.validation.readonly = true;
                }
            });
        };
        $scope.unreadonlyAll = function () {

            $scope.form.schema.fields.some(function (element, index, array) {
                if (element.validation != undefined) {
                    element.validation.readonly = false;
                }
            });
        };
        viewer.on('element.click', function (event) {
            //if (event.element.type == 'bpmn:Task') {
            //    $scope.setupTask(event.element);
            //}
            if (event.element.type == 'bpmn:ParallelGateway') {
                $scope.setupParallel(event.element);
            }
            if (event.element.type == 'bpmn:CallActivity') {
                $scope.getListBpmns();
                $scope.setupCallActivity(event.element);
            }
            if (event.element.type == 'bpmn:ExclusiveGateway') {
                $scope.setupExclusive(event.element);
            }
            //if (event.element.type == 'bpmn:ManualTask') {
            //    $scope.setupManualTask(event.element);
            //}
            if (event.element.type == 'bpmn:UserTask') {
                $scope.setupUserTask(event.element);
            }
            if (event.element.type == 'bpmn:Task') {
                $scope.setupTask(event.element);
            }
        });
        $scope.selctedOIndx = '';
        $scope.editPO = function (indexPO) {
            $scope.selctedOIndx = indexPO;

            swal(
                {
                    title: "تغییر نام داده",
                    text: "نام جدید را وارد کنید",
                    type: "input",
                    showCancelButton: true,
                    closeOnConfirm: false,
                    animation: "slide-from-top",
                    inputPlaceholder: "نام..."
                },
                function (inputValue) {

                    if (inputValue === false)
                        return false;
                    if (inputValue === "") {
                        swal.showInputError("شما باید نام را وارد کنید!");
                        return false
                    }
                    $scope.processObjs[$scope.selctedOIndx].displayName = inputValue;

                    //$scope.bpmn.form.forEach(function (form) {
                    //    form.schema.fields.forEach(function (field, index) {
                    //
                    //        if (field["name"] == item["name"]) {
                    //            form.schema.fields.splice(index, 1);
                    //        }
                    //    });
                    //
                    //});
                    $scope.bpmn.processObjs = $scope.processObjs;
                    var item = $scope.processObjs[$scope.selctedOIndx];

                    $scope.bpmn.form.forEach(function (form, indexForm) {
                        form.schema.fields.forEach(function (field, index) {

                            if (field["name"] == item["name"]) {
                                $scope.bpmn.form[indexForm].schema.fields[index].displayName = inputValue;
                            }
                        });

                    });
                    bpmnService.bpmnUpdate($stateParams.companyid, $scope.bpmn.id, $scope.bpmn).then(function (data) {
                        $scope.bpmn = data.data;
                        swal(
                            "تبریک!",
                            "داده با موفقیت تغییر نام داد. این نام داخل تمام فرم ها نیز تغییر نام داده.",
                            "success");
                    });

                });
        };
    })
;
