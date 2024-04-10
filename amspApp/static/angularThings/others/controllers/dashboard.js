'use strict';

/**
 * @ngdoc function
 * @name AniTheme.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of AniTheme
 */




var Global$http;
angular.module('AniTheme').controller(
    'DashboardCtrl',
    function ($scope,
              $injector,
              $timeout,
              $location,
              $state,
              $translate, $$$,
              $rootScope,
              $http, $mdToast,
              generalService,
              $interval) {
        Global$http = $http;


        $scope.openNews = function (news) {
            $location.url("/dashboard/" + news.id + "/Read")
        }


        $scope.news = {};


        $scope.GetNews = function () {
            $http.get("/api/v1/news/getLatest/").then(function (data) {
                $scope.news = data.data;
            });
        };
        $scope.GetNews();




        $scope.GetMyBpmsOpened = function () {
            $http.get("/api/v1/bpms-archive/getOpenedMyArchive/").then(function (data) {
                //////console.log(data);
            })
        };
        $scope.CurrentPlace = "sss";
        $rootScope.$on("UpdateCurrentPlace", function (str) {
            $scope.CurrentPlace = str;
        })
        $scope.statistics = {};
        $scope.isItWaiting = false;
        $scope.refreshStatistics = function (statistics) {
            return  // added for testing
            if ($scope.isItWaiting) {
            } else {
                $scope.isItWaiting = true;
                generalService.getStatistics(statistics).then(function (data) {
                    //////console.log(statistics);
                    $scope.statistics = data.data;
                    $scope.isItWaiting = false;
                    $scope.refreshStatistics($scope.statistics);
                    $rootScope.$broadcast("UpdateLPList");
                }).catch(function () {
                    if ($scope.isItWaiting == true) {
                        $timeout(function () {
                            $scope.isItWaiting = false;
                            $scope.refreshStatistics($scope.statistics);
                        }, 6000);
                    }
                });
            }
        };
        $timeout(function () {
            $scope.refreshStatistics($scope.statistics);
        }, 0);
        $scope.inboxStatistics = {};
        $scope.inboxIsItWaiting = false;
        $scope.inboxRefreshStatistics = function (statistics) {
            if ($scope.inboxIsItWaiting) {
            } else {
                $scope.inboxIsItWaiting = true;
                generalService.getInboxStatistics(statistics).then(function (data) {
                    $scope.inboxStatistics = data.data;
                    $scope.inboxIsItWaiting = false;
                    $scope.inboxRefreshStatistics($scope.inboxStatistics);
                    $rootScope.$broadcast("UpdateInboxStatics", $scope.inboxStatistics);
                }).catch(function () {
                    if ($scope.inboxIsItWaiting == true) {
                        $timeout(function () {
                            $scope.inboxIsItWaiting = false;
                            $scope.inboxRefreshStatistics($scope.inboxStatistics);
                        }, 6000);
                    }
                });
            }
        };
        $scope.$on("GetInboxStatic", function (event) {
            $rootScope.$broadcast("UpdateInboxStatics", $scope.inboxStatistics);
        })
        $scope.inboxStaticForFirstTime = function () {
            generalService.getFirstTimeInboxStatistics().then(function (data) {
                $scope.inboxStatistics = data.data;
                $rootScope.$broadcast("UpdateInboxStatics", $scope.inboxStatistics);
                $scope.inboxRefreshStatistics($scope.inboxStatistics);

            });

        };

        $scope.date = new Date();
        $scope.layoutToggler = function (y) {

            if (y == $scope.multiCollapseVar)
                $scope.multiCollapseVar = 0;
            else
                $scope.multiCollapseVar = y;
        };
        $scope.load = (function () {
            $http.get("/api/v1/gettimezone/").then(function (data) {
                var newLoc = data.data;
                if (data.timezone == "Asia/Tehran") {
                    $scope.changeLanguage("fa");
                }
                if (data.timezone == "Europe/London") {
                    $scope.changeLanguage("en");
                }
            });
            $scope.CheckingForAnyForceNotification();
        });
        $scope.changeLanguage = (function (l) {
            // time to change localization
            var cc = "Asia/Tehran";

            if (l == "fa") {
                cc = "Asia/Tehran";
            }
            if (l == "en") {
                cc = "Europe/London";
            }

            $http.post("/api/v1/timezone/", {
                timezone: cc,
                csrfmiddlewaretoken: Cookies.get('rahsoon-CSRF-TOKEN')
            });

            if (l == 'fa') {
                //
                if ($('body').hasClass('rtl')) {
                    $('.stat').removeClass('hvr-wobble-horizontal');
                } else {
                    $('#rtlcss').remove();

                    $('body').addClass('rtl');

                    $('.stat').removeClass('hvr-wobble-horizontal');
                }
            } else {
                $('body').removeClass('rtl');
            }
            $translate.use(l);
            if ($('body').hasClass('rtl')) {
                $('head').append('<link rel="stylesheet" href="/static/bower_components/bootstrap/bootstrap-rtl.min.css" id="rtlcss" />');

            } else {
                $('#rtlcss').remove();

            }
        });
        $scope.CheckingForAnyForceNotification = function () {
            $http.get("/api/v1/forced/getForceNotification/").then(function (data) {
                if (data.data.result == false) {

                } else {
                    $rootScope.$broadcast("notifyconnected");
                }
            })
        };
        $scope.load();

        var last = {
            bottom: false,
            top: true,
            left: false,
            right: true
        };
        var lastBotton = {
            bottom: true,
            top: false,
            left: true,
            right: false
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

        $rootScope.$on("showToast", function (event, args) {
            $scope.showSimpleToast(args);
        });
        $scope.showSimpleToast = function (message) {
            var pinTo = $scope.getToastPosition();
            $mdToast.show(
                $mdToast.simple()
                    .textContent($$$(message))
                    .position(pinTo)
                    .hideDelay(1500)
                    .action('OK')
                    .parent(angular.element(document.getElementById("thisisoool")))
            );
        };


        $scope.checkForFirstLogin = function () {
            $http.get("/api/v1/profile/getIfFirstLogin/").then(function (data) {
                if (data.data.result == 1) {
                    $state.go("welcomepage");
                }
                if (data.data.result == 2) {
                    $state.go("welcomepageClient");
                }
            })
        };

        $scope.checkForFirstLogin();

    })

    .controller(
        'DashboardMap',
        function ($scope,
                  $injector,
                  $timeout,
                  $state,
                  $translate,
                  $$$,
                  $rootScope,
                  $location,
                  $http,
                  $mdToast,
                  generalService,
                  $interval) {


            $scope.CurrentPlace = {};
            $scope.PrevPlace = {};

            $scope.Open = function (str) {
                $location.url(str);
            }


            $rootScope.$on("DetectUrlChange", function (e, toState, toParams, fromState, fromParams) {
                // debugger;
                // //console.log("urlChanged...");

                if (toParams) {
                    var url = toParams.templateUrl ? toParams.templateUrl : toParams.name;
                    if (url) {
                        $http.get("/api/v1/forced/getDashboardHelp/?q=" + url).then(function (data) {
                            $scope.CurrentPlace = data.data;
                            // //console.log(fromParams);
                            if (fromParams) {
                                var urlp = fromParams.templateUrl ? fromParams.templateUrl : fromParams.name;
                                if (fromParams.templateUrl) {
                                    $http.get("/api/v1/forced/getDashboardHelp/?q=" + urlp).then(function (datax) {
                                        $scope.PrevPlace = datax.data;
                                    })
                                }
                            }

                        })
                    }
                }
            });
        })

//

