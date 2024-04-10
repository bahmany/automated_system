'use strict';
// The restrict option is typically set to:
// 'A' - only matches attribute name
// 'E' - only matches element name
// 'C' - only matches class name
// 'M' - only matches comment
angular.module('AniTheme').directive('bpmsRelatedSimpleTable', function () {

    return {
        templateUrl: '/static/angularThings/BI/BIPages/directives/bpms_related_simple_table.html',
        restrict: 'E',
        scope: {
            currentcell: '=currentcell'
        },
        replace: true,
        controller: ['$scope', '$element', '$attrs', '$transclude', '$http',
            function ($scope, $element, $attrs, $transclude, $http) {
                $scope.getit = function () {
                    $http.post("/api/v1/bi_dashboard_page/get_type_44312/", $scope.currentcell).then(function (data) {
                        $scope.current_data = data.data
                        $scope.create_table(data.data.data);
                    })
                }

                $scope.create_table = function (myBooks) {
                    // EXTRACT VALUE FOR HTML HEADER.
                    // ('Book ID', 'Book Name', 'Category' and 'Price')
                    var col = [];
                    for (var i = 0; i < myBooks.length; i++) {
                        for (var key in myBooks[i]) {
                            if (col.indexOf(key) === -1) {
                                col.push(key);
                            }
                        }
                    }
                    // CREATE DYNAMIC TABLE.
                    var table = document.createElement("table");

                    // CREATE HTML TABLE HEADER ROW USING THE EXTRACTED HEADERS ABOVE.

                    var thead = document.createElement("thead")
                    var thead_tr = thead.insertRow(-1)
                    for (var i = 0; i < col.length; i++) {
                        var th = document.createElement("th");      // TABLE HEADER.
                        th.innerHTML = col[i];
                        thead_tr.appendChild(th);
                    }
                    table.appendChild(thead);


                    var tbody = document.createElement("tbody")        // TABLE ROW.

                    // ADD JSON DATA TO THE TABLE AS ROWS.
                    for (var i = 0; i < myBooks.length; i++) {

                        var tr = tbody.insertRow(-1);

                        for (var j = 0; j < col.length; j++) {
                            var tabCell = tr.insertCell(-1);
                            tabCell.innerHTML = myBooks[i][col[j]];
                        }
                    }
                                        table.appendChild(tbody);



                    table.className = "table table-condensed table-bordered table-striped"
                    $scope.table = table.outerHTML;

                }

                $scope.getit();
            }
        ],
        // link: function (scope, element, attr) {
        //     debugger;
        // }
    }
});
