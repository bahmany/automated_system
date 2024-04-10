'use strict';


app.filter('to_trusted', ['$sce', function ($sce) {
    return function (text) {
        return $sce.trustAsHtml(text);
    };
}])
    .config(function ($interpolateProvider, $httpProvider) {
        $interpolateProvider.startSymbol('//');
        $interpolateProvider.endSymbol('//');
        $httpProvider.defaults.timeout = 1;
        $httpProvider.defaults.xsrfCookieName = 'rahsoon-CSRF-TOKEN';
        $httpProvider.defaults.xsrfHeaderName = 'rahsoon-csrftoken';
    })
    .config(['$httpProvider', function ($httpProvider) {
        $httpProvider.interceptors.push(function ($q, $rootScope) {
            if ($rootScope.activeCalls == undefined) {
                $rootScope.activeCalls = 0;
            }

            if ($rootScope.notifyIsInProgress) {
                if ($rootScope.notifyIsInProgress == true) {
                }
            }

            return {
                request: function (config) {
                    if ((config.url.indexOf("happen") < 0)) {
                        $rootScope.activeCalls += 1;
                    }
                    //////console.log("start");
                    if ($rootScope.activeCalls < 0) {
                        $rootScope.activeCalls = 0
                    }
                    return config;
                },
                requestError: function (rejection) {
                    $rootScope.activeCalls -= 1;
                    //////console.log("end");
                    if ($rootScope.activeCalls < 0) {
                        $rootScope.activeCalls = 0
                    }
                    return rejection;
                },
                response: function (response) {
                    $rootScope.activeCalls -= 1;
                    //////console.log("end");
                    if ($rootScope.activeCalls < 0) {
                        $rootScope.activeCalls = 0
                    }
                    return response;
                },
                responseError: function (rejection) {
                    $rootScope.activeCalls -= 1;
                    //////console.log("end");
                    if ($rootScope.activeCalls < 0) {
                        $rootScope.activeCalls = 0
                    }
                    return rejection;
                }
            };
        });
    }])
    .config(['$mdIconProvider', function ($mdIconProvider) {
        $mdIconProvider
            .defaultFontSet('FontAwesome')
            .fontSet('fa', 'FontAwesome')
            .defaultIconSet('/static/images/open-iconic-master/sprite/open-iconic.min.svg', 14)
    }])
    .config(function ($translateProvider) {
        $translateProvider.useUrlLoader('/api/v1/language/');

        $translateProvider.preferredLanguage('fa');
        // Enable escaping of HTML
        $translateProvider.useSanitizeValueStrategy('escape')
    })
    .config(function ($mdThemingProvider) {
        $mdThemingProvider.definePalette('mcgpalette0', {
            '50': '#f4fcfd',
            '100': '#b2e8f2',
            '200': '#82d9ea',
            '300': '#45c7e0',
            '400': '#2bbfdc',
            '500': '#21acc7',
            '600': '#1d95ad',
            '700': '#187f93',
            '800': '#146878',
            '900': '#10515e',
            'A100': '#f4fcfd',
            'A200': '#b2e8f2',
            'A400': '#2bbfdc',
            'A700': '#187f93',
            'contrastDefaultColor': 'light',
            'contrastDarkColors': '50 100 200 300 400 500 A100 A200 A400'
        });
        $mdThemingProvider.definePalette('mcgpalette1', {
            '50': '#f8fcfc',
            '100': '#c1e6e4',
            '200': '#99d6d2',
            '300': '#66c2bc',
            '400': '#50b9b2',
            '500': '#43a8a1',
            '600': '#3a928c',
            '700': '#327c77',
            '800': '#296662',
            '900': '#20504d',
            'A100': '#f8fcfc',
            'A200': '#c1e6e4',
            'A400': '#50b9b2',
            'A700': '#327c77',
            'contrastDefaultColor': 'light',
            'contrastDarkColors': '50 100 200 300 400 500 A100 A200 A400'
        });
        $mdThemingProvider.definePalette('mcgpalette2', {
            '50': '#f7f8f2',
            '100': '#d9dec0',
            '200': '#c3ca9b',
            '300': '#a7b16d',
            '400': '#9ba759',
            '500': '#89934e',
            '600': '#767f43',
            '700': '#646b39',
            '800': '#51572e',
            '900': '#3e4324',
            'A100': '#f7f8f2',
            'A200': '#d9dec0',
            'A400': '#9ba759',
            'A700': '#646b39',
            'contrastDefaultColor': 'light',
            'contrastDarkColors': '50 100 200 300 400 500 A100 A200 A400'
        });
        $mdThemingProvider.definePalette('mcgpalette3', {
            '50': '#fffdfb',
            '100': '#fbd2b3',
            '200': '#f8b37e',
            '300': '#f48b3a',
            '400': '#f27a1d',
            '500': '#e46b0d',
            '600': '#c75d0b',
            '700': '#aa500a',
            '800': '#8d4208',
            '900': '#703506',
            'A100': '#fffdfb',
            'A200': '#fbd2b3',
            'A400': '#f27a1d',
            'A700': '#aa500a',
            'contrastDefaultColor': 'light',
            'contrastDarkColors': '50 100 200 300 400 500 A100 A200 A400'
        });
        $mdThemingProvider.definePalette('mcgpalette4', {
            '50': '#fff3ea',
            '100': '#ffc79e',
            '200': '#ffa666',
            '300': '#ff7d1e',
            '400': '#ff6b00',
            '500': '#e05e00',
            '600': '#c15100',
            '700': '#a34400',
            '800': '#843700',
            '900': '#662b00',
            'A100': '#fff3ea',
            'A200': '#ffc79e',
            'A400': '#ff6b00',
            'A700': '#a34400',
            'contrastDefaultColor': 'light',
            'contrastDarkColors': '50 100 200 300 400 A100 A200 A400'
        });
        $mdThemingProvider
            .theme('default')
            .primaryPalette('blue')
            .accentPalette('teal')
            .warnPalette('red')
            .backgroundPalette('grey');


    })

    // .config(function ($provide) {
    //     $provide.decorator('taOptions', ['taRegisterTool', '$delegate', '$modal', function (taRegisterTool, taOptions, $modal) {
    //         taRegisterTool('uploadImage', {
    //             buttontext: 'Upload Image',
    //             iconclass: "fa fa-image",
    //             action: function (deferred, restoreSelection) {
    //                 $modal.open({
    //                     controller: 'UploadImageModalInstance',
    //                     templateUrl: 'page/generic/upload.html'
    //                 }).result.then(
    //                     function (result) {
    //                         restoreSelection();
    //                         document.execCommand('insertImage', true, result);
    //                         deferred.resolve();
    //                     },
    //                     function () {
    //                         deferred.resolve();
    //                     }
    //                 );
    //                 return false;
    //             }
    //         });
    //         taOptions.toolbar[1].push('uploadImage');
    //         return taOptions;
    //     }]);
    // })




    .run(function ($rootScope, ngProgressFactory) {
        $rootScope.progressbar = ngProgressFactory.createInstance();

        $rootScope.$on('$locationChangeStart', function (e, toState, toParams, fromState, fromParams) {
            $(".md-sidenav-backdrop").click();
            $rootScope.progressbar.start();
            $rootScope.$broadcast("DetectUrlChange", e, toState, toParams, fromState, fromParams);
        });
        $rootScope
            .$on('$locationChangeSuccess',
                function (event, toState, toParams, fromState, fromParams) {
                    $rootScope.progressbar.complete();
                });
    })
    .factory('shareService', function () {
        var savedData = {};

        function set(data) {
            savedData = data;
        }

        function get() {
            return savedData;
        }

        return {
            set: set,
            get: get
        }
    })
    .factory('debounce', function ($timeout) {
        return function (callback, interval) {
            var timeout = null;
            return function () {
                $timeout.cancel(timeout);
                var args = arguments;
                timeout = $timeout(function () {
                    callback.apply(this, args);
                }, interval);
            };
        };
    })
    .service('pendingRequests', function () {
        var pending = [];

        this.get = function () {
            return pending;
        };
        this.add = function (request) {
            pending.push(request);
        };
        this.remove = function (request) {
            pending = _.filter(pending, function (p) {
                return p.url !== request;
            });
        };
        this.cancelAll = function () {
            if (pending.length == 0) return;

            angular.forEach(pending, function (p) {
                p.canceller.resolve();
            });
            pending.length = 0;
        };
    })
    .factory('$$$', ['$filter', '$translate', function ($filter, $translate) {
        return function (text) {

            //////console.log($translate.use());
            return $filter('translate')(text)
        }
    }])
    .filter('nospace', function () {
        return function (value) {
            return (!value) ? '' : value.replace(/ /g, '');
        };
    })
    .filter('humanizeDoc', function () {
        return function (doc) {
            if (!doc) return;
            if (doc.type === 'directive') {
                return doc.name.replace(/([A-Z])/g, function ($1) {
                    return '-' + $1.toLowerCase();
                });
            }

            return doc.label || doc.name;
        };
    })
    .run(['$rootScope', '$state', function ($rootScope, $state) {

        $rootScope.$on('$locationChangeStart', function () {
            $rootScope.stateIsLoading = true;
        });


        $rootScope.$on('$locationChangeSuccess', function () {
            $rootScope.stateIsLoading = false;
        });

        // require("/static/bower_components/pivottable/dist/pivot.min.js");
        // "/static/bower_components/pivottable/dist/plotly-basic-latest.min.js",
        // "/static/bower_components/pivottable/dist/pivot.min.js",
        // "/static/bower_components/pivottable/dist/plotly_renderers.min.js",

    }])
    .service('httpService', ['$http', '$q', '$rootScope', 'pendingRequests', function ($http, $q, $rootScope, pendingRequests) {
        this.allow = false;
        this.get = function (url) {
            //if (!this.allow){
            //
            //}
            var canceller = $q.defer();
            pendingRequests.add({
                url: url,
                canceller: canceller
            });
            //Request gets cancelled if the timeout-promise is resolved
            var requestPromise = $http.get(url, {timeout: canceller.promise, withCredentials: true});
            //Once a request has failed or succeeded, remove it from the pending list
            requestPromise.finally(function () {
                pendingRequests.remove(url);
            });
            return requestPromise;
        }
    }])
    .factory('shareServiceBool', function () {
        var savedData = {};

        function set(data) {
            savedData = data;
        }

        function get() {
            return savedData;
        }

        return {
            set: set,
            get: get
        }
    })
    .factory("menu", ["SERVICES", "COMPONENTS", "DEMOS", "PAGES", "$location", "$rootScope", "$http", "$window", function (e, t, a, n, o, l, i, s) {
        var r = {}
            , m = [{
            name: "Getting Started",
            url: "getting-started",
            type: "link"
        }]
            , d = [];
        angular.forEach(a, function (e) {
            d.push({
                name: e.label,
                url: e.url
            })
        }),
            m.push({
                name: "Demos",
                pages: d.sort(h),
                type: "toggle"
            }),
            m.push(),
            m.push({
                name: "Customization",
                type: "heading",
                children: [{
                    name: "CSS",
                    type: "toggle",
                    pages: [{
                        name: "Typography",
                        url: "CSS/typography",
                        type: "link"
                    }, {
                        name: "Button",
                        url: "CSS/button",
                        type: "link"
                    }, {
                        name: "Checkbox",
                        url: "CSS/checkbox",
                        type: "link"
                    }]
                }, {
                    name: "Theming",
                    type: "toggle",
                    pages: [{
                        name: "Introduction and Terms",
                        url: "Theming/01_introduction",
                        type: "link"
                    }, {
                        name: "Declarative Syntax",
                        url: "Theming/02_declarative_syntax",
                        type: "link"
                    }, {
                        name: "Configuring a Theme",
                        url: "Theming/03_configuring_a_theme",
                        type: "link"
                    }, {
                        name: "Multiple Themes",
                        url: "Theming/04_multiple_themes",
                        type: "link"
                    }, {
                        name: "Under the Hood",
                        url: "Theming/05_under_the_hood",
                        type: "link"
                    }, {
                        name: "Browser Color",
                        url: "Theming/06_browser_color",
                        type: "link"
                    }]
                }, {
                    name: "Performance",
                    type: "toggle",
                    pages: [{
                        name: "Internet Explorer",
                        url: "performance/internet-explorer",
                        type: "link"
                    }]
                }]
            });
        var c, p = {}, u = {};

        function h(e, t) {
            return e.name < t.name ? -1 : 1
        }

        return t.forEach(function (e) {
            e.docs.forEach(function (e) {
                angular.isDefined(e.private) || (u[e.type] = u[e.type] || [],
                    u[e.type].push(e),
                    p[e.module] = p[e.module] || [],
                    p[e.module].push(e))
            })
        }),
            e.forEach(function (e) {
                angular.isDefined(e.private) || (u[e.type] = u[e.type] || [],
                    u[e.type].push(e),
                    p[e.module] = p[e.module] || [],
                    p[e.module].push(e))
            }),
            m.push({
                name: "API Reference",
                type: "heading",
                children: [{
                    name: "Layout",
                    type: "toggle",
                    pages: [{
                        name: "Introduction",
                        id: "layoutIntro",
                        url: "layout/introduction"
                    }, {
                        name: "Layout Containers",
                        id: "layoutContainers",
                        url: "layout/container"
                    }, {
                        name: "Layout Children",
                        id: "layoutGrid",
                        url: "layout/children"
                    }, {
                        name: "Child Alignment",
                        id: "layoutAlign",
                        url: "layout/alignment"
                    }, {
                        name: "Extra Options",
                        id: "layoutOptions",
                        url: "layout/options"
                    }, {
                        name: "Troubleshooting",
                        id: "layoutTips",
                        url: "layout/tips"
                    }]
                }, {
                    name: "Services",
                    pages: u.service.sort(h),
                    type: "toggle"
                }, {
                    name: "Types",
                    pages: u.type.sort(h),
                    type: "toggle"
                }, {
                    name: "Directives",
                    pages: u.directive.sort(h),
                    type: "toggle"
                }]
            }),
            m.push({
                name: "Migration to Angular",
                url: "migration",
                type: "link"
            }),
            m.push({
                name: "Contributors",
                url: "contributors",
                type: "link"
            }),
            m.push({
                name: "License",
                url: "license",
                type: "link",
                hidden: !0
            }),
            l.$on("$locationChangeSuccess", function () {
                var a = o.path()
                    , e = {
                    name: "Introduction",
                    url: "/",
                    type: "link"
                };
                if ("/" === a)
                    return c.selectSection(e),
                        void c.selectPage(e, e);

                function n(e, t) {
                    -1 !== a.indexOf(t.url) && (c.selectSection(e),
                        c.selectPage(e, t))
                }

                m.forEach(function (t) {
                    t.children ? t.children.forEach(function (t) {
                        t.pages && t.pages.forEach(function (e) {
                            n(t, e)
                        })
                    }) : t.pages ? t.pages.forEach(function (e) {
                        n(t, e)
                    }) : "link" === t.type && n(t, t)
                })
            }),
            i.get("/docs.json").then(function (a) {
                a = a.data;
                var t = function () {
                    var e = s.location.pathname;
                    e.length < 2 && (e = "HEAD");
                    return e.match(/[^/]+/)[0].toLowerCase()
                }()
                    , e = {
                    type: "version",
                    url: "/HEAD",
                    id: "head",
                    name: "HEAD (master)",
                    github: ""
                }
                    , n = "head" === t ? [] : [e]
                    , o = function () {
                    if (a && a.versions && a.versions.length)
                        return a.versions.map(function (e) {
                            var t = a.latest === e;
                            return {
                                type: "version",
                                url: "/" + e,
                                name: function (e) {
                                    return e.latest ? "Latest Release (" + e.id + ")" : "Release " + e.id
                                }({
                                    id: e,
                                    latest: t
                                }),
                                id: e,
                                latest: t,
                                github: "tree/v" + e
                            }
                        });
                    return []
                }()
                    , l = o.filter(function (e) {
                    switch (t) {
                        case e.id:
                            return !1;
                        case "latest":
                            return !e.latest;
                        default:
                            return !0
                    }
                })
                    , i = function () {
                    switch (t) {
                        case "head":
                            return e;
                        case "latest":
                            return o.filter(function (e) {
                                return e.latest
                            })[0];
                        default:
                            return o.filter(function (e) {
                                return t === e.id
                            })[0]
                    }
                }() || {
                    name: "local"
                };
                r.current = i,
                    m.unshift({
                        name: "Documentation Version",
                        type: "heading",
                        className: "version-picker",
                        children: [{
                            name: i.name,
                            type: "toggle",
                            pages: n.concat(l)
                        }]
                    })
            }),
            c = {
                version: r,
                sections: m,
                selectSection: function (e) {
                    c.openedSection = e
                },
                toggleSelectSection: function (e) {
                    c.openedSection = c.openedSection === e ? null : e
                },
                isSectionSelected: function (e) {
                    return c.openedSection === e
                },
                selectPage: function (e, t) {
                    c.currentSection = e,
                        c.currentPage = t
                },
                isPageSelected: function (e) {
                    return c.currentPage === e
                }
            }
    }
    ]).filter("nospace", function () {
    return function (e) {
        return e ? e.replace(/ /g, "") : ""
    }
})
    .filter("humanizeDoc", function () {
        return function (e) {
            if (e)
                return "directive" === e.type ? e.name.replace(/([A-Z])/g, function (e) {
                    return "-" + e.toLowerCase()
                }) : e.label || e.name
        }
    }).filter("directiveBrackets", function () {
    return function (e, t) {
        if (t) {
            if (!t.element && t.attribute)
                return "[" + e + "]";
            if (t.element && -1 < e.indexOf("-"))
                return "<" + e + ">"
        }
        return e
    }
})
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

    .directive("docsScrollClass", function () {
        return {
            restrict: "A",
            link: function (e, t, a) {
                var n = t.parent()
                    , o = !1;

                function l() {
                    var e = 0 !== n[0].scrollTop;
                    e !== o && t.toggleClass(a.docsScrollClass, e),
                        o = e
                }

                l(),
                    n.on("scroll", l)
            }
        }
    })

    .controller('NotifCtrl',
        function ($scope,
                  $translate,
                  $q,
                  $state,
                  $rootScope,
                  $http,
                  $modal,
                  $location,
                  $log,
                  $timeout,
                  $mdSidenav,) {


            $scope.notifs = {};
            $scope.getNotif = function (id) {
                $http.get('/api/v1/notify/' + id + '/').then(function (data) {
                    if (data.data.id) {
                        $scope.notifs.results.splice(0, 0, data.data);
                        let appElement = document.getElementById('thisisoool');
                        if (appElement) {
                            let appScope = angular.element(appElement).scope();
                            appScope.showSimpleToast(data.data.extra.msg_body.body);
                            notifyBrowser(data.data.extra.msg_body.body);
                        }
                    }
                })
            }
            $scope.list = function () {
                $http.get('/api/v1/notify/').then(function (data) {
                    $scope.notifs = data.data;
                    let navElement = document.querySelector('#thisisoool');
                    if (navElement) {
                        let appScope = angular.element(navElement).scope();
                        if (appScope) {
                            if (data.data.results){
                                                            appScope.has_alert = !(data.data.results.length === 0);

                            }
                        }
                    }
                });

                $http.get('/api/v1/notify/get_all_unsings/').then(function (data) {
                    $scope.notifs = data.data;
                    let navElement = document.querySelector('#thisisoool');
                    if (navElement) {
                        let appScope = angular.element(navElement).scope();
                        if (appScope) {
                            if (data.data.results){
                                                            appScope.has_alert = !(data.data.results.length === 0);

                            }
                        }
                    }
                })

            }
            $scope.init = function () {
                $scope.list()
            }
            $scope.init();
        })
    .controller('ToastCtrl', function ($scope, $mdToast, toastMessage) {
        // $scope.toastMessage =
        $scope.closeToast = function () {
            $mdToast.cancel();
        };
        $scope.confirmToast = function () {
            $mdToast.hide();
        };
    }).controller('ToastConfirmCtrl', function ($scope, $mdToast, toastMessage) {
    // $scope.toastMessage =
    $scope.closeToast = function () {
        $mdToast.cancel();
    };
    $scope.confirmToast = function () {
        $mdToast.hide();
    };
})
.config(function($mdAriaProvider) {
   // Globally disables all ARIA warnings.
   $mdAriaProvider.disableWarnings();
})
    .factory('toastConfirm', function ($mdToast) {
        return {
            showConfirm: function (confirmMessage) {
                return $mdToast.show({
                    hideDelay: 0,
                    position: 'top right',
                    controller: 'ToastConfirmCtrl',
                    controllerAs: 'ctrl',
                    bindToController: true,
                    locals: {toastMessage: confirmMessage},
                    templateUrl: 'toast-confirm.html'
                })
            }
        }
    })

