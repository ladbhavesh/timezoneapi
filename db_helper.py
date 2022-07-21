import mysql.connector
from mysql.connector import Error
import datetime
import pytz
from pytz import timezone

from config import getConfig

#'Hello {name}!This is{program}.'.format(name=name,program=program)
timezone_sql = "SELECT FROM_UNIXTIME({utcepoch} + `gmt_offset`, '%a, %d %b %Y, %H:%i:%s') AS `local_time` FROM `time_zone` WHERE `time_start` <= {utcepoch} AND `zone_name` = '{zone_name}' ORDER BY `time_start` DESC LIMIT 1;"


def getalltimezones():
    return pytz.all_timezones

def toUTC(from_zone, time):
    tz = timezone(from_zone)
    localtime = tz.localize(time)
    return tz.normalize(localtime).astimezone(pytz.utc)    

def convertToUnixTime(dt):
    #date_format = datetime.datetime.strptime(dt,"%Y-%m-%d %H:%M:%S")
    unix_time = datetime.datetime(dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second).timestamp()
    #unix_time = pytz.utc.localize(dt, is_dst=False).timestamp()
    #datetime.datetime.tim
    return unix_time

def getAlltimeZones():
    return pytz.all_timezones    

def getTimezoneInfo(from_zone, to_zone, time):

    connection_initialized = False
    try:
        date_format = datetime.datetime.strptime(time,
                                         "%Y-%m-%d %H:%M:%S")
        utcTime = toUTC(from_zone, date_format)
        utcEpoch = convertToUnixTime(utcTime)
        sql = timezone_sql.format(utcepoch=utcEpoch,zone_name=to_zone)

        connection = mysql.connector.connect(host=getConfig('mysql_host'),
                                            database=getConfig('mysql_database'),
                                            user=getConfig('mysql_user'),
                                            password=getConfig('mysql_password'))
        connection_initialized = True                                    
        if connection.is_connected():
            #db_Info = connection.get_server_info()
            #print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            print(sql)
            cursor.execute(sql)
            record = cursor.fetchone()
            print(record)
            time = record[0]
            return {"result" : time}

    except Error as e:
        print("system error")
        return { "error": e }
    finally:
        if connection_initialized:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")