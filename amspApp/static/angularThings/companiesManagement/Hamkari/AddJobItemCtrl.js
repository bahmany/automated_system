'use strict';
angular.module('AniTheme')
    .controller('AddJobItemCtrl', function ($scope, $http, $translate, $rootScope, $stateParams, $location, $$$, $filter, $timeout, $mdDialog) {
        $scope.status = '  ';
        $scope.customFullscreen = false;
        $scope.jobItemsSearchText = "";
        var jobItem = {};

        function DialogController($scope, $mdDialog) {
            $scope.jobItem = jobItem
            $scope.hide = function () {
                $mdDialog.hide();
            };
            $scope.cancel = function () {
                $mdDialog.cancel();
            };
            $scope.post = function () {
                $mdDialog.hide($scope.jobItem);
            };
            $scope.editorOptions = {
                language: 'en',
                toolbar: [
                    {
                        name: 'document',
                        items: ['Source', '-', 'Save', 'NewPage', 'DocProps', 'Preview', 'Print', '-', 'Templates']
                    },
                    {
                        name: 'clipboard',
                        items: ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']
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


            $scope.AddNewExtraFields = function (item) {
                if (!(item.extraFields)) {
                    item.extraFields = [];
                }
                item.extraFields.push({"name": ""});
            };
            $scope.RemoveExtraFields = function (item, index) {
                item.extraFields.splice(index, 1);
            };


        }

        $scope.jobItemsPageTo = function (page) {
            if (page) {
                $http.get(page).then(function (data) {
                    $scope.jobItems = data.data;
                });
            }
        }

        $scope.$watch("jobItemsSearchText", function () {
            $scope.list();
        });

        $scope.showModal = function (ev) {
            jobItem = $scope.jobItem;
            $mdDialog.show({
                controller: DialogController,
                templateUrl: '/page/company/AddEditJobItems',
                parent: angular.element(document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
                jobItem: $scope.jobItem,
                fullscreen: $scope.customFullscreen // Only for -xs, -sm breakpoints.
            })
                .then(function (jobItem) {
                    if (jobItem.id) {
                        $http.patch("/api/v1/companies/" + $stateParams.companyid + "/hamkari/" + $stateParams.jobID + "/job/" + jobItem.id + "/", jobItem).then(function (data) {
                            $scope.list();
                        })

                    } else {
                        $http.post("/api/v1/companies/" + $stateParams.companyid + "/hamkari/" + $stateParams.jobID + "/job/", jobItem).then(function (data) {
                            $scope.list();
                        })
                    }


                }, function () {
                    $scope.status = 'You cancelled the dialog.';
                });
        };
        $scope.edit = function (ev, item) {
            $http.get("/api/v1/companies/" + $stateParams.companyid + "/hamkari/" + $stateParams.jobID + "/job/" + item.id + "/").then(function (data) {
                $scope.jobItem = data.data;
                $scope.showModal(ev);
            })
        }

        $scope.AddNew = function (ev) {
            $scope.jobItem = {};
            $scope.showModal(ev)
        };


        $scope.delete = function (ev, item) {
            var confirm = $mdDialog.confirm()
                .title('حذف عنوان شغلی')
                .textContent('با حذف این عنوان شغلی متقاضیان همکاری در این شغل نیز غیر فعال خواهند شد')
                .ariaLabel('حذف عنوان شغلی')
                .targetEvent(ev)
                .ok('حذف شود')
                .cancel('انصراف');

            $mdDialog.show(confirm).then(function (result) {
                $http.delete("/api/v1/companies/" + $stateParams.companyid + "/hamkari/" + $stateParams.jobID + "/job/" + item.id + "/").then(function () {
                        $scope.list();
                })

            }, function () {
                $scope.status = 'You didn\'t name your dog.';
            });

        }

        $scope.publish = function (item) {
            item.publish = false;
            $http.patch("/api/v1/companies/" + $stateParams.companyid + "/hamkari/" + $stateParams.jobID + "/job/" + item.id + "/",
                {
                    publish: item.publish
                }).then(function (data) {
            })
        }
        $scope.unpublish = function (item) {
            item.publish = true;
            $http.patch("/api/v1/companies/" + $stateParams.companyid + "/hamkari/" + $stateParams.jobID + "/job/" + item.id + "/",
                {
                    publish: item.publish
                }).then(function (data) {
            })
        }

        $scope.showModal = function (ev) {
            jobItem = $scope.jobItem;
            $mdDialog.show({
                controller: DialogController,
                templateUrl: '/page/company/AddEditJobItems',
                parent: angular.element(document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
                jobItem: $scope.jobItem,
                fullscreen: $scope.customFullscreen // Only for -xs, -sm breakpoints.
            })
                .then(function (jobItem) {
                    if (jobItem.id) {
                        $http.patch("/api/v1/companies/" + $stateParams.companyid + "/hamkari/" + $stateParams.jobID + "/job/" + jobItem.id + "/", jobItem).then(function (data) {
                            $scope.list();
                        })

                    } else {
                        $http.post("/api/v1/companies/" + $stateParams.companyid + "/hamkari/" + $stateParams.jobID + "/job/", jobItem).then(function (data) {
                            $scope.list();
                        })
                    }


                }, function () {
                    $scope.status = 'You cancelled the dialog.';
                });
        };


        $scope.jobItem = {};
        $scope.jobItems = {};
        $scope.page = 1;

        $scope.list = function () {
            $http.get("/api/v1/companies/" + $stateParams.companyid + "/hamkari/" + $stateParams.jobID + "/job/?q="+$scope.jobItemsSearchText+"&page="+$scope.page.toString()+"&page_size=10").then(function (data) {
                $scope.jobItems = data.data;
                $scope.page = data.data.current_page;

            })
        }

        $scope.list();


    });
