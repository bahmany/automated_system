import pymssql
import re

from asq.initiators import query

from amspApp.CompaniesManagment.Connections.models import ConnectionPools, Connections
from amspApp.CompaniesManagment.Connections.viewes.ConnectionsViews import ConnectionsViewSet
# from amspApp.Material.odoo_connect import insert_product_into_odoo
from amspApp.Infrustructures.Classes.DateConvertors import getCurrentYearShamsi2digit


def getRawConnection(poolName):
    AccGLKol = ConnectionPools.objects.get(name=poolName)
    AccGLKol_sql = AccGLKol.sqls[0]["code"]
    connection = Connections.objects.get(databaseName="sgdb")

    conn = pymssql.connect(server=connection.hostAddress,
                           user=connection.username,
                           password=connection.password,
                           database=connection.databaseName,
                           charset="UTF-8",
                           as_dict=True)
    conn.autocommit(True)

    # connection.execute(AccGLKol_sql)
    cursor = conn.cursor()
    # connection.execute(AccGLKol_sql)
    cursor.execute(AccGLKol_sql)
    pp = []
    for row in cursor:
        pp.append(row)
    # sql_res = cursor.fetchone()
    # cursor.close()
    conn.close()
    return pp


"""
دریافت لیست وزن ها
"""


def get_Uom():
    res = getRawConnection("get_uom_list")
    return res


"""
دریافت لیست انبارها
"""


def get_PosPart():
    res = getRawConnection("PosPart")
    return res


"""
واحدهای سنجش
"""


def get_InvMUnit():
    res = getRawConnection("InvMUnit")
    return res


"""
دریافت نوع کالا
"""


def get_InvvwPartType():
    res = getRawConnection("InvvwPartType")
    return res


"""
دریافت طبقات حساب
"""


def get_InvAccCtgry():
    res = getRawConnection("InvAccCtgry")
    return res


"""
دریافت طبقات حساب
"""


def get_NewPartID():
    res = getRawConnection("first_get_part_newID")
    return res


def check_PartName_Insert_Before(PartName):
    pool = ConnectionPools.objects.get(name="check_partname_duplicated")
    sql = pool.sqls[0]["code"]
    sql = sql.replace("<:PartName:>", PartName)
    sql = sql.replace("<:", "")
    sql = sql.replace(":>", "")
    connection = Connections.objects.get(databaseName="sgdb")
    connection = ConnectionsViewSet().getConnection(connection)
    connection.execute(sql)
    sql_res = connection.fetchall()
    return sql_res


def get_Anbar_Of_PartCode(PartSerial):
    pool = ConnectionPools.objects.get(name="get_Anbar_Of_PartCode")
    sql = pool.sqls[0]["code"]
    sql = sql.replace("<:PartSerial:>", PartSerial)
    sql = sql.replace("<:", "")
    sql = sql.replace(":>", "")
    connection = Connections.objects.get(databaseName="sgdb")
    connection = ConnectionsViewSet().getConnection(connection)
    connection.execute(sql)
    sql_res = connection.fetchall()
    return sql_res


def delete_partcode_from_mahale(StockSerial, PartSerial):
    pool = ConnectionPools.objects.get(name="delete_partcode_from_mahale")
    sql = pool.sqls[0]["code"]
    sql = sql.replace("<:StockSerial:>", str(StockSerial))
    sql = sql.replace("<:PartSerial:>", str(PartSerial))
    sql = sql.replace("<:", "")
    sql = sql.replace(":>", "")
    connection = Connections.objects.get(databaseName="sgdb")
    connection = ConnectionsViewSet().getConnectionAutoCommit(connection)
    connection.execute(sql)
    connection.close()

    return {}


"""
ورود به همکاران سیستم
"""


