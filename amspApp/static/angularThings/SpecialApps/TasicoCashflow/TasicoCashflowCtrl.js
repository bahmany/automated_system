'use strict';

angular.module('AniTheme').controller(
    '****CashflowCtrl',
    function ($scope,
              $translate,
              $q, $filter,
              $http,
              $location,
              $rootScope,
              $timeout) {

        $scope.Projects = [];

        $scope.listProjects = function () {
            $http.get("/SpecialApps/****Cashflow/api/v1/projects/").then(function (data) {
                var projects = data.data;
                for (var i = 0; projects.length > i; i++) {

                    // گشایش اعتبار
                    var dt = projects[i]["detailLink"]["daysFromFactoryToShip"] + projects[i]["detailLink"]["daysFromShipToIranPort"] + projects[i]["detailLink"]["daysFromIranPortToFactory"];
                    dt = moment(projects[i]["****Date"], "YYYY-MM-DD").add('days', dt * -1)
                    projects[i]["dateGoshayeshEtebar"] = dt;
                    projects[i]["dateGoshayeshEtebarSh"] = $filter('jalaliDate')(dt.format("YYYY/MM/DD"), 'jYYYY/jMM/jDD');
                    // حمل به کشتی
                    var dt = projects[i]["detailLink"]["daysFromFactoryToShip"] + projects[i]["detailLink"]["daysFromIranPortToFactory"];
                    dt = moment(projects[i]["****Date"], "YYYY-MM-DD").add('days', dt * -1)
                    projects[i]["dateToShip"] = dt;
                    projects[i]["dateToShipSh"] = $filter('jalaliDate')(dt.format("YYYY/MM/DD"), 'jYYYY/jMM/jDD');
                    // انتقال به کمرگ ایران
                    var dt = projects[i]["detailLink"]["daysFromIranPortToFactory"];
                    dt = moment(projects[i]["****Date"], "YYYY-MM-DD").add('days', dt * -1)
                    projects[i]["dateToIranPort"] = dt;
                    projects[i]["dateToIranPortSh"] = $filter('jalaliDate')(dt.format("YYYY/MM/DD"), 'jYYYY/jMM/jDD');
                    // رسیدن به کارخانه
                    var dt = 0;
                    dt = moment(projects[i]["****Date"], "YYYY-MM-DD").add('days', dt * -1)
                    projects[i]["****Date"] = dt;
                    projects[i]["****DateSh"] = $filter('jalaliDate')(dt.format("YYYY/MM/DD"), 'jYYYY/jMM/jDD');
                    // سر رسید
                    var dt = projects[i]["detailLink"]["daysFromShippingToLC"];
                    dt = projects[i]["****Date"].add("days", dt);
                    projects[i]["dateLC"] = dt;
                    projects[i]["dateLCSh"] = $filter('jalaliDate')(dt.format("YYYY/MM/DD"), 'jYYYY/jMM/jDD');
                }
                $scope.Projects = data.data;
            })
        };

        $scope.listProjects();

        $scope.Dates = [];
        $scope.listProjectsByDate = function () {
            $http.get("/SpecialApps/****Cashflow/api/v1/projects/getByDate/").then(function (data) {
                $scope.Dates = data.data;
            })
        };
        $scope.PayDetails = [];
        $scope.IncomeDetails = [];
        $scope.PayClick = function (item) {
            $("#modal_pay_detail").modal("show");
            $scope.PayDetails = item.payDetails;
        };
        $scope.IncomeClick = function (item) {
            $("#modal_incomdetail").modal("show");
            $scope.IncomeDetails = item.incomeDetails;
        };
        $scope.listProjectsByDate();


        $scope.GenerateMongoCache = function () {
            $http.get("/SpecialApps/****Cashflow/api/v1/projects/generateMongoCache/").then(function (data) {
                alert("Cache generated");
            })
        }

        $scope.GetDailyCache = function () {
            $http.get("/SpecialApps/****Cashflow/api/v1/daily/").then(function (data) {
            });
        }
        $scope.GetMonthlyCache = function () {
            $http.get("/SpecialApps/****Cashflow/api/v1/daily/getMonthly/").then(function (data) {
            });
        }


        $scope.QueryToMongo = "";
        $scope.QueryToTransform = "";
        $scope.QueryResult = "";


        $scope.ExecuteIt = function () {
            var js = JSON.parse($scope.QueryToMongo);
            $http.post("/SpecialApps/****Cashflow/api/v1/daily/getMonthly/", js).then(function (data) {
                var trans = JSON.parse($scope.QueryToTransform);
                $scope.QueryResult = JSON.stringify(data.data);
                document.getElementById('dynamic_table').innerHTML = json2html.transform(data.data, trans);
            });
        }

        $scope.GetMonthly = function () {
            $scope.QueryToMongo = '{"$group": {"_id": "$current_sh_month", "income": {"$sum": "$income"}, "pay": {"$sum": "$pay"}}}';
            $scope.QueryToTransform = '{"<>":"li","html":"${_id} (${income}) (${pay})"}';

        }
        $scope.GetSimpleList = function () {
            $http.get("/SpecialApps/****Cashflow/api/v1/daily/getSimpleList/").then(function (data) {

            });
        }

    });