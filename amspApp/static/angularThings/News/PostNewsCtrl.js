'use strict';


angular.module('AniTheme').controller(
    'PostNewsCtrl',
    function ($scope,
              $translate,
              $http, $stateParams,
              $q, $mdDialog,
              $rootScope,
              $modal, Upload) {

        $scope.get = function () {
            if ($stateParams.NewsID != 0) {
                $http.get("/api/v1/news/" + $stateParams.NewsID + "/").then(function (data) {
                    $scope.news = data.data;
                })
            }
        }

        $scope.addFileDetailToNew = function (companyid, fileID) {
            DMSManagementService.getFile(companyid, fileID).then(function (data) {
                $scope.newDMS.allFiles.push(data.data);
            });
        };


        $scope.news = {};

        $scope.post = function () {
            $http.post("/api/v1/news/", $scope.news).then(function (data) {

            })
        };

        $scope.get();

        $scope.editorOptions = {
            language: 'fa',
            toolbar: [
                {
                    name: 'document',
                    items: ['Source', '-', 'Save', 'NewPage', 'DocProps', 'Preview', 'Print', '-', 'Templates']
                },
                {
                    name: 'clipboard',
                    items: ['Source', 'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']
                },
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
                    items: ['LocationMap', 'Source', 'Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']
                },
                '/',
                {name: 'styles', items: ['Styles', 'Format', 'Font', 'FontSize']},
                {name: 'colors', items: ['TextColor', 'BGColor']},
                {name: 'tools', items: ['Maximize', 'ShowBlocks', '-', 'About', 'Sourcedialog']},


            ],
            extraPlugins: 'lineutils,notification,uploadwidget,uploadimage,sourcedialog,locationmap',
            removePlugins: 'sourcearea',
            filebrowserUploadUrl: '/api/v1/file/upload',
            resize_maxHeight: 900,
            height: 600

        }
        ;


    });