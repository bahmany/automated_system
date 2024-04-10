'use strict';

angular.module('AniTheme')
    .controller('datamodelCtrl', function ($scope, $http, $translate, $rootScope, $state, $stateParams, $location, $modal) {


        function convertEnglishNameToPersian(englishType) {
            for (var i = 0; formGenElemets['Text input fields'].length > i; i++) {
                if (formGenElemets['Text input fields'][i].type == englishType) {
                    return formGenElemets['Text input fields'][i].displayName
                }
            }
            for (var i = 0; formGenElemets['Connections'].length > i; i++) {
                if (formGenElemets['Connections'][i].type == englishType) {
                    return formGenElemets['Connections'][i].displayName
                }
            }
            for (var i = 0; formGenElemets['Select input fields'].length > i; i++) {
                if (formGenElemets['Select input fields'][i].type == englishType) {
                    return formGenElemets['Select input fields'][i].displayName
                }
            }
            for (var i = 0; formGenElemets['Checkbox fields'].length > i; i++) {
                if (formGenElemets['Checkbox fields'][i].type == englishType) {
                    return formGenElemets['Checkbox fields'][i].displayName
                }
            }
        }


        $scope.convertEnglishNameToPersian = convertEnglishNameToPersian;
        $scope.currentBpmn = {};
        $scope.getBpmn = function () {

            $http.get("/api/v1/companies/" + $stateParams.companyid + "/process/" + $stateParams.processId + "/")
                .then(function (data) {
                    $scope.currentBpmn = data.data;
                })
        }

        $scope.getBpmn();


        $scope.getTaskDef = function (form, index) {
            // debugger;
            $http.get("/api/v1/datamodelmngr/getTaskDetails/?objid=" + form.bpmnObjID + "&bpmnid=" + form.bpmnID).then(function (data) {
                $scope.currentBpmn.form[index] = data.data;
            })
        }


        $scope.deleteFromCurrentForm = function (form, field) {
            swal({
                title: "آیا اطمینان دارید",
                text: "داده ی انتخابی شما از سوابقتان حدف خواهد شد",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "بله حذف شود",
                closeOnConfirm: false
            }, function () {
                $http.post("/api/v1/datamodelmngr/removeFromCurrentTask/", {
                    taskID: form.bpmnObjID,
                    bpmnID: form.bpmnID,
                    fieldName: field.name
                }).then(function (data) {
                    $scope.getBpmn();
                })
                swal("حذف شد", "با موفقیت حذف شد", "success");

            });


        }


    });
