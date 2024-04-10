'use strict';

function AvatarCompleted(avatarImg) {
    var scope = angular.element($("#thisisoool")).scope();
    scope.closeAvatarModal(avatarImg);
}

function CloseAvatarModal(avatarImg) {
    var scope = angular.element($("#thisisoool")).scope();
    scope.closeAvatarModal('');
}


function CloseAvatarPop(event) {
    if (event.target.id == 'thisIsAvtarMask') {
        $("#thisIsAvtarMask").fadeOut()
    }
}

function CloseAvatarPopForced() {
    $("#thisIsAvtarMask").fadeOut()
}

angular.module('AniTheme')
    .directive('topnav', function () {
        return {
            templateUrl: '/scripts/directives/topnav/',
            restrict: 'E',
            replace: true,
            controller: function ($scope,
                                  $q,
                                  $http,
                                  $timeout,
                                  $state,
                                  $mdToast, $log,
                                  $$$, $mdMenu,
                                  $stateParams,
                                  $templateCache,
                                  $translate,
                                  $location,
                                  $rootScope,
                                  $mdDialog, $mdSidenav,
                                  httpService,
                                  pendingRequests,
                                  companiesManagmentService) {

                // console.log("nav bar loaded");
                // $rootScope.$on('$stateChangeStart', function (e, toState, toParams, fromState, fromParams) {
                //     $rootScope.progressbar.start();
                //
                //
                // })


                // $rootScope.progressbar.start();
                var last = {
                    bottom: true,
                    top: false,
                    left: true,
                    right: false
                };

                $scope.has_alert = false;
                $scope.toastPosition = angular.extend({}, last);
                $scope.openMenu = function () {
                    $mdSidenav('left').toggle();
                };


                function sanitizePosition() {
                    var current = $scope.toastPosition;
                    if (current.bottom && last.top) current.top = false;
                    if (current.top && last.bottom) current.bottom = false;
                    if (current.right && last.left) current.left = false;
                    if (current.left && last.right) current.right = false;
                    last = angular.extend({}, current);
                }


                $scope.closeToast = function () {
                    if (isDlgOpen) {
                        return;
                    }

                    $mdToast.hide(ACTION_RESOLVE).then(function () {
                        isDlgOpen = false;
                    });
                };


                $scope.showCustomToast = function (message) {
                    $mdToast.show({
                        hideDelay: 0,
                        position: 'top right',
                        controller: 'ToastCtrl',
                        controllerAs: 'ctrl',
                        bindToController: true,
                        locals: {toastMessage: message},
                        templateUrl: 'toast-template.html'
                    }).then(function (result) {

                    }).catch(function (error) {

                    });

                }
                $scope.showSimpleToast = function (message) {
                    $mdToast.show({
                        hideDelay: 0,
                        position: 'top right',
                        controller: 'ToastCtrl',
                        controllerAs: 'ctrl',
                        bindToController: true,
                        locals: {toastMessage: message},
                        templateUrl: 'toast-template-no-input.html'
                    }).then(function (result) {

                    }).catch(function (error) {

                    });

                }


                $scope.getToastPosition = function () {
                    sanitizePosition();
                    return Object.keys($scope.toastPosition)
                        .filter(function (pos) {
                            return $scope.toastPosition[pos];
                        })
                        .join(' ');
                };
                $scope.showActionToast = function (msg) {
                    var toast = $mdToast.simple()
                        .textContent(msg)
                        .action('OK')
                        .highlightAction(true)
                        .position($rootScope.getToastPosition());
                    $mdToast.show(toast).then(function (response) {
                        if (response.data == 'ok') {

                        }
                    });
                };


                $scope.OpenAvatar = function () {
                    $("#thisIsAvtarMask").fadeIn(200);
                }


                $scope.closeAvatarModal = function (avatarAddr) {
                    if (avatarAddr == "") {
                        $("#AvatarUploader").fadeOut(300);
                        return;
                    }

                    location.reload();

                    // $("#AvatarUploader").fadeOut(300);
                }
                $scope.openAvatarModal = function () {
                    $("#AvatarUploader").fadeIn(300);
                }

                // $scope.VVopenMenu = function () {
                //     $rootScope.$broadcast("ChangeSideBarVisibility");
                // }


                $scope.refresh = function () {
                    location.reload(true);
                }
                $scope.showMenu = function () {
                    $('.dashboard-page').toggleClass('showMenu');
                    $('.dashboard-page').toggleClass('push-right');
                }
                $scope.changeTheme = function (setTheme) {

                    $('<link>')
                        .appendTo('head')
                        .attr({type: 'text/css', rel: 'stylesheet'})
                        .attr('href', '{% static "ani-theme/styles/app-' + setTheme + '.css" %}');

                    // $.get('/api/change-theme?setTheme='+setTheme);

                }
                $scope.rightToLeft = function () {
                    $('body').toggleClass('rtl');

                    // var t = $('body').hasClass('rtl');
                    // ////console.log(t);

                    if ($('body').hasClass('rtl')) {
                        $('.stat').removeClass('hvr-wobble-horizontal');
                    }
                }

                $scope.currentCompany = {};
                $scope.toggleDateShow = false;
                $scope.hostname = "";

                // this function is for top clock
                $scope.init = function () {
                    startWS();
                    var url = window.location.href;
                    var arr = url.split("/");
                    var hWihoutPort = arr[2].split(":")[0];
                    $scope.hostname = arr[0] + "//" + hWihoutPort + ":8888";
                    $timeout(function () {
                        $scope.toggleDateShow = !$scope.toggleDateShow;
                        $scope.init();
                        return
                    }, 5000)
                };
                //------------
                // $scope.testIt = function () {
                //     //Notifications.happened();
                //     $scope.trackChangesHappened();
                // }

                $scope.init();
                $scope.msg = [];


                //---------------------------------------------------------------------
                //---------------------------------------------------------------------
                //---------------------------------------------------------------------
                //---------------------------------------------------------------------
                //---------------------------------------------------------------------
                //----------------------- Chatting ----------------------------------
                //---------------------------------------------------------------------
                //---------------------------------------------------------------------
                //---------------------------------------------------------------------
                //---------------------------------------------------------------------
                //---------------------------------------------------------------------


                // loadChat($scope, $http);
                loadNotification($scope, $http);


//----------------------------------------------------------------------------------------------
//----------------------------------------------------------------------------------------------
//----------------------------------------------------------------------------------------------
//----------------------------------------------------------------------------------------------
//---------------------------  Notification Part -----------------------------------------------
//----------------------------------------------------------------------------------------------
//----------------------------------------------------------------------------------------------
//----------------------------------------------------------------------------------------------
//----------------------------------------------------------------------------------------------
//----------------------------------------------------------------------------------------------
                $scope.myFilterBpms = function (item) {
                    return item.type == 3 || item.type == 2 || item.type == 4;
                };
                $scope.GetNotifications = function () {
                    if (!Cookies.get("sessionid")) {
                        // is not logined
                        return
                    }
                    $scope.GetNotificationCounts();
                };
                $scope.letterUnreadCount = 0;
                $scope.BPMSUnreadCount = 0;
                $scope.GetIntimeNotification = function () {
                    $http.get("/api/v1/notify/GetTopNotification/").then(function (data) {
                        $scope.msg = data.data;
                        $scope.letterUnreadCount = 0;
                        $scope.BPMSUnreadCount = 0;
                        for (var i = 0; data.data.length > i; i++) {
                            if (data.data[i].type == 1) {
                                $scope.letterUnreadCount += 1;

                            } else {
                                $scope.BPMSUnreadCount += 1;

                            }
                        }
                        // $rootScope.$broadcast("newNotification");
                        $scope.CheckLatest();

                    });

                };

                $scope.GetNotificationCounts = function () {
                    $http.get("/api/v1/notify/GetTopNotification/").then(function (data) {
                        $scope.msg = data.data;
                        $scope.letterUnreadCount = 0;
                        $scope.BPMSUnreadCount = 0;
                        //console.log("-----------");
                        //console.log(data);
                        for (var i = 0; data.data.length > i; i++) {
                            //console.log(data[i]);
                            if (data.data[i].type === 1) {
                                $scope.letterUnreadCount += 1;

                            } else {
                                $scope.BPMSUnreadCount += 1;

                            }
                        }
                        $scope.CheckLatest();
                        // $scope.has_alert = !(data.data.results.length === 0);
                    });

                };
                $scope.GetNotificationCounts();
                $scope.notificationTimeout = null;
                $scope.CheckLatest = function () {
                    $http.get("/api/v1/notify/GetLatestNotificationID/").then(function (data) {
                        $scope.notificationTimeout = $timeout(function () {
                            if (data.data.id) {
                                if (data.data.id == 1) {
                                    $http.get("/api/v1/notify/GetTopNotification/").then(function (data) {
                                        $scope.msg = data.data;
                                        $scope.letterUnreadCount = 0;
                                        $scope.BPMSUnreadCount = 0;
                                        for (var i = 0; data.length > i; i++) {
                                            if (data.data[i].type == 1) {
                                                $scope.letterUnreadCount += 1;

                                            } else {
                                                $scope.BPMSUnreadCount += 1;

                                            }
                                        }
                                        // $rootScope.$broadcast("newNotification");
                                        $scope.CheckLatest();

                                    });
                                } else {
                                    $scope.CheckLatest();
                                }
                            }

                            // $timeout.cancel($scope.notificationTimeout);
                        }, 6000);
                    });
                    // $http.get("/api/v1/notify/GetTopNotification/").then(function (data) {
                    //
                    // });
                };
                $rootScope.$on("notifyconnected", function (event, args) {
                    // console.log("notify broadcast recieved and ready to happened")
                    $timeout.cancel($scope.notificationTimeout);
                    //$scope.notificationTimeout.cancel()
                    $scope.CheckLatest();
                    // Notifications.happened();
                });
                $rootScope.$on("GetNotificationCounts", function () {
                    $scope.GetIntimeNotification()
                });
//----------------------------------------------------------------------------------------------
//----------------------------------------------------------------------------------------------
//----------------------------------------------------------------------------------------------
//----------------------------------------------------------------------------------------------
//---------------------------  Notification Part End  ------------------------------------------
//----------------------------------------------------------------------------------------------
//----------------------------------------------------------------------------------------------
//----------------------------------------------------------------------------------------------
//----------------------------------------------------------------------------------------------
//----------------------------------------------------------------------------------------------


                $scope.openLetter = function (item) {
                    $location.path("/dashboard/Letter/Inbox/" + item.extra.inboxID + "/Preview");
                };
                $scope.openProcess = function (item) {
                    $location.path(item.extra.url);
                };
                $scope.PageTo = function (PagerAddress) {
                    companiesManagmentService.GetCompaniesList(PagerAddress).then(
                        function (data) {
                            $scope.Companies = data.data;
                        });
                };


                $scope.GetCompaniesList = function () {
                    companiesManagmentService.companiesForCurrent().then(
                        function (data) {
                            $scope.companies = data.data;
                        });
                };
                $scope.initCurrentCompany = function (CurrentCompanyId, CurrentCompanyName) {
                    $scope.currentCompany.name = CurrentCompanyName;
                    $scope.currentCompany.id = CurrentCompanyId;
                    $scope.GetNotifications();
                };
                $scope.setAsCurrent = function (userId, companyId) {
                    companiesManagmentService.setAsCurrentService(userId, companyId).then(
                        function (data) {
                            window.location.reload();
                        });
                };
                $scope.GetCompaniesList();


                $scope.logout = function () {
                    $http.get('/api/v1/auth/logout/').then(function (data) {
                        window.location.href = "/";
                    });

                };

                $scope.has_alert = false;

                $scope.show_notif_sidebar = false;

                $scope.$watch('show_notif_sidebar', function (da) {
                    // $scope.has_alert = !($scope.show_notif_sidebar);
                })

                $scope.sendTestNotification = function (){
                    $http.get("/api/v1/notify/sendTestNotif/").then(function (data){

                    });
                }

                $scope.showNotifSidebar = function () {

                    $scope.show_notif_sidebar = !($scope.show_notif_sidebar);
                    angular.element(document.querySelector('#sidebar_notif')).scope().show_notif_sidebar = $scope.show_notif_sidebar;
                    if (!(angular.element(document.querySelector('#sidebar_notif')).scope().closeLeftSideBar)) {
                        angular.element(document.querySelector('#sidebar_notif')).scope().closeLeftSideBar = function () {
                            angular.element(document.querySelector('#sidebar_notif')).scope().show_notif_sidebar = false;
                            $scope.show_notif_sidebar = false;
                            // $scope.has_alert = false;
                        }
                    }
                    // sidebar_notif
                }

                // $scope.showNav = function () {
                // 	return $.cookie('morabaaOLDx')
                // }


//----------------------------------------------------------------------------------
//----------------------------------------------------------------------------------
//----------------------------------------------------------------------------------
//----------------------------------------------------------------------------------
//----------------------------------------------------------------------------------
//----------------------------------------------------------------------------------
//----------------------------------------------------------------------------------
//----------------------------------------------------------------------------------
//----------------------------------------------------------------------------------
//----------------------------------------------------------------------------------
//----------------------------------------------------------------------------------
//----------------------------------------------------------------------------------
//----------------------------------------------------------------------------------


//----------------------------------------------------------------------------------
//----------------------------------------------------------------------------------
//----------------------------------------------------------------------------------
//----------------------------------------------------------------------------------
//----------------------------------------------------------------------------------
//----------------------------------------------------------------------------------
//----------------------------------------------------------------------------------
//----------------------------------------------------------------------------------
//----------------------------------------------------------------------------------
//----------------------------------------------------------------------------------
//----------------------------------------------------------------------------------
            }
        }


        angular.element(document.getElementById("menu_notif")).parent().css("z-index", "99999999");


    });


