from amsp import settings
from amsp.settings import ODOO_DBNAME, ODOO_ADMIN, ODOO_PASSWORD
from amspApp.Infrustructures.odoo_connector.connectors import OdooConnector
from amspApp.MyProfile.models import Profile
from amspApp.amspUser.models import MyUser

"""
 =, !=, >, >=, <, <=, like, ilike, in, not in, child_of, parent_left, parent_right
 Hot to search, search_read and read ( using the method search() )
 selection: false,,1,Employee,45,Equipment Manager,43,Officer,44,Manager
 """


class odoo_instance():
    odoo = None
    uid = None

    def __init__(self):
        self.odoo = OdooConnector(endpoint=settings.ODOO_HTTP_REFERER,
                                  dbname=ODOO_DBNAME,
                                  username=ODOO_ADMIN,
                                  password=ODOO_PASSWORD)
        self.uid = self.odoo.connect()

    def get_odoo_group_id_by_name(self, group_name):
        res = self.odoo.search(uid=self.uid,
                               model='res.groups',
                               action='search',
                               queries=[[['name', '=', group_name]]],
                               parameters={'limit': 500})
        if len(res) == 0:
            raise Exception("module category %s does not installed" % (group_name,))
        return res[0]

    def get_user_types(self):
        Internal_User = self.get_odoo_group_id_by_name("Internal User")
        Portal = self.get_odoo_group_id_by_name("Portal")
        Public = self.get_odoo_group_id_by_name("Public")
        return "sel_groups_%d_%d_%d" % (Internal_User, Portal, Public,)

    def get_module_category_id_by_catname(self, category_name):
        res = self.odoo.search(uid=self.uid,
                               model='ir.module.category',
                               action='search',
                               queries=[[['name', '=', category_name]]],
                               parameters={'limit': 500})
        if len(res) == 0:
            raise Exception("module category %s does not installed" % (category_name,))
        return res[0]

    def check_user_if_not_create(self, username):
        userins = self.odoo.search(uid=self.uid,
                                   model='res.users',
                                   action='search',
                                   queries=[[['login', '=', username + "@****.com"]]],
                                   parameters={'limit': 1})

        if len(userins) == 0:
            user = MyUser.objects.get(username = username)
            userProfile = Profile.objects.get(userID=user.id)
            data = [{
                'login': user.username + "@****.com",
                'name': userProfile.extra.get("Name", "nothing"),
                'password': "110110"}
            ]
            user_types = self.get_user_types()
            data[0][user_types] = self.get_odoo_group_id_by_name("Internal User")
            data[0]["lang"] = "fa_IR"
            data[0]["tz"] = "Asia/Tehran"

            data[0]["notification_type"] = "inbox"
            result = self.odoo.write(uid=self.uid, model='res.users', action='create', data=data)
            return self.check_user_if_not_create(user.username + "@****.com")
        return username[0]