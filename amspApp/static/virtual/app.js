'use strict';


angular
    .module(
        'RahsoonApp',
        ['ngMaterial', 'ui.router',
            'ui.tree', 'ngDragDrop',
            'oc.lazyLoad', 'pascalprecht.translate',
            // 'ngSanitize',
            'ngFileUpload'])
    .config(function ($interpolateProvider, $httpProvider) {
        $interpolateProvider.startSymbol('//');
        $interpolateProvider.endSymbol('//');
        $httpProvider.defaults.timeout = 1;
        $httpProvider.defaults.xsrfCookieName = 'rahsoon-CSRF-TOKEN';
        $httpProvider.defaults.xsrfHeaderName = 'rahsoon-csrftoken';
    })
    .filter('to_trusted', ['$sce', function ($sce) {
        return function (text) {
            return $sce.trustAsHtml(text);
        };
    }])
    .config(['$mdIconProvider', function ($mdIconProvider) {
        $mdIconProvider
        //.iconSet('icons', '/static/images/open-iconic-master/sprite/open-iconic.min.svg', 14)
            .defaultFontSet('FontAwesome')
            .fontSet('fa', 'FontAwesome')
            .defaultIconSet('/static/images/open-iconic-master/sprite/open-iconic.min.svg', 14)
    }])
    .config(function ($translateProvider) {
        $translateProvider.useUrlLoader('/api/v1/language/');
        $translateProvider.preferredLanguage('fa');
        $translateProvider.useSanitizeValueStrategy('escape')
    })
    .factory('$$$', ['$filter', '$translate', function ($filter, $translate) {
        return function (text) {

            //console.log($translate.use());
            return $filter('translate')(text)
        }
    }])
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
    // .module('RahsoonApp').controller(
    // 'toolbarCtrl',
    // function ($scope,
    //           $translate,
    //           $q, $location,
    //           $http,
    //           $rootScope,
    //           $timeout) {
    //     $scope.getProfileLevel = function () {
    //         $http.get("/api/v1/users/GetProfileLevel/").then(function (data) {
    //             $scope.level = data;
    //         })
    //     };
    //     $scope.getProfileLevel();
    //
    //
    // })
    .config(function ($stateProvider, $urlRouterProvider) {

        //$urlRouterProvider.otherwise('/virtual');
        $urlRouterProvider.when('', '/home/introduction');
        $urlRouterProvider.otherwise('/home/introduction');
        $stateProvider
            .state('base', {
                abstract: true,
                url: '',
                templateUrl: '/reg/page/base/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/virtual/baseCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('login', {
                parent: 'base',
                url: '/login',
                templateUrl: '/reg/page/login/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/virtual/login/loginCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('forget', {
                parent: 'base',
                url: '/forget',
                templateUrl: '/reg/page/forget/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/virtual/login/forgetCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('reset', {
                parent: 'base',
                url: '/:uid/reset',
                templateUrl: '/reg/page/reset/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/virtual/login/resetCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('register', {
                parent: 'base',
                url: '/register',
                templateUrl: '/reg/page/register/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/virtual/login/regCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('goodsSupplay', {
                parent: 'base',
                url: '/goodsSupplay',
                templateUrl: '/reg/page/goodsSupplay/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/angularThings/share/file/classUploaderAPI.js',
                                '/static/virtual/goodsProviders/GoodsProvidersCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })

            .state('home', {
                parent: 'base',
                url: '/home',
                templateUrl: '/reg/page/home/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/virtual/homeCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('introduction', {
                parent: 'home',
                url: '/introduction',
                templateUrl: '/reg/page/introduction/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/virtual/profile/introductionCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })

            .state('hamkari', {
                parent: 'home',
                url: '/job/:hamkariID/list',
                templateUrl: '/reg/page/hamkariDetails/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/virtual/profile/hamkariDetailsCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })

            .state('profile', {
                parent: 'home',
                url: '/profile',
                templateUrl: '/reg/page/profile/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/virtual/profile/base.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('step1', {
                parent: 'profile',
                url: '/step1',
                templateUrl: '/reg/page/step1/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/virtual/profile/steps/stepClasses.js',
                                '/static/virtual/profile/steps/step1Ctrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('step2', {
                parent: 'profile',
                url: '/step2',
                templateUrl: '/reg/page/step2/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/virtual/profile/steps/stepClasses.js',
                                '/static/virtual/profile/steps/step2Ctrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('step3', {
                parent: 'profile',
                url: '/step3',
                templateUrl: '/reg/page/step3/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/virtual/profile/steps/stepClasses.js',
                                '/static/virtual/profile/steps/step3Ctrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('step4', {
                parent: 'profile',
                url: '/step4',
                templateUrl: '/reg/page/step4/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/virtual/profile/steps/stepClasses.js',
                                '/static/virtual/profile/steps/step4Ctrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('step5', {
                parent: 'profile',
                url: '/step5',
                templateUrl: '/reg/page/step5/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/virtual/profile/steps/stepClasses.js',
                                '/static/virtual/profile/steps/step5Ctrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('step6', {
                parent: 'profile',
                url: '/step6',
                templateUrl: '/reg/page/step6/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/virtual/profile/steps/stepClasses.js',
                                '/static/virtual/profile/steps/step6Ctrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('step7', {
                parent: 'profile',
                url: '/step7',
                templateUrl: '/reg/page/step7/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/virtual/profile/steps/stepClasses.js',
                                '/static/virtual/profile/steps/step7Ctrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('step8', {
                parent: 'profile',
                url: '/step8',
                templateUrl: '/reg/page/step8/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/virtual/profile/steps/stepClasses.js',
                                '/static/virtual/profile/steps/step8Ctrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('step9', {
                parent: 'profile',
                url: '/step9',
                templateUrl: '/reg/page/step9/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/virtual/profile/profilePrevCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('step10', {
                parent: 'profile',
                url: '/step10',
                templateUrl: '/reg/page/step10/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/virtual/profile/steps/step10jobsCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })
            .state('step11', {
                parent: 'profile',
                url: '/step11',
                templateUrl: '/reg/page/step11/',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'OCletter',
                            files: [
                                '/static/virtual/profile/steps/step11resultsCtrl.js'
                            ], catch: true
                        }).then(function () {
                        })
                    }]
                }
            })

    })


//-------------------------
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("rahsoon-csrftoken", getCookie('rahsoon-CSRF-TOKEN'));
        }
    }
});
var globalDicKeys = [];
var UnknowGlobalDicKeys = [];

function checkUknownDictionsy() {
    if (UnknowGlobalDicKeys.length != 0) {
        $.ajax({
            url: '/api/v1/translate',
            type: 'post',
            dataType: 'json',
            success: function (data) {
                setTimeout(checkUknownDictionsy, 90000)
            },
            data: {items: UnknowGlobalDicKeys.join("____")}
        })
    } else {
        setTimeout(checkUknownDictionsy, 3000)
    }
}

checkUknownDictionsy();


function downloadURL(url) {
    if ($('#idown').length) {
        $('#idown').attr('src', url);
    } else {
        $('<iframe>', {id: 'idown', src: url}).hide().appendTo('body');
    }
}