from amspApp.Administrator.Customers.views.CustomerRegistrationView import CustomerRegistrationViewSet
from amspApp.MyProfile.models import Profile
from amspApp.amspUser.serializers.UserSerializer import UserSerializer

__author__ = 'mohammad'


# ["source","dest"]
step1Mapping = [
    ["InternationalCode", "InternationalCode"],
    ["Name", "Name"],
    ["Family", "Family"],
    ["FatherName", "FatherName"],
    ["BirthDate", "BirthDate"],
    ["BirthPlace", "BirthPlace"],
    ["ShenasnamehPlace", "ShenasnamehPlace"],
    ["ShenasnamehCode", "ShenasnamehCode"],
    ["Jensiat", "Jensiat",
     [
         ['1', 'مرد'],
         ['2', 'زن'],
     ]
    ],
    ["Mazhab", "Mazhab",
     [
         ['1', 'شیعه'],
         ['2', 'سنی'],
         ['3', 'مسیحی'],
         ['4', 'سایر']
     ]
    ],
    ["Married", "Married",
     [
         ['1', 'مجرد'],
         ['2', 'متاهل']
     ]
    ],
    ["MarriedYear", "MarriedYear"],
    ["WifeJob", "WifeJob"],
    ["ChildAmount", "ChildAmount"],
    ["Soldier", "Soldier",
     [
         ['1', 'دارای کارت پایان خدمت'],
         ['2', 'مشمول'],
         ['3', 'غایب'],
         ['4', 'خرید خدمت'],
         ['5', 'معافیت پزشکی'],
         ['6', 'معافیت کفالت'],
         ['7', 'سایر معافیت'],
         ['8', 'محصل'], ]
    ],
    ["PostalCode", "PostalCode"],
    ["TelHome", "TelHome"],
    ["Mobile", "Mobile"],
    ["TelWork", "TelWork"],
    ["TelNec", "TelNec"],
    ["Web", "Web"],
    ["Country", "Country"],
    ["OstanHome", "OstanHome"],
    ["CityHome", "CityHome"],
    ["HomeAddress", "HomeAddress"],
    ["WorkAddress", "WorkAddress"],
    ["NecAddress", "NecAddress"],
]

from pymongo import MongoClient


def checkDict(dict, keyname):
    if keyname in dict:
        return dict[keyname]
    else:
        return None


