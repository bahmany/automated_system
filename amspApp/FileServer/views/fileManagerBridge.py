# coding:utf8

import datetime
import os
import shutil
import stat
import tempfile
import uuid
import zipfile

import errno

import unicodedata
from asq.initiators import query

from amsp import settings
from amspApp.FileServer.models import FileManagerItem
from amspApp.FileServer.serializers.FileSerializer import FileManagerItemSerializer
from amspApp.MyProfile.models import Profile


def timestamp_to_str(timestamp, format_str='%Y-%m-%d %I:%M:%S'):
    date = datetime.datetime.fromtimestamp(timestamp)
    return date.strftime(format_str)


def filemode(mode):
    is_dir = 'd' if stat.S_ISDIR(mode) else '-'
    dic = {'7': 'rwx', '6': 'rw-', '5': 'r-x', '4': 'r--', '0': '---'}
    perm = str(oct(mode)[-3:])
    return is_dir + ''.join(dic.get(x, x) for x in perm)


def get_file_information(path):
    fstat = os.stat(path)
    if stat.S_ISDIR(fstat.st_mode):
        ftype = 'dir'
    else:
        ftype = 'file'

    fsize = fstat.st_size
    ftime = timestamp_to_str(fstat.st_mtime)
    fmode = filemode(fstat.st_mode)

    return ftype, fsize, ftime, fmode


def change_permissions_recursive(path, mode):
    for root, dirs, files in os.walk(path, topdown=False):
        for d in [os.path.join(root, d) for d in dirs]:
            os.chmod(d, mode)
        for f in [os.path.join(root, f) for f in files]:
            os.chmod(f, mode)


def zipdir(dirPath=None, zipFilePath=None, includeDirInZip=True):
    if not zipFilePath:
        zipFilePath = dirPath + ".zip"
    if not os.path.isdir(dirPath):
        raise OSError("dirPath argument must point to a directory. "
                      "'%s' does not." % dirPath)
    parentDir, dirToZip = os.path.split(dirPath)

    # Little nested function to prepare the proper archive path
    def trimPath(path):
        archivePath = path.replace(parentDir, "", 1)
        if parentDir:
            archivePath = archivePath.replace(os.path.sep, "", 1)
        if not includeDirInZip:
            archivePath = archivePath.replace(dirToZip + os.path.sep, "", 1)
        return os.path.normcase(archivePath)

    outFile = zipfile.ZipFile(zipFilePath, "w",
                              compression=zipfile.ZIP_DEFLATED)
    for (archiveDirPath, dirNames, fileNames) in os.walk(dirPath):
        for fileName in fileNames:
            filePath = os.path.join(archiveDirPath, fileName)
            outFile.write(filePath, trimPath(filePath))
        # Make sure we get empty directories as well
        if not fileNames and not dirNames:
            zipInfo = zipfile.ZipInfo(trimPath(archiveDirPath) + "/")
            # some web sites suggest doing
            # zipInfo.external_attr = 16
            # or
            # zipInfo.external_attr = 48
            # Here to allow for inserting an empty directory.  Still TBD/TODO.
            outFile.writestr(zipInfo, "")
    outFile.close()


def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                shutil.copy2(s, d)


