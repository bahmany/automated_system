'use strict';

angular.module('AniTheme')
    .controller('TrackDoneProcessCtrl', function ($scope, $http, $translate, $rootScope, $stateParams, $state, $modal, $location, LunchedProcessService, bpmnService) {
        $scope.sendingData = {};
        var viewer;
        viewer = new BpmnModule({container: '#bpmn-viewer'});

        $scope.current = {};
        $scope.bpmn = {};
        $scope.process = {};
        $scope.renderForm = function () {
            LunchedProcessService.retrieveDoneArchiveTrackData($stateParams.lunchedProcessId).then(function (data) {
                $scope.process = data.data;
                bpmnService.getCurrent(0).then(function (dataCurrnet) {
                    $scope.current = dataCurrnet.data;
                    $scope.bpmn = data.data;
                    viewer.importXML($scope.bpmn.xml, function (err) {
                        $("#bpmn-viewer").fadeIn(150);

                        var canvas = viewer.get('canvas');
                        data.data.steps.forEach(function (obj, index) {
                            canvas.addMarker(obj, 'thisstep');

                        });
                        data.data.realPastSteps.shift();
                        data.data.realPastSteps.forEach(function (obj, index) {
                            if (obj) {
                                if (obj.split("_").length == 2) {
                                    console.log(obj);
                                    canvas.addMarker(obj, 'finished');

                                }

                            }


                        });
                        if (err) {
                            ////console.log('error rendering', err);
                        }
                    });
                    $scope.sendingData.formData = data.data.formData;

                });

            });
        };

        $scope.renderForm();
        $scope.showData = function (stepName, stepDesc) {
            var modalInstance = $modal.open({
                animation: true,
                templateUrl: '/page/generic/showBpmnStepData',
                controller: 'showDataCtrl',
                size: '',
                resolve: {
                    bpmn: function () {
                        return $scope.bpmn
                    },
                    process: function () {
                        return $scope.process
                    },
                    name: function () {
                        return stepName
                    },
                    desc: function () {
                        return stepDesc
                    }
                }
            });
        };
        viewer.on('element.click', function (event) {
            $scope.process.steps.some(function (obj, index) {
                if (event.element.id == obj) {
                    $scope.showData(obj, event.element.businessObject.name);
                    return true;
                }
            });

        });

    });

angular.module('AniTheme')
    .controller('showDataCtrl', function ($scope, $http, $translate, $modal, bpmn, process, name, desc) {
        $scope.thisStep = {};
        $scope.thisStep.name = name;
        $scope.thisStep.desc = desc;
        //$scope.thisStep.form = bpmn.form.schema;
        bpmn.form.some(function (obj, index) {
            if (obj.bpmnObjID == name) {
                $scope.thisStep.form = obj.schema;
                return true
            } else {
                return false
            }
        });
        $scope.thisStep.form.fields.forEach(function (obj, index) {
            if ($scope.thisStep.form.fields[index].validation) {
                $scope.thisStep.form.fields[index].validation['readonly'] = true;
            }

        });
        $scope.thisStep.formData = process.formData;
        //debugger;
    });