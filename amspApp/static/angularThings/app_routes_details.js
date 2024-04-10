function GenerateJsResolveFiles(files, cache, func) {
    if (!(func)) {
        func = function () {

        }
    }
    return {
        deps: ["$ocLazyLoad", function ($ocLazyLoad) {
            return $ocLazyLoad.load({
                name: 'OCletter',
                files: files
                , catch: cache
            }).then(
                func
            )
        }]
    }
}

function GenerateJsView(viewname, templateUrl, controller, controllerAs) {
    return {
        viewname: {
            templateUrl: templateUrl,
            controller: controller,
            controllerAs: controllerAs

        }
    }
}


function InjectToModule(componentName) {
    const lll = angular.module('AniTheme').requires;
    for (let i = 0; lll.length > i; i++) {
        if (lll[i] === componentName) {
            return
        }
    }
    angular.module('AniTheme').requires.push(componentName)
}


var routes_details = {
    'base': {
        abstract: true,
        url: '',
        templateUrl: '/page/base',
        controller: 'DashboardCtrl'
    },
    'freeRahsoon': {
        url: '/freeRahsoon',
        parent: 'base',
        resolve: GenerateJsResolveFiles(['/static/angularThings/authentication/forgetCtrl.js'], true),
        views: GenerateJsView('', '/page/freeRahsoon', 'RegisterCtrl', 'vm')
    },
    'welcomeBase': {
        url: '/Welcome',
        parent: 'base',
        templateUrl: '/page/welcomeBase',
        resolve: GenerateJsResolveFiles(['/static/angularThings/welcome/base.js'], true)
    },
    'welcomepage': {
        url: '/Page',
        parent: 'welcomeBase',
        templateUrl: '/page/welcomePage',
        resolve: GenerateJsResolveFiles(['/static/angularThings/FirstUse/FirstIntroCtrl.js'], true)
    },
    'welcomepageClient': {
        url: '/Page',
        parent: 'welcomeBase',
        templateUrl: '/page/welcomepageClient',
        resolve: GenerateJsResolveFiles(['/static/angularThings/FirstUse/FirstIntroCtrl.js'], true)
    },
    'selectnames': {
        url: '/Names',
        parent: 'welcomeBase',
        templateUrl: '/page/welcomeSelectNames',
        resolve: GenerateJsResolveFiles(['/static/angularThings/FirstUse/FirstIntroCtrl.js'], true)
    },
    'selectpics': {
        url: '/Pics',
        parent: 'welcomeBase',
        templateUrl: '/page/welcomeSelectPics',
        resolve: GenerateJsResolveFiles(['/static/angularThings/FirstUse/FirstIntroCtrl.js'], true)
    },
    'welcomeDone': {
        url: '/welcomeCompleted',
        parent: 'base',
        templateUrl: '/page/welcomeCompleted',
        resolve: GenerateJsResolveFiles(['/static/angularThings/FirstUse/FirstIntroCtrl.js'], true)
    },
    '404-page': {
        url: '/page/404-page',
        parent: 'base',
        templateUrl: '/404-page'
    },
    '_dash': {
        url: '/_dash',
        parent: 'base',
        templateUrl: '/page/_dash',
        resolve: GenerateJsResolveFiles(['/static/angularThings/Dashboard/DashboardCtrl.js'], true)
    },
    'dashboard': {
        url: '/dashboard',
        parent: 'base',
        templateUrl: '/page/dashboard',
        // resolve: GenerateJsResolveFiles([
        //     // '/static/bower_components/d3/d3.js'
        // ], true)
    },
    'home': {
        url: '/home',
        parent: 'dashboard',
        templateUrl: '/page/home',
        controller: 'HomeCtrl',
        resolve: GenerateJsResolveFiles([
            // '/static/bower_components/datatables/datatables.js',


            '/static/angularThings/widgets/dashboard_statitics/DashboardStaticticsDirective.js',
            '/static/angularThings/widgets/bpms_statics/BpmsStaticsDirective.js',
            '/static/angularThings/widgets/dashboard_calendar/DashboardCalendarDirective.js',
            '/static/angularThings/others/dashboardService.js',
            '/static/angularThings/others/controllers/homeCtrl.js'
        ], true)
    },

    'net': {
        url: '/net',
        parent: 'base',
        templateUrl: '/page/net',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/net/NETBaseCtrl.js',
        ], true)
    },

    'bi': {
        url: '/bi',
        parent: 'base',
        templateUrl: '/page/bibasepage',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/BI/BIBaseCtrl.js',
        ], true)
    },

    'bi-groups': {
        url: '/biGroups',
        parent: 'bi',
        templateUrl: '/page/bigroups',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/BI/BIGroup/BIGroupMemeberPartialCtrl.js',
            '/static/angularThings/BI/BIGroup/BIGroupsCtrl.js',
        ], true)
    },

    'bi-menus': {
        url: '/biMenus',
        parent: 'bi',
        templateUrl: '/page/bimenus',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/BI/BIMenus/BIMenuMemeberUsersPartialCtrl.js',
            '/static/angularThings/BI/BIMenus/BIMenuMemeberPartialCtrl.js',
            '/static/angularThings/BI/BIMenus/BIMenuItemsPartialCtrl.js',
            '/static/angularThings/BI/BIMenus/BIMenuCtrl.js',
        ], true)
    },




    'bi-dashboard-pages': {
        url: '/biDashboardPages',
        parent: 'bi',
        templateUrl: '/page/bidashboardpages',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/BI/BIGroup/BIGroupMemeberPartialCtrl.js',
            '/static/angularThings/BI/BIPages/BIDashboardPageCtrl.js',
        ], true)
    },

    'bi-dashboard-pages-design': {
        url: '/:id/dashboardpagesdesign',
        parent: 'bi',
        templateUrl: '/page/bidashboardpagesdashboard',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/BI/BIPages/BIPageDesignerCtrl.js',
        ], true)
    },


    'bi-charts': {
        url: '/biCharts',
        parent: 'bi',
        templateUrl: '/page/bicharts',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/BI/BICharts/BIChartsCtrl.js',
        ], true)
    },

    'bi-chart-design': {
        url: '/:id/chartdesign',
        parent: 'bi',
        templateUrl: '/page/bichartdesign',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/BI/BICharts/BIChartDesignerCtrl.js',
        ], true)
    },

    'bi-datasources': {
        url: '/biDatasources',
        parent: 'bi',
        templateUrl: '/page/bidatasources',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/BI/BIDatasources/BIDatasourcesCtrl.js',
        ], true)
    },

    'bi-datasources-design': {
        url: '/:id/sql',
        parent: 'bi',
        templateUrl: '/page/bisql',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/BI/BISqls/BISqlCtrl.js',
        ], true)
    },

    'bi-sqls': {
        url: '/biSqls',
        parent: 'bi',
        templateUrl: '/page/bisqls',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/BI/BISqls/BISqlsCtrl.js',
        ], true)
    },

    'bi-pages': {
        url: '/:id/biPages',
        parent: 'bi',
        templateUrl: '/page/bipages',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/BI/BIPages/BIShowPagesCtrl.js',
        ], true)
    },

    'bi-page': {
        url: '/:id/biPage',
        parent: 'bi',
        templateUrl: '/page/bipage',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/BI/BIPage/BIPageCtrl.js',
        ], true)
    },

    'bi-sample-page-for-ceo': {
        url: '/biSamplePageForCeo',
        parent: 'bi',
        templateUrl: '/page/bi_sample_page_for_ceo',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/BI/BISamplePageForCEO/sample_page_for_ceo_ctrl.js',
        ], true)
    },

    'bi-amare-roozaneh': {
        url: '/biAmareRoozaneh',
        parent: 'bi',
        templateUrl: '/page/amareroozaneh',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/BI/BIPages/specials/AmarRoozanehCtrl.js',
        ], true)
    },

    'edari': {
        url: '/edari',
        parent: 'base',
        templateUrl: '/page/edaribasepage',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/edari/EdariBaseCtrl.js',
        ], true)
    },

    'hz': {
        url: '/hz',
        parent: 'edari',
        templateUrl: '/page/hz',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/edari/hz/HZBaseCtrl.js',
        ], true)
    },
    'ez': {
        url: '/ez',
        parent: 'edari',
        templateUrl: '/page/ez',
        resolve: GenerateJsResolveFiles([
            '/static/bower_components/datatables/datatables.js',
            '/static/bower_components/datatables/datatables.min.css',

            '/static/bower_components/handsontable/handsontable.full.min.css',
            // '/static/bower_components/handsontable/ngHandsontable.min.js',

            // '/static/bower_components/jquery-ui/themes/base/jquery.ui.all.css',
            '/static/bower_components/datatables/DataTables-1.10.18/css/dataTables.jqueryui.min.css',
            '/static/angularThings/edari/ez/EzBaseCtrl.js',
        ], true)
    },
    'ezitem': {
        url: '/:id/details',
        parent: 'ez',
        templateUrl: '/page/ez-item',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/edari/ez/EzItemCtrl.js',
        ], true)
    },
    'ezlist': {
        url: '/list',
        parent: 'ez',
        templateUrl: '/page/ez-list',
        resolve: GenerateJsResolveFiles([
            '/static/bower_components/datatables/datatables.js',
            '/static/bower_components/datatables/datatables.min.css',

            '/static/bower_components/handsontable/handsontable.full.min.css',
            // '/static/bower_components/handsontable/ngHandsontable.min.js',

            // '/static/bower_components/jquery-ui/themes/base/jquery.ui.all.css',
            '/static/bower_components/datatables/DataTables-1.10.18/css/dataTables.jqueryui.min.css',
            '/static/angularThings/edari/ez/EzListCtrl.js',
        ], true)
    },
    'ezreport': {
        url: '/ezreport',
        parent: 'ez',
        templateUrl: '/page/ez-report',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/edari/ez/EzReportCtrl.js',
        ], true)
    },
    'morekhasi-saati': {
        url: '/morekhasisaati',
        parent: 'edari',
        templateUrl: '/page/morekhasisaatiBase',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/edari/morekhasi/saati/MorekhasiSaatiCtrl.js',
        ], true)
    },

    'morekhasi-saati-add': {
        url: '/:morekhasiID/morekhasisaatiadd',
        parent: 'morekhasi-saati',
        templateUrl: '/page/morekhasisaatiAdd',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/edari/morekhasi/saati/MorekhasiSaatiAddCtrl.js',
        ], true)
    },


    'morekhasi-saati-list': {
        url: '/morekhasisaatilist',
        parent: 'morekhasi-saati',
        templateUrl: '/page/morekhasisaatiList',
        resolve: GenerateJsResolveFiles([
            '/static/bower_components/datatables/datatables.js',
            '/static/bower_components/datatables/datatables.min.css',

            '/static/bower_components/handsontable/handsontable.full.min.css',
            // '/static/bower_components/handsontable/ngHandsontable.min.js',

            // '/static/bower_components/jquery-ui/themes/base/jquery.ui.all.css',
            '/static/bower_components/datatables/DataTables-1.10.18/css/dataTables.jqueryui.min.css',

            '/static/angularThings/edari/morekhasi/saati/MorekhasiSaatiListCtrl.js',
        ], true)
    },

    'morekhasi-saati-my-morekhasi': {
        url: '/morekhasisaatimymorekhasi',
        parent: 'morekhasi-saati',
        templateUrl: '/page/morekhasisaatiMyMorekhasi',
        resolve: GenerateJsResolveFiles([

            '/static/angularThings/edari/morekhasi/saati/MorekhasiSaatiMyCtrl.js',
        ], true)
    },

    'morekhasi-saati-entezamat': {
        url: '/morekhasisaatientEntezamat',
        parent: 'morekhasi-saati',
        templateUrl: '/page/morekhasisaatiEzamat',
        resolve: GenerateJsResolveFiles([

            '/static/angularThings/edari/morekhasi/saati/MorekhasiSaatiEntezamatCtrl.js',
        ], true)
    },

    'morekhasi-saati-edari': {
        url: '/morekhasisaatientEdari',
        parent: 'morekhasi-saati',
        templateUrl: '/page/morekhasisaatiEdari',
        resolve: GenerateJsResolveFiles([

            '/static/angularThings/edari/morekhasi/saati/MorekhasiSaatiEdariCtrl.js',
        ], true)
    },

    'morekhasi-roozaneh-base': {
        url: '/morekhasiRoozaneh',
        parent: 'edari',
        templateUrl: '/page/morekhasiroozanehRoozanehBase',
        resolve: GenerateJsResolveFiles([

            '/static/angularThings/edari/morekhasi/roozaneh/baseCtrl.js',
        ], true)
    },

    'emzakonandeha': {
        url: '/emzakonandeha',
        parent: 'edari',
        templateUrl: '/page/edariEmzaKonandeha',
        resolve: GenerateJsResolveFiles([

            '/static/angularThings/edari/emzakonandeha/EmzaKonandehaCtrl.js',
        ], true)
    },


    'edari-report-base': {
        url: '/edariReportBase',
        parent: 'edari',
        templateUrl: '/page/edariReportBase',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/edari/report/ReportEdariBaseCtrl.js',
        ], true)
    },


    'edari-report-taradod-mahaneh': {
        url: '/edariReportTaradodMahaneh',
        parent: 'edari-report-base',
        templateUrl: '/page/edariReportTaradodMahaneh',
        resolve: GenerateJsResolveFiles([

            '/static/angularThings/edari/report/ReportMyTaradodCtrl.js',
        ], true)
    },


    'edari-report-mandeh-morekhasi': {
        url: '/edariReportMandehMorekhasi',
        parent: 'edari-report-base',
        templateUrl: '/page/edariReportMandehMorekhasi',
        resolve: GenerateJsResolveFiles([

            '/static/angularThings/edari/report/edariReportMandehMorekhasiCtrl.js',
        ], true)
    },


    'edari-report-morekhsi-saati': {
        url: '/edariReportMorekhsiSaati',
        parent: 'edari-report-base',
        templateUrl: '/page/edariReportMorekhsiSaati',
        resolve: GenerateJsResolveFiles([

            '/static/angularThings/edari/report/ReportMorekhasiSaatiCtrl.js',
        ], true)
    },


    'edari-report-morekhsi-roozaneh': {
        url: '/edariReportMorekhsiRoozaneh',
        parent: 'edari-report-base',
        templateUrl: '/page/edariReportMorekhsiRoozaneh',
        resolve: GenerateJsResolveFiles([

            '/static/angularThings/edari/report/ReportMorekhsiRoozanehListCtrl.js',
        ], true)
    },


    'statics': {
        url: '/statics/:tmplID/show',
        parent: 'dashboard',
        templateUrl: function (params) {
            return '/page/dashboard/Statics?tmplID=' + params.tmplID
        },
        controller: 'StaticsCrtl',
        resolve: GenerateJsResolveFiles(['/static/angularThings/widgets/statics/StaticsCrtl.js'], true)
    },
    'dms': {
        url: '/dms',
        parent: 'company',
        templateUrl: function (params) {
            return '/page/company/baseDms?id=' + params.companyid
        },
        controller: 'DMSManagementCtrl',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/DMS/DMSManagementService.js',
            '/static/angularThings/DMS/DMSManagementCtrl.js'
        ], true)
    },
    'new-dms': {
        url: '/new',
        parent: 'dms',
        templateUrl: function (params) {
            return '/page/company/newDms?id=' + params.companyid
        },
        controller: 'DMSNewCtrl',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/DMS/DMSManagementService.js',
            '/static/angularThings/DMS/DMSNewCtrl.js',
            '/static/angularThings/DMS/DMSManagementCtrl.js'], true)
    },
    'edit-dms': {
        url: '/edit/:DMSId',
        parent: 'dms',
        templateUrl: function (params) {
            return '/page/company/editDms?id=' + params.companyid
        },
        controller: 'DMSEditCtrl',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/DMS/DMSManagementService.js',
            '/static/angularThings/DMS/DMSManagementCtrl.js',
            '/static/angularThings/DMS/DMSEditCtrl.js'], true)
    },
    'newbpmn': {
        url: '/newbpmn',
        parent: 'dashboard',
        templateUrl: '/page/newbpmn'
    },
    'friends': {
        url: '/Friends',
        parent: 'dashboard',
        templateUrl: '/page/friends/',
        resolve: GenerateJsResolveFiles(['/static/angularThings/friends/friendsService.js',
            '/static/angularThings/friends/friendsCtrl.js'], true)
    },
    'Contacts': {
        url: '/Contacts',
        parent: 'dashboard',
        templateUrl: '/page/contacts/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/contacts/contactsService.js',
            '/static/angularThings/contacts/contactsCtrl.js'], true)
    },
    'erp_control_project': {
        url: '/erp_control_project',
        parent: 'base',
        templateUrl: '/page/erp_control_project/'
    },
    'oldAmsp': {
        url: '/oldAmsp',
        parent: 'dashboard',
        templateUrl: '/page/oldAmsp/',
        resolve: GenerateJsResolveFiles(['/static/angularThings/oldAmsp/oldAmspCtrl.js'], true)
    },
    'myfiles': {
        url: '/myfiles',
        parent: 'dashboard',
        templateUrl: '/page/fileManager/',
    },
    'companies-dashboard': {
        url: '/Companies',
        parent: 'base',
        templateUrl: '/page/companies/',
        resolve: GenerateJsResolveFiles([
            // "/static/bower_components/codemirror/lib/codemirror.js",
            // "/static/bower_components/codemirror/mode/sql/sql.js",
            // "/static/bower_components/codemirror/mode/python/python.js",
            // "/static/bower_components/ui-codemirror/src/ui-codemirror.js",

            '/static/angularThings/companiesManagement/companiesManagmentCtrl.js'], true)
    },
    'company': {
        url: '/Company/:companyid',
        parent: 'base',
        templateUrl: function (params) {
            return '/page/comopbase?id=' + params.companyid
        },
        controller: 'CompanyCtrl',
        resolve: GenerateJsResolveFiles([
            // "/static/bower_components/codemirror/lib/codemirror.js",
            // "/static/bower_components/codemirror/mode/sql/sql.js",
            // "/static/bower_components/codemirror/mode/python/python.js",
            // "/static/bower_components/ui-codemirror/src/ui-codemirror.js",

            '/static/angularThings/companiesManagement/CompanyCtrl.js'], true)

    },
    'chart-company': {
        url: '/Chart',
        parent: 'company',
        views: {
            '': {
                templateUrl: function (params) {
                    return '/page/company/chart?id=' + params.companyid
                }
            },
            'profileView@chart-company': {
                templateUrl: function (params) {
                    return '/page/company/hamkarijobs?id=' + params.companyid
                }
            }
        },
        resolve: GenerateJsResolveFiles([
                // "/static/bower_components/d3/d3.js",
                // '/static/bower_components/bpmn-modeler/vendor/disttt2.js',
                // "/static/bower_components/angular-form-gen/angular-form-gen.js",
                // "/static/bower_components/angular-form-gen/classes/fgFieldController.js",
                // "/static/bower_components/angular-form-gen/classes/fgField.js",
                // "/static/bower_components/angular-form-gen/classes/fgConfigProvider.js",
                // "/static/bower_components/angular-form-gen/classes/templateCache.js",
                // "/static/bower_components/angular-form-gen/classes/fgTableCssClassInjector.js",
                // "/static/bower_components/angular-form-gen/classes/fgForm.js",
                // "/static/bower_components/angular-form-gen/classes/fgFormController.js",
                // "/static/bower_components/angular-form-gen/classes/fgEdit.js",
                // "/static/bower_components/angular-form-gen/classes/fgEditCanvasFieldProperties.js",
                // "/static/bower_components/angular-form-gen/classes/fgSchemaController.js",
                // "/static/bower_components/codemirror/lib/codemirror.js",
                // "/static/bower_components/codemirror/mode/sql/sql.js",
                // "/static/bower_components/codemirror/mode/python/python.js",
                // "/static/bower_components/ui-codemirror/src/ui-codemirror.js",
                '/static/angularThings/companiesManagement/Hamkari/hamkarijobsCtrl.js',
                '/static/angularThings/companiesManagement/CompanyChartCtrl.js'], true,
            function () {
                InjectToModule("fg");
                //InjectToModule("ui.codemirror");

            }
        )
    },
    'members': {
        url: '/Members',
        parent: 'company',
        templateUrl: function (params) {
            return '/page/company/members?id=' + params.companyid
        },
        resolve: GenerateJsResolveFiles([
                "/static/bower_components/d3/d3.js",
                // '/static/bower_components/bpmn-modeler/vendor/disttt2.js',
                // "/static/bower_components/angular-form-gen/angular-form-gen.js",
                // "/static/bower_components/angular-form-gen/classes/fgFieldController.js",
                // "/static/bower_components/angular-form-gen/classes/fgField.js",
                // "/static/bower_components/angular-form-gen/classes/fgConfigProvider.js",
                // "/static/bower_components/angular-form-gen/classes/templateCache.js",
                // "/static/bower_components/angular-form-gen/classes/fgTableCssClassInjector.js",
                // "/static/bower_components/angular-form-gen/classes/fgForm.js",
                // "/static/bower_components/angular-form-gen/classes/fgFormController.js",
                // "/static/bower_components/angular-form-gen/classes/fgEdit.js",
                // "/static/bower_components/angular-form-gen/classes/fgEditCanvasFieldProperties.js",
                // "/static/bower_components/angular-form-gen/classes/fgSchemaController.js",
                // "/static/bower_components/codemirror/lib/codemirror.js",
                // "/static/bower_components/codemirror/mode/sql/sql.js",
                // "/static/bower_components/codemirror/mode/python/python.js",
                // "/static/bower_components/ui-codemirror/src/ui-codemirror.js",
                '/static/angularThings/companiesManagement/MembersService.js',
                '/static/angularThings/companiesManagement/MembersCtrl.js'], true,
            function () {
                //InjectToModule("fg");
                //InjectToModule("ui.codemirror");

            })
    },
    'previewResume': {
        url: '/previewResume/:profileID',
        parent: 'dashboard',
        templateUrl: '/page/company/previewResume',
        resolve: GenerateJsResolveFiles(['/static/virtual/profile/profilePrevWithCommentCtrl.js'], true)
    },
    'secretariats': {
        url: '/Secretariats',
        parent: 'company',
        templateUrl: function (params) {
            return '/page/company/secretariats?id=' + params.companyid
        },
        resolve: GenerateJsResolveFiles([
            "/static/bower_components/d3/d3.js",
            // '/static/bower_components/bpmn-modeler/vendor/disttt2.js',
            // "/static/bower_components/angular-form-gen/angular-form-gen.js",
            // "/static/bower_components/angular-form-gen/classes/fgFieldController.js",
            // "/static/bower_components/angular-form-gen/classes/fgField.js",
            // "/static/bower_components/angular-form-gen/classes/fgConfigProvider.js",
            // "/static/bower_components/angular-form-gen/classes/templateCache.js",
            // "/static/bower_components/angular-form-gen/classes/fgTableCssClassInjector.js",
            // "/static/bower_components/angular-form-gen/classes/fgForm.js",
            // "/static/bower_components/angular-form-gen/classes/fgFormController.js",
            // "/static/bower_components/angular-form-gen/classes/fgEdit.js",
            // "/static/bower_components/angular-form-gen/classes/fgEditCanvasFieldProperties.js",
            // "/static/bower_components/angular-form-gen/classes/fgSchemaController.js",
            // "/static/bower_components/codemirror/lib/codemirror.js",
            // "/static/bower_components/codemirror/mode/sql/sql.js",
            // "/static/bower_components/codemirror/mode/python/python.js",
            // "/static/bower_components/ui-codemirror/src/ui-codemirror.js",
            '/static/angularThings/companiesManagement/SecretaraitsService.js',
            '/static/angularThings/companiesManagement/SecretaraitsCtrl.js'], true)
    },
    'hamkari': {
        url: '/Hamkari',
        parent: 'company',
        templateUrl: function (params) {
            return '/page/company/hamkari?id=' + params.companyid
        },
        resolve: GenerateJsResolveFiles(['/static/angularThings/companiesManagement/Hamkari/HamkariCtrl.js'], true)
    },
    'job': {
        url: '/Job/:jobID/Post',
        parent: 'hamkari',
        templateUrl: '/page/company/postJob',
        resolve:
            GenerateJsResolveFiles(['/static/angularThings/companiesManagement/Hamkari/AddJobCtrl.js'], true)
    },
    'items': {
        url: '/Job/:jobID/jobItems',
        parent: 'hamkari',
        templateUrl: '/page/company/jobItems',
        resolve: GenerateJsResolveFiles(['/static/angularThings/companiesManagement/Hamkari/AddJobItemCtrl.js'], true)
    },
    'requestHamkari': {
        url: '/:item/requests',
        parent: 'hamkari',
        templateUrl: '/page/company/requestHamkari',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/companiesManagement/Hamkari/RegisteredPersonCtrl.js'
        ], true)
    },
    'HamkariJob': {
        url: '/HamkariJob',
        parent: 'company',
        templateUrl: function (params) {
            return '/page/company/hamkarijobs?id=' + params.companyid
        },
        resolve: GenerateJsResolveFiles(['/static/angularThings/companiesManagement/Hamkari/hamkarijobsCtrl.js'], true)
    },
    'Connections': {
        url: '/Connections',
        parent: 'company',
        templateUrl: function (params) {
            return '/page/company/Connections?id=' + params.companyid
        },
        resolve: GenerateJsResolveFiles(['/static/angularThings/companiesManagement/Connections/ConnectionCtrl.js'], true)
    },
    'profile': {
        url: '/Profile',
        parent: 'company',
        templateUrl: function (params) {
            return '/page/company/profile?id=' + params.companyid
        },
        resolve: GenerateJsResolveFiles([
                '/static/angularThings/companiesManagement/CompanyProfileCtrl.js',
                // "/static/bower_components/d3/d3.js",
                // '/static/bower_components/bpmn-modeler/vendor/disttt2.js',
                // "/static/bower_components/angular-form-gen/angular-form-gen.js",
                // "/static/bower_components/angular-form-gen/classes/fgFieldController.js",
                // "/static/bower_components/angular-form-gen/classes/fgField.js",
                // "/static/bower_components/angular-form-gen/classes/fgConfigProvider.js",
                // "/static/bower_components/angular-form-gen/classes/templateCache.js",
                // "/static/bower_components/angular-form-gen/classes/fgTableCssClassInjector.js",
                // "/static/bower_components/angular-form-gen/classes/fgForm.js",
                // "/static/bower_components/angular-form-gen/classes/fgFormController.js",
                // "/static/bower_components/angular-form-gen/classes/fgEdit.js",
                // "/static/bower_components/angular-form-gen/classes/fgEditCanvasFieldProperties.js",
                // "/static/bower_components/angular-form-gen/classes/fgSchemaController.js",
                // "/static/bower_components/codemirror/lib/codemirror.js",
                // "/static/bower_components/codemirror/mode/sql/sql.js",
                // "/static/bower_components/codemirror/mode/python/python.js",
                // "/static/bower_components/ui-codemirror/src/ui-codemirror.js",

            ], true,
            function () {
                //InjectToModule("fg");
                //InjectToModule("ui.codemirror");

            })
    },
    'products': {
        url: '/Products',
        parent: 'company',
        templateUrl: function (params) {
            return '/page/company/products?id=' + params.companyid
        },
        resolve: GenerateJsResolveFiles([
            // '/static/bower_components/ckeditor/full/ckeditor.js',
            '/static/angularThings/companiesManagement/CompanyProductsCtrl.js',
            // '/static/bower_components/ckeditorAngularJs/ng-ckeditor.js'

        ], true)
    },
    'process': {
        url: '/Process',
        parent: 'company',
        templateUrl: function (params) {
            return '/page/company/process?id=' + params.companyid
        },
        resolve: GenerateJsResolveFiles([


            '/static/angularThings/companiesManagement/CompanyProcessCtrl.js',
            '/static/angularThings/companiesManagement/Process/bpmnService.js',
            '/static/angularThings/Letter/FileUploader/classUploader.js',
            '/static/angularThings/share/selectMembers/SelectMembersService.js',
            '/static/angularThings/share/selectMembers/SelectMembersCtrl.js'], true, function () {
            //InjectToModule("fg");
            //InjectToModule("ui.codemirror");
        })
    },
    'new-process': {
        url: '/New',
        parent: 'company',
        templateUrl: function (params) {
            return '/page/company/newProcess?id=' + params.companyid
        },
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/companiesManagement//Process/bpmnModelerCtrl.js',
            '/static/angularThings/companiesManagement/Process/bpmnService.js'], true)
    },
    'edit-process': {
        url: '/:processId/Edit',
        parent: 'company',
        templateUrl: function (params) {
            return '/page/company/newProcess?id=' + params.companyid
        },
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/companiesManagement/Process/bpmnModelerCtrl.js',
            // '/static/angularThings/companiesManagement/Process/elements/serviceTaskCtrl.js',
            '/static/angularThings/companiesManagement/Process/bpmnService.js'], true)
    },
    'setup-process': {
        url: '/:processId/setup',
        parent: 'company',
        templateUrl: function (params) {
            return '/page/company/setupProcess?id=' + params.companyid
        },
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/companiesManagement/Process/bpmnSetupCtrl.js',
            '/static/angularThings/companiesManagement/Process/bpmnService.js'], true)
    },

    'datamodel-process': {
        url: '/:processId/datamodel',
        parent: 'company',
        templateUrl: function (params) {
            return '/page/process/datamodel?id=' + params.companyid
        },
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/companiesManagement/Process/datamodelCtrl.js'], true)
    },

    'bam': {
        url: '/BAM',
        parent: 'company',
        templateUrl: '/page/company/bam',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/companiesManagement/bamService.js',
            '/static/angularThings/companiesManagement/BAMCtrl.js'], true)
    },
    'dashboard-bam': {
        url: '/dashboard',
        parent: 'bam',
        templateUrl: '/page/company/dashboardBam',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/companiesManagement/bamService.js',
            '/static/angularThings/companiesManagement/BAMCtrl.js',
            '/static/angularThings/companiesManagement/BAMDashboardCtrl.js'], true)
    },
    'new-bam': {
        url: '/new',
        parent: 'bam',
        templateUrl: '/page/company/newBam',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/companiesManagement/bamService.js',
            '/static/angularThings/companiesManagement/BAMCtrl.js',
            '/static/angularThings/companiesManagement/BAMNewCtrl.js'], true)
    },
    'edit-bam': {
        url: ':shakhesId/edit',
        parent: 'bam',
        templateUrl: '/page/company/editBam',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/companiesManagement/bamService.js',
            '/static/angularThings/companiesManagement/BAMCtrl.js',
            '/static/angularThings/companiesManagement/BAMEditCtrl.js'], true)
    },
    'shakhes': {
        url: '/shakhes/:shakhesId',
        parent: 'bam',
        templateUrl: '/page/company/shakhesBam',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/companiesManagement/bamService.js',
            '/static/angularThings/companiesManagement/BAMCtrl.js',
            '/static/angularThings/companiesManagement/BAMShowShakhesCtrl.js'], true)
    },
    'chart': {
        url: '/chart',
        parent: 'chart-company',
        templateUrl: '/page/companies-managment/chart'
    },
    'myProfile': {
        url: '/MyProfile',
        parent: 'dashboard',
        templateUrl: '/page/myProfile',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/myProfile/myProfileService.js',
            '/static/angularThings/myProfile/myProfileCrtl.js'], true)
    },
    'dashboardSettings': {
        url: '/DashboardSettings',
        parent: 'dashboard',
        templateUrl: '/page/dashboardSettings',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/myProfile/dashboardSettingsCtrl.js'], true)
    },
    'secExport': {
        url: '/SecExport',
        parent: 'secretariat',
        templateUrl: '/page/letter/sec/exportBase',
        resolve: GenerateJsResolveFiles([
            // '/static/bower_components/ckeditor/full/ckeditor.js',
            // '/static/bower_components/ckeditorAngularJs/ng-ckeditor.js',
            '/static/angularThings/Letter/Secretariat/Companies/SecCompaniesService.js',
            '/static/angularThings/Letter/Secretariat/SecretariatService.js',
            '/static/angularThings/Letter/Secretariat/Letters/ExportService.js',
            '/static/angularThings/share/selectMembers/SelectMembersService.js',
            '/static/angularThings/share/file/FileUploaderService.js',
            '/static/angularThings/share/file/FileUploaderCtrl.js',
            '/static/angularThings/Letter/Secretariat/Letters/ExportCtrl.js'], true)
    },
    'settings': {
        url: '/Settings',
        parent: 'dashboard',
        templateUrl: '/page/settings',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/settings/SettingsCrtl.js',
            '/static/angularThings/settings/SettingsService.js'], true)
    },
    'Change': {
        url: '/Change',
        parent: 'settings',
        templateUrl: '/page/settings/Change',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/settings/ChangeCtrl.js'], true)
    },
    'AccessToSecratariat': {
        url: '/AccessToSecratariat',
        parent: 'settings',
        templateUrl: '/page/settings/AccessToSecratariat',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/settings/class/AutocompleteMembers.js',
            '/static/angularThings/settings/Automation/AccessToSecratariatCrtl.js'], true)
    },
    'letter': {
        url: '/Letter',
        parent: 'dashboard',
        templateUrl: '/page/letterBase',
        resolve: GenerateJsResolveFiles([

                // "/static/bower_components/ckeditor/full/ckeditor.js",
                // "/static/bower_components/ckeditorAngularJs/ng-ckeditor.js",
                '/static/angularThings/Letter/class/ActiveSecsClass.js',
                '/static/angularThings/Letter/Sidebar/classSetupSideBar.js',
                '/static/angularThings/Letter/LetterBaseService.js',
                '/static/angularThings/Letter/LetterBaseCtrl.js',
                '/static/angularThings/Letter/LetterInboxService.js',
                '/static/angularThings/Letter/LetterInboxCtrl.js'], true,
            function () {

                //InjectToModule("ngCkeditor");
                setTimeout(function () {
                    // $('.sidenav-outer').perfectScrollbar();
                }, 100)
            })
    },
    'inbox': {
        url: '/Inbox',
        parent: 'letter',
        templateUrl: 'page/letter/inbox'
    },
    'list': {
        url: '/List',
        parent: 'inbox',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/share/selectMembers/SelectMembersService.js',
            '/static/angularThings/Letter/LetterInboxService.js',

            '/static/angularThings/share/selectMembers/SelectMembersCtrl.js',
            '/static/angularThings/Letter/Inbox/InboxListService.js',
            '/static/angularThings/Letter/Inbox/InboxListCtrl.js'
        ], true),
        views: {
            '': {
                templateUrl: 'page/letter/listinbox'
            },
            'forward@list': {
                templateUrl: 'page/public/selectmember'
            }
        }
    },
    'compose': {
        url: '/:letterID/Compose',
        parent: 'dashboard',
        resolve: GenerateJsResolveFiles([
            // '/static/bower_components/ckeditor/full/ckeditor.js',
            '/static/angularThings/Letter/Compose/LetterComposeService.js',
            '/static/angularThings/Letter/LetterInboxService.js',
            '/static/angularThings/Letter/Compose/LetterComposeCtrl.js',
            '/static/angularThings/share/selectMembers/SelectMembersService.js',
            '/static/angularThings/share/selectMembers/SelectMembersCtrl.js',
            '/static/angularThings/Letter/Compose/LetterComposeBaseService.js',
            '/static/angularThings/Letter/Compose/LetterComposeBaseCtrl.js',
            '/static/angularThings/share/file/FileUploaderCtrl.js',
            '/static/angularThings/share/file/FileUploaderService.js',
            '/static/angularThings/Letter/Preview/LetterPrevService.js',
            // '/static/bower_components/ckeditorAngularJs/ng-ckeditor.js',
            '/static/angularThings/Letter/Preview/LetterPrevController.js'], true)
        ,
        views: {
            '': {
                templateUrl: 'page/letter/compose'
            },
            'recievers@compose': {
                templateUrl: 'page/public/selectmember'
            },
            'upload@compose': {
                templateUrl: 'page/filecould'
            }
        }
    },
    'preview': {
        url: '/:inboxID/Preview',
        parent: 'inbox',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/Letter/Preview/LetterPrevService.js',
            '/static/angularThings/Letter/Inbox/InboxListService.js',
            '/static/angularThings/Letter/LetterInboxService.js',

            '/static/angularThings/share/selectMembers/SelectMembersService.js',
            '/static/angularThings/Letter/Preview/LetterPrevController.js',
            '/static/angularThings/share/selectMembers/SelectMembersCtrl.js'], true)
        ,
        views: {
            '': {
                templateUrl: 'page/letter/prev'
            },
            'recievers@preview': {
                templateUrl: 'page/public/selectmember'
            }
        }
    },
    'secretariat': {
        url: '/Secretariat',
        parent: 'letter',
        views: {
            '': {
                templateUrl: 'page/letter/secBase'
            },
            'sidebar@secretariat': {
                templateUrl: 'page/letter/secSideBar'
            }
        },
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/Letter/class/ActiveSecsClass.js',
            '/static/angularThings/Letter/Secretariat/SecretariatCrtl.js'], true)
    },
    'importList': {
        url: '/ImportList',
        parent: 'secretariat',
        templateUrl: '/page/letter/sec/importList',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/Letter/Secretariat/Letters/classes/classMembersSec.js',
            '/static/angularThings/Letter/Secretariat/Letters/Import/ImportService.js',
            '/static/angularThings/Letter/Secretariat/Letters/classes/tagClass.js',
            '/static/angularThings/share/selectMembers/SelectMembersService.js',
            '/static/angularThings/Letter/Secretariat/Letters/Import/ImportLetterListCtrl.js'], true)
    },
    'importPreview': {
        url: '/:importid/importPreview',
        parent: 'secretariat',
        templateUrl: '/page/letter/sec/importPrev',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/Letter/Secretariat/Letters/Import/ImportPreviewCtrl.js',
            '/static/angularThings/Letter/Secretariat/Letters/classes/tagClass.js'], true)
    },
    'importNew': {
        url: '/:importid/import',
        parent: 'secretariat',
        templateUrl: '/page/letter/sec/importNew',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/share/file/classUploaderAPI.js',
            '/static/angularThings/Letter/Secretariat/Letters/classes/tagClass.js',
            '/static/angularThings/Letter/Secretariat/Letters/classes/classMembersSec.js',
            '/static/angularThings/Letter/Secretariat/Companies/SecCompaniesService.js',
            '/static/angularThings/Letter/Secretariat/Letters/Import/ImportService.js',
            '/static/angularThings/share/selectMembers/SelectMembersService.js',
            '/static/angularThings/share/file/FileUploaderService.js',
            '/static/angularThings/share/file/FileUploaderCtrl.js',
            '/static/angularThings/Letter/Secretariat/Letters/Import/ImportCtrl.js'], true)
    },
    'exportList': {
        url: '/ExportList',
        parent: 'secretariat',
        templateUrl: '/page/letter/sec/exportList',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/Letter/Secretariat/Letters/classes/tagClass.js',
            '/static/angularThings/share/selectMembers/SelectMembersService.js',
            '/static/angularThings/Letter/Secretariat/Letters/classes/classMembersSec.js',
            '/static/angularThings/Letter/Secretariat/Letters/Export/ExportService.js',
            '/static/angularThings/Letter/Secretariat/Letters/Export/ExportListCtrl.js'], true)
    },
    'scan': {
        url: '/:exportid/scan',
        parent: 'exportList',
        templateUrl: '/page/letter/sec/export-scan',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/share/file/classUploaderAPI.js',
            '/static/angularThings/Letter/Secretariat/Letters/Export/ExportScanCtrl.js'], true)
    },
    'recieved': {
        url: '/:exportid/recieved',
        parent: 'exportList',
        templateUrl: '/page/letter/sec/export-recieved',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/Letter/Secretariat/Letters/Export/ExportRecievedCtrl.js'], true)
    },
    'templates': {
        url: '/:exportid/templates',
        parent: 'exportList',
        templateUrl: '/page/letter/sec/export-templates',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/Letter/Secretariat/Letters/classes/tagClass.js',
            '/static/angularThings/share/file/classUploaderAPI.js',
            '/static/angularThings/Letter/Secretariat/Letters/Export/ExportTemplateCtrl.js'], true)
    },
    'preview-exportList': {
        url: '/:exportid/preview',
        parent: 'exportList',
        templateUrl: '/page/letter/sec/export-prev',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/Letter/Secretariat/Letters/classes/tagClass.js',
            '/static/angularThings/Letter/Secretariat/Letters/Export/ExportPreviewService.js',
            '/static/angularThings/Letter/Secretariat/Letters/Export/ExportPreviewCtrl.js'], true)
    },
    'exportNew': {
        url: '/:exportid/Post',
        parent: 'secretariat',
        templateUrl: '/page/letter/sec/exportBase',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/Letter/Secretariat/Letters/classes/tagClass.js',
            '/static/angularThings/share/file/classUploaderAPI.js',
            // '/static/bower_components/ckeditor/full/ckeditor.js',
            // '/static/bower_components/ckeditorAngularJs/ng-ckeditor.js',
            '/static/angularThings/Letter/Secretariat/Companies/SecCompaniesService.js',
            '/static/angularThings/Letter/Secretariat/SecretariatService.js',
            '/static/angularThings/Letter/Secretariat/Letters/Export/ExportService.js',
            '/static/angularThings/share/selectMembers/SelectMembersService.js',
            '/static/angularThings/share/file/FileUploaderService.js',
            '/static/angularThings/share/file/FileUploaderCtrl.js',
            '/static/angularThings/Letter/Secretariat/Letters/Export/ExportCtrl.js'], true)
    },
    'companyGroups': {
        url: '/CompanyGroups',
        parent: 'secretariat',
        templateUrl: '/page/letter/sec/company-groupBase',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/Letter/Secretariat/CompanyGroups/CompanyGroupsService.js',
            '/static/angularThings/Letter/Secretariat/CompanyGroups/CompanyGroupsCtrl.js'], true)
    },
    'sec-companies': {
        url: '/SecCompanies',
        parent: 'secretariat',
        templateUrl: '/page/letter/sec/companyBase',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/Letter/Secretariat/CompanyGroups/CompanyGroupsService.js',
            '/static/angularThings/Letter/Secretariat/Companies/SecCompaniesService.js',
            '/static/angularThings/Letter/Secretariat/Companies/SecCompaniesCtrl.js'], true)
    },
    'process-dashboard': {
        url: '/Process',
        parent: 'dashboard',
        templateUrl: '/page/processBase',
        resolve: GenerateJsResolveFiles([
            "/static/bower_components/d3/d3.js",
            // '/static/bower_components/bpmn-modeler/vendor/disttt2.js',
            // "/static/bower_components/angular-form-gen/angular-form-gen.js",
            // "/static/bower_components/angular-form-gen/classes/fgFieldController.js",
            // "/static/bower_components/angular-form-gen/classes/fgField.js",
            // "/static/bower_components/angular-form-gen/classes/fgConfigProvider.js",
            // "/static/bower_components/angular-form-gen/classes/templateCache.js",
            // "/static/bower_components/angular-form-gen/classes/fgTableCssClassInjector.js",
            // "/static/bower_components/angular-form-gen/classes/fgForm.js",
            // "/static/bower_components/angular-form-gen/classes/fgFormController.js",
            // "/static/bower_components/angular-form-gen/classes/fgEdit.js",
            // "/static/bower_components/angular-form-gen/classes/fgEditCanvasFieldProperties.js",
            // "/static/bower_components/angular-form-gen/classes/fgSchemaController.js",
            // "/static/bower_components/codemirror/lib/codemirror.js",
            // "/static/bower_components/codemirror/mode/sql/sql.js",
            // "/static/bower_components/codemirror/mode/python/python.js",
            // "/static/bower_components/ui-codemirror/src/ui-codemirror.js",
            //
            // '/static/bower_components/bpmn-modeler/vendor/disttt2.js',
            '/static/angularThings/bpms/lunchedProcessService.js',
            '/static/angularThings/Letter/FileUploader/classUploader.js'], true, function () {
            //InjectToModule("fg");
            InjectToModule("ui.codemirror");
        })
    },
    'inbox-process-dashboard': {
        url: '/Inbox',
        parent: 'process-dashboard',
        templateUrl: '/page/process/inbox',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/bpms/lunchedProcessService.js',
            '/static/angularThings/companiesManagement/Process/bpmnService.js',
            '/static/angularThings/bpms/Inbox/lunchedProcessInboxCtrl.js'], true)
    },
    'message': {
        url: '/Message',
        parent: 'process-dashboard',
        templateUrl: '/page/process/message',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/bpms/Message/messageProcessService.js',
            '/static/angularThings/companiesManagement/Process/bpmnService.js',
            '/static/angularThings/bpms/Message/messageProcessCtrl.js'], true)
    },
    'doneArchive': {
        url: '/DoneArchive',
        parent: 'process-dashboard',
        templateUrl: '/page/process/doneArchive',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/bpms/lunchedProcessService.js',
            '/static/angularThings/companiesManagement/Process/bpmnService.js',
            '/static/angularThings/bpms/DoneArchive/DoneProcessArchiveCtrl.js'], true)
    },
    'lunchedArchive': {
        url: '/LunchedArchive',
        parent: 'process-dashboard',
        templateUrl: '/page/process/lunchedArchive',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/bpms/lunchedProcessService.js',
            '/static/angularThings/companiesManagement/Process/bpmnService.js',
            '/static/angularThings/bpms/LunchedArchive/lunchedProcessArchiveCtrl.js'], true)
    },
    'do': {
        url: '/:lunchedProcessId/Do',
        parent: 'inbox-process-dashboard',
        templateUrl: '/page/process/do',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/companiesManagement/Process/bpmnService.js',
            '/static/angularThings/bpms/DoProcess/DoLunchedProcessCtrl.js'

        ], true)
    },
    'new': {
        url: '/New',
        parent: 'inbox-process-dashboard',
        templateUrl: '/page/process/new',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/companiesManagement/Process/bpmnService.js',
            '/static/angularThings/bpms/Inbox/lunchedProcessInboxCtrl.js'], true)
    },
    'diagram': {
        url: '/:lunchedProcessId/Diagram',
        parent: 'inbox-process-dashboard',
        templateUrl: '/page/process/diagram',
        resolve: GenerateJsResolveFiles([
            "/static/bower_components/bpmn-modeler2/BpmnViewerApp.js",
            "/static/bower_components/bpmn-modeler2/bpmn-moddle.js",
            '/static/angularThings/companiesManagement/Process/bpmnService.js',
            '/static/angularThings/bpms/DiagramProcess/GetDiagramProcessCtrl.js'], true)
    },
    'doMessage': {
        url: '/:messageProcessId/DoMessage',
        parent: 'message-process-dashboard',
        templateUrl: '/page/process/seeMessage',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/companiesManagement/Process/bpmnService.js',
            '/static/angularThings/bpms/Message/messageProcessService.js',
            '/static/angularThings/bpms/Message/DoMessageProcessCtrl.js'], true)
    },
    'trackDoneProcess': {
        url: '/:lunchedProcessId/TrackDoneProcess',
        parent: 'doneArchive-process-dashboard',
        templateUrl: '/page/process/trackDoneProcess',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/companiesManagement/Process/bpmnService.js',
            '/static/angularThings/bpms/TrackProcess/TrackDoneProcessCtrl.js'], true)
    },
    'trackLunchedProcess': {
        url: '/:lunchedProcessId/TrackLunchedProcess',
        parent: 'lunchedArchive-process-dashboard',
        templateUrl: '/page/process/trackLunchedProcess',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/companiesManagement/Process/bpmnService.js',
            '/static/angularThings/bpms/TrackProcess/TrackLunchedProcessCtrl.js'], true)
    },
    'reports-process-dashboard': {
        url: '/Reports',
        parent: 'process-dashboard',
        templateUrl: '/page/process/reports',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/bpms/Reports/ReportsService.js',
            '/static/angularThings/bpms/Reports/ReportsCtrl.js'], true)
    },
    'search-process-dashboard': {
        url: '/ProcessSearch',
        parent: 'process-dashboard',
        templateUrl: '/page/process/search',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/bpms/Reports/SearchCtrl.js'], true)
    },
    'statistics': {
        url: '/statistics',
        parent: 'dashboard',
        templateUrl: '/page/statisticsBase',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/statistics/statisticsBaseService.js',
            '/static/angularThings/statistics/statisticsBaseCtrl.js'], true)
    },
    'advProcess': {
        url: '/advProcess',
        parent: 'dashboard',
        templateUrl: '/page/advProcess/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/advProcess/advProcessCtrl.js'], true)
    },
    'QC': {
        url: '/QC',
        parent: 'dashboard',
        templateUrl: '/page/qc/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/QC/QCBaseController.js'], true)
    },
    'QCSchedule': {
        url: '/QCSchedule',
        parent: 'QC',
        templateUrl: '/page/qcschedule/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/QC/Schedule/QCAuditingSchedualsCtrl.js'], true)
    },
    'QCFinding': {
        url: '/QCFinding',
        parent: 'QC',
        templateUrl: '/page/qcfinding/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/share/file/classUploaderAPI.js',
            '/static/angularThings/QC/Finding/QCFindingBaseCtrl.js'], true)
    },
    'QCManual': {
        url: '/QCManual',
        parent: 'QC',
        templateUrl: '/page/qcmanual/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/QC/Manual/QCManualsCtrl.js'], true)
    },
    'QCFindingPost': {
        url: '/:findingID/QCFindingPost',
        parent: 'QCFinding',
        templateUrl: '/page/qcfindingpost/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/share/file/classUploaderAPI.js',
            '/static/angularThings/settings/class/AutocompleteMembers.js',
            '/static/angularThings/settings/SettingsService.js',
            '/static/angularThings/QC/Finding/QCFindingPostCtrl.js'], true)
    },
    'QCFindingList': {
        url: '/QCFindingList',
        parent: 'QCFinding',
        templateUrl: '/page/qcfindinglist/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/Letter/Secretariat/Letters/Export/ExportService.js',
            '/static/angularThings/QC/Finding/QCFindingListCtrl.js'], true)
    },
    'QCFindingOpen': {
        url: '/:findingID/QCFindingOpen',
        parent: 'QCFinding',
        templateUrl: '/page/qcfindingopen/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/Letter/Secretariat/Letters/Export/ExportService.js',
            '/static/angularThings/QC/Finding/QCOpenFindingCtrl.js'], true)
    },
    'News': {
        url: '/News',
        parent: 'dashboard',
        templateUrl: '/page/news/',
        resolve: GenerateJsResolveFiles([
            "/static/bower_components/ckeditor/full/ckeditor.js",
            "/static/bower_components/ckeditorAngularJs/ng-ckeditor.js",
            '/static/angularThings/News/NewsCtrl.js'
        ], true, function () {
            InjectToModule("ngCkeditor");
            setTimeout(function () {
                // $('.sidenav-outer').perfectScrollbar();
            }, 100)
        })
    },
    'news-post': {
        url: '/:NewsID/Post',
        parent: 'News',
        templateUrl: '/page/newspost',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/News/PostNewsCtrl.js'], true)
    },
    'NewsBlog': {
        url: '/NewsBlog',
        parent: 'dashboard',
        templateUrl: '/page/newsBlog',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/News/NewsBlogCtrl.js'], true)
    },
    'Newsread': {
        url: '/:NewsID/Read',
        parent: 'dashboard',
        templateUrl: '/page/newsread',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/News/ReadNewsCtrl.js'], true)
    },
    // 'ControlProject': {
    //     url: '/ControlProject',
    //     parent: 'dashboard',
    //     templateUrl: '/page/ControlProject/',
    //     resolve: GenerateJsResolveFiles([
    //         '/static/angularThings/share/tableNavBar/TableNavigation.js',
    //         '/static/angularThings/ControlProject/ControlProjectBaseCtrl.js'], true)
    // },
    // 'Year': {
    //     url: '/Year',
    //     parent: 'ControlProject',
    //     templateUrl: '/page/ControlProject/Year/',
    //     resolve: GenerateJsResolveFiles([
    //         '/static/angularThings/share/tableNavBar/TableNavigation.js',
    //         '/static/angularThings/ControlProject/ControlProjectYearCtrl.js'], true)
    // },
    // 'Projects': {
    //     url: '/:YearID/Projects',
    //     parent: 'dashboard',
    //     templateUrl: '/page/ControlProject/Projects',
    //     resolve: GenerateJsResolveFiles([
    //         '/static/angularThings/share/tableNavBar/TableNavigation.js',
    //         '/static/angularThings/ControlProject/projects/crudClass.js',
    //         '/static/angularThings/ControlProject/projects/ControlProjectProjectsCtrl.js'], true)
    // },
    // 'SubProjects': {
    //     url: '/:ProjectID/SubProjects',
    //     parent: 'ControlProject',
    //     templateUrl: '/page/ControlProject/SubProjects',
    //     resolve: GenerateJsResolveFiles([
    //         '/static/angularThings/share/tableNavBar/TableNavigation.js',
    //         '/static/angularThings/ControlProject/projects/crudClass.js',
    //         '/static/angularThings/ControlProject/SubProjects/ControlProjectSubProjectsCtrl.js'], true)
    // },
    // 'Share': {
    //     url: '/Year/:YearID/ShareYear',
    //     parent: 'Year',
    //     templateUrl: '/page/ControlProject/Year/Share',
    //     resolve: GenerateJsResolveFiles([
    //         '/static/angularThings/settings/class/AutocompleteMembers.js',
    //         '/static/angularThings/settings/SettingsService.js',
    //         '/static/angularThings/ControlProject/ControlProjectShareCtrl.js'], true)
    // },
    // 'Outcome': {
    //     url: '/Outcome',
    //     parent: 'ControlProject',
    //     templateUrl: '/page/ControlProject/Outcome',
    //     resolve: GenerateJsResolveFiles([
    //         '/static/angularThings/ControlProject/ControlProjectOutcomeTypesCtrl.js'], true)
    // },
    // 'Income': {
    //     url: '/Income',
    //     parent: 'ControlProject',
    //     templateUrl: '/page/ControlProject/Income',
    //     resolve: GenerateJsResolveFiles([
    //         '/static/angularThings/ControlProject/ControlProjectIncomeTypesCtrl.js'], true)
    // },
    'datatables': {
        url: '/datatables',
        parent: 'dashboard',
        templateUrl: '/page/datatables',
        resolve: GenerateJsResolveFiles([
            "/static/bower_components/codemirror/lib/codemirror.js",
            '/static/bower_components/ui-codemirror/src/ui-codemirror.js',
            "/static/bower_components/codemirror/mode/sql/sql.js",
            "/static/bower_components/codemirror/mode/python/python.js",
            '/static/angularThings/dataTables/DataTablesCtrl.js'

        ], true, function () {
            InjectToModule("ui.codemirror");
        })
    },
    'new-datatable': {
        url: '/:DataTableId/New',
        parent: 'datatables',
        templateUrl: '/page/datatables/new',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/settings/class/AutocompleteMembers.js',
            '/static/angularThings/settings/SettingsService.js',
            '/static/angularThings/dataTables/EditDataTableCtrl.js'], true)
    },
    'script-datatable': {
        url: '/:DataTableId/Script',
        parent: 'datatables',
        templateUrl: '/page/datatables/script',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/dataTables/ScriptDataTableCtrl.js'], true)
    },
    'share-datatables': {
        url: '/:DataTableId/Share',
        parent: 'datatables',
        templateUrl: '/page/datatables/share',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/settings/class/AutocompleteMembers.js',
            '/static/angularThings/settings/SettingsService.js',
            '/static/angularThings/dataTables/ShareDataTableCtrl.js'], true)
    },
    'value-datatables': {
        url: '/:DataTableId/Value',
        parent: 'base',
        templateUrl: '/page/datatables/value',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/dataTables/ValueDataTableCtrl.js'], true)
    },
    'dms-dashboard': {
        url: '/dms',
        parent: 'dashboard',
        templateUrl: '/page/dmsBase',
        // resolve: GenerateJsResolveFiles([
        //     '/static/angularThings/DMS/DMSManagementService.js',
        //     '/static/angularThings/DMS/DMSUserInboxCtrl.js'], true)
    },
    'new-statistics': {
        url: '/New',
        parent: 'statistics',
        templateUrl: '/page/statistics/new',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/statistics/statisticsBaseService.js',
            '/static/angularThings/statistics/statisticsNewCtrl.js'], true)
    },
    'share-statistics': {
        url: '/:MSTemplateId/Share',
        parent: 'statistics',
        templateUrl: '/page/statistics/share',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/settings/class/AutocompleteMembers.js',
            '/static/angularThings/settings/SettingsService.js',
            '/static/angularThings/statistics/userShareCtrl.js'], true)
    },
    'edit-statistics': {
        url: ':MSTemplateId/Edit',
        parent: 'statistics',
        templateUrl: '/page/statistics/edit',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/statistics/statisticsBaseService.js',
            '/static/angularThings/statistics/statisticsEditCtrl.js'], true)
    },
    'data-statistics': {
        url: '/:MSTemplateId/Data',
        parent: 'statistics',
        templateUrl: '/page/statistics/data',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/statistics/statisticsBaseService.js',
            '/static/angularThings/statistics/statisticsDataCtrl.js'
        ], true)
    },
    'trace': {
        url: '/trace',
        parent: 'base',
        templateUrl: 'page/cog_trace_base',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/Trace/baseTraceCtrl.js'
        ], true)
    },
    'trace-cat': {
        url: '/cat',
        parent: 'trace',
        templateUrl: 'page/cog_trace_base_cat',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/Trace/Category/TraceCatCtrl.js'
        ], true)
    },
    'trace-types': {
        url: '/types',
        parent: 'trace',
        templateUrl: 'page/cog_trace_types',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/Trace/Types/TraceTypesCtrl.js'
        ], true)
    },
    'trace-entry': {
        url: '/entry',
        parent: 'trace',
        templateUrl: 'page/cog_trace_entry',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/Trace/Entry/TraceEntryCtrl.js'
        ], true)
    },
    'request-goods': {
        url: '/rg',
        parent: 'base',
        templateUrl: 'page/RGIndex',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/RequestGoods/baseCtrl.js'
        ], true)
    },
    'request-goods-chat': {
        url: '/rgchat',
        parent: 'base',
        templateUrl: 'page/talkToAnbar'
    },
    'request-goods-help': {
        url: '/rghelp',
        parent: 'base',
        templateUrl: 'page/helpRG'
    },
    'request-goods-item': {
        url: '/:idof/rgitem',
        parent: 'base',
        templateUrl: 'page/RGItem',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/sales/sign/signBodyCtrl.js',
            '/static/angularThings/RequestGoods/RGItemCtrl.js',
        ], true)
    },
    'Sales': {
        url: '/Sales',
        parent: 'base',
        templateUrl: '/page/sales/',
        resolve: GenerateJsResolveFiles([

                "/static/angularThings/datatables/datatables.js",
                "/static/bower_components/angular-timeline/angular-timeline.css?v=0.01",
                "/static/bower_components/angular-timeline/angular-timeline-bootstrap.css?v=0.01",
                "/static/bower_components/angular-timeline/angular-timeline-animations.css?v=0.01",
                "/static/angularThings/datatables/datatables.min.css",
                // "/static/bower_components/angular-timeline/angular-timeline.js?v=0.01",
                // "/static/angularThings/angular-bootstrap/ui-bootstrap.min.js",
                // "/static/bower_components/angular-qrcode/qrcode.min.js",
                // "/static/bower_components/angular-qrcode/angular-qr.min.js",

                // "/static/bower_components/ckeditor/full/ckeditor.js?v=0.01",
                // "/static/bower_components/ckeditorAngularJs/ng-ckeditor.js?v=0.01",
                // "/static/angularThings/Financial/assets/plugins/angular-datatables/bundles/angular-datatables.umd.min.js",
                '/static/angularThings/share/file/classUploaderAPI.js',


                '/static/angularThings/sales/baseCtrl.js'
            ], true,
            function () {
                if (!($.fn.dataTable)) {

                    window.dt = require('/static/angularThings/datatables/datatables.js')();

                }
                // InjectToModule("ja.qr");
                // InjectToModule("md.data.table");
                // InjectToModule("ngCkeditor");
                // InjectToModule("ui.bootstrap");

            })
    },
    'SalesTataabogh': {
        url: '/SalesTataabogh',
        parent: 'Sales',
        templateUrl: '/page/salesTataabogh/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/sales/TataaboghCtrl.js'
        ], true)
    },
    'SalesConversations': {
        url: '/SalesConversations',
        parent: 'Sales',
        templateUrl: '/page/salesConversations/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/share/file/classUploaderAPI.js',
            '/static/angularThings/sales/salesConversationCtrl.js'
        ], true)
    },
    'SalesConv': {
        url: '/SalesConv',
        parent: 'Sales',
        templateUrl: '/page/salesConv/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/share/file/classUploaderAPI.js',
            '/static/angularThings/sales/ConvCtrl.js'
        ], true)
    },
    'SalesMojoodi': {
        url: '/SalesMojoodi',
        parent: 'Sales',
        templateUrl: '/page/salesMojoodi/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/share/file/classUploaderAPI.js',
            '/static/angularThings/sales/SalesMojoodiCtrl.js'
        ], true)
    },
    'SalesProfile': {
        url: '/SalesProfile',
        parent: 'Sales',
        templateUrl: '/page/SalesProfile/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/share/file/classUploaderAPI.js',
            '/static/angularThings/sales/SalesProfileCtrl.js'
        ], true)
    },


    'SalesReportBase': {
        url: '/SalesReport',
        parent: 'base',
        templateUrl: '/page/sales_report_base/',
        resolve: GenerateJsResolveFiles([
                '/static/angularThings/sales/reports/salesReportBaseCtrl.js'
            ], true,
            function () {


            })
    },

    'KhoroojRep1': {
        url: '/khoroojRep1',
        parent: 'SalesReportBase',
        templateUrl: '/page/KhoroojRep1/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/sales/reports/khorooj/KhoroojRep1Ctrl.js'

        ], true)
    },

    'HavalehForooshTrace': {
        url: '/havalehForooshTrace',
        parent: 'SalesReportBase',
        templateUrl: '/page/sales_report_trace_havaleh_foroosh/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/sales/reports/havalehForoosh/havalehForooshTraceCtrl.js'

        ], true)
    },

    'OldHavalehForoosh': {
        url: '/OldHavalehForoosh',
        parent: 'Sales',
        templateUrl: '/page/OldHavalehForoosh/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/sales_old/havalehForoosh/HavalehForooshCtrl.js'
        ], true)
    },
    'OldHavalehForooshChange': {
        url: '/:ApproveID/:Step/OldHavalehForooshChange',
        parent: 'Sales',
        templateUrl: '/page/OldHavalehForooshChange/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/sales_old/havalehForoosh/HavalehForooshChangeCtrl.js'

        ], true)
    },
    'OldHavalehForooshDetails': {
        url: '/Oldhf/:hfdid/details',
        parent: 'Sales',
        templateUrl: '/page/OldHavalehForooshDetails/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/share/file/classUploaderAPI.js',
            '/static/angularThings/sales_old/sign/signBodyCtrl.js',
            '/static/angularThings/sales_old/havalehForoosh/HavalehForooshDetailsCtrl.js'

        ], true)
    },


    'HavalehForoosh': {
        url: '/HavalehForoosh',
        parent: 'Sales',
        templateUrl: '/page/HavalehForoosh/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/sales/havalehForoosh/HavalehForooshCtrl.js'
        ], true)
    },
    'HavalehForooshChange': {
        url: '/:ApproveID/:Step/HavalehForooshChange',
        parent: 'Sales',
        templateUrl: '/page/HavalehForooshChange/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/sales/havalehForoosh/HavalehForooshChangeCtrl.js'

        ], true)
    },
    'HavalehForooshDetails': {
        url: '/hf/:hfdid/details',
        parent: 'Sales',
        templateUrl: '/page/HavalehForooshDetails/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/share/file/classUploaderAPI.js',
            '/static/angularThings/sales/sign/signBodyCtrl.js',
            '/static/angularThings/sales/havalehForoosh/HavalehForooshDetailsCtrl.js'

        ], true)
    },


    'Pishfactor': {
        url: '/Pishfactor/:pishID/',
        parent: 'Sales',
        templateUrl: '/page/get_pishfactor_base/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/sales/pishfactor/PishfactorBaseCtrl.js'

        ], true)
    },
    'Khorooj': {
        url: '/Khorooj',
        parent: 'Sales',
        templateUrl: '/page/Khorooj/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/share/file/classUploaderAPI.js',
            '/static/angularThings/sales/khorooj/KhoroojCtrl.js'

        ], true)
    },
    'KhoroojDetails': {
        url: '/kh/:khid/details',
        parent: 'Sales',
        templateUrl: '/page/KhoroojDetails/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/sales/sign/signBodyCtrl.js',
            '/static/angularThings/share/file/classUploaderAPI.js',
            '/static/angularThings/sales/khorooj/KhoroojDetailsCtrl.js'

        ], true)
    },
    'SendSMS': {
        url: '/sendsms',
        parent: 'Sales',
        templateUrl: '/page/SendSMS/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/sales/SendSMS/SendSMSBaseCtrl.js'

        ], true)
    },
    'MojoodiGhabeleForoosh': {
        url: '/MojoodiGhabeleForoosh',
        parent: 'Sales',
        templateUrl: '/page/MojoodiGhabeleForooshBase/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/sales/mojoodi/MojoodiGhabeleForooshBaseCtrl.js'

        ], true)
    },

    'OldKhorooj': {
        url: '/OldKhorooj',
        parent: 'Sales',
        templateUrl: '/page/OldKhorooj/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/share/file/classUploaderAPI.js',
            '/static/angularThings/sales_old/khorooj/KhoroojCtrl.js'

        ], true)
    },
    'OldKhoroojDetails': {
        url: '/kh/:khid/olddetails',
        parent: 'Sales',
        templateUrl: '/page/OldKhoroojDetails/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/sales_old/sign/signBodyCtrl.js',
            '/static/angularThings/share/file/classUploaderAPI.js',
            '/static/angularThings/sales_old/khorooj/KhoroojDetailsCtrl.js'

        ], true)
    },

    'Fees': {
        url: '/Fees',
        parent: 'Sales',
        templateUrl: '/page/fees/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/Fees/baseCtrl.js'

        ], true)
    },

    'SalesProfileDetails': {
        url: '/:profileID/SalesProfileDetails',
        parent: 'Sales',
        templateUrl: '/page/SalesProfileDetails/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/share/file/classUploaderAPI.js',
            '/static/angularThings/sales/SalesProfileDetailsCtrl.js'

        ], true)
    },
    'SalesProfilePhones': {
        url: '/SalesProfilePhones',
        parent: 'Sales',
        templateUrl: '/page/SalesProfilePhones/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/sales/SalesProfilePhonesCtrl.js'
        ], true)
    },
    'SalesConversationsItems': {
        url: '/:ConvID/SalesConversationsItems',
        parent: 'Sales',
        templateUrl: '/page/salesConversationsItems/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/share/file/classUploaderAPI.js',
            '/static/angularThings/share/autocomplete.js',
            '/static/angularThings/sales/SalesConversationItemsCtrl.js'
        ], true)
    },
    'SalesTamin': {
        url: '/SalesTamin',
        parent: 'Sales',
        templateUrl: '/page/salesTamin/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/sales/tamin/TaminCtrl.js'

        ], true)
    },
    'SalesTaminProjects': {
        url: '/SalesTaminProjects',
        parent: 'SalesTamin',
        templateUrl: '/page/SalesTaminProjects/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/sales/tamin/taminProject/TaminProjectCtrl.js'
        ], true)
    },
    'SalesTaminDetails': {
        url: '/SalesTaminDetails',
        parent: 'SalesTamin',
        templateUrl: '/page/SalesTaminDetails/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/sales/tamin/Details/DetailsCtrl.js'

        ], true)
    },
    'Karshenasi': {
        url: '/Karshenasi',
        parent: 'SalesTamin',
        templateUrl: '/page/Karshenasi/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/sales/tamin/karshenasi/karshenasiCtrl.js'
        ], true)
    },
    'KarshenasiTahili': {
        url: '/KarshenasiTahili',
        parent: 'SalesTamin',
        templateUrl: '/page/KarshenasiTahili/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/sales/tamin/karshenasi/TahlilKarshenasiCtrl.js'
        ], true)
    },
    'TaminDakheliRegistered': {
        url: '/TaminDakheliRegistered',
        parent: 'SalesTamin',
        templateUrl: '/page/AdminTaminDakheli/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/share/file/classUploaderAPI.js',
            '/static/angularThings/sales/tamin/registered/TaminDakheliRegisteredCtrl.js'
        ], true)
    },
    'TaminDakheliRegisteredDetails': {
        url: '/:details/TaminDakheliRegisteredDetails/',
        parent: 'SalesTamin',
        templateUrl: '/page/AdminTaminDakheliDetails/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/share/file/classUploaderAPI.js',
            '/static/angularThings/sales/tamin/registered/TaminDakheliRegisteredDetailsCtrl.js'
        ], true)
    },
    'CustomerTahili': {
        url: '/CustomerTahili',
        parent: 'Sales',
        templateUrl: '/page/SalesCustomerTahili/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/sales/tamin/karshenasi/CustomerTahlilCtrl.js'

        ], true)
    },
    'CustomerTahiliDetails': {
        url: '/:cusID/CustomerTahiliDetails\'',
        parent: 'Sales',
        templateUrl: '/page/SalesCustomerTahiliDetails/',
        resolve: GenerateJsResolveFiles([
            '/static/angularThings/sales/tamin/karshenasi/CustomerTahlilDetailsCtrl.js'
        ], true)
    },

    //  cog ----------------------------------------------------------
    //  cog ----------------------------------------------------------
    //  cog ----------------------------------------------------------
    //  cog ----------------------------------------------------------
    //  cog ----------------------------------------------------------
    //  cog ----------------------------------------------------------
    //  cog ----------------------------------------------------------

    'cog': {
        url: '/cog',
        parent: 'base',
        templateUrl: '/Financial/page/cog/',
        resolve: GenerateJsResolveFiles([

                '/static/bower_components/datatables/datatables.js',
                '/static/bower_components/datatables/datatables.min.css',

                '/static/bower_components/handsontable/handsontable.full.min.css',
                // '/static/bower_components/handsontable/ngHandsontable.min.js',

                // '/static/bower_components/jquery-ui/themes/base/jquery.ui.all.css',
                '/static/bower_components/datatables/DataTables-1.10.18/css/dataTables.jqueryui.min.css',

                '/static/angularThings/Financial/my.js',
                '/static/angularThings/Financial/cog/cogCtrl.js'
            ], true,
            function () {

                if (!($.fn.dataTable)) {
                    console.log("data table not loaded...!");
                }
                // InjectToModule("ngHandsontable");
            })
    },
    'control_project': {
        url: '/control_project',
        parent: 'base',
        templateUrl: '/page/control_project/',
    },
    'cog_home': {
        url: '/cog_home',
        parent: 'cog',
        templateUrl: '/Financial/page/cog_home/',
        resolve: GenerateJsResolveFiles([
                '/static/bower_components/datatables/datatables.js',
                '/static/angularThings/Financial/cog/CogHomeCtrl.js'

            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
    'cog_m_avalieh': {
        url: '/rialiAvaleDoreh',
        parent: 'cog_home',
        templateUrl: '/Financial/page/cog_rialiAvaleDoreh/',
        resolve: GenerateJsResolveFiles([
                '/static/angularThings/Financial/cog/rialiAvaleDoreh/RialiAvaleDorehCtrl.js'
            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
    'cog_m_77_base': {
        url: '/rial77',
        parent: 'cog_home',
        templateUrl: '/Financial/page/cog_m_77_base/',
        resolve: GenerateJsResolveFiles([
                '/static/angularThings/Financial/cog/riali77/Cog77BaseCtrl.js'
            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
    'cog_m_77': {
        url: '/rial77',
        parent: 'cog_m_77_base',
        templateUrl: '/Financial/page/cog_rial77/',
        resolve: GenerateJsResolveFiles([
                '/static/angularThings/Financial/cog/riali77/RialM77Ctrl.js'
            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
    'cog_m_riali_sazi_77': {
        url: '/rialSazi77',
        parent: 'cog_m_77_base',
        templateUrl: '/Financial/page/cog_rialSazi77/',
        resolve: GenerateJsResolveFiles([
                '/static/angularThings/Financial/cog/rialiSazi77/RialSazi77Ctrl.js'
            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
    'cog_m_riali_sazi_77_ebtedaye_doreh': {
        url: '/rialSazi77EbtedayeDore',
        parent: 'cog_m_77_base',
        templateUrl: '/Financial/page/cog_rialSazi77_ebtedaye_doreh/',
        resolve: GenerateJsResolveFiles([
                '/static/angularThings/Financial/cog/rialiSazi77/RialSazi77EbtedayeDorehCtrl.js'

            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
    'cog_m_gardeshe_77': {
        url: '/cog_Gardeshe77',
        parent: 'cog_m_77_base',
        templateUrl: '/Financial/page/cog_Gardeshe77/',

        resolve: GenerateJsResolveFiles([
                '/static/angularThings/Financial/cog/rialiSazi77/Gardeshe77Ctrl.js'

            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
    'cog_ghooti_base': {
        url: '/cog_ghooti_base',
        parent: 'cog_home',
        templateUrl: '/Financial/page/cog_ghooti_base/',

        resolve: GenerateJsResolveFiles([
                '/static/angularThings/Financial/cog/riali89/RialSazi89BaseCtrl.js'

            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
    'cog_gardesh_ghooti_ebtedaye_doreh': {
        url: '/GardesheGhootiEbtedayeDoreh',
        parent: 'cog_ghooti_base',
        templateUrl: '/Financial/page/cog_MGhootiEbtedayeDoreh/',

        resolve: GenerateJsResolveFiles([
                '/static/angularThings/Financial/cog/rialiGhooti/RialSaziGhootiEbtedayeDorehCtrl.js'

            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
    'cog_gardesh_ghooti': {
        url: '/GardesheGhooti',
        parent: 'cog_ghooti_base',
        templateUrl: '/Financial/page/cog_GardesheGhooti/',

        resolve: GenerateJsResolveFiles([
                '/static/angularThings/Financial/cog/rialiGhooti/GardesheGhootiCtrl.js'

            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
    'cog_base_asaan_baz_shoo': {
        url: '/cog_ghooti_base',
        parent: 'cog_home',
        templateUrl: '/Financial/page/cog_base_asaan_baz_shoo/',

        resolve: GenerateJsResolveFiles([
                '/static/angularThings/Financial/cog/rialiAsaanBazShoo/RialSaziAsanBaseCtrl.js'

            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
    'cog_gardesh_asaan_baz_shoo_ebtedaye_doreh': {
        url: '/GardesheAsaanBaazShooEbtedayeDoreh',
        parent: 'cog_base_asaan_baz_shoo',
        templateUrl: '/Financial/page/cog_MAsaanBazShooEbtedayeDoreh/',

        resolve: GenerateJsResolveFiles([
                '/static/angularThings/Financial/cog/rialiAsaanBazShoo/RialSaziAsaanBazShooEbtedayeDorehCtrl.js'

            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
    'cog_gardesh_asaan_baz_shoo': {
        url: '/GardesheAsaanBazShoo',
        parent: 'cog_base_asaan_baz_shoo',
        templateUrl: '/Financial/page/cog_MAsaanBazShoo/',

        resolve: GenerateJsResolveFiles([
                '/static/angularThings/Financial/cog/rialiAsaanBazShoo/GardesheAsaanBazShooCtrl.js'

            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
    'cog_report': {
        url: '/CogReport',
        parent: 'cog_home',
        templateUrl: '/Financial/page/cog_report/',

        resolve: GenerateJsResolveFiles([
                '/static/angularThings/Financial/cog/reports/CogReportCtrl.js'

            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
    'cog_report_check': {
        url: '/CogReportCheck',
        parent: 'cog_home',
        templateUrl: '/Financial/page/cog_report_check/',

        resolve: GenerateJsResolveFiles([
                '/static/angularThings/Financial/cog/reports/CogReportCheckCtrl.js'

            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },

    'cog_m_88_base': {
        url: '/cog_m_88_base',
        parent: 'cog_home',
        templateUrl: '/Financial/page/cog_m_88_base/',

        resolve: GenerateJsResolveFiles([
                '/static/angularThings/Financial/cog/riali88/RialSazi88BaseCtrl.js'

            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
    'cog_m_riali_sazi_88_ebtedaye_doreh': {
        url: '/rialSazi88EbtedayeDore',
        parent: 'cog_m_88_base',
        templateUrl: '/Financial/page/cog_rialSazi88_ebtedaye_doreh/',
        resolve: GenerateJsResolveFiles([
                '/static/angularThings/Financial/cog/riali88/RialSazi88EbtedayeDorehCtrl.js'

            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
    'cog_m_gardeshe_88': {
        url: '/cog_Gardeshe88',
        parent: 'cog_m_88_base',
        templateUrl: '/Financial/page/cog_rialSazi88/',

        resolve: GenerateJsResolveFiles([
                '/static/angularThings/Financial/cog/riali88/RialSazi88Ctrl.js'

            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },


    'cog_ca_home': {
        url: '/CA',
        parent: 'cog_home',
        templateUrl: '/Financial/page/cog_ca_home/',
        resolve: GenerateJsResolveFiles([
                '/static/angularThings/Financial/cog/ca/CaHomeCtrl.js'

            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
    'cog_ca_automated_sums': {
        url: '/calc',
        parent: 'cog_ca_home',
        templateUrl: '/Financial/page/cog_ca_automated_sum/',

        resolve: GenerateJsResolveFiles([
                '/static/angularThings/Financial/cog/ca/CaAutomatedSumsCtrl.js'

            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
    'cog_ca_categorize': {
        url: '/Sales',
        parent: 'cog_home',
        templateUrl: '/Financial/page/cog_ca_categ/',

        resolve: GenerateJsResolveFiles([
                '/static/angularThings/Financial/cog/ca/AccCategoryCtrl.js'

            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
    'cog_salemali': {
        url: '/salemali',
        parent: 'cog_home',
        templateUrl: '/Financial/page/cog_salemali/',

        resolve: GenerateJsResolveFiles([
                '/static/angularThings/Financial/cog/salemali/salemaliCtrl.js'

            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
    'cog_ca_davayere_tolidi': {
        url: '/cog_ca_davayere_tolidi',

        parent: 'cog_ca_home',
        templateUrl: '/Financial/page/cog_ca_davayere_tolidi/',

        resolve: GenerateJsResolveFiles([
                '/static/angularThings/Financial/cog/ca/CaToDavayereTolidiCtrl.js'

            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
    'cog_ca_after_calc': {
        url: '/cog_ca_after_calc',

        parent: 'cog_ca_home',
        templateUrl: '/Financial/page/cog_ca_after_calc/',

        resolve: GenerateJsResolveFiles([
                '/static/angularThings/Financial/cog/ca/CaToDavayereTolidiAfterCalcCtrl.js'

            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
// 89 ------------------------------------------------------
// 89 ------------------------------------------------------
// 89 ------------------------------------------------------
    'cog_89_base': {
        url: '/cog_89_base',
        parent: 'cog_home',
        templateUrl: '/Financial/page/cog_M89Base/',

        resolve: GenerateJsResolveFiles([
                '/static/angularThings/Financial/cog/riali89/RialSazi89BaseCtrl.js'

            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
    'cog_89_ebtedaye_doreh': {
        url: '/rialSazi89EbtedayeDore',
        parent: 'cog_89_base',
        templateUrl: '/Financial/page/cog_rialSazi89_ebtedaye_doreh/',
        resolve: GenerateJsResolveFiles([
                '/static/angularThings/Financial/cog/riali89/RialSazi89EbtedayeDorehCtrl.js'

            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
    'cog_89_gardesh': {
        url: '/cog_89_gardesh',
        parent: 'cog_89_base',
        templateUrl: '/Financial/page/cog_89_gardesh/',
        resolve: GenerateJsResolveFiles([
                '/static/angularThings/Financial/cog/riali89/Gardeshe89Ctrl.js'

            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
// 89 ------------------------------------------------------
// 89 ------------------------------------------------------
// 85 ------------------------------------------------------
// 85 ------------------------------------------------------
    'cog_85_base': {
        url: '/cog_85_base',
        parent: 'cog_home',
        templateUrl: '/Financial/page/cog_85_base/',

        resolve: GenerateJsResolveFiles([
                '/static/angularThings/Financial/cog/riali85/RialSazi85BaseCtrl.js'

            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
    'cog_85_ebtedaye_doreh': {
        url: '/cog_85_ebtedaye_doreh',
        parent: 'cog_85_base',
        templateUrl: '/Financial/page/cog_85_ebtedaye_doreh/',
        resolve: GenerateJsResolveFiles([
                '/static/angularThings/Financial/cog/riali85/RialSazi85EbtedayeDorehCtrl.js'

            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
    'cog_85_gardesh': {
        url: '/cog_85_gardesh',
        parent: 'cog_85_base',
        templateUrl: '/Financial/page/cog_85_gardesh/',
        resolve: GenerateJsResolveFiles([
                '/static/angularThings/Financial/cog/riali85/RialSazi85Ctrl.js'

            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
// 75 ------------------------------------------------------
// 75 ------------------------------------------------------
    'cog_75_base': {
        url: '/cog_75_base',
        parent: 'cog_home',
        templateUrl: '/Financial/page/cog_75_base/',

        resolve: GenerateJsResolveFiles([
                '/static/angularThings/Financial/cog/riali75/RialSazi75BaseCtrl.js'

            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
    'cog_75_ebtedaye_doreh': {
        url: '/cog_75_ebtedaye_doreh',
        parent: 'cog_75_base',
        templateUrl: '/Financial/page/cog_75_ebtedaye_doreh/',
        resolve: GenerateJsResolveFiles([
                '/static/angularThings/Financial/cog/riali75/RialSazi75EbtedayeDorehCtrl.js'

            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
    'cog_75_gardesh': {
        url: '/cog_75_gardesh',
        parent: 'cog_75_base',
        templateUrl: '/Financial/page/cog_75_gardesh/',
        resolve: GenerateJsResolveFiles([
                '/static/angularThings/Financial/cog/riali75/RialSazi75Ctrl.js'

            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
    // material -------------------------------------
    // material -------------------------------------
    // material -------------------------------------
    // material -------------------------------------
    'material_base': {
        url: '/material',
        parent: 'base',
        templateUrl: '/Material/page/materialbase/',
        resolve: GenerateJsResolveFiles([
                "/static/angularThings/datatables/datatables.js",
                "/static/bower_components/angular-timeline/angular-timeline.css?v=0.01",
                "/static/bower_components/angular-timeline/angular-timeline-bootstrap.css?v=0.01",
                "/static/bower_components/angular-timeline/angular-timeline-animations.css?v=0.01",
                "/static/angularThings/datatables/datatables.min.css",
                '/static/angularThings/material/baseCtrl.js',


            ], true,
            function () {
                if (!($.fn.dataTable)) {

                    window.dt = require('/static/angularThings/datatables/datatables.js')();

                }
            })
    },
    'material_locations': {
        url: '/material-locations',
        parent: 'material_base',
        templateUrl: '/Material/page/materiallocations/',
        resolve: GenerateJsResolveFiles([
                '/static/angularThings/material/locationsCtrl.js'

            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
    'material_baskol': {
        url: '/material_baskol',
        parent: 'material_base',
        templateUrl: '/Material/page/materialbaskol/',
        resolve: GenerateJsResolveFiles([
                '/static/angularThings/material/baskolCtrl.js'

            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
    'material_vorood_khrooj': {
        url: '/material_vorood_khrooj',
        parent: 'material_base',
        templateUrl: '/Material/page/materialVoroodKhrooj/',
        resolve: GenerateJsResolveFiles([
                '/static/angularThings/material/materialVoroodKhroojCtrl.js'

            ], true,
            function () {
                // InjectToModule("ja.qr");
            })
    },
    'material_barcode_list': {
        url: '/material_barcode_list',
        parent: 'material_base',
        templateUrl: '/Material/page/materialBarcodeList/',
        resolve: GenerateJsResolveFiles([
                '/static/angularThings/material/barcodeListCtrl.js'
            ], true,
            function () {
                if (!($.fn.dataTable)) {

                    window.dt = require('/static/angularThings/datatables/datatables.js')();

                }
            })
    },
    'material_bakol_to_anbar': {
        url: '/material_bakol_to_anbar',
        parent: 'material_base',
        templateUrl: '/Material/page/fromBaskolToAnbar/',
        resolve: GenerateJsResolveFiles([
                '/static/angularThings/material/materialBakolToAnbarCtrl.js'
            ], true,
            function () {
                if (!($.fn.dataTable)) {
                    window.dt = require('/static/angularThings/datatables/datatables.js')();
                }
            })
    },
    'qc_blackplate': {
        url: '/qc_blackplate',
        parent: 'material_base',
        templateUrl: '/Material/page/fromQCBlackplate/',
        resolve: GenerateJsResolveFiles([
                '/static/angularThings/material/fromQCBlackplateCtrl.js'
            ], true,
            function () {
                if (!($.fn.dataTable)) {
                    window.dt = require('/static/angularThings/datatables/datatables.js')();
                }
            })
    },
    'material_tolid_sale_conv': {
        url: '/material_tolid_sale_conv',
        parent: 'material_base',
        templateUrl: '/Material/page/tolidSaleConv/',
        resolve: GenerateJsResolveFiles([
                '/static/angularThings/material/tolidSaleConvCtrl.js'
            ], true,
            function () {
                // if (!($.fn.dataTable)) {
                //     window.dt = require('/static/angularThings/datatables/datatables.js')();
                // }
            })
    },
    'material_tolid_sale_conv_sale': {
        url: '/material_tolid_sale_conv_sale',
        parent: 'material_tolid_sale_conv',
        templateUrl: '/Material/page/tolidSaleConvSale/',
        resolve: GenerateJsResolveFiles([
                '/static/angularThings/material/tolidSaleConvSaleCtrl.js'
            ], true,
            function () {
                // if (!($.fn.dataTable)) {
                //     window.dt = require('/static/angularThings/datatables/datatables.js')();
                // }
            })
    },
    'material_tolid_sale_conv_sale_item': {
        url: '/:sale_item/material_tolid_sale_conv_sale_item',
        parent: 'material_tolid_sale_conv_sale',
        templateUrl: '/Material/page/tolidSaleConvSaleItem/',
        resolve: GenerateJsResolveFiles([
                '/static/angularThings/material/tolidSaleConvSaleItemCtrl.js'
            ], true,
            function () {
                // if (!($.fn.dataTable)) {
                //     window.dt = require('/static/angularThings/datatables/datatables.js')();
                // }
            })
    }
    ,
    'material_barname_base': {
        url: '/material_barname_base',
        parent: 'material_base',
        templateUrl: '/Material/page/materialBarnameBase/',
        resolve: GenerateJsResolveFiles([
                // "/static/bower_components/pivottable/dist/plotly-basic-latest.min.js",
                // "/static/bower_components/pivottable/dist/pivot.min.js",
                // "/static/bower_components/pivottable/dist/plotly_renderers.min.js",
                '/static/angularThings/material/MaterialBarnameBase.js'
            ], true,
            function () {
                // if (!($.fn.dataTable)) {
                //     window.dt = require('/static/angularThings/datatables/datatables.js')();
                // }
            })
    },
    'material_barname_tolid': {
        url: '/material_barname_tolid',
        parent: 'material_base',
        templateUrl: '/Material/page/materialBarnameTolid/',
        resolve: GenerateJsResolveFiles([
                // "/static/bower_components/pivottable/dist/plotly-basic-latest.min.js",
                // "/static/bower_components/pivottable/dist/pivot.min.js",
                // "/static/bower_components/pivottable/dist/plotly_renderers.min.js",
                '/static/angularThings/material/TolidMavadAzBarnameriziCtrl.js'
            ], true,
            function () {
                // if (!($.fn.dataTable)) {
                //     window.dt = require('/static/angularThings/datatables/datatables.js')();
                // }
            })
    },
    'material_reports': {
        url: '/material_reports',
        parent: 'material_base',
        templateUrl: '/Material/page/materialReportBase/',
        resolve: GenerateJsResolveFiles([
                '/static/angularThings/material/MaterialReportBaseCtrl.js'
            ], true,
            function () {


            })
    },
    'material_reports_report_1': {
        url: '/material_reports_1',
        parent: 'material_reports',
        templateUrl: '/Material/page/materialReport1/',
        resolve: GenerateJsResolveFiles([
                '/static/angularThings/material/MaterialReport1Ctrl.js'
            ], true,
            function () {

            })
    },
    'material_reports_report_2': {
        url: '/material_reports_2',
        parent: 'material_reports',
        templateUrl: '/Material/page/materialReport2/',
        resolve: GenerateJsResolveFiles([
                '/static/angularThings/material/MaterialReport2Ctrl.js'
            ], true,
            function () {

            })
    }
}