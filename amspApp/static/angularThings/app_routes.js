'use strict';
app.config(function ($stateProvider, $urlRouterProvider) {

    $urlRouterProvider.when('/dashboard', '/dashboard/home');
    $urlRouterProvider.when('/dashboard/Letter', '/dashboard/Letter/list');
    $urlRouterProvider.otherwise('/dashboard/home');

    $stateProvider
        .state('base', routes_details['base'])
        .state('freeRahsoon', routes_details['freeRahsoon'])
        .state('welcomeBase', routes_details['welcomeBase'])
        .state('welcomepage', routes_details['welcomepage'])
        .state('welcomepageClient', routes_details['welcomepageClient'])
        .state('selectnames', routes_details['selectnames'])
        .state('selectpics', routes_details['selectpics'])
        .state('welcomeDone', routes_details['welcomeDone'])
        .state('404-page', routes_details['404-page'])
        .state('_dash', routes_details['_dash'])
        .state('dashboard', routes_details['dashboard'])

        .state('home', routes_details['home'])
        .state('net', routes_details['net'])


        .state('bi', routes_details['bi'])
        .state('bi-groups', routes_details['bi-groups'])

        .state('bi-menus', routes_details['bi-menus'])


        .state('bi-dashboard-pages', routes_details['bi-dashboard-pages'])
        .state('bi-dashboard-pages-design', routes_details['bi-dashboard-pages-design'])


        .state('bi-charts', routes_details['bi-charts'])
        .state('bi-chart-design', routes_details['bi-chart-design'])


        .state('bi-datasources', routes_details['bi-datasources'])
        .state('bi-datasources-design', routes_details['bi-datasources-design'])


        .state('bi-sqls', routes_details['bi-sqls'])

        .state('bi-pages', routes_details['bi-pages'])
        .state('bi-page', routes_details['bi-page'])


        .state('bi-sample-page-for-ceo', routes_details['bi-sample-page-for-ceo'])
        .state('bi-amare-roozaneh', routes_details['bi-amare-roozaneh'])


        .state('edari', routes_details['edari'])
        .state('hz', routes_details['hz'])
        .state('ez', routes_details['ez'])
        .state('ezitem', routes_details['ezitem'])
        .state('ezlist', routes_details['ezlist'])
        .state('ezreport', routes_details['ezreport'])
        .state('morekhasi-saati', routes_details['morekhasi-saati'])
        .state('morekhasi-saati-add', routes_details['morekhasi-saati-add'])
        .state('morekhasi-saati-list', routes_details['morekhasi-saati-list'])
        .state('morekhasi-saati-my-morekhasi', routes_details['morekhasi-saati-my-morekhasi'])
        .state('morekhasi-saati-entezamat', routes_details['morekhasi-saati-entezamat'])
        .state('morekhasi-saati-edari', routes_details['morekhasi-saati-edari'])
        .state('emzakonandeha', routes_details['emzakonandeha'])


        .state('morekhasi-roozaneh-base', routes_details['morekhasi-roozaneh-base'])


        .state('edari-report-base', routes_details['edari-report-base'])
        .state('edari-report-taradod-mahaneh', routes_details['edari-report-taradod-mahaneh'])
        .state('edari-report-mandeh-morekhasi', routes_details['edari-report-mandeh-morekhasi'])
        .state('edari-report-morekhsi-saati', routes_details['edari-report-morekhsi-saati'])
        .state('edari-report-morekhsi-roozaneh', routes_details['edari-report-morekhsi-roozaneh'])


        .state('statics', routes_details['statics'])
        .state('dms', routes_details['dms'])
        .state('new-dms', routes_details['new-dms'])
        .state('edit-dms', routes_details['edit-dms'])
        .state('newbpmn', routes_details['newbpmn'])
        .state('friends', routes_details['friends'])
        .state('Contacts', routes_details['Contacts'])
        // .state('erp_control_project', routes_details['erp_control_project'])
        .state('oldAmsp', routes_details['oldAmsp'])
        .state('myfiles', routes_details['myfiles'])
        .state('companies-dashboard', routes_details['companies-dashboard'])
        .state('company', routes_details['company'])
        .state('chart-company', routes_details['chart-company'])
        .state('members', routes_details['members'])
        .state('previewResume', routes_details['previewResume'])
        .state('secretariats', routes_details['secretariats'])
        .state('hamkari', routes_details['hamkari'])
        .state('items', routes_details['items'])
        .state('requestHamkari', routes_details['requestHamkari'])
        .state('HamkariJob', routes_details['HamkariJob'])
        .state('Connections', routes_details['Connections'])
        .state('profile', routes_details['profile'])
        .state('products', routes_details['products'])
        .state('job', routes_details['job'])
        .state('process', routes_details['process'])
        .state('new-process', routes_details['new-process'])
        .state('edit-process', routes_details['edit-process'])
        .state('datamodel-process', routes_details['datamodel-process'])
        .state('setup-process', routes_details['setup-process'])
        .state('bam', routes_details['bam'])
        .state('dashboard-bam', routes_details['dashboard-bam'])
        .state('new-bam', routes_details['new-bam'])
        .state('edit-bam', routes_details['edit-bam'])
        .state('shakhes', routes_details['shakhes'])
        .state('chart', routes_details['chart'])
        .state('myProfile', routes_details['myProfile'])
        .state('dashboardSettings', routes_details['dashboardSettings'])
        .state('secExport', routes_details['secExport'])
        .state('settings', routes_details['settings'])
        .state('Change', routes_details['Change'])
        .state('AccessToSecratariat', routes_details['AccessToSecratariat'])
        .state('letter', routes_details['letter'])
        .state('inbox', routes_details['inbox'])
        .state('list', routes_details['list'])
        .state('compose', routes_details['compose'])
        .state('preview', routes_details['preview'])
        .state('secretariat', routes_details['secretariat'])
        .state('importList', routes_details['importList'])
        .state('importPreview', routes_details['importPreview'])
        .state('importNew', routes_details['importNew'])
        .state('exportList', routes_details['exportList'])
        .state('scan', routes_details['scan'])
        .state('recieved', routes_details['recieved'])
        .state('templates', routes_details['templates'])
        .state('preview-exportList', routes_details['preview-exportList'])
        .state('exportNew', routes_details['exportNew'])
        .state('companyGroups', routes_details['companyGroups'])
        .state('sec-companies', routes_details['sec-companies'])
        .state('process-dashboard', routes_details['process-dashboard'])
        .state('inbox-process-dashboard', routes_details['inbox-process-dashboard'])
        .state('message-process-dashboard', routes_details['message'])
        .state('doMessage', routes_details['doMessage'])
        .state('doneArchive-process-dashboard', routes_details['doneArchive'])
        .state('lunchedArchive-process-dashboard', routes_details['lunchedArchive'])
        .state('inbox-process-do', routes_details['do'])
        .state('inbox-process-new', routes_details['new'])
        .state('inbox-process-diagram', routes_details['diagram'])
        .state('reports-process-dashboard', routes_details['reports-process-dashboard'])
        .state('search-process-dashboard', routes_details['search-process-dashboard'])
        .state('trackDoneProcess', routes_details['trackDoneProcess'])
        .state('trackLunchedProcess', routes_details['trackLunchedProcess'])
        .state('statistics', routes_details['statistics'])
        .state('advProcess', routes_details['advProcess'])
        .state('QC', routes_details['QC'])
        .state('QCSchedule', routes_details['QCSchedule'])
        .state('QCFinding', routes_details['QCFinding'])
        .state('QCManual', routes_details['QCManual'])
        .state('QCFindingPost', routes_details['QCFindingPost'])
        .state('QCFindingList', routes_details['QCFindingList'])
        .state('QCFindingOpen', routes_details['QCFindingOpen'])
        .state('News', routes_details['News'])
        .state('news-post', routes_details['news-post'])
        .state('NewsBlog', routes_details['NewsBlog'])
        .state('Newsread', routes_details['Newsread'])
        // .state('ControlProject', routes_details['ControlProject'])
        // .state('Year', routes_details['Year'])
        // .state('Projects', routes_details['Projects'])
        // .state('SubProjects', routes_details['SubProjects'])
        // .state('Share', routes_details['Share'])
        // .state('Outcome', routes_details['Outcome'])
        // .state('Income', routes_details['Income'])
        .state('datatables', routes_details['datatables'])
        .state('new-datatable', routes_details['new-datatable'])
        .state('script-datatable', routes_details['script-datatable'])
        .state('share-datatables', routes_details['share-datatables'])
        .state('value-datatables', routes_details['value-datatables'])
        .state('dms-dashboard', routes_details['dms-dashboard'])
        .state('new-statistics', routes_details['new-statistics'])
        .state('share-statistics', routes_details['share-statistics'])
        .state('edit-statistics', routes_details['edit-statistics'])
        .state('data-statistics', routes_details['data-statistics'])
        .state('trace', routes_details['trace'])
        .state('trace-cat', routes_details['trace-cat'])
        .state('trace-types', routes_details['trace-types'])
        .state('trace-entry', routes_details['trace-entry'])
        .state('request-goods', routes_details['request-goods'])
        .state('request-goods-chat', routes_details['request-goods-chat'])
        .state('request-goods-help', routes_details['request-goods-help'])
        .state('request-goods-item', routes_details['request-goods-item'])


        // commerce
        .state('Sales', routes_details['Sales'])
        .state('SalesTataabogh', routes_details['SalesTataabogh'])
        .state('SalesConversations', routes_details['SalesConversations'])
        .state('SalesConv', routes_details['SalesConv'])
        .state('SalesMojoodi', routes_details['SalesMojoodi'])
        .state('SalesProfile', routes_details['SalesProfile'])

        .state('SalesReportBase', routes_details['SalesReportBase'])
        .state('KhoroojRep1', routes_details['KhoroojRep1'])
        .state('HavalehForooshTrace', routes_details['HavalehForooshTrace'])


        .state('HavalehForoosh', routes_details['HavalehForoosh'])
        .state('HavalehForooshChange', routes_details['HavalehForooshChange'])
        .state('HavalehForooshDetails', routes_details['HavalehForooshDetails'])

        .state('OldHavalehForoosh', routes_details['OldHavalehForoosh'])
        .state('OldHavalehForooshChange', routes_details['OldHavalehForooshChange'])
        .state('OldHavalehForooshDetails', routes_details['OldHavalehForooshDetails'])


        .state('Khorooj', routes_details['Khorooj'])
        .state('KhoroojDetails', routes_details['KhoroojDetails'])
        .state('Pishfactor', routes_details['Pishfactor'])

        .state('MojoodiGhabeleForoosh', routes_details['MojoodiGhabeleForoosh'])

        .state('OldKhorooj', routes_details['OldKhorooj'])
        .state('OldKhoroojDetails', routes_details['OldKhoroojDetails'])

        .state('SendSMS', routes_details['SendSMS'])

        .state('Fees', routes_details['Fees'])


        .state('SalesProfileDetails', routes_details['SalesProfileDetails'])
        .state('SalesProfilePhones', routes_details['SalesProfilePhones'])
        .state('SalesConversationsItems', routes_details['SalesConversationsItems'])
        .state('SalesTamin', routes_details['SalesTamin'])
        .state('SalesTaminProjects', routes_details['SalesTaminProjects'])
        .state('SalesTaminDetails', routes_details['SalesTaminDetails'])
        .state('Karshenasi', routes_details['Karshenasi'])
        .state('KarshenasiTahili', routes_details['KarshenasiTahili'])
        .state('TaminDakheliRegistered', routes_details['TaminDakheliRegistered'])
        .state('TaminDakheliRegisteredDetails', routes_details['TaminDakheliRegisteredDetails'])
        .state('CustomerTahili', routes_details['CustomerTahili'])
        .state('CustomerTahiliDetails', routes_details['CustomerTahiliDetails'])

        .state('control_project', routes_details['control_project'])
        // financial
        .state('cog', routes_details['cog'])
        .state('cog_home', routes_details['cog_home'])
        // .state('cog_riali_sazi_ebtedaye_doreh_chaap', routes_details['cog_riali_sazi_ebtedaye_doreh_chaap'])
        // .state('cog_gardesh_chaap', routes_details['cog_gardesh_chaap'])
        // .state('cog_gardesh_ghooti_ebtedaye_doreh', routes_details['cog_gardesh_ghooti_ebtedaye_doreh'])
        // .state('cog_gardesh_ghooti', routes_details['cog_gardesh_ghooti'])
        .state('cog_report', routes_details['cog_report'])
        .state('cog_report_check', routes_details['cog_report_check'])
        // .state('cog_ca', routes_details['cog_ca'])

        // tashim ------------------------------
        .state('cog_ca_home', routes_details['cog_ca_home'])
        .state('cog_ca_automated_sums', routes_details['cog_ca_automated_sums'])
        .state('cog_ca_davayere_tolidi', routes_details['cog_ca_davayere_tolidi'])
        .state('cog_ca_after_calc', routes_details['cog_ca_after_calc'])
        // --------------------------------
        // anbar -----------------------------------
        .state('cog_m_avalieh', routes_details['cog_m_avalieh'])
        //------------------------------------
        // 77 ----------------------------------
        .state('cog_m_77_base', routes_details['cog_m_77_base'])
        .state('cog_m_77', routes_details['cog_m_77'])
        .state('cog_m_gardeshe_77', routes_details['cog_m_gardeshe_77'])
        .state('cog_m_riali_sazi_77', routes_details['cog_m_riali_sazi_77'])
        .state('cog_m_riali_sazi_77_ebtedaye_doreh', routes_details['cog_m_riali_sazi_77_ebtedaye_doreh'])
        //------------------------------------
        //88----------------------------------
        .state('cog_m_88_base', routes_details['cog_m_88_base'])
        .state('cog_m_riali_sazi_88_ebtedaye_doreh', routes_details['cog_m_riali_sazi_88_ebtedaye_doreh'])
        .state('cog_m_gardeshe_88', routes_details['cog_m_gardeshe_88'])
        //------------------------------------
        //75---Khadamaat-------------------------------
        .state('cog_75_base', routes_details['cog_75_base'])
        .state('cog_75_ebtedaye_doreh', routes_details['cog_75_ebtedaye_doreh'])
        .state('cog_75_gardesh', routes_details['cog_75_gardesh'])
        //------------------------------------
        //85---Khadamaat-------------------------------
        .state('cog_85_base', routes_details['cog_85_base'])
        .state('cog_85_ebtedaye_doreh', routes_details['cog_85_ebtedaye_doreh'])
        .state('cog_85_gardesh', routes_details['cog_85_gardesh'])
        //------------------------------------
        //89---Chaap---------------------------------
        .state('cog_89_base', routes_details['cog_89_base'])
        .state('cog_89_ebtedaye_doreh', routes_details['cog_89_ebtedaye_doreh'])
        .state('cog_89_gardesh', routes_details['cog_89_gardesh'])
        //------------------------------------
        //Ghooti------------------------------------
        .state('cog_ghooti_base', routes_details['cog_ghooti_base'])
        .state('cog_gardesh_ghooti_ebtedaye_doreh', routes_details['cog_gardesh_ghooti_ebtedaye_doreh'])
        .state('cog_gardesh_ghooti', routes_details['cog_gardesh_ghooti'])
        //------------------------------------
        //Asaan Baz Shoo ------------------------------------
        .state('cog_base_asaan_baz_shoo', routes_details['cog_base_asaan_baz_shoo'])
        .state('cog_gardesh_asaan_baz_shoo_ebtedaye_doreh', routes_details['cog_gardesh_asaan_baz_shoo_ebtedaye_doreh'])
        .state('cog_gardesh_asaan_baz_shoo', routes_details['cog_gardesh_asaan_baz_shoo'])

        //---Settings ---------------------------------
        .state('cog_ca_categorize', routes_details['cog_ca_categorize'])
        .state('cog_salemali', routes_details['cog_salemali'])

        // ---Material -----------------------------------
        .state('material_base', routes_details['material_base'])
        .state('material_locations', routes_details['material_locations'])
        .state('material_baskol', routes_details['material_baskol'])
        .state('material_vorood_khrooj', routes_details['material_vorood_khrooj'])
        .state('material_barcode_list', routes_details['material_barcode_list'])
        .state('material_bakol_to_anbar', routes_details['material_bakol_to_anbar'])
        .state('qc_blackplate', routes_details['qc_blackplate'])
        .state('material_tolid_sale_conv', routes_details['material_tolid_sale_conv'])
        .state('material_tolid_sale_conv_sale', routes_details['material_tolid_sale_conv_sale'])
        .state('material_tolid_sale_conv_sale_item', routes_details['material_tolid_sale_conv_sale_item'])
        .state('material_barname_base', routes_details['material_barname_base'])
        .state('material_barname_tolid', routes_details['material_barname_tolid'])
        .state('material_reports', routes_details['material_reports'])
        .state('material_reports_report_1', routes_details['material_reports_report_1'])
        .state('material_reports_report_2', routes_details['material_reports_report_2'])


    for (let i = 0; i < 27; i++) {
        $stateProvider.state('s' + i.toString(), {
            parent: 'TaminDakheliRegisteredDetails',
            url: '/s' + i.toString(),
            params: {formIndex: i},
            templateUrl: '/dashboards/page/supplyItems/' + i.toString() + "/",
            resolve: {
                deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        name: 'OCletter',
                        files: [
                            '/static/angularThings/share/file/FileUploaderCtrl.js',
                            '/static/angularThings/share/file/FileUploaderService.js',
                            '/static/angularThings/sales/tamin/registered/GoodsProvidersCtrl.js'
                        ], catch: true
                    }).then(function () {
                    })
                }]
            }
        })
    }


    $GlobalStateProvider = $stateProvider;
});
