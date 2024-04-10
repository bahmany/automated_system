# import pymssql
#
# from amsp import settings
# from amsp.settings import ODOO_DBNAME, ODOO_ADMIN, ODOO_PASSWORD
# from amspApp.CompaniesManagment.Connections.models import ConnectionPools, Connections
# from amspApp.CompaniesManagment.Connections.viewes.ConnectionsViews import ConnectionsViewSet
# from amspApp.Infrustructures.odoo_connector.connectors import OdooConnector
# from amspApp.Material.utilities import fixChar
#
#
# def getRawConnection(poolName):
#     AccGLKol = ConnectionPools.objects.get(name=poolName)
#     AccGLKol_sql = AccGLKol.sqls[0]["code"]
#     connection = Connections.objects.get(databaseName="sgdb")
#
#     conn = pymssql.connect(server=connection.hostAddress,
#                            user=connection.username,
#                            password=connection.password,
#                            database=connection.databaseName,
#                            charset="UTF-8",
#                            as_dict=True)
#     conn.autocommit(True)
#
#     # connection.execute(AccGLKol_sql)
#     cursor = conn.cursor()
#     # connection.execute(AccGLKol_sql)
#     cursor.execute(AccGLKol_sql)
#     pp = []
#     for row in cursor:
#         pp.append(row)
#     # sql_res = cursor.fetchone()
#     # cursor.close()
#     conn.close()
#     return pp
#
#
# def get_PartInstanceComplete_By_PartCode(PartCode):
#     pool = ConnectionPools.objects.get(name="get_part_instance_from_list")
#     sql = pool.sqls[0]["code"]
#     sql = sql.replace("<:PartCode:>", PartCode)
#     sql = sql.replace("<:", "")
#     sql = sql.replace(":>", "")
#     connection = Connections.objects.get(databaseName="sgdb")
#     connection = ConnectionsViewSet().getConnection(connection)
#     connection.execute(sql)
#     sql_res = connection.fetchall()
#     return sql_res
#
#
# """
# دریافت لیست وزن ها
# """
#
#
# def get_Uom():
#     res = getRawConnection("get_uom_list")
#     return res
#
# def connectToOdoo():
#     # ssl._create_default_https_context = ssl._create_unverified_context
#
#     odoo = OdooConnector(endpoint=settings.ODOO_HTTP_REFERER,
#                          dbname=ODOO_DBNAME,
#                          username=ODOO_ADMIN,
#                          password=ODOO_PASSWORD)
#     # odoo = OdooConnector(endpoint=ODOO_Platform,
#     #                      dbname='odoodb',
#     #                      username='bahmanymb@gmail.com',
#     #                      password='****')
#     return odoo
#
# def get_vendors():
#     odoo = connectToOdoo()
#     uid = odoo.connect()
#     res = odoo.search(uid=uid,
#                       model='res.partner',
#                       action='search_read',
#                       queries=[[['supplier', '=', True]]],
#                       parameters={'limit': 99999})
#     return res
#
#
# def get_and_check_if_product_category_exist(title):
#     odoo = connectToOdoo()
#     uid = odoo.connect()
#     res = odoo.search(uid=uid,
#                       model='product.category',
#                       action='search_read',
#                       queries=[[['name', '=', title]]],
#                       parameters={'limit': 99999})
#     if len(res) == 0:
#         dt = {
#             'name': title
#         }
#         odoo.write(uid=uid,
#                    model='product.category', action="create", data=[dt])
#
#     res = odoo.search(uid=uid,
#                       model='product.category',
#                       action='search_read',
#                       queries=[[['name', '=', title]]],
#                       parameters={'limit': 99999})
#     return res[0]['id']
#
# def get_product_from_hamkaran_serial(Serial):
#     odoo = connectToOdoo()
#     uid = odoo.connect()
#     res = odoo.search(uid=uid,
#                       model='product.template',
#                       action='search_read',
#                       queries=[[['default_code', '=', Serial]]],
#                       parameters={'limit': 99999})
#     return res[0]
#
# def uom_id(title):
#     odoo = connectToOdoo()
#     uid = odoo.connect()
#     res = odoo.search(uid=uid,
#                       model='product.uom',
#                       action='search_read',
#                       queries=[[['name', '=', fixChar(title)]]],
#                       parameters={'limit': 99999})
#     return res[0]['id']
#
#
# def insert_product_into_odoo(json):
#     odoo = connectToOdoo()
#     uid = odoo.connect()
#     update_uom_with_hamkaran()
#     category_id = get_and_check_if_product_category_exist('مواد اولیه')
#     complete_instance_of_product = get_PartInstanceComplete_By_PartCode(json['PartCode'])[0]
#     weight_title = fixChar(complete_instance_of_product['UnitName'])
#     odoo_uom_id = uom_id(weight_title)
#     odoo_uom_po_id = uom_id(weight_title)
#     odoo_name = json['PartCode']
#     odoo_description = json['PartName']
#     odoo_sale_ok = False
#     odoo_purchase_ok = True
#     odoo_type = "product"
#     odoo_categ_id = category_id
#     odoo_tracking = "lot"
#     odoo_default_code = json['Serial']
#
#     dt = dict(
#         uom_id=odoo_uom_id,
#         uom_po_id=odoo_uom_po_id,
#         name=odoo_name,
#         description=odoo_description,
#         sale_ok=odoo_sale_ok,
#         purchase_ok=odoo_purchase_ok,
#         type=odoo_type,
#         categ_id=odoo_categ_id,
#         tracking=odoo_tracking,
#         default_code=odoo_default_code
#     )
#
#     odoo.write(uid=uid,
#                model='product.template', action="create", data=[dt])
#
#
#
#
# def update_uom_with_hamkaran():
#     hamkaran_uom = get_Uom()
#     odoo = connectToOdoo()
#     uid = odoo.connect()
#     for h in hamkaran_uom:
#         id_of_category = None
#         if (h['parent_cat']):
#             res = odoo.search(uid=uid,
#                               model='product.uom.categ',
#                               action='search_read',
#                               queries=[[['name', '=', fixChar(h['parent_cat'])]]],
#                               parameters={'limit': 99999})
#             if len(res) == 0:
#                 odoo.write(uid=uid,
#                            model='product.uom.categ', action="create", data=[{'name': fixChar(h['parent_cat'])}])
#
#                 res = odoo.search(uid=uid,
#                                   model='product.uom.categ',
#                                   action='search_read',
#                                   queries=[[['name', '=', fixChar(h['parent_cat'])]]],
#                                   parameters={'limit': 99999})
#             id_of_category = res[0]['id']
#
#         res = odoo.search(uid=uid,
#                           model='product.uom',
#                           action='search_read',
#                           queries=[[['name', '=', fixChar(h['UnitName'])]]],
#                           parameters={'limit': 99999})
#         if len(res) == 0:
#             dt = dict(
#                 name=fixChar(h['UnitName']),
#                 category_id=id_of_category if id_of_category else 1,
#                 uom_type="reference",
#                 factor_inv=1.0,
#                 active=True,
#                 rounding=0.00100
#             )
#             odoo.write(uid=uid,
#                        model='product.uom', action="create", data=[dt])
