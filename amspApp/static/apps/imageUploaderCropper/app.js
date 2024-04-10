angular.module('app',
    ['ngMaterial', 'ui.router', 'ui.tree', 'ngDragDrop', 'oc.lazyLoad', 'pascalprecht.translate', 'ngSanitize', 'md.data.table', 'ngFileUpload', 'angular-img-cropper']
)
    .config(function ($interpolateProvider, $httpProvider) {
        $interpolateProvider.startSymbol('//');
        $interpolateProvider.endSymbol('//');
        $httpProvider.defaults.timeout = 1;
        $httpProvider.defaults.xsrfCookieName = 'rahsoon-CSRF-TOKEN';
        $httpProvider.defaults.xsrfHeaderName = 'rahsoon-csrftoken';
    })
    .config(['$mdIconProvider', function ($mdIconProvider) {
        $mdIconProvider
            .defaultFontSet('FontAwesome')
            .fontSet('fa', 'FontAwesome')
            .defaultIconSet('/static/images/open-iconic-master/sprite/open-iconic.min.svg', 14)
    }])
    .config(function ($translateProvider) {
        $translateProvider.useUrlLoader('/api/v1/language/');

        $translateProvider.preferredLanguage('fa');
        // Enable escaping of HTML
        $translateProvider.useSanitizeValueStrategy('escape')
    })
    .config(function ($mdThemingProvider) {


        $mdThemingProvider.definePalette('mcgpalette0', {
            '50': '#f4fcfd',
            '100': '#b2e8f2',
            '200': '#82d9ea',
            '300': '#45c7e0',
            '400': '#2bbfdc',
            '500': '#21acc7',
            '600': '#1d95ad',
            '700': '#187f93',
            '800': '#146878',
            '900': '#10515e',
            'A100': '#f4fcfd',
            'A200': '#b2e8f2',
            'A400': '#2bbfdc',
            'A700': '#187f93',
            'contrastDefaultColor': 'light',
            'contrastDarkColors': '50 100 200 300 400 500 A100 A200 A400'
        });

        $mdThemingProvider.definePalette('mcgpalette1', {
            '50': '#f8fcfc',
            '100': '#c1e6e4',
            '200': '#99d6d2',
            '300': '#66c2bc',
            '400': '#50b9b2',
            '500': '#43a8a1',
            '600': '#3a928c',
            '700': '#327c77',
            '800': '#296662',
            '900': '#20504d',
            'A100': '#f8fcfc',
            'A200': '#c1e6e4',
            'A400': '#50b9b2',
            'A700': '#327c77',
            'contrastDefaultColor': 'light',
            'contrastDarkColors': '50 100 200 300 400 500 A100 A200 A400'
        });

        $mdThemingProvider.definePalette('mcgpalette2', {
            '50': '#f7f8f2',
            '100': '#d9dec0',
            '200': '#c3ca9b',
            '300': '#a7b16d',
            '400': '#9ba759',
            '500': '#89934e',
            '600': '#767f43',
            '700': '#646b39',
            '800': '#51572e',
            '900': '#3e4324',
            'A100': '#f7f8f2',
            'A200': '#d9dec0',
            'A400': '#9ba759',
            'A700': '#646b39',
            'contrastDefaultColor': 'light',
            'contrastDarkColors': '50 100 200 300 400 500 A100 A200 A400'
        });

        $mdThemingProvider.definePalette('mcgpalette3', {
            '50': '#fffdfb',
            '100': '#fbd2b3',
            '200': '#f8b37e',
            '300': '#f48b3a',
            '400': '#f27a1d',
            '500': '#e46b0d',
            '600': '#c75d0b',
            '700': '#aa500a',
            '800': '#8d4208',
            '900': '#703506',
            'A100': '#fffdfb',
            'A200': '#fbd2b3',
            'A400': '#f27a1d',
            'A700': '#aa500a',
            'contrastDefaultColor': 'light',
            'contrastDarkColors': '50 100 200 300 400 500 A100 A200 A400'
        });

        $mdThemingProvider.definePalette('mcgpalette4', {
            '50': '#fff3ea',
            '100': '#ffc79e',
            '200': '#ffa666',
            '300': '#ff7d1e',
            '400': '#ff6b00',
            '500': '#e05e00',
            '600': '#c15100',
            '700': '#a34400',
            '800': '#843700',
            '900': '#662b00',
            'A100': '#fff3ea',
            'A200': '#ffc79e',
            'A400': '#ff6b00',
            'A700': '#a34400',
            'contrastDefaultColor': 'light',
            'contrastDarkColors': '50 100 200 300 400 A100 A200 A400'
        });

        $mdThemingProvider.theme('mcgtheme')

            .primaryPalette('blue')

            .accentPalette('orange');


    })
    .controller('myApp', function ($scope, $http, $window) {


        $scope.cropper = {};
        $scope.cropper.sourceImage = null;
        $scope.cropper.croppedImage = null;
        $scope.bounds = {};
        $scope.bounds.left = 0;
        $scope.bounds.right = 0;
        $scope.bounds.top = 0;
        $scope.bounds.bottom = 0;


        $scope.UploadPic = function () {
            $("#file").click();
        }


        function dataURItoBlob(dataURI) {
            var byteString = atob(dataURI.split(',')[1]);
            var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0]
            var ab = new ArrayBuffer(byteString.length);
            var ia = new Uint8Array(ab);
            for (var i = 0; i < byteString.length; i++) {
                ia[i] = byteString.charCodeAt(i);
            }

            var blob = new Blob([ab], {type: mimeString});
            return blob;
        }

        $scope.sendProfilePic = function () {


            var img = "";

            img = $(".croppedAvt").attr("src");

            // iframe = $("iframe");

            // debugger;

            // debugger;
            //
            //
            // var formData = new FormData();
            // var croppedImage = dataURItoBlob(vm.myCroppedImage);

            // formData.set("file", croppedImage, "myProfile.jpg");


            $http.post("/api/v1/profile/saveProfileFromCropper/", {avatar: img}).then(function (data) {


                if (data.data.img) {
                    parent.AvatarCompleted(img);
                }
            });
        }

    });
