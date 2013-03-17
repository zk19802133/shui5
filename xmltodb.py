# from xml.etree import ElementTree as ET
from xml.dom import minidom
import MySQLdb as db
import chardet

conn=db.connect("127.0.0.1","root","admin","spider",charset='utf8')
cur=conn.cursor()

filename="shui5.xml"
xmldoc=minidom.parse(filename)
items=xmldoc.documentElement.getElementsByTagName('item')

count=0
for item in items:
    count+=1
    try:
        title = item.getElementsByTagName('title')[0].childNodes[0].nodeValue.encode('utf-8')
        title=db.escape_string(title)
        link = item.getElementsByTagName('link')[0].childNodes[0].nodeValue.encode('utf-8')
        link=db.escape_string(link)
        content = item.getElementsByTagName('content')[0].childNodes[0].nodeValue.encode('utf-8')
        content=db.escape_string(content)
        sql="insert into `shui5` (`title`,`link`,`content`) values('"+title+"','"+link+"','"+content+"');"
        cur.execute(sql)
    except IndexError:
        count-=1
        pass
    # print sql
    # print type(sql)
    # print chardet.detect(sql)
    print 'insert '+repr(count)+' records'
print '****************  '+repr(count)+'  records*******************'

cur.close()
conn.close()