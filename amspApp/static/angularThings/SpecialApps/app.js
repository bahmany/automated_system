angular
    .module(
        'AniTheme',
        ['ngMaterial',
            'ui.router', 'ui.tree', 'ngDragDrop', 'ja.qr',
            'oc.lazyLoad', 'pascalprecht.translate', 'angularFileUpload',
            'ngSanitize', 'md.data.table', 'ngFileUpload',

            'ngCkeditor', 'ui.bootstrap', 'ui.utils']
    )
    .config(function ($interpolateProvider, $httpProvider) {
        $interpolateProvider.startSymbol('//');
        $interpolateProvider.endSymbol('//');
        $httpProvider.defaults.timeout = 1;
        $httpProvider.defaults.xsrfCookieName = 'rahsoon-CSRF-TOKEN';
        $httpProvider.defaults.xsrfHeaderName = 'rahsoon-csrftoken';
    })
    .config(['$mdIconProvider', function ($mdIconProvider) {
        $mdIconProvider
        //.iconSet('icons', '/static/images/open-iconic-master/sprite/open-iconic.min.svg', 14)
            .defaultFontSet('FontAwesome')
            .fontSet('fa', 'FontAwesome')
            .defaultIconSet('/static/images/open-iconic-master/sprite/open-iconic.min.svg', 14)
    }])
    .factory('$$$', ['$filter', '$translate', function ($filter, $translate) {
        return function (text) {

            //console.log($translate.use());
            return $filter('translate')(text)
        }
    }])


    .run(function ($rootScope, $state, $stateParams) {
        // $rootScope.$state = $state;
        // $rootScope.$stateParams = $stateParams;
        // $rootScope.$on("$stateChangeSuccess", function (event, toState, toParams, fromState, fromParams) {
        //     // to be used for back button //won't work when page is reloaded.
        //     debugger;
        //     $rootScope.previousState_name = fromState.name;
        //     $rootScope.previousState_params = fromParams;
        // });
        // //back button function called from back button's ng-click="back()"
        // $rootScope.back = function () {
        //     debugger;
        //     $state.go($rootScope.previousState_name, $rootScope.previousState_params);
        // };

        $rootScope.$on('$stateChangeSuccess', function (event, toState, toParams, fromState, fromParams) {
            console.log("root change success");
        })

        $rootScope.$on('$stateChangeStart', function (event, toState, toParams, fromState, fromParams, options) {
            console.log("root change start");
        })

        $rootScope.$on('$stateChangeError', function (event, toState, toParams, fromState, fromParams, error) {
            console.log("root change error");
        })
    })

    .directive("compareTo", function () {
        return {
            require: "ngModel",
            scope: {
                otherModelValue: "=compareTo"
            },
            link: function (scope, element, attributes, ngModel) {
                ngModel.$validators.compareTo = function (modelValue) {
                    return modelValue == scope.otherModelValue;
                };
                scope.$watch("otherModelValue", function () {
                    ngModel.$validate();
                });
            }
        };
    })

    .directive('validNumber', [function () {
        return {
            require: 'ngModel',
            link: function (scope, elem, attrs, ctrl) {
                if (!ctrl) return;
                var range = attrs.validNumber.split(',').map(Number);
                ctrl.$validators.validNumber = function (value) {
                    return value >= range[0] && value <= range[1];
                };
            }
        };
    }])


    .filter('jalaliDate', function () {
        return function (inputDate, format) {
            if (inputDate) {
                inputDate = new Date(inputDate);
                var date = moment(inputDate);
                //return date.fromNow()+" "+date.format(format);
                return date.format(format);
            }
        }
    })
    .filter('jalaliDateFromNow', function () {
        return function (inputDate, format) {
            if (inputDate) {
                inputDate = new Date(inputDate);
                var date = moment(inputDate);
                return date.fromNow();
                //return date.format(format);
            }
        }
    })
    .filter('to_trusted', ['$sce', function ($sce) {
        return function (text) {
            return $sce.trustAsHtml(text);
        };
    }])
    .config(function ($stateProvider, $urlRouterProvider) {

        //$urlRouterProvider.otherwise('/virtual');
        $urlRouterProvider.when('', '/home/');
        $urlRouterProvider.otherwise('/home/');

        $stateProvider
            .state('base', {
                abstract: true,
                url: '',
                templateUrl: '/SpecialApps/page/base/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/angularThings/SpecialApps/dashCtrl.js',
                                '/static/angularThings/SpecialApps/baseCtrl.js'

                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('home', {
                parent: 'base',
                url: '/home',
                templateUrl: '/SpecialApps/page/home/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/angularThings/SpecialApps/homeCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('dash', {
                parent: 'base',
                url: '/dash',
                templateUrl: '/SpecialApps/page/dash/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/angularThings/SpecialApps/dashCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })


            .state('Sales', {
                url: '/Sales',
                parent: 'home',
                templateUrl: '/page/sales/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        //////console.log("perparing to get scripts");
                        return $ocLazyLoad.load({
                            name: 'OCcontacs',
                            files: [
                                '/static/angularThings/sales/baseCtrl.js'
                            ],
                            catch: true
                        }).then(
                            function () {
                            }
                        )
                    }]
                }
            })
            .state('SalesTataabogh', {
                url: '/SalesTataabogh',
                parent: 'Sales',
                templateUrl: '/page/salesTataabogh/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        //////console.log("perparing to get scripts");
                        return $ocLazyLoad.load({
                            name: 'OCcontacs',
                            files: [
                                '/static/angularThings/sales/TataaboghCtrl.js'
                            ],
                            catch: true
                        }).then(
                            function () {
                            }
                        )
                    }]
                }
            })
            .state('SalesConversations', {
                url: '/SalesConversations',
                parent: 'Sales',
                templateUrl: '/page/salesConversations/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        //////console.log("perparing to get scripts");
                        return $ocLazyLoad.load({
                            name: 'OCcontacs',
                            files: [
                                '/static/angularThings/share/file/classUploaderAPI.js',
                                '/static/angularThings/sales/salesConversationCtrl.js'
                            ],
                            catch: true
                        }).then(
                            function () {
                            }
                        )
                    }]
                }
            })
            .state('SalesConv', {
                url: '/SalesConv',
                parent: 'Sales',
                templateUrl: '/page/salesConv/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        //////console.log("perparing to get scripts");
                        return $ocLazyLoad.load({
                            name: 'OCcontacs',
                            files: [
                                '/static/angularThings/share/file/classUploaderAPI.js',
                                '/static/angularThings/sales/ConvCtrl.js'
                            ],
                            catch: true
                        }).then(
                            function () {
                            }
                        )
                    }]
                }
            })
            .state('SalesMojoodi', {
                url: '/SalesMojoodi',
                parent: 'Sales',
                templateUrl: '/page/salesMojoodi/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        //////console.log("perparing to get scripts");
                        return $ocLazyLoad.load({
                            name: 'OCcontacs',
                            files: [
                                '/static/angularThings/share/file/classUploaderAPI.js',
                                '/static/angularThings/sales/SalesMojoodiCtrl.js'
                            ],
                            catch: true
                        }).then(
                            function () {
                            }
                        )
                    }]
                }
            })
            .state('SalesProfile', {
                url: '/SalesProfile',
                parent: 'Sales',
                templateUrl: '/page/SalesProfile/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        //////console.log("perparing to get scripts");
                        return $ocLazyLoad.load({
                            name: 'OCcontacs',
                            files: [
                                '/static/angularThings/share/file/classUploaderAPI.js',
                                '/static/angularThings/sales/SalesProfileCtrl.js'
                            ],
                            catch: true
                        }).then(
                            function () {


                            }
                        )
                    }]
                }
            })
            .state('HavalehForoosh', {
                url: '/HavalehForoosh',
                parent: 'Sales',
                templateUrl: '/page/HavalehForoosh/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        //////console.log("perparing to get scripts");
                        return $ocLazyLoad.load({
                            name: 'OCcontacs',
                            files: [
                                '/static/angularThings/sales/havalehForoosh/HavalehForooshCtrl.js'
                            ],
                            catch: true
                        }).then(
                            function () {
                            }
                        )
                    }]
                }
            })
            .state('HavalehForooshChange', {
                url: '/:ApproveID/:Step/HavalehForooshChange',
                parent: 'Sales',
                templateUrl: '/page/HavalehForooshChange/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        //////console.log("perparing to get scripts");
                        return $ocLazyLoad.load({
                            name: 'OCcontacs',
                            files: [
                                '/static/angularThings/sales/havalehForoosh/HavalehForooshChangeCtrl.js'
                            ],
                            catch: true
                        }).then(
                            function () {
                            }
                        )
                    }]
                }
            })
            .state('HavalehForooshDetails', {
                url: '/hf/:hfdid/details',
                parent: 'Sales',
                templateUrl: '/page/HavalehForooshDetails/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        //////console.log("perparing to get scripts");
                        return $ocLazyLoad.load({
                            name: 'OCcontacs',
                            files: [
                                '/static/angularThings/share/file/classUploaderAPI.js',
                                '/static/angularThings/sales/sign/signBodyCtrl.js',
                                '/static/angularThings/sales/havalehForoosh/HavalehForooshDetailsCtrl.js'
                            ],
                            catch: true
                        }).then(
                            function () {
                            }
                        )
                    }]
                }
            })
            .state('Khorooj', {
                url: '/Khorooj',
                parent: 'Sales',
                templateUrl: '/page/Khorooj/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        //////console.log("perparing to get scripts");
                        return $ocLazyLoad.load({
                            name: 'OCcontacs',
                            files: [
                                '/static/angularThings/share/file/classUploaderAPI.js',
                                '/static/angularThings/sales/khorooj/KhoroojCtrl.js'
                            ],
                            catch: true
                        }).then(
                            function () {
                            }
                        )
                    }]
                }
            })
            .state('KhoroojDetails', {
                url: '/kh/:khid/details',
                parent: 'Sales',
                templateUrl: '/page/KhoroojDetails/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        //////console.log("perparing to get scripts");
                        return $ocLazyLoad.load({
                            name: 'OCcontacs',
                            files: [
                                '/static/angularThings/sales/sign/signBodyCtrl.js',
                                '/static/angularThings/share/file/classUploaderAPI.js',
                                '/static/angularThings/sales/khorooj/KhoroojDetailsCtrl.js'
                            ],
                            catch: true
                        }).then(
                            function () {
                            }
                        )
                    }]
                }
            })
            .state('SalesProfileDetails', {
                url: '/:profileID/SalesProfileDetails',
                parent: 'Sales',
                templateUrl: '/page/SalesProfileDetails/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        //////console.log("perparing to get scripts");
                        return $ocLazyLoad.load({
                            name: 'OCcontacs',
                            files: [
                                '/static/angularThings/share/file/classUploaderAPI.js',
                                '/static/angularThings/sales/SalesProfileDetailsCtrl.js'
                            ],
                            catch: true
                        }).then(
                            function () {
                            }
                        )
                    }]
                }
            })
            .state('SalesProfilePhones', {
                url: '/SalesProfilePhones',
                parent: 'Sales',
                templateUrl: '/page/SalesProfilePhones/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        //////console.log("perparing to get scripts");
                        return $ocLazyLoad.load({
                            name: 'OCcontacs',
                            files: [
                                '/static/angularThings/sales/SalesProfilePhonesCtrl.js'
                            ],
                            catch: true
                        }).then(
                            function () {
                            }
                        )
                    }]
                }
            })
            .state('SalesConversationsItems', {
                url: '/:ConvID/SalesConversationsItems',
                parent: 'Sales',
                templateUrl: '/page/salesConversationsItems/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        //////console.log("perparing to get scripts");
                        return $ocLazyLoad.load({
                            name: 'OCcontacs',
                            files: [
                                '/static/angularThings/share/file/classUploaderAPI.js',
                                '/static/angularThings/share/autocomplete.js',
                                '/static/angularThings/sales/SalesConversationItemsCtrl.js'
                            ],
                            catch: true
                        }).then(
                            function () {
                            }
                        )
                    }]
                }
            })
            .state('SalesTamin', {
                url: '/SalesTamin',
                parent: 'Sales',
                templateUrl: '/page/salesTamin/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        //////console.log("perparing to get scripts");
                        return $ocLazyLoad.load({
                            name: 'OCcontacs',
                            files: [
                                '/static/angularThings/sales/tamin/TaminCtrl.js'
                            ],
                            catch: true
                        }).then(
                            function () {
                            }
                        )
                    }]
                }
            })
            .state('SalesTaminProjects', {
                url: '/SalesTaminProjects',
                parent: 'SalesTamin',
                templateUrl: '/page/SalesTaminProjects/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        //////console.log("perparing to get scripts");
                        return $ocLazyLoad.load({
                            name: 'OCcontacs',
                            files: [
                                '/static/angularThings/sales/tamin/taminProject/TaminProjectCtrl.js'
                            ],
                            catch: true
                        }).then(
                            function () {
                            }
                        )
                    }]
                }
            })
            .state('SalesTaminDetails', {
                url: '/SalesTaminDetails',
                parent: 'SalesTamin',
                templateUrl: '/page/SalesTaminDetails/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        //////console.log("perparing to get scripts");
                        return $ocLazyLoad.load({
                            name: 'OCcontacs',
                            files: [
                                '/static/angularThings/sales/tamin/Details/DetailsCtrl.js'
                            ],
                            catch: true
                        }).then(
                            function () {
                            }
                        )
                    }]
                }
            })
            .state('Karshenasi', {
                url: '/Karshenasi',
                parent: 'SalesTamin',
                templateUrl: '/page/Karshenasi/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        //////console.log("perparing to get scripts");
                        return $ocLazyLoad.load({
                            name: 'OCcontacs',
                            files: [
                                '/static/angularThings/sales/tamin/karshenasi/karshenasiCtrl.js'
                            ],
                            catch: true
                        }).then(
                            function () {
                            }
                        )
                    }]
                }
            })
            .state('KarshenasiTahili', {
                url: '/KarshenasiTahili',
                parent: 'SalesTamin',
                templateUrl: '/page/KarshenasiTahili/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        //console.log("perparing to get scripts");
                        return $ocLazyLoad.load({
                            name: 'OCcontacs',
                            files: [
                                '/static/angularThings/sales/tamin/karshenasi/TahlilKarshenasiCtrl.js'
                            ],
                            catch: true
                        }).then(
                            function () {
                            }
                        )
                    }]
                }
            })
            .state('TaminDakheliRegistered', {
                url: '/TaminDakheliRegistered',
                parent: 'SalesTamin',
                templateUrl: '/page/AdminTaminDakheli/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        //console.log("perparing to get scripts");
                        return $ocLazyLoad.load({
                            name: 'OCcontacs',
                            files: [
                                '/static/angularThings/share/file/classUploaderAPI.js',
                                '/static/angularThings/sales/tamin/registered/TaminDakheliRegisteredCtrl.js'
                            ],
                            catch: true
                        }).then(
                            function () {
                            }
                        )
                    }]
                }
            })
            .state('TaminDakheliRegisteredDetails', {
                url: '/:details/TaminDakheliRegisteredDetails/',
                parent: 'SalesTamin',
                templateUrl: '/page/AdminTaminDakheliDetails/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        //console.log("perparing to get scripts");
                        return $ocLazyLoad.load({
                            name: 'OCcontacs',
                            files: [
                                '/static/angularThings/share/file/classUploaderAPI.js',
                                '/static/angularThings/sales/tamin/registered/TaminDakheliRegisteredDetailsCtrl.js'
                            ],
                            catch: true
                        }).then(
                            function () {
                            }
                        )
                    }]
                }
            })
            .state('CustomerTahili', {
                url: '/CustomerTahili',
                parent: 'Sales',
                templateUrl: '/page/SalesCustomerTahili/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        //console.log("perparing to get scripts");
                        return $ocLazyLoad.load({
                            name: 'OCcontacs',
                            files: [
                                '/static/angularThings/sales/tamin/karshenasi/CustomerTahlilCtrl.js'
                            ],
                            catch: true
                        }).then(
                            function () {
                            }
                        )
                    }]
                }
            })
            .state('CustomerTahiliDetails', {
                url: '/:cusID/CustomerTahiliDetails',
                parent: 'Sales',
                templateUrl: '/page/SalesCustomerTahiliDetails/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        //console.log("perparing to get scripts");
                        return $ocLazyLoad.load({
                            name: 'OCcontacs',
                            files: [
                                '/static/angularThings/sales/tamin/karshenasi/CustomerTahlilDetailsCtrl.js'
                            ],
                            catch: true
                        }).then(
                            function () {
                            }
                        )
                    }]
                }
            })


        for (let i = 0; i < 27; i++) {
            $stateProvider.state('s' + i.toString(), {
                parent: 'TaminDakheliRegisteredDetails',
                url: '/s' + i.toString(),
                params: {formIndex: i},
                templateUrl: '/dashboards/page/supplyItems/' + i.toString() + "/",
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/angularThings/sales/tamin/registered/GoodsProvidersCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
        }


    })


