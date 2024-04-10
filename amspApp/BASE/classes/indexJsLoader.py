from amsp.settings import STATIC_URL


class IndexLoaders:
    jsList = [
        "bower_components/jquery/jquery-1.12.4.js",
        # "bower_components/noconfict.js"
        "bower_components/jquery-ui/ui/minified/jquery-ui.min.js",
        "bower_components/bootstrap/dist/js/popper.min.js",

        # "bower_components/pivottable/dist/tips_data.min.js",

        "bower_components/bootstrap/dist/js/bootstrap.min.js",
        "bower_components/bootstrap/dist/js/bootstrap.bundle.min.js",
        "bower_components/jquery.cookie.js",
        # "bower_components/jalalijscalendar/jalali.js",
        # "bower_components/jalalijscalendar/calendar.js",
        # "bower_components/jalalijscalendar/calendar-setup.js",
        # "bower_components/jalalijscalendar/lang/calendar-fa.js",
        "bower_components/Scroll/jquery.mCustomScrollbar.concat.min.js",


        "bower_components/angular/angular.min.js",
        "bower_components/angular/angular-resource.min.js",
        "bower_components/md-table/md-table.js",

        "bower_components/angular/angular-animate.min.js",
        "bower_components/angular/angular-route.min.js",
        "bower_components/angular/angular-aria.min.js",
        "bower_components/angular/angular-messages.min.js",
        "bower_components/angular-material/angular-material.min.js",
        "bower_components/angular-material/modules/js/button/button.js",
        "bower_components/angular-material/modules/js/tooltip/tooltip.js",
        "bower_components/angular-material/modules/js/toolbar/toolbar.js",
        "bower_components/angular-material/modules/js/menu/menu.js",
        "bower_components/angular-material/modules/js/menuBar/menuBar.js",
        "bower_components/angular-material/modules/js/sidenav/sidenav.js",
        "bower_components/angular-material/modules/js/list/list.js",
        "bower_components/angular-material/modules/js/toast/toast.js",
        "bower_components/handsontable/handsontable.full.min.js",
        # "bower_components/ws4redis/ws4redis.js",

        "bower_components/handsontable/languages/all.min.js",
        "bower_components/handsontable/ngHandsontable.min.js",

        "angularThings/others/fitlers/moment.js",
        "angularThings/others/fitlers/moment-jalaali.js",
        # "angularThings/others/directives/topnav/chats.js",
        "angularThings/others/directives/topnav/notifications.js",

        # "bower_components/jquery-treetable.js",
        "bower_components/ng-file-upload/ng-file-upload.min.js",
        "bower_components/angular/angular-cookies.js",
        "bower_components/ocLazyLoad/ocLazyLoad.min.js",
        "bower_components/jqueryuidatepicker/scripts/jquery.ui.datepicker-cc.all.min.js",

        # "bower_components/checklist-model/checklist-model.js",

        # "bower_components/google-firebase/firebase-app.js",
        # "bower_components/google-firebase/firebase-analytics.js",
        # "bower_components/google-firebase/firebase-auth.js",
        # "bower_components/google-firebase/firebase-firestore.js",
        # "bower_components/google-firebase/firebase-messaging.js",

        "bower_components/perfect-scrollbar/js/perfect-scrollbar.js",
        "angularThings/others/extras/modernizr.custom.js",
        "bower_components/perfect-scrollbar/js/perfect-scrollbar.jquery.js",
        "bower_components/ui-router/release/angular-ui-router.min.js",
        "bower_components/angular-ui-tree-master/dist/angular-ui-tree.min.js",

        "bower_components/angular-scroll-glue/src/scrollglue.js",
        # "bower_components/classie/classie.js",
        "bower_components/picker.js",
        "bower_components/ckeditor/full/ckeditor.js",
        "bower_components/ckeditorAngularJs/ng-ckeditor.js",
        "bower_components/qrcode/qrcode.min.js",
        "bower_components/angular-progress-button-styles/dist/angular-progress-button-styles.min.js",
        "bower_components/angular-translate/angular-translate.js",
        "bower_components/angular-translate-loader-url/angular-translate-loader-url.js",
        "bower_components/angular-translate-loader-static-files/angular-translate-loader-static-files.js",
        "bower_components/ui-mask-master/dist/mask.min.js",
        "bower_components/angular-dragdrop-master/src/angular-dragdrop.js",
        "bower_components/angular-bootstrap/ui-bootstrap-tpls.min.js",
        "bower_components/sweetalert/sweetalert.min.js",


        "bower_components/money/ko_money.js",
        # "bower_components/md-data-table-master/dist/md-data-table.min.js",
        "bower_components/angular-timeline/angular-scroll-animate.js",
        "bower_components/angular-timeline/angular-timeline.js",
        "bower_components/angular-ivh-treeview/dist/ivh-treeview.min.js",
        # "bower_components/angular-material/docs.js",
        "bower_components/ws4redis/ws4redis.js",
        "bower_components/ngProgress/build/ngprogress.min.js",
        # "bower_components/tree/tree.js",
        "bower_components/ui-select/dist/select.min.js",
        "bower_components/angular-qrcode/qrcode.min.js",
        "bower_components/angular-qrcode/angular-qr.min.js",


        "bower_components/d3/d3.js",
        'bower_components/bpmn-modeler/vendor/disttt2.js',
        "bower_components/angular-form-gen/angular-form-gen.js",
        "bower_components/angular-form-gen/classes/fgFieldController.js",
        "bower_components/angular-form-gen/classes/fgField.js",
        "bower_components/angular-form-gen/classes/fgConfigProvider.js",
        "bower_components/angular-form-gen/classes/templateCache.js",
        "bower_components/angular-form-gen/classes/fgTableCssClassInjector.js",
        "bower_components/angular-form-gen/classes/fgForm.js",
        "bower_components/angular-form-gen/classes/fgFormController.js",
        "bower_components/angular-form-gen/classes/fgEdit.js",
        "bower_components/angular-form-gen/classes/fgEditCanvasFieldProperties.js",
        "bower_components/angular-form-gen/classes/fgSchemaController.js",
        "bower_components/codemirror/lib/codemirror.js",
        "bower_components/codemirror/mode/sql/sql.js",
        "bower_components/codemirror/mode/python/python.js",
        "bower_components/ui-codemirror/src/ui-codemirror.js",

        "bower_components/chart.js/dist/chart.min.js",
        "bower_components/chart.js/chartjs-plugin-datalabels/dist/chartjs-plugin-datalabels.min.js",
        "bower_components/chart.js/chartjs-plugin-gauge/chartjs-gauge/dist/chartjs-gauge.min.js",
        # "bower_components/chart.js/src/adapters/my-adapter.moment.js",
        # "bower_components/angular-chart.js/dist/angular-chart.min.js",



        "angularThings/app_init.js",
        "angularThings/app_settings.js",
        "angularThings/app_routes_details.js",
        "angularThings/app_routes.js",


        "angularThings/companiesManagement/companiesManagmentService.js",
        "angularThings/others/extras/progressButton.js",
        "angularThings/authentication/loginCtrl.js",
        "angularThings/authentication/logoutCtrl.js",
        "angularThings/others/controllers/dashboard.js",
        "angularThings/others/generalService.js",
        "angularThings/others/controllers/userTableCtrl.js",
        "angularThings/others/controllers/groupTableCtrl.js",
        "angularThings/others/controllers/timepickerCtrl.js",
        "angularThings/others/controllers/sidebarCtrl.js",
        "angularThings/authentication/registerCtrl.js",
        "angularThings/others/controllers/ModalAreYouSureInstanceCtrl.js",
        "angularThings/others/controllers/ModalPermissionDeniedInstanceCtrl.js",
        "angularThings/others/controllers/dropdownCtrl.js",
        "angularThings/companiesManagement/companyTableCtrl.js",
        "bower_components/content-editable.js",
        "bower_components/angular/ngMask.min.js",
        "angularThings/others/directives/topnav/topnav.js",
        "angularThings/others/directives/sidebar/sidebar.js",
        "angularThings/others/directives/stats/stats.js",
        "angularThings/others/directives/content-editable/content-editable.js",
        "angularThings/others/directives/avatar/avatarDirective.js",
        "angularThings/others/directives/HtmlContainerDirective.js",
        "angularThings/authentication/authentication.service.js",
        "angularThings/others/directives/dispatcher/ngRepeatFinished.js",
        "angularThings/others/extras/getServerTime.js",
        "angularThings/Letter/FileUploader/classUploader.js",

        "angularThings/others/fitlers/jalaliDateFilter.js",
        "angularThings/others/directives/select_position_directive/selectPositionDirective.js",

        "angularThings/BI/BIPages/directives/num2persian-min.js",
        "angularThings/BI/BIPages/directives/chart_funcs.js",
        "angularThings/BI/BIPages/directives/chart_options.js",
        "angularThings/BI/BIPages/directives/bpms_related_simple_table.js",
        "angularThings/BI/BIPages/directives/bpms_related_chart.js",
        # "angularThings/BI/BIPages/directives/bi_single_value.js",
        "angularThings/BI/BICharts/directives/bi_chart.js",
        "angularThings/BI/BICharts/directives/bi_top5.js",
        "angularThings/BI/BICharts/directives/bi_table.js",
        "angularThings/BI/BICharts/directives/bi_single_value.js",
        "angularThings/BI/BICharts/directives/bi_latestdatatable.js",
        "angularThings/Financial/others/json2table.js",

    ]

    def getJsLoads(self, version):
        res = []
        for js in self.jsList:
            res.append(STATIC_URL + js + "?v=" + version)
        return res
