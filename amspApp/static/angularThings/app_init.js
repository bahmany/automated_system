'use strict';


window.app_version = 1.11;
var $GlobalStateProvider;
var CKEDitor_loaded = false;
var happenedCreatedBefore = false;

var app = angular
    .module(
        'AniTheme', [
            'ui.router',
            'ivh.treeview',
            'ngMaterial',
            'ngAnimate',
            // 'ngSanitize',
            // 'angularTreeview',
            // 'textAngular',
            // 'angular-progress-button-styles',
            'pascalprecht.translate',
            'ui.bootstrap',
            'ngCookies',
            'ng',
            // 'ds.clock',
            // 'md.data.table',
            'ngDragDrop',
            'ui.tree',
            // 'ui.tree',
            'ngFileUpload',
            'material.components.table',
            'picker',
            'ngProgress',
            'oc.lazyLoad',
            'ngCkeditor',
            'fcsa-number',
            'ui.select',
            'ui.codemirror',
            'ngMask',
            'ui.mask',
            // 'chart.js',
            'fg',
            'ja.qr',
            'angularTreeview',
            'ngHandsontable',
            // 'luegg.directives',
            // 'angular-timeline',
            'angular-scroll-animate'
        ]);