def startMapping():
    client = MongoClient()
    db = client['ams']
    col = db["Estekhdam"].find()
    n = []
    for c in col:
        d = {}
        # creating user
        d["user"] = {}
        d["user"]["Email"] = "cc"+c["Email"]
        d["user"]["username"] = "uuu" + c["InternationalCode"]
        d["user"]["password"] = c["InternationalCode"]
        # step 1
        d["Shenasnameh"] = {}
        for m in step1Mapping:
            d["Shenasnameh"][m[1]] = c[m[0]] if m[0] in c else None
        for m in step1Mapping:
            if len(m) == 3:
                res = ""
                for mm in m[2]:
                    if mm[0] == d["Shenasnameh"][m[1]]:
                        d["Shenasnameh"][m[1]] = mm[1]

        # step 2
        d["Education"] = {}
        d["Education"]["EducationType"] = ""
        d["Education"]["items"] = []
        # detecting education level
        # detecting diploma

        heIsDip = False
        if len(c["Educations"]) == 1:
            if c["Educations"][0]["LevelofEducation"] == "دیپلم":
                heIsDip = True
                d["Education"]["EducationType"] = "دیپلم"
                d["Education"]["LevelofEducation"] = "دیپلم"
                d["Education"]["SelectedBranch"] = c["Educations"][0]["Branch"]
                d["Education"]["EndYear"] = c["Educations"][0]["EndYear"]
                d["Education"]["AverageOfLicense"] = c["Educations"][0]["AverageOfLicense"]
                d["Education"]["EducationalPlaceName"] = ""
        if heIsDip == False:
            d["Education"]["LevelofEducation"] = "دارای تحصیلات دانشگاهی"
            levels = []
            for edu in c["Educations"]:
                cccc = {}
                cccc["Education"] = checkDict(edu, "LevelofEducation")
                cccc["SelectedBranch"] = checkDict(edu, "Branch")
                cccc["Gerayesh"] = checkDict(edu, "Gerayesh")
                cccc["UniversityType"] = checkDict(edu, "UniversityType")
                cccc["EducationalPlaceName"] = checkDict(edu, "EducationalPlaceName")
                cccc["StartYear"] = checkDict(edu, "StartYear")
                cccc["EndYear"] = checkDict(edu, "EndYear")
                cccc["AverageOfLicense"] = checkDict(edu, "AverageOfLicense")
                cccc["Country"] = checkDict(edu, "Country")
                cccc["HasLicense"] = checkDict(edu, "HasLicense")
                levels.append(cccc)
            d["Education"]["items"] = levels

        # step 3 lang
        levels = []
        d["Languages"] = {}
        d["Languages"]["items"] = []
        for lng in c["Languages"]:
            lll = {}
            lll["Name"] = checkDict(lng, "Name")
            lll["Skill"] = checkDict(lng, "Skill")
            lll["LatestCertificateName"] = checkDict(lng, "LatestCertificateName")
            lll["Explaination"] = checkDict(lng, "Explaination")
            levels.append(lll)
        d["Languages"]["items"] = levels

        # step 4 Doreh
        levels = []
        d["Dore"] = {}
        d["Dore"]["items"] = []
        for lng in c["Dorehs"]:
            lll = {}
            lll["WorkshopName"] = checkDict(lng, "WorkshopName")
            lll["YearOfWorkshop"] = checkDict(lng, "YearOfWorkshop")
            lll["Institute"] = checkDict(lng, "Institute")
            lll["TimeAmount"] = checkDict(lng, "TimeAmount")
            lll["HaveCertificate"] = checkDict(lng, "HaveCertificate")
            lll["KindOfKnowing"] = checkDict(lng, "KindOfKnowing")
            levels.append(lll)
        d["Dore"]["items"] = levels

        # step 5 Experience
        levels = []
        d["Experience"] = {}
        d["Experience"]["items"] = []
        for lng in c["Experiences"]:
            lll = {}
            lll["Name"] = checkDict(lng, "Name")
            lll["Level"] = checkDict(lng, "Level")
            lll["AgeOfPracticalSkills"] = checkDict(lng, "AgeOfPracticalSkills")
            lll["Explanations"] = checkDict(lng, "Explanations")
            levels.append(lll)
        d["Experience"]["items"] = levels
        # step 6 Software
        levels = []
        d["Software"] = {}
        d["Software"]["items"] = []
        for lng in c["Softwares"]:
            lll = {}
            lll["Name"] = checkDict(lng, "Name")
            lll["Level"] = checkDict(lng, "Level")
            lll["Explanations"] = checkDict(lng, "Explanations")
            levels.append(lll)
        d["Software"]["items"] = levels
        # step 7 Job
        levels = []
        d["Job"] = {}
        d["Job"]["items"] = []
        for lng in c["Jobs"]:
            lll = {}
            lll["Name"] = checkDict(lng, "Name")
            lll["NameOnvan"] = ""
            lll["Company"] = checkDict(lng, "Company")
            lll["StartYear"] = checkDict(lng, "StartYear")
            lll["EndYear"] = checkDict(lng, "EndYear")
            lll["Salary"] = checkDict(lng, "Salary")
            lll["CauseOfLeftingJob"] = checkDict(lng, "CauseOfLeftingJob")
            lll["InsuranceNoandExplanation"] = checkDict(lng, "InsuranceNoandExplanation")
            lll["OtherExplanations"] = checkDict(lng, "OtherExplanations")
            levels.append(lll)
        d["Job"]["items"] = levels
        # step 8 Resume






        n.append(d)
    for m in n:
        dt = {
            "username": m['user']["username"],
            "email": m['user']["Email"],
            "password": m['user']["password"],
            "confirm_password": m['user']["password"]
        }
        serializer = UserSerializer(data=dt)
        if serializer.is_valid():
            # add user
            try:
                result = serializer.create(serializer.validated_data)
                # add to ****
                CustomerRegistrationViewSet().addUserToCustomer(result.id, 1)
                # getting profile instance
                profile = Profile.objects.get(userID=result.id)
                extra = profile.extra
                m.pop('user')
                extra["job"] = m
                profile.extra = profile.extra
                profile.save()
                print(str(result.id)+" -- created ")
            except:
                print("errrrrrrrrror")
                pass





#startMapping()