class FileManager:
    def __init__(self, userID, show_dotfiles=True):

        self.root = (settings.FILE_PATH + "files_" + str(userID) + "/").encode('utf8', 'surrogateescape').decode('utf8',
                                                                                                                 'surrogateescape')
        self.userID = userID
        self.pathSpliter = '_*c}#~_'.encode('utf8', 'surrogateescape').decode('utf8', 'surrogateescape')
        self.tmp = (tempfile.gettempdir()).encode('utf8', 'surrogateescape').decode('utf8', 'surrogateescape')

        if not os.path.exists(self.root):
            os.makedirs(self.root)

        self.root = os.path.abspath(self.root).encode('utf8', 'surrogateescape').decode('utf8', 'surrogateescape')
        self.show_dotfiles = show_dotfiles

    def shareItem(self, request):
        splittter = self.pathSpliter if request.data['selectedFolder']['model']['type'] != "dir" else ""
        sharedFolder = splittter + self.pathSpliter.join(
            request.data['selectedFolder']['model']['path']) + self.pathSpliter + \
                       request.data['selectedFolder']['model']['name']

        sharedFolder = sharedFolder.replace(self.pathSpliter + self.pathSpliter, self.pathSpliter)
        fileInstances = list(
            FileManagerItem.objects.filter(
                address=sharedFolder.encode('utf8', 'surrogateescape').decode('utf8', 'surrogateescape'),
                userID=self.userID).order_by('-id').limit(10))
        if len(fileInstances) == 0:
            raise Exception("No File or folder found in mongodb")
        getUsersAndDeletePermission = [
            {
                "userID": x["userID"],
                "canDelete": x["CanDelete"] if "CanDelete" in x else False
            } for x in request.data['shareUsersID']
        ]
        fileInstances = fileInstances[0]
        fileInstances.update(set__share__users=getUsersAndDeletePermission)
        return {}

    def decodeToFarsi(self, _bytes):
        return unicodedata.normalize('NFC', _bytes)

    def RequestedShareFolder(self, request):
        splittter = self.pathSpliter if request.data['requestedShareFolder']['model']['type'] != "dir" else ""
        sharedFolder = splittter + self.pathSpliter.join(
            request.data['requestedShareFolder']['model']['path']) + self.pathSpliter + \
                       request.data['requestedShareFolder']['model']['name']
        sharedFolder = sharedFolder.replace(self.pathSpliter + self.pathSpliter, self.pathSpliter)
        fileInstances = list(
            FileManagerItem.objects.filter(
                address=sharedFolder.encode('utf8', 'surrogateescape').decode('utf8', 'surrogateescape'),
                userID=self.userID).order_by('-id').limit(10))
        res = []
        if len(fileInstances) == 0:
            raise Exception("No File or folder found in mongodb")
        if "users" in fileInstances[0].share:
            res = fileInstances[0].share["users"]
        getUsersAndDeletePermission = [
            {
                "userID": x["userID"],
                "CanDelete": x["canDelete"] if "canDelete" in x else False
            } for x in res
        ]
        profiles = list(
            Profile.objects.filter(userID__in=[x["userID"] for x in getUsersAndDeletePermission]).limit(100))
        profiles = [
            {"name": x.extra["Name"] if "Name" in x.extra else "",
             "userID": x.userID,
             "avatar": x.extra["profileAvatar"]["url"] if "profileAvatar" in x.extra else ""
             } for x in profiles
        ]

        for g in getUsersAndDeletePermission:
            res = query(profiles).where(lambda x: x["userID"] == g["userID"]).to_list()
            g["avatar"] = dict(query(profiles).where(lambda x: x["userID"] == g["userID"]).to_list()[0])["avatar"]
            g["name"] = dict(query(profiles).where(lambda x: x["userID"] == g["userID"]).to_list()[0])["name"]

        return getUsersAndDeletePermission

    def list(self, request):
        reqPath = request['path']
        path = os.path.abspath(self.root + request['path'])
        if not os.path.exists(path) or not path.startswith(self.root):
            return {'result': ''}

        files = []
        # files = [self.decodeToFarsi(f) for f in os.listdir(path.decode())]
        files = os.listdir(path)

        newfiles = []
        for fname in sorted(files):
            if fname.startswith('.') and not self.show_dotfiles:
                continue

            fpath = os.path.join(path, fname)

            try:
                ftype, fsize, ftime, fmode = get_file_information(fpath)
            except Exception as e:
                continue

            newfiles.append({
                'name': fname,
                'rights': fmode,
                'size': fsize,
                'date': ftime,
                'type': ftype,
            })

        for f in newfiles:
            currentPath = (request['path'] + "/" + f["name"]).replace("//", "/").replace("\\", "/").replace(
                '/', self.pathSpliter)
            fmisItems = list(
                FileManagerItem.objects.filter(userID=self.userID,
                                               address=currentPath.encode('utf8', 'surrogateescape').decode('utf8',
                                                                                                            'surrogateescape')).limit(
                    1000).order_by('-id'))

            itemType = 1 if f["type"] == "dir" else 2
            userAllowToRemove = True
            userAllowToRename = True
            share = {}

            if len(fmisItems) == 0:
                newFileItem = {
                    'address': currentPath.encode('utf8', 'surrogateescape').decode('utf8', 'surrogateescape'),
                    'itemType': itemType,
                    'userID': self.userID,
                    'userAllowToRemove': userAllowToRemove,
                    'userAllowToRename': userAllowToRename,
                    'share': share
                }
                fserial = FileManagerItemSerializer(data=newFileItem)
                fserial.is_valid(raise_exception=True)
                fserial.save()
            else:
                currentItem = fmisItems[0]
                itemType = currentItem.itemType
                userAllowToRemove = currentItem.userAllowToRemove
                userAllowToRename = currentItem.userAllowToRename
                share = currentItem.share

            f["share"] = share
            f["type"] = "dir" if itemType == 1 else "file"
            f["userAllowToRemove"] = userAllowToRemove
            f["userAllowToRename"] = userAllowToRename

        return {'result': newfiles}

    def rename(self, request):
        try:
            src = os.path.abspath(self.root + request['path'])
            dst = os.path.abspath(self.root + request['newPath'])
            print('rename {} {}'.format(src, dst))
            if not (os.path.exists(src) and src.startswith(self.root) and dst.startswith(self.root)):
                return {'result': {'success': 'false', 'error': 'Invalid path'}}

            shutil.move(src, dst)
        except Exception as e:
            return {'result': {'success': 'false', 'error': e.message}}

        return {'result': {'success': 'true', 'error': ''}}

    def copy(self, request):
        try:
            items = [request['path']]
            if len(items) == 1 and 'singleFilename' in request:
                src = os.path.abspath(self.root + items[0])
                dst = os.path.abspath(self.root + request['singleFilename'])
                if not (os.path.exists(src) and src.startswith(self.root) and dst.startswith(self.root)):
                    return {'result': {'success': 'false', 'error': 'File not found'}}

                shutil.move(src, dst)
            else:
                path = os.path.abspath(self.root + request['newPath'])
                for item in items:
                    src = os.path.abspath(self.root + item)
                    if not (os.path.exists(src) and src.startswith(self.root) and path.startswith(self.root)):
                        return {'result': {'success': 'false', 'error': 'Invalid path'}}

                    shutil.copy(src, path)
        except Exception as e:
            return {'result': {'success': 'false', 'error': e.message}}

        return {'result': {'success': 'true', 'error': ''}}

    def rawcopy(self, request):
        items = [request['path']]
        if len(items) == 1 and 'singleFilename' in request:
            src = os.path.abspath(items[0])
            dst = os.path.abspath(request['singleFilename'])
            if not (os.path.exists(src) and dst.startswith(self.root)):
                return {'result': {'success': 'false', 'error': 'File not found'}}

            shutil.move(src, dst)
        else:
            path = os.path.abspath(self.root + request['newPath'])
            for item in items:
                src = os.path.abspath(self.root + item)
                if not (os.path.exists(src)):
                    return {'result': {'success': 'false', 'error': 'Invalid path'}}

                shutil.copy(src, path)

        return {'result': {'success': 'true', 'error': ''}}

    def remove(self, request):
        try:
            items = [request['path']]
            for item in items:
                path = os.path.abspath(self.root + item)
                if not (os.path.exists(path) and path.startswith(self.root)):
                    return {'result': {'success': 'false', 'error': 'Invalid path'}}

                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
        except Exception as e:
            return {'result': {'success': 'false', 'error': e.message}}

        return {'result': {'success': 'true', 'error': ''}}

    def edit(self, request):
        try:
            path = os.path.abspath(self.root + request['item'])
            if not path.startswith(self.root):
                return {'result': {'success': 'false', 'error': 'Invalid path'}}

            content = request['content']
            with open(path, 'w') as f:
                f.write(content)
        except Exception as e:
            return {'result': {'success': 'false', 'error': e.message}}

        return {'result': {'success': 'true', 'error': ''}}

    def getContent(self, request):
        try:
            path = os.path.abspath(self.root + request)
            if not path.startswith(self.root):
                return {'result': {'success': 'false', 'error': 'Invalid path'}}

            with open(path, 'r') as f:
                content = f.read()
        except Exception as e:
            content = e.message

        return {'result': content}

    def createFolder(self, request):
        # try:
        path = os.path.abspath(self.root + "/" + request['path'] + "/" + request['name'])
        if not path.startswith(self.root):
            return {'result': {'success': 'false', 'error': 'Invalid path'}}

        os.makedirs(path)
        # except Exception as e:
        #     return {'result': {'success': 'false', 'error': e.message}}

        return {'result': {'success': 'true', 'error': ''}}

    def changePermissions(self, request):

        try:
            items = request['items']
            permissions = int(request['perms'], 8)
            recursive = request['recursive']
            print('recursive: {}, type: {}'.format(recursive, type(recursive)))
            for item in items:
                path = os.path.abspath(self.root + item)
                if not (os.path.exists(path) and path.startswith(self.root)):
                    return {'result': {'success': 'false', 'error': 'Invalid path'}}

                if recursive == 'true':
                    change_permissions_recursive(path, permissions)
                else:
                    os.chmod(path, permissions)
        except Exception as e:
            return {'result': {'success': 'false', 'error': e.message}}

        return {'result': {'success': 'true', 'error': ''}}

    def compress(self, request):
        try:
            items = [request['path']]
            path = os.path.abspath(self.root + request['destination'])
            MainPath = os.path.abspath(self.root + request['path'])
            if not path.startswith(self.root):
                return {'result': {'success': 'false', 'error': 'Invalid path'}}

            zipdir(MainPath, path)

            # zip_file = zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED)
            # for item in items:
            #     path = os.path.abspath(self.root + item)
            #     if not (os.path.exists(path) and path.startswith(self.root)):
            #         continue
            #
            #     if os.path.isfile(path):
            #         zip_file.write(path)
            #     else:
            #         for root, dirs, files in os.walk(path):
            #             for f in files:
            #                 zip_file.write(
            #                     os.path.join(root, f),
            #                     os.path.relpath(os.path.join(root, f), os.path.join(path, '..'))
            #                 )
            #
            # zip_file.close()
        except Exception as e:
            return {'result': {'success': 'false', 'error': e.message}}

        return {'result': {'success': 'true', 'error': ''}}

    def extract(self, request):
        try:
            src = os.path.abspath(self.root + request['sourceFile'])
            dst = os.path.abspath(self.root + request['destination'])
            if not (os.path.isfile(src) and src.startswith(self.root) and dst.startswith(self.root)):
                return {'result': {'success': 'false', 'error': 'Invalid path'}}

            zip_file = zipfile.ZipFile(src, 'r')
            zip_file.extractall(dst)
            zip_file.close()
        except Exception as e:
            return {'result': {'success': 'false', 'error': e.message}}

        return {'result': {'success': 'true', 'error': ''}}

    def upload(self, request):
        try:
            destination = os.path.abspath(self.root + request.data["destination"])
            for name in request._files:
                fileinfo = request._files[name]
                filename = fileinfo.name
                path = os.path.abspath(os.path.join(self.root, destination, filename))
                if not path.startswith(self.root):
                    return {'result': {'success': 'false', 'error': 'Invalid path'}}
                with open(path, 'wb') as f:
                    f.write(fileinfo.file.read())
        except Exception as e:
            return {'result': {'success': 'false', 'error': e.message}}

        return {'result': {'success': 'true', 'error': ''}}

    def download(self, path):
        path = os.path.abspath(self.root + path)
        content = ''
        if path.startswith(self.root) and os.path.isfile(path):
            print(path)
            try:
                with open(path, 'rb') as f:
                    content = f.read()
            except Exception as e:
                pass
        return content

    def MakeFilesCompress(self, atts):
        # zipFile = zipfile.ZipFile("zip.zip", "w" )
        # converting atts to file address

        fileAddress = []
        for at in atts:
            if at['path'] != None:
                path = at["path"]
                # path = [self.root] + path + [at["name"]]
                # path = os.path.join(self.root, *path)
                fileAddress.append({"path": path, "type": at["type"], "name": at["name"]})
        # making target dir to start compress
        # first step is make a directory in temp folder
        if not os.path.isdir(os.path.abspath(self.tmp)):
            os.mkdir(os.path.abspath(self.tmp))
        uid = uuid.uuid1().hex
        dirToCopy = os.path.abspath(os.path.join(self.tmp, uid))
        os.mkdir(dirToCopy)
        for f in fileAddress:
            if f["type"] == "dir":
                copytree(f["path"], os.path.join(dirToCopy, f["name"]))
            if f["type"] == "file":
                shutil.copyfile(f["path"], os.path.join(dirToCopy, f["name"]))

        # copying entire folder and files into new directory
        # now we have to compress them
        zipdir(dirToCopy, dirToCopy + ".zip")
        shutil.rmtree(dirToCopy)

        return dirToCopy + ".zip"
