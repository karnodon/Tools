# coding=utf-8
import sys

__author__ = 'Frostbite'
import os
from docx import *

import xlrd
teachers = {}
classes = {}
pupils = []
final_table = {}

def compare_pupils(a, b):
    c1 = int(a[2])
    c2 = int(b[2])
    if c1 == c2:
        if a[3] == b[3]:
            return 0
        if a[3] > b[3]:
            return 1
        return -1
    return  c1 - c2


def print_content(name):
    rb = xlrd.open_workbook(name, formatting_info=False)
    sheet = rb.sheet_by_index(1)
    column_titles = (u'Фамилия', u'Имя', u'Класс', u'буква', u'ФИО', u'победитель/призер')
    columns = []
    head_row = sheet.row_values(21)#Строка с заголовками
    cl_idx = 0
    for cl in head_row:
        if isinstance(cl, unicode) and not(cl_idx in columns):
            if cl == column_titles[0] or cl == column_titles[1] or cl.find(column_titles[2]) >= 0 or cl.find(
                column_titles[3]) >= 0 or cl.find(column_titles[4]) >= 0  or cl == column_titles[5]:
                columns.append(cl_idx)
        cl_idx += 1
    s = ''
    for c in column_titles:
        s += c + '|'
    print s.rstrip('|')
    the_end = False
    tab = []
    for row_num in range(sheet.nrows):
        if 22 < row_num < 80 and not the_end:
            row = sheet.row_values(row_num)
            s = ''
            k = 0
            tr = []
            for c_el in row:
                if k in columns:
                    if c_el == '':
                        the_end = True
                        break
                    if isinstance(c_el, float):
                        v = str(round(c_el)).rstrip('0').rstrip('.')
                    else:
                        v = c_el.strip()
                    s += v + '|'
                    tr.append(v)
                k += 1
            if s != '' and len(tr) > 0:
                p = (tr[0], tr[1], tr[2], tr[3])
                if not (p in pupils):
                    cls = tr[2] + tr[3]
                    if cls in classes:
                        classes[cls] += 1
                    else:
                        classes[cls] = 1
                    pupils.append(p)

                if tr[4] in teachers:
                    teachers[tr[4]] += 1
                else:
                    teachers[tr[4]] = 1
                tab.append(tr)
    if len(tab) > 0:
        tab.sort(compare_pupils)
        tab.insert(0, column_titles)
        final_table[name] = tab
#        for t in final_table:
#            s = ''
#            for c in t:
#               s += c + '|'
#            print s.rstrip('|')

def print_teachers():
    if len(teachers):
        t_list = sorted(teachers.keys())
        for t_name in t_list:
            print t_name + " : " + str(teachers[t_name])

def print_classes():
    if len(classes):
        total = 0
        c_list = sorted(classes.keys())
        for cls in c_list:
            total += classes[cls]
            print cls + " : " + str(classes[cls])
        print u"всего = " + str(total)
def save_to_word(name):
    # Default set of relationshipships - these are the minimum components of a document
    relationships = relationshiplist()

    # Make a new document tree - this is the main part of a Word document
    document = newdocument()

    # This xpath location is where most interesting content lives
    docbody = document.xpath('/w:document/w:body', namespaces=nsprefixes)[0]

    # Append two headings and a paragraph
    docbody.append(heading(u'Отчет по Олимпиадам 2012', 1))
    for subj in final_table:
        docbody.append(paragraph(subj))
        # Append a table
        docbody.append(table(final_table[subj]))

    # Create our properties, contenttypes, and other support files
    coreprops = coreproperties(title='Python docx demo', subject='Report',
        creator='Max Morozov', keywords=['python', 'Office Open XML', 'Word'])
    appprops = appproperties()
    ct = contenttypes()
    ws = websettings()
    wr = wordrelationships(relationships)
    # Save our document
    savedocx(document, coreprops, appprops, ct, ws, wr, 'Olympic report.docx')
if len(sys.argv) > 1:
    files = os.listdir(sys.argv[1])
    for file in files:
        print '**************************' + file + '******************************'
        print_content(sys.argv[1] + file)
#    print_teachers()
    print_classes()
save_to_word('abc')
