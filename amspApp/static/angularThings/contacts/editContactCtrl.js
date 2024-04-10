'use strict';

angular.module('AniTheme')
    .controller('ContactModalCtrl',
    [
        '$scope',
        '$modal',
        '$translate',
        '$http','$rootScope',
        //'oldItem',
        function ($scope,
                  $modal,
                  $translate,
                  $http,$rootScope
                  //oldItem
        ) {


            $scope.NewContact = {};
            $scope.Contact = {};

            $scope.$root.$on("SetCurrentContact", function (event, args) {
                if (args) {
                    $scope.Contact = args;
                    $("#inputContactName").hide();
                    $("#ContactForm").show();
                }
            });

            $scope.init = function () {
                $rootScope.$broadcast("GetSelectedContact");
            };

            $scope.init();


            $scope.ChangeLabel = function (item) {
                var newName = prompt("Please Enter Label Name", item.fieldName);
                if (newName) {
                    item.fieldName = newName;
                }
            };

            $scope.AddNewField = function (item) {
                $scope.Contact.fields.push({
                    fieldName: "Label...",
                    fieldValue: "",
                    placeholder: "+98-912-111-2222",
                    require: false,
                    style: "direction:ltr!important"
                })
            };

            $scope.ChangeStar = function () {
                $scope.Contact.extra.starred = !($scope.Contact.extra.starred == true);
            };

            $scope.CreateContact = function () {
                $scope.Contact = {
                    fields: [{
                        fieldName: "Name",
                        fieldValue: $scope.NewContact.Name,
                        require: true,
                        style: "direction:rtl!important"
                    }],
                    publish: {
                        privacy: 1,
                        other_companies_can_see: false
                    },
                    extra: {
                        starred: false,
                        avatar: "/static/images/default-avatar-contact.jpg"
                    }
                };
                $http.post("/api/v1/contacts/", $scope.Contact).then(function (data) {
                    $scope.Contact = data.data;
                    $("#inputContactName").fadeOut(function () {
                        $("#ContactForm").fadeIn()
                    })
                });
            };

            $scope.PostContact = function () {
                var t = this;
                $http.patch("/api/v1/contacts/" + $scope.Contact.id + "/", $scope.Contact).then(function (data) {
                    $scope.Contact = data.data;
                $rootScope.$broadcast("reloadContacts");

                    t.$parent.$dismiss('cancel');


                });
            }
            $scope.CancelContact = function () {
                //////console.log(this);
                this.$parent.$dismiss('cancel');
            }
        }]);
