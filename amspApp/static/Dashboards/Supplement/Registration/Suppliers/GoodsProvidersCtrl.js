'use strict';

angular.module('Supplement').controller(
    'GoodsProvidersCtrl',
    [
        '$scope',
        '$mdDialog',
        '$q',
        '$http',
        '$stateParams',
        '$mdToast',
        'FileUploader',
        '$rootScope',
        '$state',
        '$timeout', function ($scope, $mdDialog, $q, $http, $stateParams, $mdToast, FileUploader, $rootScope, $state, $timeout) {

        $scope.customFullscreen = false;


        $scope.showImageDialog = function (ev, images, stepNumber) {
            $mdDialog.show({
                locals: {
                    dataToSend: {
                        parentScope: $scope,
                        images: images
                    }
                },
                controller: imageUploaderCtrl,
                templateUrl: '/dashboards/page/imageDialog/',
                parent: angular.element(document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
                fullscreen: $scope.customFullscreen // Only for -xs, -sm breakpoints.
            })
                .then(function (answer) {
                    // debugger;
                    if (!($scope.provider)) {
                        $scope.provider = {};
                    }
                    if (!($scope.provider["frm" + stepNumber])) {
                        $scope.provider["frm" + stepNumber] = {};
                    }
                    $scope.provider["frm" + stepNumber]['files'] = $scope.uploadedFiles;
                    $scope.status = 'You said the information was "' + answer + '".';
                }, function () {
                    $scope.status = 'You cancelled the dialog.';
                });
        };
        $scope.uploadedFiles = [];


        function imageUploaderCtrl(
            $scope, FileUploader, $timeout, dataToSend, $mdDialog) {
            $scope.hide = function () {
                $mdDialog.hide();
            };
            $scope.cancel = function () {
                $mdDialog.cancel();
            };
            $scope.answer = function (answer) {
                $scope.uploadedFiles = dataToSend.parentScope.uploadedFiles;
                $mdDialog.hide(answer);
            };

            var uploader = $scope.uploader = new FileUploader({
                url: '/api/v1/file/upload'
            });
// FILTERS
            uploader.filters.push({
                name: 'customFilter',
                fn: function (item /*{File|FileLikeObject}*/, options) {
                    return this.queue.length < 10;
                }
            });


            uploader.onCompleteItem = function (fileItem, response, status, headers) {
                fileItem.serverAddress = response;
                if (!($scope.uploadedFiles)) {
                    $scope.uploadedFiles = [];
                }
                $scope.uploadedFiles.push(response);
                dataToSend.parentScope.uploadedFiles = $scope.uploadedFiles;
                console.info('onCompleteItem', fileItem, response, status, headers);
            };
            var controller = $scope.controller = {
                isImage: function (item) {
                    var type = '|' + item.type.slice(item.type.lastIndexOf('/') + 1) + '|';
                    return '|jpg|pdf|png|jpeg|bmp|gif|'.indexOf(type) !== -1;
                }
            };
        }

        $scope.showImageViewer = function (ev, files) {
            $mdDialog.show({
                locals: {
                    dataToSend: {
                        parentScope: $scope,
                        files: files
                    }
                },
                controller: imageViewUploaderCtrl,
                templateUrl: '/dashboards/page/imageViewDialog/',
                parent: angular.element(document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
                fullscreen: $scope.customFullscreen // Only for -xs, -sm breakpoints.
            })
                .then(function (answer) {

                }, function () {
                    $scope.status = 'You cancelled the dialog.';
                });
        }

        function imageViewUploaderCtrl(
            $scope, FileUploader, $timeout, dataToSend, $mdDialog) {
            $scope.imageToPrev = dataToSend.files;

            $scope.hide = function () {
                $mdDialog.hide();
            };
            $scope.cancel = function () {
                $mdDialog.cancel();
            };
            $scope.answer = function (answer) {
                $mdDialog.hide(answer);
            };

        }

        $scope.headerDet = {};
        $scope.Files = {};
        $scope.pages_order = [
            [1, 4, 7, 19, 21, 14, 16, 25, 26],
            [2, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 25, 26],
            [3, 5, 6, 7, 20, 12, 22, 23, 24, 15, 13, 18, 25, 26]
        ];
        $scope.menuTitles = [
            '',
            'اطلاعات فروشنده ',
            'اطلاعات خدماتی ها',
            'اطلاعات سازندگان',
            'اطلاعات تماس ',
            'اطلاعات تماس سازندگان',
            'اطلاعات هیات مدیره',
            'عضویت در لیست تامین کنندگان ',
            'حق امتیاز ، لیسانس یا نمایندگی ',
            'تعداد کارکنان در مقاطع تحصیلی',
            'مشخصات کارکنان کلیدی',
            'محصولات یا خدمات',
            'استاندارد ها',
            'سابقه قراردادهای قبلی',
            'حسن سابقه',
            'حسن سابقه',
            'سوالات مخصوص ',
            'سوالات مخصوص ',
            'سوالات مخصوص ',
            'زمینه فعالیت',
            'زمینه فعالیت',
            'سوابق کاری',
            'فهرست تجهیزات',
            'گواهینامه ها',
            'تضمین کیفیت',
            'آپلود فایل',
            'ثبت'
        ];
        $scope.menuTitlesExp = [
            '',
            'در این قسمت اطلاعاتی از قبل نام فروشنده ، نوع شرکت ، شماره ثبت سایر اطلاعات هویتی فروشنده وارد می شود',
            'اطلاعات خدماتی ها',
            'اطلاعات سازندگان',
            'در این قسمت اطلاعات مربوط به نحوه ی ارتباط با فروشنده یا تامین کننده خدمات قرار میگیرد مثل پست الکترونیکی ، شماره های تماس و ...',
            'اطلاعات تماس سازندگان',
            'اطلاعات هیات مدیره',
            '  عضویت در لیست تامین کنندگان سایر شرکت ها ',
            '  در صورت دارا بودن حق امتیاز ، لیسانس یا نمایندگی ',
            'تعداد کارکنان در مقاطع تحصیلی',
            '  لطفا مشخصات کارکنان کلیدی خود را وارد کنید ',
            'محصولات یا خدمات قابل ارائه',
            '  استاندارد های ****ی ،نظامنامه يا گواهی نامه های مديريت ',
            'سابقه قراردادهای قبلی طی ۳ سال گذشته',
            '  حسن سابقه در کارهای قبلی مخصوص خدماتی',
            '  حسن سابقه در کارهای قبلی مخصوص سازندگان',
            'سوالات مخصوص فروشندگان',
            'سوالات مخصوص خدماتی',
            'سوالات مخصوص سازندگان',
            '  زمینه فعالیت مخصوص فروشندگان',
            '  زمینه فعالیت مخصوص سازندگان',
            'سوابق کاری و حرفه ای',
            'فهرست ماشین الات ، تجهیزات و دستگاه ها با ارائه مستندات لازم',
            'گواهینامه های استاندارد محصولات',
            'تضمین کیفیت محصول و خدمات پس از فروش',
            'آپلود فایل',
            'ثبت'
        ];
        $scope.requireFields = {
            'provider.frm1.name': {"required": true, requireMsg: 'نام را خالی رها نکنید'},
            'provider.frm1.mellicode': {"required": true, requireMsg: 'کد ملی را خالی رها نکنید'},
            'provider.frm1.noeMalekiat': {"required": true, requireMsg: 'نوع مالکیت را خالی رها نکنید'},
            'provider.frm4.email': {},
            'provider.frm4.fax': {},
            'provider.frm4.address1': {},
            'provider.frm4.phone1': {},
            'provider.frm4.cell1': {},
            'provider.frm19.canSendNemooneh': {}
        };
        $scope.currentStep = 0;
        $scope.downloadFile = {};
        $scope.provider = {};
        $scope.getUerType = function () {
            $scope.stepNumber = $stateParams.formIndex;
            $http.get("/dashboards/api/v1/firstreg/getUserType/").then(function (data) {
                $scope.type = data.data.type;
            })
        };
        $scope.getUerType();


        $scope.save_next = function (ev) {
            var dtToSv = {};
            var confirm = $mdDialog.confirm()
                .title('سوال')
                .textContent('آیا اطمینان دارید تغییراتی که اعمال کرده اید رخیره شود ؟')
                .ariaLabel('')
                .targetEvent(ev)
                .ok('ذخیره شود')
                .cancel('تغییرات ذخیره نشود');
            $mdDialog.show(confirm).then(function () {
                    dtToSv.extra = $scope.provider;
                    dtToSv.extra.files = $scope.UploadedFiles;
                    angular.element(document.getElementById("divSaveStep")).text("در حال ذخیر").attr("disabled", true);
                    $http.post("/dashboards/api/v1/save_supply/", dtToSv).then(function (data) {
                        if (data.data.msg === "ok") {
                            // $scope.result = data.data;
                            $scope.showSaveToast();
                            $scope.getInstance();
                            angular.element(document.getElementById("divSaveStep")).text("ذخیره").attr("disabled", false);

                            // $scope.showSucc(ev);
                            // $scope.reset();
                            // angular.element(document.querySelector('#div_reg')).fadeOut(function () {
                            //     angular.element(document.querySelector('#div_result')).fadeIn()
                            // })

                        }
                    })

                }, function () {
                    // $scope.status = 'You decided to keep your debt.';
                    angular.element(document.getElementById("divSaveStep")).text("ذخیره").attr("disabled", false);
                }
            );


        };


        $scope.nextStep = function () {


            let cty = -1;
            if ($scope.type === 4) {
                cty = 0;
            }
            if ($scope.type === 5) {
                cty = 1;
            }
            if ($scope.type === 6) {
                cty = 2;
            }

            var dtToSv = {};
            dtToSv.extra = $scope.provider;
            dtToSv.extra.files = $scope.UploadedFiles;
            angular.element(document.getElementById("NextStep")).text("در حال ذخیر").attr("disabled", true);
            angular.element(document.getElementById("divNextStep")).text("در حال ذخیر").attr("disabled", true);
            $http.post("/dashboards/api/v1/save_supply/", dtToSv).then(function (data) {
                if (data.data.msg === "ok") {
                    // $scope.result = data.data;
                    $scope.showSaveToast();
                    $scope.getInstance();
                    angular.element(document.getElementById("NextStep")).text("ذخیره و بعدی").attr("disabled", false);
                    angular.element(document.getElementById("divNextStep")).text("ذخیره و قبلی").attr("disabled", false);
                    let steps = $scope.pages_order[cty];
                    let currentIndex = steps.indexOf($stateParams.formIndex);
                    let newIndex = steps.indexOf($stateParams.formIndex) + 1;
                    $state.go("s" + steps[newIndex].toString());
                }
            })


        }
        $scope.prevStep = function () {
            let cty = -1;
            if ($scope.type === 4) {
                cty = 0;
            }
            if ($scope.type === 5) {
                cty = 1;
            }
            if ($scope.type === 6) {
                cty = 2;
            }


            var dtToSv = {};
            dtToSv.extra = $scope.provider;
            dtToSv.extra.files = $scope.UploadedFiles;
            angular.element(document.getElementById("NextStep")).text("در حال ذخیر").attr("disabled", true);
            angular.element(document.getElementById("divNextStep")).text("در حال ذخیر").attr("disabled", true);
            $http.post("/dashboards/api/v1/save_supply/", dtToSv).then(function (data) {
                if (data.data.msg === "ok") {
                    // $scope.result = data.data;
                    $scope.showSaveToast();
                    $scope.getInstance();
                    angular.element(document.getElementById("NextStep")).text("ذخیره و بعدی").attr("disabled", false);
                    angular.element(document.getElementById("divNextStep")).text("ذخیره و قبلی").attr("disabled", false);
                    let steps = $scope.pages_order[cty];
                    let currentIndex = steps.indexOf($stateParams.formIndex);
                    let newIndex = steps.indexOf($stateParams.formIndex) - 1;
                    $state.go("s" + steps[newIndex].toString());
                }
            })


        }
        $scope.provider.type_of_provider = null;
        $scope.provider.frm6_list = [];
        $scope.provider.frm7_list = [];
        $scope.provider.frm8_list = [];
        $scope.provider.frm10_list = [];
        $scope.provider.frm11_list = [];
        $scope.provider.frm12_list = [];
        $scope.provider.frm13_list = [];
        $scope.provider.frm14_list = [];
        $scope.provider.frm15_list = [];
        $scope.provider.frm19_list = [];
        $scope.provider.frm20_list = [];
        $scope.provider.frm21_list = [];
        $scope.provider.frm22_list = [];
        $scope.provider.frm23_list = [];
        $scope.provider.frm24_list = [];
        $scope.provider.files = {};
        $scope.provider.frm6 = {};
        $scope.provider.frm7 = {};
        $scope.provider.frm8 = {};
        $scope.provider.frm10 = {};
        $scope.provider.frm11 = {};
        $scope.provider.frm12 = {};
        $scope.provider.frm13 = {};
        $scope.provider.frm14 = {};
        $scope.provider.frm15 = {};
        $scope.provider.frm19 = {};
        $scope.provider.frm20 = {};
        $scope.provider.frm21 = {};
        $scope.provider.frm22 = {};
        $scope.provider.frm23 = {};
        $scope.provider.frm24 = {};

        $scope.frms = [6, 7, 8, 10, 11, 12, 13, 14, 15, 19, 20, 21, 22, 23, 24];


        $scope.addTofrm = function (xx) {
            if ($scope.provider["frm" + xx + "_list"] === undefined) {
                $scope.provider["frm" + xx + "_list"] = [];
            }
            $scope.provider["frm" + xx + "_list"].push($scope.provider["frm" + xx]);
            $scope.provider["frm" + xx] = {};
        };
        $scope.removefrm = function (xx, index) {
            $scope.provider["frm" + xx + "_list"].splice(index, 1);
        }
        $scope.reset = function () {
            $scope.headerDet = {};
            $scope.Files = {};
            $scope.downloadFile = {};
            $scope.provider = {};

            $scope.provider.type_of_provider = null;

            $scope.provider.frm6_list = [];
            $scope.provider.frm7_list = [];
            $scope.provider.frm8_list = [];
            $scope.provider.frm10_list = [];
            $scope.provider.frm11_list = [];
            $scope.provider.frm12_list = [];
            $scope.provider.frm13_list = [];
            $scope.provider.frm14_list = [];
            $scope.provider.frm15_list = [];
            $scope.provider.frm19_list = [];
            $scope.provider.frm20_list = [];
            $scope.provider.frm21_list = [];
            $scope.provider.frm22_list = [];
            $scope.provider.frm23_list = [];
            $scope.provider.frm24_list = [];
            $scope.provider.files = {};

            $scope.provider.frm6 = {};
            $scope.provider.frm7 = {};
            $scope.provider.frm8 = {};
            $scope.provider.frm10 = {};
            $scope.provider.frm11 = {};
            $scope.provider.frm12 = {};
            $scope.provider.frm13 = {};
            $scope.provider.frm14 = {};
            $scope.provider.frm15 = {};
            $scope.provider.frm19 = {};
            $scope.provider.frm20 = {};
            $scope.provider.frm21 = {};
            $scope.provider.frm22 = {};
            $scope.provider.frm23 = {};
            $scope.provider.frm24 = {};
        };
        $scope.openZamineh = function (ev) {
            $scope.showAdvanced(ev);
        }
        $scope.showAdvanced = function (ev) {
            $mdDialog.show({
                controller: DialogController,
                templateUrl: '/dashboards/page/OpenCateg/',
                parent: angular.element(document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
                fullscreen: false // Only for -xs, -sm breakpoints.
            })
                .then(function (answer) {

                    // $scope.provider
                    // debugger;
                    $scope.provider["frm" + $scope.stepNumber.toString()]['zamineh_faaliat'] = answer;
                    // $scope.status = 'You said the information was "' + answer + '".';
                }, function () {
                    $scope.status = 'You cancelled the dialog.';
                });
        };

        function DialogController($scope, $mdDialog, $http) {


            $scope.hide = function () {
                $mdDialog.hide();
            };

            $scope.cancel = function () {
                $mdDialog.cancel();
            };

            $scope.answer = function (answer) {
                $mdDialog.hide(answer);
            };

            $scope.cats = [];

            $scope.getlistOf = function () {
                $http.get("/dashboards/api/v1/firstreg/getCats/").then(function (data) {
                    $scope.cats = data.data;
                })
            }

            $scope.selectIt = function (item) {
                $mdDialog.hide(item);

            }

            $scope.getlistOf();


        }

// -------------------------------------------------------------------------------------
// -------------------------------------------------------------------------------------
// -------------------------------------------------------------------------------------
// -------------------------------------------------------------------------------------
// -------------------------------------------------------------------------------------
        var last = {
            bottom: false,
            top: true,
            left: false,
            right: true
        };
        $scope.toastPosition = angular.extend({}, last);
        $scope.getToastPosition = function () {
            sanitizePosition();
            return Object.keys($scope.toastPosition)
                .filter(function (pos) {
                    return $scope.toastPosition[pos];
                })
                .join(' ');
        };

        function sanitizePosition() {
            var current = $scope.toastPosition;
            if (current.bottom && last.top) current.top = false;
            if (current.top && last.bottom) current.bottom = false;
            if (current.right && last.left) current.left = false;
            if (current.left && last.right) current.right = false;
            last = angular.extend({}, current);
        }

        $scope.showSaveToast = function () {
            var pinTo = $scope.getToastPosition();
            $mdToast.show(
                $mdToast.simple()
                    .textContent('ذخیره شد')
                    .position(pinTo)
                    .hideDelay(3000)
            );
        };
// -------------------------------------------------------------------------------------
// -------------------------------------------------------------------------------------
// -------------------------------------------------------------------------------------
// -------------------------------------------------------------------------------------
// -------------------------------------------------------------------------------------


        $scope.step1_invalid = false;
        $scope.step2_invalid = false;
        $scope.step8_invalid = false;

        $scope.beforeSave = {};
        $scope.getInstance = function () {
            $scope.reset();
            $http.get("/dashboards/api/v1/get_supply/").then(function (data) {
                $scope.provider = data.data["extra"];
                if (!($scope.provider)) {
                    $scope.provider = {};
                }
                angular.copy($scope.provider, $scope.beforeSave, 5);
                $scope.applyWatcher();
            })
        };
        $scope.getInstance();
        $scope.errmsg = [];


        $scope.getOzviatCode = function (ev) {
            $http.get("/dashboards/api/v1/get_ozviat_code/").then(function (data) {
            });
        }

        $scope.hasDiffer = false;


        // $scope.provider = {};
        $scope.applyWatcher = function () {
            for (let i = 0; i < 40; i++) {
                if (!($scope.provider["frm" + i.toString() + "_list"])) {
                    $scope.provider["frm" + i.toString() + "_list"] = [];
                }
                if ($scope.provider["frm" + i.toString() + "_list"]) {
                    $scope.$watchCollection("provider.frm" + i.toString() + "_list", function () {
                        console.log($scope.provider["frm" + i.toString() + "_list"]);
                        $scope.hasDiffer = !(angular.equals($scope.provider, $scope.beforeSave));
                    });
                }
                if (!($scope.provider["frm" + i.toString()])) {
                    $scope.provider["frm" + i.toString()] = {};
                }

                if ($scope.provider["frm" + i.toString()]) {
                    $scope.$watchCollection("provider.frm" + i.toString(), function () {
                        console.log($scope.provider["frm" + i.toString()]);
                        $scope.hasDiffer = !(angular.equals($scope.provider, $scope.beforeSave));
                    });
                }
            }
        };

        $scope.$watch("hasDiffer", function () {
            if ($scope.hasDiffer) {
                $rootScope.$broadcast("changeLeftSlider", {action: "start"});
            } else {
                $rootScope.$broadcast("changeLeftSlider", {action: "end"});
            }

        });

        $scope.$watch("files_parvanehKast.length", function (newVal, oldVal) {
            console.log($scope.files_parvanehKast);
        });


        // ------------------------------------------------------------------------------------
        // ------------------------------------------------------------------------------------
        // ------------------------------------------------------------------------------------
        // ------------------------------------------------------------------------------------
        // ------------------------------------------------------------------------------------
        // ------------------------------------------------------------------------------------
        // ------------------------------------------------------------------------------------
        // ------------------------------------------------------------------------------------
        // ------------------------------------------------------------------------------------
        // ------------------------------------------------------------------------------------

        var uploaderDict = {
            name: 'customFilter',
            fn: function (item /*{File|FileLikeObject}*/, options) {
                return this.queue.length < 10;
            }
        };
        var uploaderUrl = {url: '/api/v1/file/upload'};
        var uploader1 = $scope.uploader1 = new FileUploader(uploaderUrl);
        var uploader2 = $scope.uploader2 = new FileUploader(uploaderUrl);
        var uploader3 = $scope.uploader3 = new FileUploader(uploaderUrl);
        var uploader4 = $scope.uploader4 = new FileUploader(uploaderUrl);
        var uploader5 = $scope.uploader5 = new FileUploader(uploaderUrl);
        var uploader6 = $scope.uploader6 = new FileUploader(uploaderUrl);
        var uploader7 = $scope.uploader7 = new FileUploader(uploaderUrl);
        uploader1.filters.push(uploaderDict);
        uploader2.filters.push(uploaderDict);
        uploader3.filters.push(uploaderDict);
        uploader4.filters.push(uploaderDict);
        uploader5.filters.push(uploaderDict);
        uploader6.filters.push(uploaderDict);
        uploader7.filters.push(uploaderDict);
        $scope["provider"]["frm" + $stateParams.formIndex] = {};
        $scope["provider"]["frm" + $stateParams.formIndex].files1 = [];
        $scope["provider"]["frm" + $stateParams.formIndex].files2 = [];
        $scope["provider"]["frm" + $stateParams.formIndex].files3 = [];
        $scope["provider"]["frm" + $stateParams.formIndex].files4 = [];
        $scope["provider"]["frm" + $stateParams.formIndex].files5 = [];
        $scope["provider"]["frm" + $stateParams.formIndex].files6 = [];
        $scope["provider"]["frm" + $stateParams.formIndex].files7 = [];

        function addToImg(filename) {
            return {
                file: filename.file
            }
        }

        var upload_func1 = function (fileItem) {
            $rootScope.$broadcast("fileUploading", {"action": "start"});
            uploader1.uploadAll();
        };
        var upload_func2 = function (fileItem) {
            $rootScope.$broadcast("fileUploading", {"action": "start"});
            uploader2.uploadAll();
        };
        var upload_func3 = function (fileItem) {
            $rootScope.$broadcast("fileUploading", {"action": "start"});
            uploader3.uploadAll();
        };
        var upload_func4 = function (fileItem) {
            $rootScope.$broadcast("fileUploading", {"action": "start"});
            uploader4.uploadAll();
        };
        var upload_func5 = function (fileItem) {
            $rootScope.$broadcast("fileUploading", {"action": "start"});
            uploader5.uploadAll();
        };
        var upload_func6 = function (fileItem) {
            $rootScope.$broadcast("fileUploading", {"action": "start"});
            uploader6.uploadAll();
        };
        var upload_func7 = function (fileItem) {
            $rootScope.$broadcast("fileUploading", {"action": "start"});
            uploader7.uploadAll();
        };

        function init() {
            if (!($scope["provider"]["frm" + $stateParams.formIndex])) {
                $scope["provider"]["frm" + $stateParams.formIndex] = {};
            }
        }

        function addAfterCompl(fileNumber, fileItem, response) {
            init();
            if (!($scope["provider"]["frm" + $stateParams.formIndex]["files" + fileNumber])) {
                $scope["provider"]["frm" + $stateParams.formIndex]["files" + fileNumber] = [];
            }
            $scope["provider"]["frm" + $stateParams.formIndex]["files" + fileNumber].push({
                file: fileItem.file,
                encoded: response.name
            });
            $rootScope.$broadcast("fileUploading", {"action": "end"});

        }

        var upload_comp_1 = function (fileItem, response, status, headers) {
            addAfterCompl("1", fileItem, response)
        };
        var upload_comp_2 = function (fileItem, response, status, headers) {
            addAfterCompl("2", fileItem, response)
        };
        var upload_comp_3 = function (fileItem, response, status, headers) {
            addAfterCompl("3", fileItem, response)

        };
        var upload_comp_4 = function (fileItem, response, status, headers) {
            addAfterCompl("4", fileItem, response)
        };
        var upload_comp_5 = function (fileItem, response, status, headers) {
            addAfterCompl("5", fileItem, response)
        };
        var upload_comp_6 = function (fileItem, response, status, headers) {
            addAfterCompl("6", fileItem, response)
        };
        var upload_comp_7 = function (fileItem, response, status, headers) {
            addAfterCompl("7", fileItem, response)
        };

        uploader1.onAfterAddingFile = upload_func1;
        uploader2.onAfterAddingFile = upload_func2;
        uploader3.onAfterAddingFile = upload_func3;
        uploader4.onAfterAddingFile = upload_func4;
        uploader5.onAfterAddingFile = upload_func5;
        uploader6.onAfterAddingFile = upload_func6;
        uploader7.onAfterAddingFile = upload_func7;

        uploader1.onCompleteItem = upload_comp_1;
        uploader2.onCompleteItem = upload_comp_2;
        uploader3.onCompleteItem = upload_comp_3;
        uploader4.onCompleteItem = upload_comp_4;
        uploader5.onCompleteItem = upload_comp_5;
        uploader6.onCompleteItem = upload_comp_6;
        uploader7.onCompleteItem = upload_comp_7;

        $scope.uploadDoc = function (ev, inputID, formID) {
            // $scope.provider['frm'+formID]['file'+inputID]
            document.getElementById("fileUploader_" + inputID).click();
        }

        $scope.removeFile = function (formID, inputID, fileID) {
            if (confirm("آیا از حذف عکس مورد نظر اطمینان دارید ؟")) {
                $scope["provider"]["frm" + $stateParams.formIndex]['files' + inputID].splice(fileID, 1);
            }
        }
        // ------------------------------------------------------------------------------------
        // ------------------------------------------------------------------------------------
        // ------------------------------------------------------------------------------------
        // ------------------------------------------------------------------------------------
        // ------------------------------------------------------------------------------------
        // ------------------------------------------------------------------------------------
        // ------------------------------------------------------------------------------------
        // ------------------------------------------------------------------------------------


    }]);