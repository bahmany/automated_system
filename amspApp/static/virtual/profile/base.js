'use strict';

angular.module('RahsoonApp').controller(
    'profileCtrl',
    function ($scope,
              $translate,
              $q, $location,
              $http,
              $rootScope,
              $timeout) {
        $scope.toggleLeft = buildDelayedToggler('left');
        $scope.isOpenLeft = function () {
            return $mdSidenav('left').isOpen();
        };
        $scope.leftSideMenu = [
            {name: 'اطلاعات شناسایی', selected: false, id: 1},
            {name: 'تحصیلات', selected: false, id: 2},
            {name: 'زبان های خارجی', selected: false, id: 3},
            {name: 'دوره های آموزشی', selected: false, id: 4},
            {name: 'تجربیات و مهارت ها', selected: false, id: 5},
            {name: 'نرم افزارها', selected: false, id: 6},
            {name: 'سوابق شغلی', selected: false, id: 7},
            {name: 'عکس و رزومه', selected: false, id: 8},
            {name: 'مرور اطلاعات', selected: false, id: 9}
            // {name: 'انتخاب شغل و همکاری', selected: false, id: 10},
            // {name: 'مشاهده نتایج', selected: false, id: 11}
        ]
        $scope.Select = function (item) {
            angular.forEach($scope.leftSideMenu, function (value, key) {
                $scope.leftSideMenu[key].selected = false;
            });
            $location.url("/home/profile/step" + item.id);
            item.selected = true;
        }
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
                $mdSidenav(navID)
                    .toggle()
                    .then(function () {
                        $log.debug("toggle " + navID + " is done");
                    });
            }, 200);
        }
        function buildToggler(navID) {
            return function () {
                $mdSidenav(navID)
                    .toggle()
                    .then(function () {
                        $log.debug("toggle " + navID + " is done");
                    });
            }
        }


        // $scope.Logout = function () {
        //     $http.get("/reg/api/v1/login/logout/").then(function () {
        //         debugger;
        //         $location.url("/");
        //         //location.reload();
        //     })
        // }


    }
)