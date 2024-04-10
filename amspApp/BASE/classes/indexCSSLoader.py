from amsp.settings import STATIC_URL


class IndexCSSLoaders:
    cssList = [
        # "bower_components/bootstrap/dist/css/bootstrap.min.css",
        # "bower_components/bootstrap/dist/css/bootstrap-theme.min.css",
        "bower_components/bootstrap/dist/css/bootstrap-rtl.min.css",

        "bower_components/animate.css/animate.css",
        "bower_components/Scroll/jquery.mCustomScrollbar.min.css",
        "bower_components/font-awesome/css/all.min.css",
        # "bower_components/textAngular/src/textAngular.css",
        "bower_components/perfect-scrollbar/css/perfect-scrollbar.css",
        "bower_components/sweetalert/sweetalert.css",
        # "bower_components/bootstrap-select/dist/css/bootstrap-select.min.css",

        "bower_components/ckeditorAngularJs/ng-ckeditor.css",
        # "bower_components/angular-ui-tree-master/dist/angular-ui-tree.min.css",
        "bower_components/jqueryuidatepicker/styles/jquery-ui-1.8.14.css",
        # "bower_components/angular-clock-master/dist/angular-clock.css",
        "bower_components/angular-form-gen/angular-form-gen.min.css",
        # "bower_components/angular-progress-button-styles/dist/angular-progress-button-styles.min.css",
        # "styles/app-blue.css",
        # "bower_components/introjs/minified/introjs.min.css",
        # "bower_components/introjs/minified/introjs-rtl.min.css",
        # "bower_components/pivottable/dist/pivot.min.css",

        # "bower_components/datatables/DataTables-1.10.18/css/dataTables.jqueryui.min.css",
        # "bower_components/chart/nv.d3.min.css",
        # "bower_components/jalalijscalendar/skins/calendar-system.css",
        # "bower_components/ng-file-upload/angular-filemanager-master/src/css/angular-filemanager.css",
        # "bower_components/jalalijscalendar/skins/calendar-system.css",
        # "bower_components/angular-timeline/angular-timeline.css",
        # "bower_components/angular-timeline/angular-timeline-bootstrap.css",
        # "bower_components/angular-timeline/angular-timeline-animations.css",

        "bower_components/ngProgress/ngProgress.css",
        # "bower_components/ui-select/dist/select.min.css",
        "styles/fonts.css",
        # "styles/mrbStyles.css",
        "styles/printcss.css",
        # "styles/docs.css",

        "bower_components/angular-material/angular-material.min.css",
        "bower_components/angular-material/angular-material.layouts.min.css",
        "bower_components/angular-material/modules/js/button/button.css",
        "bower_components/angular-material/modules/js/tooltip/tooltip.css",
        "bower_components/angular-material/modules/js/toolbar/toolbar.css",
        "bower_components/angular-material/modules/js/menu/menu.css",
        "bower_components/angular-ivh-treeview/dist/ivh-treeview.min.css",
        "bower_components/angular-ivh-treeview/dist/ivh-treeview-theme-basic.css",
        "bower_components/angular-material/modules/js/menuBar/menuBar.css",
        "bower_components/angular-material/modules/js/sidenav/sidenav.css",
        "bower_components/angular-material/modules/js/list/list.css",
        "bower_components/angular-material/modules/js/toast/toast.css",
        # "bower_components/handsontable/handsontable.full.min.css",
        # "bower_components/Chart.js/dist/Chart.min.css",
        # "bower_components/angular-chart.js/dist/angular-chart.min.js",

        "bower_components/md-table/md-table.css",
        "bower_components/md-table/material-icons.css",

        # "bower_components/angular-ui-tree-master/dist/angular-ui-tree.min.css",
        # "bower_components/webdatarocks-1.3.3/webdatarocks.min.css",

        "styles/myStyles.css",
        "bower_components/ace-master/build/css/ace.css",
        "bower_components/ace-master/build/css/theme/sqlserver.css",
        "bower_components/codemirror/lib/codemirror.css",

    ]

    def getCSSLoads(self, version):
        res = []
        for css in self.cssList:
            res.append(STATIC_URL + css + "?v=" + version)
        return res
