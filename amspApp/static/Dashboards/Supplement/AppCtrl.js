'use strict';

angular.module('Supplement').controller(
    'AppCtrl',
    function ($scope,
              $q,
              $http,
              $state,
              $location,
              $rootScope,
              $timeout) {


        $scope.pages_order = [
            [],
            [],
            [],
            [],
            [1, 4, 7, 19, 21, 14, 16, 25, 26],
            [2, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 25, 26],
            [3, 5, 6, 7, 20, 12, 22, 23, 24, 15, 13, 18, 25, 26],
            [],
            []
        ];

        $scope.menuTitles = [
            '',
            'اطلاعات فروشنده ',
            'اطلاعات خدماتی ها',
            'اطلاعات سازندگان',
            'اطلاعات تماس ',
            'اطلاعات تماس سازندگان',
            'اطلاعات هیات مدیره',
            'عضویت در لیست تامین کنندگان ',
            'حق امتیاز ، لیسانس یا نمایندگی ',
            'تعداد کارکنان در مقاطع تحصیلی',
            'مشخصات کارکنان کلیدی',
            'محصولات یا خدمات',
            'استاندارد ها',
            'سابقه قراردادهای قبلی',
            'حسن سابقه',
            'حسن سابقه',
            'سوالات مخصوص ',
            'سوالات مخصوص ',
            'سوالات مخصوص ',
            'زمینه فعالیت',
            'زمینه فعالیت',
            'سوابق کاری',
            'فهرست تجهیزات',
            'گواهینامه ها',
            'تضمین کیفیت',
            'آپلود فایل',
            'کد  پیگیری'
        ];

        $scope.menuTitlesExp = [
            '',
            'در این قسمت اطلاعاتی از قبل نام فروشنده ، نوع شرکت ، شماره ثبت سایر اطلاعات هویتی فروشنده وارد می شود',
            'اطلاعات خدماتی ها',
            'اطلاعات سازندگان',
            'در این قسمت اطلاعات مربوط به نحوه ی ارتباط با فروشنده یا تامین کننده خدمات قرار میگیرد مثل پست الکترونیکی ، شماره های تماس و ...',
            'اطلاعات تماس سازندگان',
            'اطلاعات هیات مدیره',
            '  عضویت در لیست تامین کنندگان سایر شرکت ها ',
            '  در صورت دارا بودن حق امتیاز ، لیسانس یا نمایندگی ',
            'تعداد کارکنان در مقاطع تحصیلی',
            '  لطفا مشخصات کارکنان کلیدی خود را وارد کنید ',
            'محصولات یا خدمات قابل ارائه',
            '  استاندارد های ****ی ،نظامنامه يا گواهی نامه های مديريت ',
            'سابقه قراردادهای قبلی طی ۳ سال گذشته',
            '  حسن سابقه در کارهای قبلی مخصوص خدماتی',
            '  حسن سابقه در کارهای قبلی مخصوص سازندگان',
            'سوالات مخصوص فروشندگان',
            'سوالات مخصوص خدماتی',
            'سوالات مخصوص سازندگان',
            '  زمینه فعالیت مخصوص فروشندگان',
            '  زمینه فعالیت مخصوص سازندگان',
            'سوابق کاری و حرفه ای',
            'فهرست ماشین الات ، تجهیزات و دستگاه ها با ارائه مستندات لازم',
            'گواهینامه های استاندارد محصولات',
            'تضمین کیفیت محصول و خدمات پس از فروش',
            'آپلود فایل',
            'ثبت'
        ];


        $scope.type = 2;
        $scope.getUerType = function () {
            $http.get("/dashboards/api/v1/firstreg/getUserType/").then(function (data) {
                $scope.type = data.data.type;
            })
        };
        $scope.getUerType();

        $rootScope.$on("changeLeftSlider", function (event, args) {
            $scope.action = args.action;
            console.log('-----------------');
            console.log(args);
        });


        $rootScope.$on("fileUploading", function (event, args) {
            $scope.isUploading = args.action;
            console.log('-----------------');
            console.log(args);
        })


    });