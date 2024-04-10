from datetime import datetime

from django.utils import timezone
from mongoengine import *


#
# class ProfileDetailsField(EmbeddedDocument):
#     AboutMe=StringField(max_length=200)
#     Name
#     Phones
#     Title
#     profileAvatar
#     profileHeaderBackground
#     friends


class SalesCustomerProfile(Document):
    positionID = IntField(required=True, )
    companyID = IntField(required=True, )
    dateOfPost = DateTimeField(default=datetime.now())
    name = StringField(unique=True)
    hamkaranCode = StringField(required=False)
    desc = StringField()
    exp = DictField()


class SalesCustomerProfileSalesRequestsSizes(Document):
    positionID = IntField(required=True, )
    companyID = IntField(required=True, )
    dateOfPost = DateTimeField(default=datetime.now())
    profileLink = ReferenceField(SalesCustomerProfile)
    desc = DictField()


class SaleConversations(Document):
    positionID = IntField()
    companyID = IntField()
    dateOfPost = DateTimeField(default=datetime.now())
    """
    Open :
    does this conversation open or it is finished
    """
    Open = BooleanField(default=True)
    PrefactorID = StringField()
    # CustomerName = StringField()
    """
    CustomerIsInAccounting:
    Has this customer ID in accounting system
    """
    CustomerIsInAccounting = BooleanField(default=True)
    CustomerID = IntField(null=True)
    CustomerName = StringField()
    HamkaranCode = StringField()
    customerLink = ReferenceField(SalesCustomerProfile, required=True)
    Files = DictField(null=True)


class SaleConversationComments(Document):
    positionID = IntField()
    companyID = IntField()
    saleConversationLink = ReferenceField(SaleConversations, required=True)
    dateOfPost = DateTimeField(default=datetime.now())
    comment = StringField()
    confirmedBy = DictField()


class SaleConversationCommentsReplays(Document):
    SaleConversationCommentsLink = ReferenceField(SaleConversationComments, required=True)
    positionID = IntField()
    comment = StringField()
    dateOfPost = DateTimeField(default=datetime.now())
    companyID = IntField()


class SaleCurrentBasket(Document):
    positionID = IntField(required=True, )
    companyID = IntField(required=True, )
    dateOfPost = DateTimeField(default=datetime.now())
    transfered = BooleanField(default=False)  # is currently in basket ?
    desc = DictField()


class SaleConversationItems(Document):
    positionID = IntField(required=True, )
    companyID = IntField(required=True, )
    saleConversationLink = ReferenceField(SaleConversations, required=True)
    dateOfPost = DateTimeField(default=datetime.now())
    paymentType = StringField()
    itemID = StringField(required=False, )  # ID in hamkaran system
    itemName = StringField(required=False, )
    amount = IntField(required=True, )
    fee = IntField(required=True, )
    off = FloatField(required=True, )
    index = IntField()
    ignore = BooleanField(default=False)
    comment = StringField()
    desc = DictField()


class TaminDetails(Document):
    positionID = IntField(required=True, )
    companyID = IntField(required=True, )
    dateOfPost = DateTimeField(default=datetime.now())

    noe = IntField()
    keshvar = IntField()
    temper = IntField()
    sath = IntField()
    zekhamat = IntField()

    arz = IntField()
    arzAfterTrim = IntField()
    keifiat = IntField()
    tool = IntField()
    qty = IntField()  # killograms / tedad

    mahaleAnbar = StringField()
    dasteBandiKharid = IntField()
    somarehSefaresh = StringField()
    tarikheVoroodBeGomrok = DateTimeField()
    tarikheBoresh = DateTimeField()
    masraf = StringField()
    toozihateKeifi = StringField()
    toozihateBarnameRizi = StringField()
    tozihat = StringField()


class TaminProject(Document):
    positionID = IntField(required=True, )
    companyID = IntField(required=True, )
    dateOfPost = DateTimeField(default=datetime.now())
    projectName = StringField()
    factoryName = StringField()
    totalAmount = IntField()
    projectStartDate = DateTimeField()
    typeOfTamin = IntField()  # 1= dakheli  2=khareji
    desc = StringField()


class TaminProjectIncomingItems(Document):
    positionID = IntField(required=True, )
    companyID = IntField(required=True, )
    dateOfPost = DateTimeField(default=datetime.now())
    projectName = StringField()
    """
    whereToRecieveType
    by this field we track all way of items
    1 = if items comes to factory
    2 = if items does not come to factory eg BandarAbas Port
    """
    whereToRecieveType = IntField()  # 1=karkhaneh  2=Not Karkhaneh
    """
    whereToRecieveStr:
    name of receiver place like karkhaneh or gomrok
    """
    whereToRecieveStr = StringField()
    recievedDate = DateTimeField()
    amount = IntField()
    desc = StringField()
    """
    positionOfItem :
    1 = active
    2 = suspended
    """
    positionOfItem = IntField(default=1)


class PishfactorsIgnore(Document):
    positionID = IntField()
    companyID = IntField()
    dateOfPost = DateTimeField(default=datetime.now())
    CstmrCode = IntField()
    VchItmId = IntField()
    VchHdrRef = IntField()
    PartRef = IntField()
    VchNo = IntField()
    details = DictField()


class HamkaranKhorooj(Document):
    ID = IntField(required=True, unique=True)
    exp = DictField()


class HamkaranKhoroojItems(Document):
    khoroojLink = ObjectIdField(required=False, null=True, )
    item = DictField()


