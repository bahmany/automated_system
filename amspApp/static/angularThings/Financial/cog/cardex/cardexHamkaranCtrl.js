'use strict';

angular.module('AniTheme').controller(
    'CardexHamkaranCtrl',
    function ($scope,
              //$translate,
              $q,
              $http,
              $location,
              $rootScope,
              $timeout) {

        $scope.GetCardexFromHamkaran = function () {
            $http.get("/Financial/api/v1/cardexhamk/getFromHamkran/").then(function (data) {

            })
        };

        $scope.cardexs = {};
        $scope.list = function () {
            $http.get("/Financial/api/v1/cardexhamk/").then(function (data) {
                $scope.cardexs = data.data;
            })
        };

        // $scope.list();


        var tablePageChange = function (hii) {
            console.log(hii)
        }


        $scope.dataTableOpt = {
            // fnPageChange: tablePageChange,

            //custom datatable options
            "aLengthMenu": [[10, 50, 100, 200], [10, 50, 100, 200]],
            "bProcessing": true,
            "sAjaxSource": '/Financial/api/v1/cardexhamk/',
            "bServerSide": true,
            "aoColumns": [
                {"mData": "row.CodeTabaghe", "sTitle":"کد طبقه", "bSortable":false},
                {"mData": "row.NameTabaghe", "sTitle":"نام طبقه", "bSortable":false},
                {"mData": "row.CodeKala", "sTitle":"کد کالا"},
                {"mData": "row.NameKala", "sTitle":"نام کالا"},
                {"mData": "row.z_MeghdareMandePayamDoreh", "sTitle":"مقداری مانده پایان دوره", "sType":"numeric"},
                {"mData": "row.z_MablagheMandePayamDoreh", "sTitle":"ریالی مانده پایان دوره", "sType":"numeric"},
                {"mData": "row.z_MeghdareKhaleseTolidi", "sTitle":"مقداری خالص مصرف تولیدی", "sType":"numeric"},
                {"mData": "row.z_MablagheKhaleseTolidi", "sTitle":"ریالی خالص مصرف تولیدی", "sType":"numeric"}
            ]
        };


        /*  Initialse DataTables, with no sorting on the 'details' column  */
        // var oTable = $('#table2').dataTable({
        //     "aoColumnDefs": [{
        //         "bSortable": false,
        //         "aTargets": [0]
        //     }],
        //     "aaSorting": [
        //         [1, 'asc']
        //     ]
        // });
        /*  Add event listener for opening and closing details  */
        // $(document).on('click', '#table2 tbody td i', function () {
        //     var nTr = $(this).parents('tr')[0];
        //     if (oTable.fnIsOpen(nTr)) {
        //         /* This row is already open - close it */
        //         $(this).removeClass().addClass('fa fa-plus-square-o');
        //         oTable.fnClose(nTr);
        //     } else {
        //         /* Open this row */
        //         $(this).removeClass().addClass('fa fa-minus-square-o');
        //         oTable.fnOpen(nTr, fnFormatDetails(oTable, nTr), 'details');
        //     }
        // });

    });


