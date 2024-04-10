'use strict';

angular.module('RahsoonApp').controller(
    'dashboardCtrl',
    function ($scope,
              $translate,
              $q,
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
        ]
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


        $scope.Estekhdam = {};
        $scope.Education = {};
        $scope.EducationItem = {};
        $scope.Educations = [];
        $scope.Estekhdam = {};
        $scope.Estekhdam.Educations = [];
        $scope.Estekhdam.Languages = [];
        $scope.Estekhdam.Dorehs = [];
        $scope.Estekhdam.Experiences = [];
        $scope.Estekhdam.Softwares = [];
        $scope.Estekhdam.Jobs = [];
        $scope.Education = {};
        $scope.Language = {};
        $scope.Doreh = {};
        $scope.Experience = {};
        $scope.Software = {};
        $scope.Job = {};
        $scope.SearchFilter = {};
        $scope.Require = {};
// education
// ---------------------------------------------------------------
// ---------------------------------------------------------------
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
            //if (!(item.SelectedBranch)){
            //    sweetAlert("اخطار", "لطفا سطح تحصیلات خود را مشخص نمایید", "error");
            //    return;
            //}

            if (!(item.LicenseType)) {
                sweetAlert("اخطار", "لطفا نوع مدرک را در مرحله ی دوم مشخص نمایید", "error");
                return;
            }
            if (!($scope.SelectedReshteh.value)) {
                sweetAlert("اخطار", "لطفا رشته ی تحصیلی را لیستی که ظاهر می شود انتخاب نمایید - رشته های تحصیلی معتبر هستند که از لیست ظاهر شده انتخاب میشوند", "error");

                return;
            }

            $scope.Educations.push(item);
            $scope.EducationItem = {};
            $scope.SelectedReshteh = {};

        };
        $scope.EditEducationItem = function (item, index) {
            $scope.EducationItem = item;
            $scope.SelectedReshteh = {
                value: item.SelectedBranch,
                display: item.SelectedBranch
            };
            $scope.Educations.splice(index, 1);

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
                $scope.Educations.splice(index, 1);
                $scope.$apply();
                swal("حذف شد", "داده ی مورد نظر شما حذف شد - در صورتی این تغییر در سوابق شما ثبت خواهد شد که دکمه ی ذخیره در سوابق را انتخاب نمایید", "success");

            });
        }
// ---------------------------------------------------------------
// ---------------------------------------------------------------
// languages
        $scope.LanguagesAddToList = function (item) {
            $scope.Language = {
                Name: "English",
                Skill: "خوب"
            };
            $scope.Estekhdam.Languages.push(item);

        }
        $scope.LanguagesEdit = function (item, index) {
            $scope.Language = item;
            $scope.Estekhdam.Languages.splice(index, 1);
        }
        //-------------------------------
        //-------------------------------
        //-------------------------------
        //------ Add to doreh --------
        $scope.DorehsAddToList = function (item) {
            $scope.Estekhdam.Dorehs.push(item);
            $scope.Doreh = {};

        }
        $scope.DorehEdit = function (item, index) {
            $scope.Doreh = item;
            $scope.Estekhdam.Dorehs.splice(index, 1);
        }
        //-------------------------------
        //-------------------------------
        //-------------------------------
        //--------------Exprience---------
        $scope.ExperiencesAddToList = function (item) {
            $scope.Estekhdam.Experiences.push(item);
            $scope.Experience = {};

        }
        $scope.ExperiencesEdit = function (item, index) {
            $scope.Experience = item;
            $scope.Estekhdam.Experiences.splice(index, 1);
        }
        //-------------------------------
        //-------------------------------
        //-------------------------------
        //-------------------------------
        //--------------Software---------
        $scope.SoftwaresAddToList = function (item) {
            $scope.Estekhdam.Softwares.push(item);
            $scope.Software = {};

        }
        $scope.SoftwaresEdit = function (item, index) {
            $scope.Software = item;
            $scope.Estekhdam.Softwares.splice(index, 1);
        }
        //-------------------------------
        //-------------------------------
        //-------------------------------
        //-------------------------------
        //--------------Job---------
        $scope.JobAddToList = function (item) {
            $scope.Estekhdam.Jobs.push(item);
            $scope.Job = {};

        };
        $scope.JobEdit = function (item, index) {
            $scope.Job = item;
            $scope.Estekhdam.Jobs.splice(index, 1);
        };
        //-------------------------------
        //-------------------------------

    });