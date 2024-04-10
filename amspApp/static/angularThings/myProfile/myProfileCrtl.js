'use strict';


angular.module('AniTheme').controller(
    'profileCtrl',
    function ($scope,
              $translate,
              $q,
              $rootScope,
              $http,
              $modal,
              ProfileService) {

        $scope.Profile = {};
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


        //it is for timeline pagination
        $scope.loadMore = function (element) {
            if ($scope.Posts.next == null) {
                $(element.target).addClass('disabled');
            } else {
                ProfileService.listPostsByUrl($scope.Posts.next).then(function (data) {
                    for (var i = 0; data.data.results.length > i; i++) {
                        $scope.Posts.results.push(data.data.results[i]);
                    }

                    $scope.Posts.next = data.data.next;

                });
            }
        };

        $scope.GetProfile = function () {
            ProfileService.retrieveProfile().then(function (data) {
                // checking if first time
                $http.get("/api/v1/forced/profileSeenFirstTime/").then(function (data) {
                    if (data.data.result == false) {
                        introJs("body").start();
                    }
                    //////console.log("intro start");
                });
                $scope.Profile = data.data;
            })
        };
        $scope.GetProfile();


        $scope.Post = {};

        $scope.Posts = [];
        $scope.ListPosts = function () {
            ProfileService.listPosts().then(function (data) {
                $scope.Posts = data.data;
                ////console.log($scope.Profile.extra);
                $("#imgPostAvatar").attr("src", $scope.Profile.extra.profileAvatar.url);
                $(".fit-height").mCustomScrollbar({
                    theme: "minimal-dark",
                    alwaysShowScrollbar: 1
                });
            });
        };
        $scope.ListPosts();


        $scope.CreatePost = function () {
            var defer = $q.defer();

            var res = ProfileService.createPost($scope.Post);
            res.then(function (data) {
                $scope.ListPosts();
                return defer.resolve(res);

            }).catch(function (data) {
                return defer.reject("");

            });
            return defer.promise;

        };

        $scope.UpdatePost = function (item) {
            ProfileService.updatePost(item.id, item).then(function (data) {
                item.isItEditing = false;

            })
        };

        $scope.ShowUpdatePanel = function (post) {
            post.isItEditing = true;
        }
        $scope.CancelUpdatePost = function (post) {
            post.isItEditing = false;
        }

        $scope.DeletePost = function (item, $index) {
            swal({
                title: "Are you sure?",
                text: "After deleting the phone number, You can not recover that",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "Yes, delete it!",
                closeOnConfirm: false
            }, function () {

                ProfileService.deletePost(item.id).then(
                    function (data) {
                        $scope.ListPosts();
                        swal("Deleted!", "Your post successfully deleted", "success");
                        item.splice($index, 1);
                        $scope.$apply();
                    });
            });
        };

        $scope.AddPhone = function (profile) {
            $scope.Profile.extra.Phones.push({
                tel: "enter your number here ...",
                security: 1,
                phoneORemail: 1
            })
        };
        $scope.RemovePhone = function (item, index) {
            swal({
                title: "Are you sure?",
                text: "After deleting the phone number, You can not recover that",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "Yes, delete it!",
                closeOnConfirm: false
            }, function () {
                item.splice(index, 1);
                $scope.$apply()
                swal("Deleted!", "Your phone successfully deleted, press save button to commit your changes", "success");
            });
        }
        $scope.ChangeAccessPhone = function (item) {
            item.security += 1;
            if (item.security == 5) {
                item.security = 1;
            }
        };
        $scope.ChangeAccessPhoneType = function (item) {
            item.phoneORemail += 1;
            if (item.phoneORemail == 3) {
                item.phoneORemail = 1;
            }
        };


        $scope.UpdateProfile = function () {
            var defer = $q.defer();
            var res = ProfileService.updateProfile($scope.Profile);
            res.then(function (data) {
                return defer.resolve(res);
            }).catch(function (data) {
                data.message.forEach(function (err) {
                    swal(err.name, err.message, "error");
                });
                return defer.reject("");
            });

            return defer.promise;
        };


    });

