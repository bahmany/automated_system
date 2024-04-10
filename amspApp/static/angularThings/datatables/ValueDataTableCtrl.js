/**
 * Created by m on 9/11/2016.
 */


angular.module('AniTheme').controller(
    'ValueDataTablesCtrl',
    function ($scope,
              $translate,
              $http,
              $timeout,
              $element,
              $q,
              $state,
              $stateParams,
              $mdDialog,
              $rootScope,
              $modal) {

        $scope.isNumeric = num => /^-?[0-9]+(?:\.[0-9]+)?$/.test(num+'');


        $scope.filter = {};
        $scope.values = {};
        $scope.selected = [];
        $scope.lookupsearch = {};

        var originatorEv;

        $scope.openMenu = function (mdMenu, event) {
            originatorEv = event;
            mdMenu.open(event);
        }




        $scope.updateObjects = function () {
            $timeout(function () {
                $(".picker").datepicker({
                    showOn: 'button',
                    buttonImage: 'static/images/open-iconic-master/png/calendar-2x.png',
                    buttonImageOnly: true,
                    dateFormat: 'yy/mm/dd'
                });
                $element.find('.demo-header-searchbox').on('keydown', function (ev) {
                    ev.stopPropagation();
                });
            }, 0);
        };


        $scope.editValueRow = function (val) {
            var gt = $http.get("/api/v1/datatablevalues/" + val.id + "/");

            gt.then(function (data) {
                $scope.values.cols = data.values;
                $scope.values.id = data.id;
            });

            // //console.log(val)

        }

        $scope.removeValueRow = function (val) {

            var gt = $http.delete("/api/v1/datatablevalues/" + val.id + "/");


            swal({
                title: "حذف رکورد",
                text: "آیا از حذف رکورد انتخابی اطمینان دارید",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "بله",
                closeOnConfirm: false
            }, function () {
                gt.then(function (data) {
                    $rootScope.$broadcast("showToast", "با موفقیت حذف شد");
                    $scope.getData();
                    $scope.resetValues();
                    swal("حذف شد!", "جهت ثبت تغییرات دکمه را کلیک کنید در غیر اینصورت صفحه را ببندید", "success");
                });
            });


            // //console.log(val)

        }

        $scope.findTrueValue = function (col, vals) {
            // debugger;
            for (var i = 0; vals.values.length > i; i++) {
                if (vals.values[i].fieldname == col.fieldname) {
                    return {val: vals.values[i].value, owner: vals.values[i].owner}
                }


            }
        }


        $scope.resetValues = function () {
            for (var i = 0; $scope.values.cols.length > i; i++) {
                $scope.values.cols[i].value = null;
            }
        }


        $scope.searchTerm;
        $scope.clearSearchTerm = function () {
            $scope.searchTerm = '';
        };


        $scope.GoToPage = function (url) {
            var gt = $http.get(url);
            gt.then(function (data) {
                $scope.values = data.data;
            })
        }


        $scope.addValue = function () {
            var pst;
            for (var i = 0; $scope.values.cols.length > i; i++) {
                if ($scope.values.cols[i]["dataType"] == "date") {
                    // if ($scope.values.cols[i]["value"] == "") {
                    //     $scope.values.cols[i]["value"] = "0"
                    // }
                    // $scope.values.cols[i]["value"] = 13000000 + parseInt($scope.values.cols[i]["value"]);
                }
                if ($scope.values.cols[i]["dataType"] == "time") {
                    if ($scope.values.cols[i]["value"] == "") {
                        $scope.values.cols[i]["value"] = "0000"
                    }
                    $scope.values.cols[i]["value"] = parseInt($scope.values.cols[i]["value"]);
                }
            }


            if (!($scope.values.id)) {
                pst = $http.post("/api/v1/datatablevalues/" + $stateParams.DataTableId + "/postValue/", $scope.values.cols);
            } else {

                pst = $http.patch("/api/v1/datatablevalues/" + $scope.values.id + "/", {
                    values: $scope.values.cols,
                    id: $scope.values.id

                });
            }


            pst.then(function (data) {
                $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
                $scope.getData();
                $scope.resetValues();
                $scope.values.id = null;

            })

        };

        $scope.filters = [];

        $scope.convertToNew = function () {
            var pst = $http.get("/api/v1/datatablevalues/convertToNew/");
            pst.then(function (data) {
                $rootScope.$broadcast("showToast", "با موفقیت تبدیل شد");

            })
        }

        $scope.makeFilter = function (download) {
            var pst;
            if (download == 'yes') {

                $http({
                    url: "/api/v1/datatablevalues/" + $stateParams.DataTableId + "/filterData/?xls=yes&dt=" + $stateParams.DataTableId,
                    method: "POST",
                    data: $scope.filters, //this is your json data string
                    headers: {
                        'Content-type': 'application/json'
                    },
                    responseType: 'arraybuffer'
                }).then(function (data, status, headers, config) {
                    var blob = new Blob([data], {type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"});
                    var objectUrl = URL.createObjectURL(blob);
                    window.open(objectUrl);
                }).catch(function (data, status, headers, config) {
                    //upload failed
                });


                // pst = $http.post("/api/v1/datatablevalues/" + $stateParams.DataTableId + "/filterData/?xls=yes&dt=" + $stateParams.DataTableId, $scope.filters);
            }
            else {
                pst = $http.post("/api/v1/datatablevalues/" + $stateParams.DataTableId + "/filterData/?dt=" + $stateParams.DataTableId, $scope.filters);
                pst.then(function (data) {
                    $scope.values = data.data;
                    // $scope.filters = angular.copy(data.cols);
                    $scope.updateObjects();
                })
            }


        }


        $scope.showFilter = false;

        $scope.showVFilter = function () {
            $scope.showFilter = !$scope.showFilter;
            if (!$scope.showFilter) {
                $scope.getData();
            }
        }

        $scope.getData = function () {
            var pst = $http.get("/api/v1/datatablevalues/?dt=" + $stateParams.DataTableId);
            pst.then(function (data) {
                $scope.values = data.data;
                $scope.filters = angular.copy(data.cols);
                $scope.updateObjects();
            })
        }

        $scope.getData();


    });