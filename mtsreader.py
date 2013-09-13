# coding=utf-8
import os
import sys

__author__ = 'Frostbite'
from xml.dom import minidom


def read_xml():
    root_dir = None
    if len(sys.argv) > 1:
        root_dir = sys.argv[1]
    total = dict()
    total_pay = 0
    total_talks = 0
    sms_pay = 0

    if root_dir is not None and os.path.isdir(root_dir):
        for fn in os.listdir(root_dir):
            # //fn = 'C:/Users/Frostbite/Documents/Doc_d1492b1fd6984418be4c080030d9b128-1.xml'
            if not fn.endswith(".xml"):
                continue
            xmldoc = minidom.parse(root_dir + '/' + fn)
            itemlist = xmldoc.getElementsByTagName('Report')[0].childNodes
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
                            tel = ds.attributes['s'].value == u'Телеф.'
                            if (tel or sms) and ds.attributes['c'].value != '0':
                                pay = float(ds.attributes['c'].value.replace(',', '.'))
                                total_pay += pay
                                if sms:
                                    sms_pay += pay
                                if tel:
                                    total_talks += int(ds.attributes['du'].value.split(':')[0]) * 60 + int(
                                        ds.attributes['du'].value.split(':')[0])
                                print ds.attributes['d'].value + ' at ' + ds.attributes['n'].value + ' for ' + \
                                      ds.attributes['c'].value + ('(sms)' if sms else '')

                    break
        h = total.get('HSDPA (3G)', 0) / 1024
        g = total.get('gprs', 0) / 1024
        print '3G: %dMb; GPRS: %dMb; total = %dMb' % (h, g, h + g)
        print 'Total payment: %f; sms payment: %f; total talks: %d:%d' % \
              (total_pay, sms_pay, total_talks / 60, total_talks % 60)


read_xml()