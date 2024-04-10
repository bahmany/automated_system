'use strict';


function loadFileUploader($scope, Upload, $http) {


    $scope.UploadedFiles = [];
    $scope.listFileFolders = [];
    $scope.listFileFoldersJson = [];
    $scope.UploadPercent = "-";
    $scope.fileFolder = {};
    $scope.isEditing = false;
    $scope.SelectedFileFolder = {};
    $scope.FolderFiles = [];
    $scope.draggedFoldersFiles = [];
    $scope.draggedFile = {};
    $scope.isUploading = false;


    $scope.uploadFiles = function (files) {
        $scope.isUploading = true;
        if (files && files.length) {
            for (var i = 0; i < files.length; i++) {
                $scope.isUploading = true;
                Upload.upload({
                    method: 'POST',
                    headers: {'Content-Type': files[i].type},
                    data: {
                        file: files[i]
                    },
                    file: files[i],
                    url: '/api/v1/file/upload'
                }).then(function (resp) {
                    // console.log(resp);
                    $scope.isUploading = false;
                    var newObject = {
                        'lastModified': resp.config.file.lastModified,
                        'lastModifiedDate': resp.config.file.lastModifiedDate,
                        'name': resp.config.file.name,
                        'size': resp.config.file.size,
                        'type': resp.config.file.type
                    };
                    var upladed = {
                        imgLink: "/api/v1/file/upload?q=thmum50_" + resp.data.name,
                        imgInf: newObject
                    };
                    $scope.UploadedFiles.push(upladed);
                }, function (resp) {

                    $scope.isUploading = false;

                }, function (evt) {
                    $scope.UploadPercent = parseInt(100.0 * evt.loaded / evt.total);

                })
            }

        }
    };
    $scope.GetFoldersList = function () {
        $http.get("/api/v1/file/folders/").then(function (data) {
            $scope.listFileFolders = data.data;
        })
    };
    $scope.GetFoldersJson = function () {
        $http.get("/api/v1/file/folders/getRecursive/").then(function (data) {
            $scope.listFileFoldersJson = data.data;
        })
    };
    $scope.GetFoldersJson();
    $scope.OpenFolderEdit = function () {
        $scope.isEditing = true;
    };
    $scope.CancelFolderEdit = function () {
        $scope.isEditing = false;
        $scope.fileFolder = {};
    };
    $scope.EditFileFolder = function (item) {
        $scope.fileFolder = item;
        $scope.OpenFolderEdit();
    };
    $scope.PostFolder = function () {
        if ($scope.fileFolder.hasOwnProperty("id")) {
            $http.put("/api/v1/file/folders/" + $scope.fileFolder.id + "/", $scope.fileFolder).then(function (data) {
                $scope.GetFoldersList();
                $scope.GetFoldersJson();
                $scope.isEditing = false;
            })
        } else {
            $http.post("/api/v1/file/folders/", $scope.fileFolder).then(function (data) {
                $scope.GetFoldersList();
                $scope.GetFoldersJson();
                $scope.isEditing = false;
            })
        }
    };
    $scope.DeleteFileFolder = function (node) {
        if (confirm("Ready to Remove Folder ?")) {
            $http.delete("/api/v1/file/folders/" + node.id + "/").then(function (data) {
                $scope.GetFoldersList();
                $scope.GetFoldersJson();
            })
        }
    };
    $scope.RemoveFromUploaded = function (index) {
        if (confirm("Ready to Delete from Uploaded ?")) {
            $scope.UploadedFiles.splice(index, 1);
        }
    };
    $scope.RemoveFromCloud = function (item, $index) {
        if (confirm("Ready to Delete from Cloud ?")) {
            $http.delete("/api/v1/file/folders/" + item.folder.id + "/items/" + item.id + "/").then(function (data) {
                $scope.FolderFiles.results.splice($index, 1);
                $scope.ShowSelectedFolderItems();
            })
        }
    };
    $scope.EditCloudFileName = function (item, $index) {
        var ccc = window.prompt("Enter new name", item.file.originalFileName)
        if (ccc == "") {
            return
        }
        if (ccc) {
            $http.put("/api/v1/file/folders/" + item.folder.id + "/items/" + item.id + "/", {
                "file.originalFileName": ccc
            }).then(function (data) {
                $scope.FolderFiles.results.splice($index, 1);
                $scope.ShowSelectedFolderItems();
            })
        }
    };
    $scope.AddFileToFolder = function (file, event, index) {
        event.stopPropagation();
        if ($scope.SelectedFileFolder == {}) {
            alert("Please select a folder");
            return
        }
        $http.post("/api/v1/file/folders/" + $scope.SelectedFileFolder.id + "/items/", file).then(function (data) {
            $scope.ShowSelectedFolderItems();
        })

    };
    $scope.ShowSelectedFolderItems = function () {
        $http.get("/api/v1/file/folders/" + $scope.SelectedFileFolder.id + "/items/").then(function (data) {
            $scope.FolderFiles = data.data;

        })
    };
    $scope.SelectFolder = function (folder, event) {
        $(".inbox-dynamic-folders").css("background-color", "white");
        $(event.target).css("background-color", "rgb(178, 196, 242)");
        $scope.SelectedFileFolder = folder;
        $scope.ShowSelectedFolderItems();
    };
    // getting folders list for select parent combobox
    $scope.GetFoldersList();
    $scope.AddFromCloudToSelected = function (item) {
        var obj = {};
        obj.imgInf = {};
        obj.imgInf.size = item.file.size;
        obj.imgInf.name = item.file.originalFileName;
        obj.imgLink = item.file.decodedFileName;
        obj.thisIsCloud = true;
        $scope.UploadedFiles.push(obj);


    };
    $scope.$on('ngRepeatFinished', function (ngRepeatFinishedEvent) {
        $(".inbox-dynamic-items").hover(function () {
            //$(this).css("background-color", "#FAFFB7");
            $(this).find(".btnss").fadeIn(70);
        }, function () {
            //$(this).css("background-color", "#FFFFFF");
            $(this).find(".btnss").fadeOut(20);
        });

        //$(".inbox-dynamic-items .fa-cloud-download").click(function (e) {
        //
        //})

    });
    $scope.startCallback = function (event, ui, title) {
        //
        //   //////console.log(title);
        //var newOne = angular.copy(title);
        $scope.draggedFile = angular.copy(title);
        $(".inbox-dynamic-folders").addClass("drag-started-folders");
        //return false;
    };
    $scope.stopCallback = function (event, ui) {
        ////////console.log('Why did you stop draggin me?');
        $(".inbox-dynamic-folders").removeClass("drag-started-folders");
    };
    $scope.dragCallback = function (event, ui) {
        ////////console.log('hey, look I`m flying');
    };
    $scope.dropCallback = function (event, ui, folder, hhh) {
        var q = {
            fileID: this.dndDragItem.id,
            folderID: folder.id
        };
        $http.post("/api/v1/file/folders/UpdateFileToFolder/", q).then(function (data) {
            $scope.GetFoldersJson();
        });
    };


}