def insert_Hamkaran(json):
    res = check_PartName_Insert_Before(json['PartName'])
    if (len(res) != 0):
        raise Exception("PartName insert before ")

    sql = """
insert into Inv.Part
  (
  Serial, MUnitRef, AccCtgryRef, PartCode,
  PartName, LatinName, PartNo, ORDERLIMIT,
  ORDERPOINT, MINQTY, MAXQTY, PartType,
  Comment, DisActive , IranCode , UseForBascul
  )
values
  (
  %d, %d, %d, '%s',
  '%s','%s',   '%s', NULL,
  NULL, NULL, NULL, '%s',
'%s', %s , '%s' , %d
)
 
    """ % (
        json['Serial'], json['MUnitRef'], json['AccCtgryRef'], json['PartCode'],
        json['PartName'], json.get('LatinName', ''), json.get('PartNo', ''),
        json['PartType'].strip(),
        json.get('Comment', ''), int(not json['DisActive']), json.get('IranCode', ''), int(json['UseForBascul']),
    )

    connection = Connections.objects.get(databaseName="sgdb")
    conn = pymssql.connect(server=connection.hostAddress,
                           user=connection.username,
                           password=connection.password,
                           database=connection.databaseName,
                           charset="UTF-8", )

    cursor = conn.cursor()
    cursor.execute(sql)
    # cursor.commit()
    # cursor.close()
    conn.commit()
    conn.close()
    json['InsertedInstance'] = get_PartInstance_By_PartNo(json['PartCode'])
    # insert_product_into_odoo(json)
    # sql_res = connection.fetchall()
    return {}


def get_PartInstance_By_PartNo(PartNo):
    pool = ConnectionPools.objects.get(name="check_if_partcode_insert_before_rahkaran")
    sql = pool.sqls[0]["code"]
    PartNo = re.sub('[^A-Za-z0-9]+', '', PartNo)
    sql = sql.replace("<:partnumber:>", PartNo)
    sql = sql.replace("<:", "")
    sql = sql.replace(":>", "")
    connection = Connections.objects.get(databaseName="RahkaranDB")
    connection = ConnectionsViewSet().getConnection(connection)
    connection.execute(sql)
    sql_res = connection.fetchall()
    return sql_res


def get_VchHdrIDFromVchNum(VchNum):
    pool = ConnectionPools.objects.get(name="InvVchHdr")
    sql = pool.sqls[0]["code"]
    VchNum = re.sub('[^A-Za-z0-9]+', '', str(VchNum))
    sql = sql.replace("<:vchnum:>", VchNum)
    sql = sql.replace("<:year:>", getCurrentYearShamsi2digit())
    sql = sql.replace("<:", "")
    sql = sql.replace(":>", "")
    connection = Connections.objects.get(databaseName="sgdb")
    connection = ConnectionsViewSet().getConnection(connection)
    connection.execute(sql)
    sql_res = connection.fetchall()
    return sql_res


def get_AccDLs(search):
    if search == 'undefined':
        search = ""
    pool = ConnectionPools.objects.get(name="accdl")
    sql = pool.sqls[0]["code"]
    # search = re.sub('[^A-Za-z0-9]+', '', search)
    sql = sql.replace("<:titlesearch:>", search)
    sql = sql.replace("<:", "")
    sql = sql.replace(":>", "")
    connection = Connections.objects.get(databaseName="sgdb")
    connection = ConnectionsViewSet().getConnection(connection)
    connection.execute(sql)
    sql_res = connection.fetchall()
    return sql_res


def get_PartInstanceComplete_By_PartCode(PartCode):
    pool = ConnectionPools.objects.get(name="get_part_instance_from_list")
    sql = pool.sqls[0]["code"]
    sql = sql.replace("<:PartCode:>", PartCode)
    sql = sql.replace("<:", "")
    sql = sql.replace(":>", "")
    connection = Connections.objects.get(databaseName="sgdb")
    connection = ConnectionsViewSet().getConnection(connection)
    connection.execute(sql)
    sql_res = connection.fetchall()
    return sql_res


def get_PartInstance_By_PartCode(PartCode):
    pool = ConnectionPools.objects.get(name="check_if_partcode_insert_before")
    sql = pool.sqls[0]["code"]
    sql = sql.replace("<:partnumber:>", PartCode)
    sql = sql.replace("<:", "")
    sql = sql.replace(":>", "")
    connection = Connections.objects.get(databaseName="sgdb")
    connection = ConnectionsViewSet().getConnection(connection)
    connection.execute(sql)
    sql_res = connection.fetchall()
    return sql_res


