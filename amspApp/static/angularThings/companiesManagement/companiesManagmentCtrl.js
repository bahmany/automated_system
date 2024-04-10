'use strict';


angular.module('AniTheme').controller(
    'companiesManagmentCtrl',
    function ($scope,
              $translate,
              $filter,
              $location,
              $$$,$state,
              $rootScope,
              $modal,
              companiesManagmentService) {

        $scope.Companies = [];
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
        $scope.PageTo = function (PagerAddress) {
            companiesManagmentService.GetCompaniesList(PagerAddress).then(
                function (data) {
                    $scope.Companies = data.data;
                }
            )
        };
        $scope.SelectedCompanyID = -1;
        $scope.Profile = [];
        $scope.Productions = [];
        $scope.GetCompaniesList = function () {
            $scope.pleasewait = true;

            companiesManagmentService.GetCompaniesList().then(
                function (data) {
                    $scope.pleasewait = false;
                    $scope.Companies = data.data;
                }
            )
        };
        $scope.CreateNewCompany = function () {
            //////console.log($translate.use("New Company"));
            swal(
                {
                    title: $$$("New Company"),
                    text: $$$("Enter your new company name"),
                    type: "input",
                    showCancelButton: true,
                    closeOnConfirm: false,
                    animation: "slide-from-top",
                    inputPlaceholder: $$$("Write something")
                },
                function (inputValue) {

                    if (inputValue === false)
                        return false;
                    if (inputValue === "") {
                        swal.showInputError("You need to write something!");
                        return false
                    }
                    companiesManagmentService.doInsert(inputValue).then(
                        function (data) {
                            $scope.GetCompaniesList();
                            swal(
                                $$$("Nice") + "!",
                                $$$("You wrote") + ": " + data.data.name,
                                "success");
                        }
                    ).catch(
                        function (err) {
                            swal.showInputError(err.data.name[0]);
                        }
                    )

                });
        };
        $scope.DeleteThisCompamy = function (product, index) {
            swal({
                title: "Are you sure?",
                text: "By deleting this product every thing about this will be gone for ever",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "Yes, delete it!",
                closeOnConfirm: false
            }, function () {
                companiesManagmentService.DeleteProduction($stateParams.companyid, product.id).then(function () {
                    $scope.Productions.results.splice(index, 1);
                    $scope.GetProductionsList($stateParams.companyid);
                    swal("Deleted!", "the product deleted.", "success");
                });

            });
        };
        $scope.GetCompaniesList();


        $scope.selectedCompany = {};

        $scope.GoToCompany = function (company) {
            $scope.selectedCompany = company;
            $state.go("profile", {companyid: company.id.toString()});
            // $location.url("/Company/"+company.id.toString()+"/Profile");
            return
        }

    });


