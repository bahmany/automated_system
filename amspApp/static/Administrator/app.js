'use strict';


angular
    .module(
    'RahsoonAdminApp',
    [
        'ui.router',
        'ui.tree',
        'oc.lazyLoad'

    ])
    .config(function ($interpolateProvider, $httpProvider) {
        $interpolateProvider.startSymbol('//');
        $interpolateProvider.endSymbol('//');
        $httpProvider.defaults.timeout = 1;
        $httpProvider.defaults.xsrfCookieName = 'rahsoon-CSRF-TOKEN';
        $httpProvider.defaults.xsrfHeaderName = 'rahsoon-csrftoken';
    })
    .config(function ($stateProvider, $urlRouterProvider) {
        $urlRouterProvider.when('', '/home');
        $urlRouterProvider.otherwise('/home');

        $stateProvider
            .state('base', {
                abstract: true,
                url: '',
                templateUrl: '/administrator/page/base/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Administrator/baseCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('home', {
                parent: 'base',
                url: '/home',
                templateUrl: '/administrator/page/home/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Administrator/homeCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })

            .state('customers', {
                parent: 'home',
                url: '/customers',
                templateUrl: '/administrator/page/customer/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Administrator/Customers/CustomerBaseCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })

            .state('customers-register', {
                parent: 'customers',
                url: '/register',
                templateUrl: '/administrator/page/customer/register/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Administrator/Customers/CustomerRegisterCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })

            .state('billing', {
                parent: 'home',
                url: '/billing',
                templateUrl: '/administrator/page/billing/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Administrator/Billing/BillingBaseCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('billing-register', {
                parent: 'billing',
                url: '/register',
                templateUrl: '/administrator/page/billing/register/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Administrator/Billing/NewBillingCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })

            .state('payment', {
                parent: 'home',
                url: '/payment',
                templateUrl: '/administrator/page/billing/payment/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Administrator/Billing/PaymentBaseCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })

            .state('payment-register', {
                parent: 'payment',
                url: '/register',
                templateUrl: '/administrator/page/billing/payment/register/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Administrator/Billing/PaymentCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })



            .state('languages', {
                parent: 'home',
                url: '/languages',
                templateUrl: '/administrator/page/languages/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Administrator/Languages/LanguagesBaseCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })

            .state('languages-register', {
                parent: 'languages',
                url: '/register',
                templateUrl: '/administrator/page/languages/register/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/Administrator/Languages/LanguagesCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })

    })


function showError(errorMsg) {
    var err = "";

    for (var key in errorMsg) {
        err = key + ": " + "<br>"
        for (var b in errorMsg[key]) {
            err = err + "   " + errorMsg[key][b] + "<br>";
        }
    }

    sweetAlert("Ooops", err, "error");
}

function showSucc(succMsg) {
    sweetAlert("با موفقیت", succMsg, "success");
}