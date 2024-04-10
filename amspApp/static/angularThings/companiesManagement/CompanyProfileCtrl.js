'use strict';


angular.module('AniTheme')
    .directive("loadMoreData", [function () {
        return {
            restrict: 'ACE',
            link: function ($scope, element, attrs, ctrl) {
                var raw = element[0];
                element.scroll(function () {
                    ////console.log("hiiii");
                    if (raw.scrollTop + raw.offsetHeight >= raw.scrollHeight) {
                        $scope.$apply("loadMoreData()");
                    }
                });
            }
        };

    }]);


angular.module('AniTheme')
    .controller('CompanyProfileCtrl', function ($scope, $http, $q, $translate, $rootScope, $stateParams, $location, $modal, companiesManagmentService) {
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
            height: 400

        };
        $scope.GetCompanyProfile = function (item) {
            companiesManagmentService.GetCompanyProfile(item).then(function (data) {
                $scope.Profile = data.data[0];
            });
        };
        $scope.GetCompanyProfile($stateParams.companyid);
        $scope.UpdateProfile = function () {
            var defer = $q.defer();
            var res = companiesManagmentService.UpdateProfile($scope.Profile);
            res.then(function (data) {
                $scope.GetCompanyProfile($stateParams.companyid);
                $rootScope.$broadcast("showToast", "با موفقیت");
                return defer.resolve(res);
            }).catch(function (data) {
                data.message.forEach(function (err) {
                    swal(err.name, err.message, "error");
                });
                return defer.reject("");
            });
                return defer.promise;
        };
    });
