'use strict';

angular.module('AniTheme')
    .directive('dashboardCalendar', function () {
        return {
            templateUrl: '/static/angularThings/widgets/dashboard_calendar/DCD_template1.html',
            restrict: 'E',
            scope: {},
            replace: true,
            controller: function ($scope,
                                  $q,
                                  $http,
                                  $timeout,
                                  $state,
                                  $mdToast,
                                  $$$, $filter,
                                  $stateParams,
                                  $templateCache,
                                  $translate,
                                  $location,
                                  $attrs,
                                  $element,
                                  $rootScope) {


                $scope.showCal = true;

                var currentEventHandler;
                var thisIsForEventCach = false;


                $scope.AddNewCalItem = function () {
                    $scope.CalendarItem = {};
                    $scope.CalendarItem.startDate = $scope.selectedDay + " " + getCurrentTime();
                    $('.list-cal-items').fadeOut(function () {
                        $('.add-new-cal-item').fadeIn()

                    })
                };

                $scope.edit = function (item) {
                    if (item.startDate) {
                        item.startDate = $filter('jalaliDate')(item.startDate, 'jYYYY/jMM/jDD hh:mm');
                    }
                    if (item.endDate) {
                        item.endDate = $filter('jalaliDate')(item.endDate, 'jYYYY/jMM/jDD hh:mm');
                    }
                    $scope.CalendarItem = item;
                    $('.list-cal-items').fadeOut(function () {
                        $('.add-new-cal-item').fadeIn()

                    })
                };


                $scope.cancel = function () {
                    $scope.CalendarItem = {};
                    $scope.CalendarItem.startDate = $scope.selectedDay + " " + getCurrentTime();
                    $('.add-new-cal-item').fadeOut(function () {
                        $('.list-cal-items').fadeIn()

                    })
                }



                ///
                /// in the calendar table i decided to show these things :
                ///
                ///
                ///
                ///
                ///

                $scope.handleTable = function () {
                    var el;
                    var days = [];


                    $(".cal-cal td .day").not('.wn').not('.name').each(function (k, ev) {
                        days.push(ev.caldate.print("%Y/%m/%d", ev.calendar.dateType, false));
                    });

                    $http.post("/api/v1/calendarItem/getCount/", {'dates': days}).then(function (data) {

                        var currentDate;
                        var txthtml;
                        var col_count = 0;
                        var inb_seen_count = 0;
                        var inb_unseen_count = 0;
                        $(".dash-cal-ul-counts").remove();
                        $(".cal-cal td .day").not('.wn').not('.name').each(function (k, ev) {
                            currentDate = ev.caldate.print("%Y/%m/%d", ev.calendar.dateType, false);
                            txthtml = $(ev).html();
                            col_count = 0;
                            inb_seen_count = 0;
                            inb_unseen_count = 0;
                            $(ev).html("");

                            for (var i = 0; data.data.cal_count.length > i; i++) {
                                if (data.data.cal_count[i].dt == currentDate) {
                                    col_count = data.data.cal_count[i].count;
                                }
                            }
                            // for (var i = 0; data.inb_seen.length > i; i++) {
                            //     if (data.inb_seen[i].dt == currentDate) {
                            //         inb_seen_count = data.inb_seen[i].count;
                            //     }
                            // }
                            for (var i = 0; data.data.inb_unseen.length > i; i++) {
                                if (data.data.inb_unseen[i].dt == currentDate) {
                                    inb_unseen_count = data.data.inb_unseen[i].count;
                                }
                            }

                            $(ev).html(txthtml +
                                "<ul class='dash-cal-ul-counts'><li title='تعداد فعالیت های انجام نشده' class='dash-cal-count'>" + col_count.toString() + "</li>" +
                                "<li title='تعداد نامه های خوانده نشده' class='dash-inbx-seen-count'>" + inb_unseen_count.toString() + "</li></ul>"
                            )


                        });


                    }).catch(function (data) {

                    })
                }


                $scope.selectedDay = "";

                $scope.selectedStr = "";


                $scope.showItems = function (dayStr, todayStr) {

                    $scope.selectedDay = dayStr;
                    $scope.selectedStr = todayStr;
                    $scope.showCal = false;

                    if (!($scope.CalendarItem.id)) {
                        $scope.CalendarItem.startDate = $scope.selectedDay + " " + getCurrentTime();
                    }

                    $scope.list($scope.selectedDay)
                };
                $scope.showCalc = function () {
                    $scope.showCal = true;
                    $scope.handleTable();

                };

                $scope.CalendarItem = {};
                $scope.CalendarItems = {};
                $scope.itemsErr = [];

                $scope.finished = function (itemID) {
                    $http.post("/api/v1/calendarItem/" + itemID + '/partialUpdate/', {
                        finished: true
                    }).then(function (data) {
                        $scope.list($scope.selectedDay);
                        $rootScope.$broadcast("showToast", "تغییرات ذخیره شد");
                    });
                }
                $scope.unfinished = function (itemID) {
                    $http.post("/api/v1/calendarItem/" + itemID + '/partialUpdate/', {
                        finished: false
                    }).then(function (data) {
                        $scope.list($scope.selectedDay);
                        $rootScope.$broadcast("showToast", "تغییرات ذخیره شد");
                    });
                }

                $scope.delete = function () {
                    swal({
                        title: "آیا اطمینان دارید",
                        text: "داده ی انتخابی شما از سوابقتان حدف خواهد شد",
                        type: "warning",
                        showCancelButton: true,
                        confirmButtonColor: "#DD6B55",
                        confirmButtonText: "بله حذف شود",
                        closeOnConfirm: false
                    }, function () {
                        $http.delete("/api/v1/calendarItem/" + $scope.CalendarItem.id + '/', {}).then(function (data) {
                            $scope.cancel();
                            $scope.list($scope.selectedDay);
                            $rootScope.$broadcast("showToast", "تغییرات ذخیره شد");
                            swal("حذف شد", "فعالیت مورد نظر حذف شد", "success");


                        });

                    });


                };

                $scope.GoToPage = function (url) {
                    $http.get(url).then(function (data) {
                        $scope.CalendarItems = data.data;
                    })
                }

                $scope.list = function (selectedDay) {
                    $http.get("/api/v1/calendarItem/?q=" + selectedDay).then(function (data) {
                        $scope.CalendarItems = data.data;
                    })
                }


                $scope.save = function () {
                    $http.post("/api/v1/calendarItem/", $scope.CalendarItem).then(function (data) {

                        if (!(data.data.status)) {
                            $scope.list($scope.selectedDay);
                            $rootScope.$broadcast("showToast", "تغییرات ذخیره شد");
                            $scope.cancel();
                        } else {
                            $scope.itemsErr = data.data;
                        }


                    }).catch(function (data) {
                        $scope.itemsErr = data.data;
                    })
                }


                $(function () {
                    setActiveStyleSheet("Aqua");
                    var flatCal = Calendar.setup({
                        flat: "flat_calendar",
                        inputField: "date_input_field",   // id of the input field
                        ifFormat: "%Y-%m-%d",       // format of the input field
                        dateType: "jalali",
                        langNumbers: true,
                        showOthers: true,
                        weekNumbers: true
                    });

                    $('.calendar table').addClass("table");
                    $('.calendar .combo').css("display", "none");

                    $('.calendar .day').not('.wn').not('.name').on("click", function (ev) {

                        var el = Calendar.getElement(ev);
                        if (thisIsForEventCach == false) {
                            if (el.disabled) {
                                return false;
                            }
                            var cal = el.calendar;
                            var today = el.caldate.print("%Y/%m/%d", el.calendar.dateType, false);
                            var todayStr = el.caldate.print(el.calendar.ttDateFormat, el.calendar.dateType, el.calendar.langNumbers);
                            $scope.showItems(today, todayStr);
                        } else {
                            currentEventHandler = el;
                        }


                    });


                    $('.headrow td div').on("click", function (ev) {

                        $scope.handleTable();


                    });


                    $scope.handleTable();


                });


            }
        }
    });