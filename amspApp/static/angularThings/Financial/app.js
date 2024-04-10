'use strict';

var brandPrimary = '#20a8d8';
var brandSuccess = '#4dbd74';
var brandInfo = '#63c2de';
var brandWarning = '#f8cb00';
var brandDanger = '#f86c6b';

var grayDark = '#2a2c36';
var gray = '#55595c';
var grayLight = '#818a91';
var grayLighter = '#d1d4d7';
var grayLightest = '#f8f9fa';

angular
    .module(
        'AniTheme',
        [
            'ui.router',
            'oc.lazyLoad',
            'pascalprecht.translate',
            'ncy-angular-breadcrumb',
            'angular-loading-bar',
            'ngSanitize',
            'ngAnimate'
        ]
    )

    .config(['cfpLoadingBarProvider', function (cfpLoadingBarProvider) {
        cfpLoadingBarProvider.includeSpinner = false;
        cfpLoadingBarProvider.latencyThreshold = 1;
    }])
    .run(['$rootScope', '$state', '$stateParams', function ($rootScope, $state, $stateParams) {
        $rootScope.$on('$stateChangeSuccess', function () {
            document.body.scrollTop = document.documentElement.scrollTop = 0;
        });
        $rootScope.$state = $state;
        return $rootScope.$stateParams = $stateParams;
    }])

    .config(function ($interpolateProvider, $httpProvider) {
        $interpolateProvider.startSymbol('//');
        $interpolateProvider.endSymbol('//');
        $httpProvider.defaults.timeout = 1;
        $httpProvider.defaults.xsrfCookieName = 'rahsoon-CSRF-TOKEN';
        $httpProvider.defaults.xsrfHeaderName = 'rahsoon-csrftoken';
    })
    // .config(['$mdIconProvider', function ($mdIconProvider) {
    //     $mdIconProvider
    //     //.iconSet('icons', '/static/images/open-iconic-master/sprite/open-iconic.min.svg', 14)
    //         .defaultFontSet('FontAwesome')
    //         .fontSet('fa', 'FontAwesome')
    //         .defaultIconSet('/static/images/open-iconic-master/sprite/open-iconic.min.svg', 14)
    // }])
    // .factory('$$$', ['$filter', '$translate', function ($filter, $translate) {
    //     return function (text) {
    //
    //         //console.log($translate.use());
    //         return $filter('translate')(text)
    //     }
    // }])
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

    .directive("disableonrequest", function ($http) {
        return function (scope, element, attrs) {
            scope.$watch(function () {
                return $http.pendingRequests.length > 0;
            }, function (request) {
                if (!request) {
                    element.prop("disabled", false);
                    element.html("<span >" + attrs.notloading + "</span>");
                } else {
                    element.prop("disabled", true);
                    element.html("<span >" + attrs.loading + "</span><i class='fa fa-spinner fa-spin'></i>");
                }
            });
        }
    })

    .config(function (
        $stateProvider, $urlRouterProvider, $ocLazyLoadProvider, $breadcrumbProvider) {
        $ocLazyLoadProvider.config({debug: false});
        //$urlRouterProvider.otherwise('/virtual');
        $breadcrumbProvider.setOptions({
            prefixStateName: 'HeaderCtrl',
            includeAbstract: true,
            template: '<li class="breadcrumb-item" ng-repeat="step in steps" ng-class="{active: $last}" ng-switch="$last || !!step.abstract"><a ng-switch-when="false" href="{{step.ncyBreadcrumbLink}}">{{step.ncyBreadcrumbLabel}}</a><span ng-switch-when="true">{{step.ncyBreadcrumbLabel}}</span></li>'
        });
        $urlRouterProvider.when('', '/home/');
        $urlRouterProvider.otherwise('/home/');
        $stateProvider
            .state('base', {
                abstract: true,
                url: '',
                templateUrl: '/Financial/page/base/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Financial/dashCtrl.js',
                                '/static/Financial/baseCtrl.js'

                            ], catch: true
                        }).then(function () {
                        })
                    }]
                    ,
                    loadCSS: ['$ocLazyLoad', function ($ocLazyLoad) {
                        return $ocLazyLoad.load([{
                            serie: true,
                            name: 'Toastr',
                            files: ['/static/Financial/vendors/toastr.min.css']
                        }, {
                            serie: true,
                            name: 'DateRangePicker',
                            files: ['/static/Financial/vendors/daterangepicker.min.css']
                        }]);
                    }],
                    loadPlugin: ['$ocLazyLoad', function ($ocLazyLoad) {
                        return $ocLazyLoad.load([{
                            serie: true,
                            name: 'chart.js',
                            files: ['/static/Financial/vendors/Chart.min.js', '/static/Financial/vendors/angular-chart.min.js']
                        }, {
                            serie: true,
                            files: ['/static/Financial/vendors/daterangepicker.min.js', '/static/Financial/vendors/angular-daterangepicker.min.js']
                        }, {files: ['/static/Financial/vendors/angular-toastr.tpls.min.js']}]);
                    }]
                }
            })

            .state('home', {
                parent: 'base',
                url: '/home',
                templateUrl: '/Financial/page/home/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Financial/homeCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            // .state('dash', {
            //             //     parent: 'base',
            //             //     url: '/dash',
            //             //     templateUrl: '/Financial/page/dash/',
            //             //     resolve: {
            //             //         deps: ["$ocLazyLoad", function ($ocLazyLoad) {
            //             //             return $ocLazyLoad.load({
            //             //                 name: 'OCletter',
            //             //                 files: [
            //             //                     '/static/Financial/dashCtrl.js'
            //             //                 ], catch: true
            //             //             }).then(function () {
            //             //             })
            //             //         }]
            //             //     }
            //             // })
            .state('cog', {
                parent: 'home',
                url: '/cog',
                templateUrl: '/Financial/page/cog/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Financial/cog/cogCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('cog_home', {
                parent: 'cog',
                url: '/cog_home',
                templateUrl: '/Financial/page/cog_home/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Financial/cog/CogHomeCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('cog_m_avalieh', {
                parent: 'cog',
                url: '/rialiAvaleDoreh',
                templateUrl: '/Financial/page/cog_rialiAvaleDoreh/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Financial/cog/rialiAvaleDoreh/RialiAvaleDorehCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('cog_m_77', {
                parent: 'cog',
                url: '/rial77',
                templateUrl: '/Financial/page/cog_rial77/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Financial/cog/riali77/RialM77Ctrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })

            .state('cog_m_riali_sazi_77', {
                parent: 'cog',
                url: '/rialSazi77',
                templateUrl: '/Financial/page/cog_rialSazi77/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Financial/cog/rialiSazi77/RialSazi77Ctrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('cog_m_riali_sazi_77_ebtedaye_doreh', {
                parent: 'cog',
                url: '/rialSazi77EbtedayeDore',
                templateUrl: '/Financial/page/cog_rialSazi77_ebtedaye_doreh/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Financial/cog/rialiSazi77/RialSazi77EbtedayeDorehCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('cog_m_riali_sazi_88_ebtedaye_doreh', {
                parent: 'cog',
                url: '/rialSazi88EbtedayeDore',
                templateUrl: '/Financial/page/cog_rialSazi88_ebtedaye_doreh/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Financial/cog/riali88/RialSazi88EbtedayeDorehCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('cog_riali_sazi_ebtedaye_doreh_chaap', {
                parent: 'cog',
                url: '/rialSaziChaapEbtedayeDore',
                templateUrl: '/Financial/page/cog_MChaap/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Financial/cog/rialiChaap/RialSaziChaapEbtedayeDorehCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('cog_gardesh_chaap', {
                parent: 'cog',
                url: '/GardesheChaap',
                templateUrl: '/Financial/page/cog_GardesheChaap/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Financial/cog/rialiChaap/GardesheChaapCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })


            .state('cog_gardesh_ghooti_ebtedaye_doreh', {
                parent: 'cog',
                url: '/GardesheGhootiEbtedayeDoreh',
                templateUrl: '/Financial/page/cog_MGhootiEbtedayeDoreh/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Financial/cog/rialiGhooti/RialSaziGhootiEbtedayeDorehCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('cog_gardesh_ghooti', {
                parent: 'cog',
                url: '/GardesheGhooti',
                templateUrl: '/Financial/page/cog_GardesheGhooti/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Financial/cog/rialiGhooti/GardesheGhootiCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('cog_gardesh_asaan_baz_shoo_ebtedaye_doreh', {
                parent: 'cog',
                url: '/GardesheAsaanBaazShooEbtedayeDoreh',
                templateUrl: '/Financial/page/cog_MAsaanBazShooEbtedayeDoreh/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Financial/cog/rialiAsaanBazShoo/RialSaziAsaanBazShooEbtedayeDorehCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('cog_report', {
                parent: 'cog',
                url: '/CogReport',
                templateUrl: '/Financial/page/cog_report/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Financial/cog/reports/CogReportCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('cog_gardesh_asaan_baz_shoo', {
                parent: 'cog',
                url: '/GardesheAsaanBazShoo',
                templateUrl: '/Financial/page/cog_MAsaanBazShoo/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Financial/cog/rialiAsaanBazShoo/GardesheAsaanBazShooCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })

            .state('cog_m_gardeshe_77', {
                parent: 'cog',
                url: '/cog_Gardeshe77',
                templateUrl: '/Financial/page/cog_Gardeshe77/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Financial/cog/rialiSazi77/Gardeshe77Ctrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('cog_m_gardeshe_88', {
                parent: 'cog',
                url: '/cog_Gardeshe88',
                templateUrl: '/Financial/page/cog_rialSazi88/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Financial/cog/riali88/RialSazi88Ctrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })

            .state('cog_ca', {
                parent: 'cog',
                url: '/CA',
                templateUrl: '/Financial/page/cog_ca_base/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Financial/cog/ca/CaBaseCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('cog_ca_home', {
                parent: 'cog',
                url: '/CA',
                templateUrl: '/Financial/page/cog_ca_home/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Financial/cog/ca/CaHomeCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('cog_ca_automated_sums', {
                parent: 'cog',
                url: '/calc',
                templateUrl: '/Financial/page/cog_ca_automated_sum/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Financial/cog/ca/CaAutomatedSumsCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('cog_ca_categorize', {
                parent: 'cog',
                url: '/cats',
                templateUrl: '/Financial/page/cog_ca_categ/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Financial/cog/ca/AccCategoryCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('cog_ca_davayere_tolidi', {
                parent: 'cog',
                url: '/cog_ca_davayere_tolidi',
                templateUrl: '/Financial/page/cog_ca_davayere_tolidi/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Financial/cog/ca/CaToDavayereTolidiCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })


    });


var csrftoken = Cookies.get('rahsoon-CSRF-TOKEN');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("rahsoon-csrftoken", csrftoken);
        }
    }
});
