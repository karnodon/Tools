# coding=utf-8
__author__ = 'Frostbite'
from xml.dom import minidom
def read_xml():
    fn = 'C:/Users/Frostbite/Documents/Doc_d1492b1fd6984418be4c080030d9b128-1.xml'
    xmldoc = minidom.parse(fn)
    itemlist = xmldoc.getElementsByTagName('Report')[0].childNodes
    total = dict()
    total_pay = 0
    sms_pay = 0
    for nd in itemlist:
        if nd.nodeName == 'ds':
            print nd.attributes['n'].value
            ds_list = nd.childNodes
            for ds in ds_list:
                if ds.nodeName == 'i':
                    if ds.attributes['n'].value == 'internet.mts.ru':
                        kb = int(ds.attributes['du'].value[:-2])
                        k = ds.attributes['s'].value
                        if k in total:
                            total[k] += kb
                        else:
                            total[k] = kb
                    sms = ds.attributes['s'].value == u'sms o'
                    if (ds.attributes['s'].value == u'Телеф.' or sms) and ds.attributes['c'].value != '0':
                        pay = float(ds.attributes['c'].value.replace(',', '.'))
                        total_pay += pay
                        if sms:
                            sms_pay += pay
                        print ds.attributes['d'].value + ' at ' + ds.attributes['n'].value + ' for ' + ds.attributes['c'].value + ('(sms)' if sms else '')

            break
    h = total['HSDPA (3G)']/1024
    g = total['gprs']/1024
    print '3G:' + str(h) + 'Mb; GPRS: ' + str(g) + 'Mb; total = ' + str(h + g) + 'Mb'
    print 'Total payment: ' + str(total_pay) + '; sms payment: ' + str(sms_pay)

read_xml()