class HamkaranKhoroojSigns(Document):
    dateOfPost = DateTimeField(default=datetime.now())
    positionID = IntField()
    khoroojLink = ReferenceField(HamkaranKhorooj)
    whichStep = IntField()
    comment = StringField(null=True, required=False)


class HamkaranKhoroojSignsSnapshot(Document):
    khoroojSignLink = ReferenceField(HamkaranKhoroojSigns)
    snapshot = DictField()


class HamkaranKhoroojSMS(Document):
    positionID = IntField()
    dateOfPost = DateTimeField(default=datetime.now())
    khoroojLink = ReferenceField(HamkaranKhorooj, )
    cellNoToSMS = StringField()
    genID = StringField()
    linkID = StringField()
    msg = StringField()
    result = BooleanField()
    seenDate = DateTimeField(default=None)


class HamkaranKhoroojFiles(Document):
    dateOfPost = DateTimeField(default=datetime.now())
    khoroojLink = ReferenceField(HamkaranKhorooj, )
    Files = DictField()


class Exits(Document):
    dateOfPost = DateTimeField(default=datetime.now())
    item = DictField()


class ExitsSigns(Document):
    dateOfPost = DateTimeField(default=datetime.now())
    positionID = IntField()
    exitsLink = ReferenceField(Exits)
    whichStep = IntField()
    comment = StringField(null=True, required=False)


class ExtisFiles(Document):
    dateOfPost = DateTimeField(default=datetime.now())
    VchHdrId = IntField()
    Files = DictField()


class ExitsSMS(Document):
    positionID = IntField()
    dateOfPost = DateTimeField(default=datetime.now())
    VchHdrId = IntField()
    cellNoToSMS = StringField()
    genID = StringField()
    linkID = StringField()
    msg = StringField()
    result = BooleanField()
    seenDate = DateTimeField(default=None)


class lastExitID(Document):
    lastVchHdrId = IntField(default=0)


class HavalehForooshs(Document):
    dateOfPost = DateTimeField(default=datetime.now())
    VchHdrRef = StringField(unique=True)
    havalehNo = StringField()
    customerName = StringField()
    tarikheSodoor = StringField()
    mizanAvaliehSefaresh = IntField()
    # lastSignDate = DateTimeField(default=datetime.now(), null=True, required=True)


class HavalehForooshApprove(Document):
    havalehForooshLink = ObjectIdField(required=True)
    parent = ObjectIdField(null=True, required=False)
    item = DictField()
    reason = StringField()
    positionID = IntField(default=None, required=False, null=True)  # position ID of havaleh foroosh Creator
    dateOfPost = DateTimeField(default=datetime.now())


class HavalehForooshSigns(Document):
    dateOfPost = DateTimeField(default=datetime.now())
    positionID = IntField()
    HavalehForooshApproveLink = ObjectIdField(required=True)
    whichStep = IntField()
    comment = StringField(null=True, required=False)


class HavalehForooshSignsSnapshot(Document):
    havalehForooshSignsLink = ReferenceField(HavalehForooshSigns)
    snapshot = DictField()



class HamkaranHavaleForoosh(Document):
    ID = IntField(required=True, unique=True)
    Number = IntField(required=True, )
    vaziat = IntField(required=True, )
    mizanAvaliehSefaresh = IntField(required=False, null=True, )
    customerName = StringField(required=True, )
    tarikheSodoor = DateTimeField()
    tarikheEngheza = DateTimeField()
    exp = DictField()


class HamkaranHavaleForooshOrderApprove(Document):
    havalehForooshLink = ReferenceField(HamkaranHavaleForoosh)
    parent = ObjectIdField(null=True, required=False)
    dateOfPost = DateTimeField(default=datetime.now())
    item = DictField()


class HamkaranSalesCustomerProfile(Document):
    positionID = IntField(required=True, )
    companyID = IntField(required=True, )
    name = StringField(unique=True)
    CustomerID = IntField(required=False, unique=True)
    exp = DictField()


class HamkaranCustomerNotes(Document):
    EntityRef = IntField(required=False)
    Notes = StringField()


class HamkaranCustomerAddress(Document):
    CustomerAddressID = IntField(required=False)
    exp = DictField()


class HavalehForooshFiles(Document):
    dateOfPost = DateTimeField(default=datetime.now())
    havalehForooshLink = ReferenceField(HamkaranHavaleForooshOrderApprove)
    Files = DictField()


class HavalehForooshConv(Document):
    HavalehForooshApproveLink = ReferenceField(HamkaranHavaleForooshOrderApprove)
    positionID = IntField()
    comment = StringField()
    dateOfPost = DateTimeField(default=datetime.now())
    companyID = IntField()
    exp = DictField()


class lastHavalehForooshID(Document):
    lastVchHdrRef = IntField(default=0)


class OldlastHavalehForooshID(Document):
    lastVchHdrRef = IntField(default=0)


class HamkaranIssuePermit(Document):
    ID = IntField(required=True, unique=True)
    exp = DictField()


class HamkaranIssuePermitItem(Document):
    ID = IntField(required=True, unique=True)
    exp = DictField()


class MojoodiGhabeleForoosh(Document):
    PartCode = StringField(required=True, )
    Year = IntField(required=True, )
    details = DictField()


class MojoodiGhabeleForooshKeifi(Document):
    HavalehForooshApproveLink = ReferenceField(MojoodiGhabeleForoosh)
    mizan = IntField(required=True, )
    kasrAsMojoodi = BooleanField(required=False)
    dalil = StringField(required=True, )
    details = DictField()
    positionID = IntField()
    dateOfPost = DateTimeField(default=datetime.now())
