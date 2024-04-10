/**
 * Created by mohammad on 1/4/16.
 */


'use strict';


angular.module('AniTheme').controller(
    'LetterBaseCtrl',
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
              $mdSidenav,
              shareService,
              LetterBaseService) {


        $scope.toggleLeft = buildDelayedToggler('left');
        $scope.toggleRight = buildToggler('right');
        $scope.isOpenRight = function () {
        }


        $rootScope.$on("sendSuccShowInbox", function (data, args) {

            if (args.sign) {

                if (args.letterType == 1 && args.sign.id) {
                    $scope.sentLetter = args;
                }
            }


        })

        $scope.sentLetter = {};


        $scope.CloseIt = function () {
            $mdSidenav('rightInboxList').close()

            // document.getElementById("btnInboxShowRightMenu").click();
            angular.element(document.getElementById("divList")).css("margin-right", "0");

            angular.element(document.getElementById("btnInboxShowRightMenu")).text("نمایش منو");
        }

        $scope.closeRighBar = function () {
            $mdSidenav('right').close()
                .then(function () {

                });
        };

        // $event


        $rootScope.$on("composeLoading", function (ev, args) {
            $scope.isOpeningNewLetter = args.loading;
        });


        $scope.isOpeningNewLetter = false;
        $scope.MakeNewLetter = function ($event) {
            // $scope.isOpeningNewLetter = true;
            // angular.element(document.querySelector('#btnCompose'));
            // $scope.$broadcast("makeNewLetter");


            var elem = angular.element(document.querySelector('#btnCompose'));
            $rootScope.$broadcast("composeLoading", {loading: true});


            if ($scope.loadingComposeLetter) {
                return
            }
            $scope.loadingComposeLetter = true;
            var letter = {};
            //$scope.letter.itemType = 1;
            // in the server
            // backend automatically change item mode to 7 for first send and
            // put 1 to other
            // to show in send items
            letter.itemType = 7;
            letter.itemMode = 4;
            letter.itemPlace = 1;

            letter.letterType = 7;
            letter.letterMode = 4;
            letter.letterPlace = 1;
            letter.body = " ";
            letter.subject = " ";
            letter.selectedMembers = [];
            $http.post("/api/v1/letter/", letter).then(function (data) {
                $scope.loadingComposeLetter = false;
                // $rootScope.GetIntimeNotification();
                // $location.path('/dashboard/Letter/Inbox/' + data.data.id + '/Compose');
                $rootScope.$broadcast("composeLoading", {loading: false});
                $rootScope.$broadcast("hideInboxLeft");
                // debugger;
                // $state.go("dashboard.letter.inbox.Compose", {'letterID': data.data.id});

                // $timeout(function () {
                // debugger;
                $state.go("compose", {'letterID': data.data.id});
                // }, 200);


                // $state.go("Compose", {'letterID': data.data.id});

            }).catch(function () {
                $rootScope.$broadcast("composeLoading", {loading: false});
                $rootScope.$broadcast("hideInboxLeft");

            });


        };


        $scope.toggleRight = buildToggler('right');
        $scope.isOpenRight = function () {
            return $mdSidenav('right').isOpen();
        };

        function debounce(func, wait, context) {
            var timer;
            return function debounced() {
                var context = $scope,
                    args = Array.prototype.slice.call(arguments);
                $timeout.cancel(timer);
                timer = $timeout(function () {
                    timer = undefined;
                    func.apply(context, args);
                }, wait || 10);
            };
        }

        function buildDelayedToggler(navID) {
            return debounce(function () {
                // Component lookup should always be available since we are not using `ng-if`
                $mdSidenav(navID)
                    .toggle()
                    .then(function () {
                        $log.debug("toggle " + navID + " is done");
                    });
            }, 200);
        }

        function buildToggler(navID) {
            return function () {
                // Component lookup should always be available since we are not using `ng-if`
                $mdSidenav(navID)
                    .toggle()
                    .then(function () {
                        $log.debug("toggle " + navID + " is done");
                    });
            }
        }


    })
;