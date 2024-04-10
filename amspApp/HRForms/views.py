# coding=utf-8
import json
import os
from asq.initiators import query
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext




#
#
# def Form(request):
#     form = HRFormsFormMix(scope_prefix="One")
#     # grid = GetGrid(request.user.userprofile.person.ow_id, user=request.user)
#     # newBtn = """
#     # <a class="btn btn-default" data-target="#addNewForm"
#     # data-toggle="modal" style="margin-left: 150px;" >جدید</a>
#     # """
#     templatename = "HRForms/base.html"
#
#     return render_to_response(
#         templatename,
#         {"form": form,
#          "newBtn": newBtn},
#         context_instance=RequestContext(request)
#     )
#
#
# def GetTable(request):
#     grid = GetGrid(request.user.userprofile.person.ow_id, user=request.user)
#     return HttpResponse(json.dumps(grid), mimetype="application/json")
#
#
# def GetGrid(OwnerID, orderby="name", user=None):
#     # the following grid contains these rows :
#     # Onvan - Farayande Mortabet - Shomareh - Vahed - NoeSanad - Akharin Rev. Date - Action btns
#     items = HRForms.objects.all().filter(ow=OwnerID).order_by(orderby)
#
#     # checking if the user has super admin access or not
#     if user != None:
#         userAccess = not_in_SuperAdmin_group(user)
#
#     items = query(items).select(lambda
#                                     x: {
#         "id": x.id,
#         "name": x.name,
#         "farayandhayeMortabet": x.farayandhayeMortabet.name,
#         "shomarehSanad": x.shomarehSanad,
#         "Vahed": x.Vahed.name,
#         "typeOfSanad": x.typeOfSanad.name,
#         "format": x.formatDoc.name,
#         "hasAccess": userAccess,
#         "visible": x.visible if x.visible == True else False,
#         "latestFile": x.link_to_form.get(isItDefault=True).formAddress if x.link_to_form.filter(
#             isItDefault=True).count() > 0 else "",
#         "latestFileDateUploaded": mil_to_sh(x.link_to_form.get(isItDefault=True).dateOfPost) if x.link_to_form.filter(
#             isItDefault=True).count() > 0 else "",
#     }).to_list()
#     return items
#     # return HttpResponse(json.dumps(items), mimetype="application/json")
#
#
#
#
# def Post(request):
#     body = json.loads(request.body)
#
#     # adding to form
#     # owID = request.user.userprofile.person.ow_id
#     # body["fileAddress"] = body["File"]
#     hasItDefault = False
#     for i in body["UploadedFiles"]:
#         hasItDefault = i["default"]
#         if hasItDefault == True:
#             break
#
#     if hasItDefault == False:
#         return HttpResponse(
#             CreateAlarmMessage("اشتباه", "لطفا یکی از این فایلهایی که آپلود کردید رو بعنوان پیش فرض انتخاب کنید"),
#             mimetype="application/json")
#
#     if body.has_key("id"):
#         newForm = HRForms.objects.get(id=body["id"])
#         newForm.typeOfSanad_id = int(body["HRSanadType"])
#         newForm.shomarehSanad = body["code"]
#         newForm.name = body["name"]
#         newForm.Vahed_id = int(body["Vahed"])
#         newForm.formatDoc_id = int(body["Format"])
#         newForm.farayandhayeMortabet_id = int(body["FarayandhayeMortabet"])
#         newForm.noeSanad_id = int(body["NoeSanad"])
#     else:
#         newForm = HRForms(
#             typeOfSanad=HRSanadType.objects.get(id=int(body["HRSanadType"])),
#             shomarehSanad=body["code"],
#             name=body["name"],
#             Vahed=Vahed.objects.get(id=int(body["Vahed"])),
#             formatDoc=Format.objects.get(id=int(body["Format"])),
#             farayandhayeMortabet=FarayandhayeMortabet.objects.get(id=int(body["FarayandhayeMortabet"])),
#             noeSanad=NoeSanad.objects.get(id=int(body["NoeSanad"])),
#             ow=request.user.userprofile.person.ow.ow,
#         )
#
#     newForm.save()
#     if body.has_key("id"):
#         newForm.link_to_form.all().delete()
#
#     for item in body["UploadedFiles"]:
#         items = HRFormItems(
#             formAddress=item["savedfileName"],
#             form=newForm,
#             isItDefault=item["default"]
#         )
#         items.save()
#
#     return HttpResponse(
#         CreateSuccMessage("موفقیت", "با موفقیت ثبت شد"),
#         mimetype="application/json")
#
#
#
#
# def Remove(request):
#     body = json.loads(request.body)
#     HRForms.objects.all().filter(id=body["id"]).delete()
#     return HttpResponse(
#         CreateSuccMessage("موفقیت", "با موفقیت حذف شد - برو حالش رو ببر"),
#         mimetype="application/json")
#
#
# def GetOne(request):
#     body = json.loads(request.body)
#     hrform = HRForms.objects.get(id=body["id"])
#     res = {
#         "FarayandhayeMortabet": hrform.farayandhayeMortabet_id,
#         "Format": hrform.formatDoc_id,
#         "HRSanadType": hrform.typeOfSanad_id,
#         "NoeSanad": hrform.noeSanad_id,
#         "Vahed": hrform.Vahed_id,
#         "code": hrform.shomarehSanad,
#         "name": hrform.name,
#         "id": hrform.id
#     }
#
#     uploadedForms = hrform.link_to_form.all()
#     items = []
#     for item in uploadedForms:
#         file_inf = get_file_info_hr(item.formAddress + ".dat")
#         items.append(
#             {
#                 "dateOfUpload": file_inf["dateOfUpload"],
#                 "savedfileName": item.formAddress + ".dat",
#                 "default": item.isItDefault,
#                 "fileName": file_inf["fileName"],
#                 "fileSize": file_inf["fileSize"],
#             }
#         )
#
#     res["UploadedFiles"] = items
#
#     return HttpResponse(
#         json.dumps(res),
#         mimetype="application/json")
#
#
# def get_file_info_hr(fileNameWithDatExe):
#     fileInfo = fileNameWithDatExe.split(".")[0]
#     file = Files.objects.all().filter(saved_file_name=fileInfo)[0]
#     # fileHr = HRFormItems.objects.all().filter(formAddress=json.loads(request.body)["fileID"])[0]
#     fileToLoad = publicPath + file.saved_file_name + ".dat"
#     fileSize = str(os.path.getsize(fileToLoad) / 1024) + "kb"
#     result = {
#         "savedfileName": file.saved_file_name,
#         "fileName": file.orginal_file_name,
#         "fileSize": fileSize,
#         "dateOfUpload": mil_to_sh(file.date_of_create),
#         "default": False
#     }
#
#     return result
#
#
# def FindBy(request):
#     return None
#
#
#     # def RemoveFile(request):
#     # body = json.loads(request.body)
#     # return None
#
#
# # @login_required(login_url='/dms/login/')
# # @user_passes_test(not_in_SuperAdmin_group, login_url="/dms/access-denied/")
# def Toggle(request):
#     body = json.loads(request.body)
#     updatedItem = HRForms.objects.get(id=body["id"])
#     updatedItem.visible = True if updatedItem.visible == False else False
#     updatedItem.save()
#     res = {
#         "visible": updatedItem.visible
#     }
#     return HttpResponse(
#         json.dumps(res),
#         mimetype="application/json")
