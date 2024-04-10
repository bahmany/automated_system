'use strict';

angular.module('AniTheme').controller(
    'LetterComposeCtrl',
    function ($scope,
              $translate,
              $q,
              $http, $$$,
              $rootScope,
              $stateParams,
              $state,
              $location,
              $timeout,
              $compile,
              Upload,
              shareServiceBool,
              LetterInboxService,
              LetterComposeService) {
        $rootScope.$broadcast("hideInboxLeft");

        $scope.finalList = [];
        $scope.paramOfSend = {};
        $scope.letter = {};
        $scope.selects = [];
        $scope.empty = {};
        $scope.selectedFiles = [];


        $rootScope.$on("updateAttachments", function (event, SelectedObjs) {
            $scope.selectedFiles = SelectedObjs;
            $scope.letter.attachments = SelectedObjs;
            $scope.saveLetter();

        })


        $scope.editorOptions = {
            language: 'fa',
            toolbar: [
                {
                    name: 'document',
                    items: ['Source', '-', 'Save', 'NewPage', 'DocProps', 'Preview', 'Print', '-', 'Templates']
                },
                {name: 'clipboard', items: ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
                {name: 'editing', items: ['Find', 'Replace', '-', 'SelectAll', '-', 'SpellChecker', 'Scayt']},
                {
                    name: 'forms',
                    items: ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                        'HiddenField']
                },
                '/',
                {
                    name: 'basicstyles',
                    items: ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']
                },
                {
                    name: 'paragraph',
                    items: ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv',
                        '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl']
                },
                {name: 'links', items: ['Link', 'Unlink', 'Anchor']},
                {
                    name: 'insert',
                    items: ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']
                },
                '/',
                {name: 'styles', items: ['Styles', 'Format', 'Font', 'FontSize']},
                {name: 'colors', items: ['TextColor', 'BGColor']},
                {name: 'tools', items: ['Maximize', 'ShowBlocks', '-', 'About']}

            ],
            extraPlugins: 'lineutils,notification,uploadwidget,uploadimage',
            removePlugins: 'sourcearea',
            filebrowserUploadUrl: '/api/v1/file/upload',
            resize_maxHeight: 900,
            height: 600
        };


        $scope.$on("setPrevLetter", function (event, args) {
            $scope.MakeLetterToEdit(args.letterPrev.letter);
        });
        $scope.doesLetterPreparedToEdit = false;
        $scope.MakeLetterToEdit = function (letter) {
            $scope.letter = letter;
            $scope.UploadedFiles = $scope.letter.attachments;
            $scope.letter.selectedMembers = $scope.letter.recievers;
        };
        $scope.initial = function () {
            if ($scope.prevLetterReplay) {
                if ($scope.prevLetterReplay.hasOwnProperty('letter')) {
                    ////////console.log("This is replay !!");
                    var newObj = angular.copy($scope.prevLetterReplay);
                    $timeout(function () {
                        //////debugger;
                        $scope.letter.subject = "پاسخ :" + newObj.letter.subject;
                        $scope.letter.replyedInbox = newObj;
                        ////////console.log($scope.letter);
                        $scope.letter.body = "<div>" + $$$("Related letter text") + " : </div><div class='replay-frame'>" + newObj.letter.body + "</div><div>" + $$$("type here") + "</div>";
                        $scope.letter.selectedMembers = [];
                        $scope.letter.selectedMembers.push(newObj.sender);
                        ////////console.log($scope.prevLetterReplay);
                        $scope.prevLetterReplay = {};
                    }, 0);

                }

            }

            $scope.GetLetter();
            loadFileUploader($scope, Upload, $http);

        };
        $scope.GetLetter = function () {
            $http.get("/api/v1/letter/" + $stateParams.letterID + "/").then(function (data) {
                if (data.data.exp) {
                    if (data.data.exp.extraAttachments) {
                        $scope.UploadedFiles = data.data.exp.extraAttachments;
                    }
                }
                $scope.letter = data.data;
            });
        };
        $scope.loadPanel = function (panelName) {
            $(".hideIt").hide();
            $("#" + panelName).show();

        };
        //$scope.SelectAttachments = function () {
        //$scope.loadPanel("divUploads");
        //$scope.loadRecieverPanel();
        //};
        $scope.CancelAttachments = function () {
            //$scope.loadPanel("divMessage");
            //$scope.loadRecieverPanel();
        };
        $scope.AcceptAtts = function () {
            $scope.loadPanel("divMessage");
            //$scope.loadRecieverPanel();
        };
        $scope.selectPositions = function () {
            ////console.log("PositionsLoded...");
            $rootScope.$broadcast("setSelectMemProp", {
                prevDivName: "divCompose",
                currDivName: "divRec",
                thisListIsFor: 1, // compose
                letterID: $stateParams.letterID
            });
            if ($scope.letter.hasOwnProperty("exp")) {

                if ($scope.letter.exp.hasOwnProperty("recievers_raw")) {
                    if ($scope.letter.exp.recievers_raw.hasOwnProperty("id")) {
                        $rootScope.$broadcast("CallMembers", $scope.letter.exp.recievers_raw.id);
                    }
                }
            }
            $("#divCompose").fadeOut(function () {
                $("#divRec").fadeIn();
            });
            $scope.saveLetter();
        };
        $scope.selectAtts = function () {
            $rootScope.$broadcast("setAtts", {
                prevDivName: "#divCompose",
                currDivName: "#divAtts",
                thisListIsFor: 1, // compose
                letterID: $stateParams.letterID
            });
            //////console.log($scope.letter);
            if ($scope.letter.hasOwnProperty("exp")) {
                if ($scope.letter.exp.hasOwnProperty("attachment_raw")) {
                    if ($scope.letter.exp.attachment_raw.hasOwnProperty("id")) {
                        $rootScope.$broadcast("CallFileAtts", $scope.letter.exp.attachment_raw.id);
                    }
                }
            }
            $("#divCompose").fadeOut(function () {
                $("#divAtts").fadeIn();
            });
            $scope.saveLetter();
        };
        $scope.RemoveFromUploaded = function (index) {
            $scope.letter.attachments.splice(index, 1);
        }
        // $scope.$on("UpdateFiles", function (event, args) {
        //////console.log(args);
        // $scope.letter.attachments = args.files;
        // var ex = $scope.letter.exp;
        // ex.attachment_raw = args;
        // $scope.letter.exp = ex;
        // $scope.saveLetter();
        // });
        $scope.$on("UpdateRecievers", function (event, args) {
            if (!$scope.letter.exp) {
                $scope.letter.exp = {};
            }
            //debugger;
            var ex = $scope.letter.exp;
            ex.recievers_id = args.id;
            ex.recievers_raw = args;
            $scope.letter.recievers = args.afterProcess;
            $scope.letter.exp = ex;
            $scope.saveLetter();
        });
        $scope.handleSelect = function () {
            //$scope.letter.selectedMembers = $scope.Selected.data;
            $scope.loadPanel("divMessage");
        };
        $scope.cancelSelect = function () {
            $scope.loadPanel("divMessage");
        };
        $scope.sendLetter = function () {

            if (true == $scope.isUploading) {
                sweetAlert("صبر کنید", "لطفا تا پایان انتقال فایل ها منتظر بمانید", "warning");
                return
            }

            if (!$scope.CheckLetterIntegrity($scope.letter)) {
                return;
            }
            $scope.letter.itemType = 1;
            // in the server
            // backend automatically change item mode to 7 for first send and
            // put 1 to other
            // to show in send items
            $scope.letter.itemMode = 1;
            $scope.letter.itemPlace = 1;
            $scope.letter.letterType = $scope.letter.itemType;
            $scope.letter.letterMode = $scope.letter.itemMode;
            $scope.letter.letterPlace = $scope.letter.itemPlace;
            $scope.letter.previousInboxId = $stateParams.inboxID;
            $scope.postLetter("با موفقیت ارسال شد");
            // $scope.cancelLetter();
        };
        $scope.SaveAsDraftThenClose = function () {
            $scope.saveLetter();
            //$scope.cancelLetter();

        }
        $scope.saveLetter = function () {
            if ($scope.isUploading === true) {
                sweetAlert("صبر کنید", "لطفا تا پایان انتقال فایل ها منتظر بمانید", "warning");
                return
            }
            //debugger;
            $scope.letter.itemType = 7;
            $scope.letter.itemMode = 4;
            $scope.letter.itemPlace = 1;
            if (!$scope.letter.subject) {
                $scope.letter.subject = " ";
            }
            if (!$scope.letter.body) {
                $scope.letter.body = " ";
            }
            $scope.postLetter("با موفقیت در پیش نویس ها ذخیره شد");
        };
        $scope.cancelLetter = function () {
            //$scope.ComposeModal.dismiss("cancel");
            shareServiceBool.set(true);
            $location.path('/dashboard/Letter/Inbox/List');
        };

        $scope.isSending = false;
        $scope.postLetter = function (succmsg) {
            $scope.isSending = true;

            if (!$scope.letter.exp) {
                $scope.letter.exp = {};
            }
            $scope.letter.exp.extraAttachments = $scope.UploadedFiles;
            LetterComposeService.SendLetter($scope.letter).then(function (data) {
                if (data.data.id) {
                    $rootScope.$broadcast("showToast", succmsg);
                    $rootScope.$broadcast("callInboxItems");
                    $rootScope.$broadcast("sendSuccShowInbox", data.data);
                    $rootScope.GetIntimeNotification();
                    $scope.isSending = false;
                    if (succmsg === "با موفقیت ارسال شد") {
                        $location.path('/dashboard/Letter/Inbox/List');
                    }

                } else {
                    sweetAlert("اخطار", "مشکلی پیش آمده", "error");
                    $scope.isSending = false;


                }
            }).catch(function (data) {
                sweetAlert("اخطار", "مشکلی پیش آمده", "error");
                $scope.isSending = false;

                return;
            })
        };
        $scope.CheckLetterIntegrity = function (letter) {
            //debugger;
            if (!$scope.letter.subject) {
                sweetAlert("اخطار", "عنوان نامه را وارد نمایید", "error");
                return false;
            }
            if ($scope.letter.subject == "") {
                sweetAlert("اخطار", "عنوان نامه را وارد نمایید", "error");
                return false;
            }
            if (!$scope.letter.recievers) {
                sweetAlert("اخطار", "شخص یا اشخاصی را بعنوان گیرنده نامه انتخاب نمایید", "error");
                return false;
            }
            if ($scope.letter.recievers.length < 1) {
                sweetAlert("اخطار", "شخص یا اشخاصی را بعنوان گیرنده نامه انتخاب نمایید", "error");
                return false;
            }
            return true;

        };
        $scope.initial();

    });
