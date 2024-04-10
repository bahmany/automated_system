angular
    .module(
        'Supplement',
        ['ngMaterial', 'oc.lazyLoad', 'ui.router', 'ngMdIcons', 'angularFileUpload','ui.mask'

            // 'pascalprecht.translate',
            // 'ngSanitize',
            // 'ngFileUpload',
            // 'ui.utils'

        ]
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
    .config(['$httpProvider', function ($httpProvider) {
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    }])

    .directive('ngThumb', ['$window', function ($window) {
        var helper = {
            support: !!($window.FileReader && $window.CanvasRenderingContext2D),
            isFile: function (item) {
                return angular.isObject(item) && item instanceof $window.File;
            },
            isImage: function (file) {
                var type = '|' + file.type.slice(file.type.lastIndexOf('/') + 1) + '|';
                return '|jpg|png|jpeg|bmp|gif|'.indexOf(type) !== -1;
            }
        };

        return {
            restrict: 'A',
            template: '<canvas/>',
            link: function (scope, element, attributes) {
                if (!helper.support) return;

                var params = scope.$eval(attributes.ngThumb);

                if (!helper.isFile(params.file)) return;
                if (!helper.isImage(params.file)) return;

                var canvas = element.find('canvas');
                var reader = new FileReader();

                reader.onload = onLoadFile;
                reader.readAsDataURL(params.file);

                function onLoadFile(event) {
                    var img = new Image();
                    img.onload = onLoadImage;
                    img.src = event.target.result;
                }

                function onLoadImage() {
                    var width = params.width || this.width / this.height * params.height;
                    var height = params.height || this.height / this.width * params.width;
                    canvas.attr({width: width, height: height});
                    canvas[0].getContext('2d').drawImage(this, 0, 0, width, height);
                }
            }
        };
    }])


    // .directive("compareTo", function () {
    //     return {
    //         require: "ngModel",
    //         scope: {
    //             otherModelValue: "=compareTo"
    //         },
    //         link: function (scope, element, attributes, ngModel) {
    //             ngModel.$validators.compareTo = function (modelValue) {
    //                 return modelValue == scope.otherModelValue;
    //             };
    //             scope.$watch("otherModelValue", function () {
    //                 ngModel.$validate();
    //             });
    //         }
    //     };
    // })
    // .filter('jalaliDate', function () {
    //     return function (inputDate, format) {
    //         if (inputDate) {
    //             inputDate = new Date(inputDate);
    //             var date = moment(inputDate);
    //             //return date.fromNow()+" "+date.format(format);
    //             return date.format(format);
    //         }
    //     }
    // })
    // .filter('jalaliDateFromNow', function () {
    //     return function (inputDate, format) {
    //         if (inputDate) {
    //             inputDate = new Date(inputDate);
    //             var date = moment(inputDate);
    //             return date.fromNow();
    //             //return date.format(format);
    //         }
    //     }
    // })
    .filter('to_trusted', ['$sce', function ($sce) {
        return function (text) {
            return $sce.trustAsHtml(text);
        };
    }])


    .config(function ($stateProvider, $urlRouterProvider) {

        //$urlRouterProvider.otherwise('/virtual');
        $urlRouterProvider.when('', '/home');
        $urlRouterProvider.otherwise('/home');
        $stateProvider
            .state('base', {
                abstract: true,
                url: '',
                templateUrl: '/dashboards/page/base/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Dashboards/Supplement/baseCtrl.js'

                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('home', {
                parent: 'base',
                url: '/home',
                templateUrl: '/dashboards/page/home/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Dashboards/Supplement/homeCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('profile', {
                parent: 'base',
                url: '/profile',
                templateUrl: '/dashboards/page/profile/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Dashboards/Supplement/Registration/Profile/profileCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('login', {
                parent: 'base',
                url: '/login',
                templateUrl: '/dashboards/page/login/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Dashboards/Supplement/Login/LoginCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('firstReg', {
                parent: 'base',
                url: '/firstReg',
                templateUrl: '/dashboards/page/firstreg/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Dashboards/Supplement/Registration/First/FirstRegCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('secondReg', {
                parent: 'base',
                url: '/secondReg',
                templateUrl: '/dashboards/page/secondreg/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Dashboards/Supplement/Registration/Second/SecondRegistrationStepCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('forgetPass', {
                parent: 'base',
                url: '/forgetPass',
                templateUrl: '/dashboards/page/forgetPass/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Dashboards/Supplement/Registration/Forget/ForgetPassCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('supply', {
                parent: 'base',
                url: '/supply',
                templateUrl: '/dashboards/page/baseSupply/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Dashboards/Supplement/Registration/Suppliers/baseSupplyCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            });


        for (let i = 0; i < 27; i++) {
            $stateProvider.state('s' + i.toString(), {
                parent: 'supply',
                url: '/s' + i.toString(),
                params: {formIndex:i},
                templateUrl: '/dashboards/page/supplyItems/' + i.toString() + "/",
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Dashboards/Supplement/Registration/Suppliers/GoodsProvidersCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
        }


    });




