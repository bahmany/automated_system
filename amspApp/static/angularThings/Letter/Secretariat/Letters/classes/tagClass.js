'use strict';

function TagClass($scope, $http, $q, tagSecType) {


    $scope.AddNewTag = function () {
        swal({
                title: "تگ جدید",
                text: "لطفا عنوان تگ مورد نظر را وارد نمایید",
                type: "input",
                showCancelButton: true,
                closeOnConfirm: false,
                animation: "slide-from-top",
                showLoaderOnConfirm: true,
                inputPlaceholder: "عنوان تگ"
            },
            function (inputValue) {
                if (inputValue === false) return false;

                if (inputValue === "") {
                    swal.showInputError("نامی را وارد نمایید");
                    return false
                }

                $http.post("/api/v1/letter/sec/tag/", {
                    "name": inputValue,
                    "type": tagSecType
                }).then(function (data) {
                    if (data.data.id) {
                        $scope.GetAllTags();
                        swal("ثبت شد", "تک جدید شما :  " + inputValue, "success");
                    } else {
                        swal("خطا", "شما مجاز به ثبت تگ نیستید", "error");
                    }
                }).catch(function (data) {
                    swal("خطا", "شما مجاز به ثبت تگ نیستید", "error");

                });

            });
    };
    $scope.EditTag = function (selectedTag) {
        swal({
                title: "تغییر تگ",
                text: "نام جدید را وارد نمایید",
                type: "input",
                showCancelButton: true,
                closeOnConfirm: false,
                animation: "slide-from-top",
                inputPlaceholder: "نام تگ اجباریست"
            },
            function (inputValue) {
                if (inputValue === false) return false;

                if (inputValue === "") {
                    swal.showInputError("لطفا خالی رها نکنید");
                    return false
                }
                $http.patch("/api/v1/letter/sec/tag/" + selectedTag.id + "/", {
                    "name": inputValue,
                    "type": tagSecType

                }).then(function (data) {
                    if (data.data.id) {
                        $scope.GetAllTags();

                        swal("انجام شد", "تگ جدید با نام: " + inputValue + " ثبت شد", "success");
                    } else {
                        swal("خطا", "شما مجاز به ثبت تگ نیستید", "error");
                    }
                }).catch(function (data) {
                    swal("خطا", "شما مجاز به ثبت تگ نیستید", "error");
                });
            });
    }
    $scope.RemoveTagFromLetter = function (tag) {
        swal({
                title: "برداشتن تگ از نامه",
                text: "آیا از برداشتن تگ انتخابی از نامه مورد نظر اطمینان دارید؟",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "بله و حذف شود",
                cancelButtonText: "خیر و انصراف",
                closeOnConfirm: false,
                closeOnCancel: false
            },
            function (isConfirm) {
                if (isConfirm) {
                    $http.get("/api/v1/letter/sec/tag/"+tag.id+"/removeFromLetter/").then(function (data) {
                        $scope.GetAllTags();
                        swal("حذف شد", "تگ مورد نظر از نامه جدا شد", "success");
                    }).catch(function (data) {
                        swal("خطا", "شما مجاز به ثبت تگ نیستید", "error");

                    })
                } else {
                    swal("انصراف", "تگ مورد نظر جدا نشد", "error");
                }
            });
    };
    $scope.RemoveTagFromSec = function (tag) {
        swal({
                title: "حذ تگ از دبیرخانه",
                text: "آیا شما از حذف تگ اطمینان دارید ؟",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "بله حذف شود",
                cancelButtonText: "انصراف ",
                closeOnConfirm: false,
                closeOnCancel: false
            },
            function (isConfirm) {
                if (isConfirm) {
                    $http.delete("/api/v1/letter/sec/tag/" + tag.id + "/").then(function (data) {
                        $scope.GetAllTags();

                        swal("حذف شد", "تگ انتخابی شما حذف شد", "success");

                    }).catch(function () {
                        swal("خطا", "شما مجاز به حذف تگ نیستید", "error");

                    })
                } else {
                    swal("انصراف", "تگ مد نظر شما حذف نشد", "error");
                }
            });
    };
    function loadContacts() {
        return $scope.tagsResult.map(function (c, index) {
            var name = c.name;
            var id = c.id;
            var contact = {
                name: name,
                id: id
            };
            contact._lowername = contact.name.toLowerCase();
            return contact;
        });
    }
    var pendingSearch, cancelSearch = angular.noop;
    var lastSearch;
    $scope.allContacts = loadContacts;
    $scope.asyncContacts = [];
    $scope.filterSelected = true;
    $scope.querySearch = querySearch;
    $scope.delayedQuerySearch = delayedQuerySearch;
    $scope.tagsResult = [];
    function querySearch(criteria) {
        return criteria ? $scope.allContacts().filter(createFilterFor(criteria)) : [];
    }

    function delayedQuerySearch(criteria) {
        return pendingSearch = $q(function (resolve, reject) {
            cancelSearch = reject;
            $http.get("/api/v1/letter/sec/tag/?q=" + criteria).then(function (data) {
                var newN = [];
                for (var i = 0; data.data.length > i; i++) {
                    newN.push({
                        "name": data.data[i]["name"] + " (" + data.data[i]["count"].toString() + ")",
                        "id": data.data[i]["id"]
                    });
                }
                $scope.tagsResult = newN;
                resolve($scope.querySearch(criteria))
            });

        });


        return pendingSearch;
    }

    function refreshDebounce() {
        lastSearch = 0;
        pendingSearch = null;
        cancelSearch = angular.noop;
    }

    function debounceSearch() {
        var now = new Date().getMilliseconds();
        lastSearch = lastSearch || now;

        return ((now - lastSearch) < 300);
    }

    function createFilterFor(query) {
        console.log("createFilterFor(" + query + ")");
        var lowercaseQuery = angular.lowercase(query);
        return function filterFn(contact) {
            return (contact._lowername.indexOf(lowercaseQuery) != -1);
        };

    }

    $scope.EditingMode = false;
    $scope.makeEdit = function (editMode) {
        if (editMode == 1) {
            $scope.EditingMode = true;

        }
        if (editMode == 2) {
            $scope.EditingMode = false;

        }
    }

    $scope.tags = [];
    $scope.GetAllTags = function () {
        $http.get("/api/v1/letter/sec/tag/?q=&t=" + tagSecType.toString()).then(function (data) {
            $scope.tags = data.data;
        }).catch(function (data) {

        })
    };
    $scope.GetAllTags();
    $scope.GetTagFilter = function (tag) {
        if (tag.selected) {
            tag.selected = false;
        } else {
            tag.selected = true;
        }

        $scope.filter.tags = [];
        $scope.tags.forEach(function (value) {
            if (value.selected) {
                $scope.filter.tags.push(value.id)
            }
        });
        $scope.filter.tags = $scope.filter.tags.join();
    }
}