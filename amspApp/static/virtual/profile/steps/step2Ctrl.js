'use strict';

angular.module('RahsoonApp').controller(
    'step2Ctrl',
    function ($scope,
              $translate,
              $q, $location,
              $http,
              $rootScope,
              $timeout) {
        $scope.Education = {};
        $scope.Education.items = [];
        $scope.EducationItem = {};

        //$scope.GetProfiles();
        $scope.sortOrder = ["کاردانی",
            "کارشناسی",
            "کارشناسی ارشد",
            "دکتری",
            "حوزوی",
            "پزشکی"];

        $scope.GetHigherEducation = function () {
            var sort = -1;
            var final = {};
            if (!($scope.Education.items)){
                return
            }
            for (var i = 0; $scope.Education.items.length > i; i++) {
                for (var c = 0; $scope.sortOrder.length > c; c++) {
                    if ($scope.Education.items[i].Education == $scope.sortOrder[c]) {
                        if (c >= sort) {
                            sort = c;
                            final = $scope.Education.items[i];
                        }
                    }
                }
            }
            return final
        };


        $scope.Get = function (step, jsonObjStr) {
            $http.get("/reg/api/v1/login/" + step + "/getstep/").then(function (data) {
                //debugger;
                $scope[jsonObjStr] = data.data;

            })
        };

        //$scope.Get(currentStep, jsonObjStr);

        $scope.Post = function (step, jsonObj) {
            var ifEducationEntered = true;

            if (!($scope.Education)) {
                ifEducationEntered = false;
            }

            if (!($scope.Education.EducationType)) {
                ifEducationEntered = false;
            }
            if ($scope.Education.EducationType == "دارای تحصیلات دانشگاهی") {
                if (!($scope.Education.items)) {
                    ifEducationEntered = false;
                } else {
                    if ($scope.Education.items.length == 0) {
                        ifEducationEntered = false;
                    }
                }
            } else {
                $scope.Education.items = []
            }

            if (ifEducationEntered == false) {
                swal("خطا", "لطفا اطلاعات تحصیلی را بدرستی ثبت نمایید - اگر دارای تحصیلات دانشگاهی هستید ابتدا سطوح تحصیلاتی را به لیست اضافه نمایید", "error");
                return
            }


            var result = {};
            var ff = {};
            ff = $scope.GetHigherEducation();
            for (var key in jsonObj) result[key] = jsonObj[key];
            for (var key in ff) result[key] = ff[key];
            $http.post("/reg/api/v1/login/" + step + "/step/", result).then(function (data) {
                $rootScope.$broadcast("showToast", "اطلاعات شما با موفقیت ثبت شد");
                $location.url("/home/profile/step" + (parseInt(step) + 1).toString());

            })
        }


        $scope.Get("2", "Education");
        $scope.Branches = EducationBranches;
        $scope.Education_simulateQuery = false;
        $scope.Education_isDisabled = false;
        $scope.Education_states = Education_loadAll();
        $scope.Education_querySearch = Education_querySearch;
        $scope.Education_selectedItemChange = Education_selectedItemChange;
        $scope.Education_searchTextChange = Education_searchTextChange;
        $scope.Education_newState = Education_newState;
        $scope.Education_searchText = "ا";
        function Education_newState(state) {
            //alert("Sorry! You'll need to create a Constituion for " + state + " first!");
        }

        $scope.Education_sortOrder = [
            {"name": "کاردانی", "value": 1, "contains": 0},
            {"name": "کارشناسی", "value": 2, "contains": 0},
            {"name": "کارشناسی ارشد", "value": 3, "contains": 0},
            {"name": "دکتری", "value": 4, "contains": 0},
            {"name": "حوزوی", "value": 5, "contains": 0},
            {"name": "پزشکی", "value": 6, "contains": 0}];


        function Education_querySearch(query) {
            var results = query ? $scope.Education_states.filter(Education_createFilterFor(query)) : self.states,

                deferred;

            //if (query == ""){
            //    return Education_loadAll();
            //}
            if ($scope.Education_simulateQuery) {
                deferred = $q.defer();
                $timeout(function () {
                    deferred.resolve(results);
                }, Math.random() * 1000, false);
                return deferred.promise;
            } else {
                return results;
            }
        }

        function Education_searchTextChange(text) {
            //$log.info('Text changed to ' + text);
        }

        $scope.SelectedReshteh = {};
        function Education_selectedItemChange(item) {
            $scope.EducationItem.SelectedBranch = item.display;
            $scope.SelectedReshteh = item;
        }

        function Education_createFilterFor(query) {
            var lowercaseQuery = angular.lowercase(query);
            return function filterFn(state) {
                return (state.value.indexOf(lowercaseQuery) === 0);
            };
        }

        function Education_loadAll() {
            var allStates = $scope.Branches;
            return allStates.map(function (state) {
                return {
                    value: state.toLowerCase(),
                    display: state
                };
            });
        }

        $scope.EducationAddToList = function (item) {

            if (!(item.Education)) {
                sweetAlert("اخطار", "لطفا نوع مدرک را در مرحله ی دوم مشخص نمایید", "error");
                return;
            }
            if (!($scope.SelectedReshteh.value)) {
                sweetAlert("اخطار", "لطفا رشته ی تحصیلی را لیستی که ظاهر می شود انتخاب نمایید - رشته های تحصیلی معتبر هستند که از لیست ظاهر شده انتخاب میشوند", "error");

                return;
            }
            if (!($scope.Education.hasOwnProperty("items"))) {
                $scope.Education.items = [];
            }
            $scope.Education.items.push(item);
            $scope.EducationItem = {};
            $scope.SelectedReshteh = {};

        };
        $scope.EditEducationItem = function (item, index) {
            $scope.EducationItem = item;
            $scope.SelectedReshteh = {
                value: item.SelectedBranch,
                display: item.SelectedBranch
            };


            $scope.Education.items.splice(index, 1);

        };
        $scope.RemoveEducationItem = function (index) {
            swal({
                title: "آیا اطمینان دارید",
                text: "داده ی انتخابی شما از سوابقتان حدف خواهد شد",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "بله حذف شود",
                closeOnConfirm: false
            }, function () {
                $scope.Education.items.splice(index, 1);
                $scope.$apply();
                swal("حذف شد", "داده ی مورد نظر شما حذف شد - در صورتی این تغییر در سوابق شما ثبت خواهد شد که دکمه ی ذخیره در سوابق را انتخاب نمایید", "success");

            });
        }

    })