window.onload = function () {
    var options =
        {
            imageBox: '.imageBox',
            thumbBox: '.thumbBox',
            spinner: '.spinner',
            imgSrc: 'avatar.png'
        }
    var cropper;


    if (document.querySelector('#file')) {
        document.querySelector('#file').addEventListener('change', function () {
            var reader = new FileReader();
            reader.onload = function (e) {
                options.imgSrc = e.target.result;
                cropper = new cropbox(options);
            }
            reader.readAsDataURL(this.files[0]);
            // this.files = [];
        })
    }

    if (document.querySelector('#btnCrop')) {
        document.querySelector('#btnCrop').addEventListener('click', function () {
            var img = cropper.getDataURL()
            document.querySelector('.cropped').innerHTML = '<img class="croppedAvt" src="' + img + '">';
        })

    }
    if (document.querySelector('#btnZoomIn')) {
        document.querySelector('#btnZoomIn').addEventListener('click', function () {
            cropper.zoomIn();
        })

    }
    if (document.querySelector('#btnZoomOut')) {
        document.querySelector('#btnZoomOut').addEventListener('click', function () {
            cropper.zoomOut();
        })
    }

};

var cropbox = function (options) {
    var el = document.querySelector(options.imageBox),
        obj =
            {
                state: {},
                ratio: 1,
                options: options,
                imageBox: el,
                thumbBox: el.querySelector(options.thumbBox),
                spinner: el.querySelector(options.spinner),
                image: new Image(),
                getDataURL: function () {
                    var width = this.thumbBox.clientWidth,
                        height = this.thumbBox.clientHeight,
                        canvas = document.createElement("canvas"),
                        dim = el.style.backgroundPosition.split(' '),
                        size = el.style.backgroundSize.split(' '),
                        dx = parseInt(dim[0]) - el.clientWidth / 2 + width / 2,
                        dy = parseInt(dim[1]) - el.clientHeight / 2 + height / 2,
                        dw = parseInt(size[0]),
                        dh = parseInt(size[1]),
                        sh = parseInt(this.image.height),
                        sw = parseInt(this.image.width);

                    canvas.width = width;
                    canvas.height = height;
                    var context = canvas.getContext("2d");
                    context.drawImage(this.image, 0, 0, sw, sh, dx, dy, dw, dh);
                    var imageData = canvas.toDataURL('image/png');
                    return imageData;
                },
                getBlob: function () {
                    var imageData = this.getDataURL();
                    var b64 = imageData.replace('data:image/png;base64,', '');
                    var binary = atob(b64);
                    var array = [];
                    for (var i = 0; i < binary.length; i++) {
                        array.push(binary.charCodeAt(i));
                    }
                    return new Blob([new Uint8Array(array)], {type: 'image/png'});
                },
                zoomIn: function () {
                    this.ratio *= 1.1;
                    setBackground();
                },
                zoomOut: function () {
                    this.ratio *= 0.9;
                    setBackground();
                }
            },
        attachEvent = function (node, event, cb) {
            if (node.attachEvent)
                node.attachEvent('on' + event, cb);
            else if (node.addEventListener)
                node.addEventListener(event, cb);
        },
        detachEvent = function (node, event, cb) {
            if (node.detachEvent) {
                node.detachEvent('on' + event, cb);
            } else if (node.removeEventListener) {
                node.removeEventListener(event, render);
            }
        },
        stopEvent = function (e) {
            if (window.event) e.cancelBubble = true;
            else e.stopImmediatePropagation();
        },
        setBackground = function () {
            var w = parseInt(obj.image.width) * obj.ratio;
            var h = parseInt(obj.image.height) * obj.ratio;

            var pw = (el.clientWidth - w) / 2;
            var ph = (el.clientHeight - h) / 2;

            el.setAttribute('style',
                'background-image: url(' + obj.image.src + '); ' +
                'background-size: ' + w + 'px ' + h + 'px; ' +
                'background-position: ' + pw + 'px ' + ph + 'px; ' +
                'background-repeat: no-repeat');
        },
        imgMouseDown = function (e) {
            stopEvent(e);

            obj.state.dragable = true;
            obj.state.mouseX = e.clientX;
            obj.state.mouseY = e.clientY;
        },
        imgMouseMove = function (e) {
            stopEvent(e);

            if (obj.state.dragable) {
                var x = e.clientX - obj.state.mouseX;
                var y = e.clientY - obj.state.mouseY;

                var bg = el.style.backgroundPosition.split(' ');

                var bgX = x + parseInt(bg[0]);
                var bgY = y + parseInt(bg[1]);

                el.style.backgroundPosition = bgX + 'px ' + bgY + 'px';

                obj.state.mouseX = e.clientX;
                obj.state.mouseY = e.clientY;
            }
        },
        imgMouseUp = function (e) {
            stopEvent(e);
            obj.state.dragable = false;
        },
        zoomImage = function (e) {
            var evt = window.event || e;
            var delta = evt.detail ? evt.detail * (-120) : evt.wheelDelta;
            delta > -120 ? obj.ratio *= 1.1 : obj.ratio *= 0.9;
            setBackground();
        }

    obj.spinner.style.display = 'block';
    obj.image.onload = function () {
        obj.spinner.style.display = 'none';
        setBackground();

        attachEvent(el, 'mousedown', imgMouseDown);
        attachEvent(el, 'mousemove', imgMouseMove);
        attachEvent(document.body, 'mouseup', imgMouseUp);
        var mousewheel = (/Firefox/i.test(navigator.userAgent)) ? 'DOMMouseScroll' : 'mousewheel';
        attachEvent(el, mousewheel, zoomImage);
    };
    obj.image.src = options.imgSrc;
    attachEvent(el, 'DOMNodeRemoved', function () {
        detachEvent(document.body, 'DOMNodeRemoved', imgMouseUp)
    });

    return obj;
};


function downloadURL(url) {
    if ($('#idown').length) {
        $('#idown').attr('src', url);
    } else {
        $('<iframe>', {id: 'idown', src: url}).hide().appendTo('body');
    }
}