def set_Location_To_PartNo(json):
    connection = Connections.objects.get(databaseName="sgdb")

    conn = pymssql.connect(server=connection.hostAddress,
                           user=connection.username,
                           password=connection.password,
                           database=connection.databaseName,
                           charset="UTF-8", )
    pool = ConnectionPools.objects.get(name="add_part_to_location")

    sql = pool.sqls[0]["code"]
    sql = sql.replace("<:PartRef:>", str(json['Serial']))
    sql = sql.replace("<:PosPartRef:>", str(json['PosPartRef']))
    sql = sql.replace("<:Active:>", str(json['Active']))
    sql = sql.replace("<:", "")
    sql = sql.replace(":>", "")

    cursor = conn.cursor()
    cursor.execute(sql)
    # cursor.commit()
    # cursor.close()
    conn.commit()
    conn.close()
    # sql_res = connection.fetchall()
    return {}


PartCodeChar3_to_Hamkaran_mapper = [
    dict(char3='0', hamkaran_code='330687', hamkaran_name='شرکت جولي (JOLEE)'),
    dict(char3='1', hamkaran_code='', hamkaran_name=''),
    dict(char3='2', hamkaran_code='340001', hamkaran_name='شرکت تيان جين - TIANJIN'),
    dict(char3='3', hamkaran_code='', hamkaran_name=''),
    dict(char3='4', hamkaran_code='330735', hamkaran_name='MMK STEEL TRADE AG'),
    dict(char3='5', hamkaran_code='', hamkaran_name=''),
    dict(char3='6', hamkaran_code='330440', hamkaran_name='جيان گين کمت(Jiangin Comat Metal)'),
    dict(char3='7', hamkaran_code='330054', hamkaran_name='شرکت **** ****ه'),
    dict(char3='8', hamkaran_code='330316', hamkaran_name='صنايع هفت ****'),
    dict(char3='9', hamkaran_code='330053', hamkaran_name='شرکت **** غرب آسيا'),
    dict(char3='A', hamkaran_code='', hamkaran_name=''),
    dict(char3='B', hamkaran_code='', hamkaran_name=''),
    dict(char3='C', hamkaran_code='', hamkaran_name=''),
    dict(char3='D', hamkaran_code='', hamkaran_name=''),
    dict(char3='E', hamkaran_code='', hamkaran_name=''),
    dict(char3='F', hamkaran_code='', hamkaran_name=''),
    dict(char3='G', hamkaran_code='', hamkaran_name=''),
    dict(char3='H', hamkaran_code='', hamkaran_name=''),
    dict(char3='I', hamkaran_code='', hamkaran_name=''),
    dict(char3='J', hamkaran_code='', hamkaran_name=''),
    dict(char3='K', hamkaran_code='', hamkaran_name=''),
    dict(char3='L', hamkaran_code='', hamkaran_name=''),
    dict(char3='M', hamkaran_code='', hamkaran_name=''),
    dict(char3='N', hamkaran_code='', hamkaran_name=''),
    dict(char3='O', hamkaran_code='', hamkaran_name=''),
    dict(char3='P', hamkaran_code='', hamkaran_name=''),
    dict(char3='Q', hamkaran_code='', hamkaran_name=''),
    dict(char3='R', hamkaran_code='', hamkaran_name=''),
    dict(char3='S', hamkaran_code='', hamkaran_name=''),
    dict(char3='T', hamkaran_code='', hamkaran_name=''),
    dict(char3='U', hamkaran_code='', hamkaran_name=''),
    dict(char3='V', hamkaran_code='', hamkaran_name=''),
    dict(char3='W', hamkaran_code='', hamkaran_name=''),
    dict(char3='X', hamkaran_code='', hamkaran_name=''),
    dict(char3='Y', hamkaran_code='', hamkaran_name=''),
    dict(char3='Z', hamkaran_code='', hamkaran_name='')
]


def PartCodeChar3_to_Hamkaran(Char3):
    s = query(PartCodeChar3_to_Hamkaran_mapper).where(lambda x: x['char3'] == Char3).first_or_default({
        'hamkaran_code': 0,
        'hamkaran_name': 'کد معرفی نشده'
    })
