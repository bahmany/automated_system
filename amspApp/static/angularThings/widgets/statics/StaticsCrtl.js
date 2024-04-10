'use strict';


angular.module('AniTheme').controller(
    'StaticsCrtl',
    function ($scope,
              $translate,
              $q, $timeout,
              $rootScope,
              $http, $element,
              $stateParams,
              $modal) {

        $timeout(function () {
            if (typeof ($(".picker").datepicker) !== 'function') {
                return
            }
            $(".picker").datepicker({
                showOn: 'button',
                buttonImage: 'static/images/open-iconic-master/png/calendar-2x.png',
                buttonImageOnly: true,
                dateFormat: 'yy/mm/dd'
            });
        }, 0);

        $scope.filter = {};
        $scope.filter.tmplID = $stateParams.tmplID;
        $scope.filter.order = "-entryDate";
        $scope.selected = [];

        $scope.$watchGroup(
            [
                "filter.startdate",
                "filter.enddate",
                "filter.max",
                "filter.min"], function () {
                $scope.getStatics();

            })


        $scope.staticData = [];
        $scope.getStatics = function () {


            $http.post("/api/v1/dataForMS/getData/", $scope.filter).then(function (data) {
                $scope.staticData = data.data;

                var lbls = [];
                var vals = [];
                for (var i = 0; data.dt.length > i; i++) {
                    if (data.dt[i]["entryDate"]) {
                        lbls.push(data.dt[i]["entryDate"])
                    } else {
                        lbls.push(null)
                    }
                    if (data.dt[i]["value"]) {
                        vals.push(parseInt(data.dt[i]["value"]))
                    } else {
                        vals.push(null)
                    }
                }
                var maxmin = data.tmpl.exp;
                if (maxmin) {
                    maxmin = [{
                        "y": maxmin.max,
                        "style": "rgba(255, 0, 0, .3)",
                        "text": "max"
                    }, {
                        "y": maxmin.min,
                        "text": "min"
                    }]
                } else {
                    maxmin = []
                }

                var ctx = $($($element).find(".canvbpm")[0])[0].getContext("2d");


                var myChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: lbls,
                        datasets: [{
                            borderColor: 'black',
                            borderWidth: 2,
                            label: data.tmpl.name,
                            data: vals
                        }]
                    },
                    options: {
                        horizontalLine: maxmin,
                        scales: {
                            yAxes: [{
                                display: true,
                                ticks: {
                                    // max: top,
                                    // min: botton,
                                    beginAtZero: false,
                                    callback: function (value, index, values) {
                                        return value.toLocaleString();
                                    }
                                }
                            }],
                            xAxes: [{}]
                        },
                        title: {
                            display: false,
                            text: ''
                        },
                        legend: {
                            display: true
                        }
                    }
                });


            })
        }


    });

