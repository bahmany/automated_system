'use strict';
angular.module('AniTheme')
    .controller('AddJobCtrl', function ($scope, $http, $translate, $rootScope, $stateParams, $location, $$$, $filter, $timeout) {
        $scope.companyId = $stateParams.companyid;
        $scope.hamkaries = [];
        function init() {
            $scope.hamkari = {};
            $scope.hamkari.jobs = [];
            $scope.hamkari.extraFields = [];
            $scope.showEdit = false;
            if ($stateParams.jobID) {
                if ($stateParams.jobID != "") {
                    $scope.EditHamkari();
                }
            }


        };
        $scope.AddNewJob = function () {
            //init();
            if (!($scope.hamkari.jobs)){
                $scope.hamkari.jobs = [];
            }
            $scope.hamkari.jobs.push({"name": ""});
        };
        $scope.RemoveJob = function (index) {
            $scope.hamkari.jobs.splice(index, 1);
        };

        $scope.Post = function () {
            $http.post("/api/v1/companies/" + $scope.companyId + "/hamkari/", $scope.hamkari).then(function (data) {
                if (data.data.id) {
                    $scope.$parent.$parent.list();
                    init();
                    $scope.showEdit = false;
                    swal($$$("Good job"), $$$("It has been successfully saved"), "success")
                }
            }).catch(function (data) {
            })
        };
        $scope.EditHamkari = function () {
            $http.get("/api/v1/companies/" + $scope.companyId + "/hamkari/" + $stateParams.jobID + "/").then(function (data) {
                $scope.hamkari = data.data;
                $scope.hamkari.startDate = $filter('jalaliDate')($scope.hamkari.startDate, 'jYYYY/jMM/jDD');
                $scope.hamkari.endDate = $filter('jalaliDate')($scope.hamkari.endDate, 'jYYYY/jMM/jDD');
                $scope.showEdit = true;
            })
        };
        $scope.Cancel = function () {
            init();
        };
        $scope.DeleteHamkari = function (item) {
            swal({
                title: $$$("Are you sure"),
                text: $$$("You will not be able to recover this imaginary file"),
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: $$$("Yes, delete it"),
                closeOnConfirm: false
            }, function () {
                $http.delete("/api/v1/companies/" + $scope.companyId + "/hamkari/" + item.id + "/").then(function (data) {
                    $scope.list();
                    init();
                    swal($$$("Deleted"), $$$("Your imaginary file has been deleted"), "success");
                })
            });
        };
        $scope.list = function () {
            $http.get("/api/v1/companies/" + $scope.companyId + "/hamkari/").then(function (data) {
                $scope.hamkaries = data.data;
            })
        };
        $scope.list();

        $scope.editorOptions = {
            language: 'en',
            toolbar: [
                {
                    name: 'document',
                    items: ['Source', '-', 'Save', 'NewPage', 'DocProps', 'Preview', 'Print', '-', 'Templates']
                },
                {name: 'clipboard', items: ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
                {name: 'editing', items: ['Find', 'Replace', '-', 'SelectAll', '-', 'SpellChecker', 'Scayt']},
                {
                    name: 'forms',
                    items: ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                        'HiddenField']
                },
                '/',
                {
                    name: 'basicstyles',
                    items: ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']
                },
                {
                    name: 'paragraph',
                    items: ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv',
                        '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl']
                },
                {name: 'links', items: ['Link', 'Unlink', 'Anchor']},
                {
                    name: 'insert',
                    items: ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']
                },
                '/',
                {name: 'styles', items: ['Styles', 'Format', 'Font', 'FontSize']},
                {name: 'colors', items: ['TextColor', 'BGColor']},
                {name: 'tools', items: ['Maximize', 'ShowBlocks', '-', 'About']}

            ],
            extraPlugins: 'lineutils,notification,uploadwidget,uploadimage',
            removePlugins: 'sourcearea',
            filebrowserUploadUrl: '/api/v1/file/upload',
            resize_maxHeight: 300,
            height: 100

        };

        $timeout(function () {
            $('#txt_dateOfEnd').datepicker({
                dateFormat: 'yy/mm/dd'
            });
            $('#txt_dateOfStart').datepicker({
                dateFormat: 'yy/mm/dd'
            });
        }, 0);

        init();

    });
