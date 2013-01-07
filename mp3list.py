# coding=utf-8
__author__ = 'Frostbite'
import re
import os
import sys

main_list = []
total_files = 0
total_albums = 0#only files no sub dirs
show_files  = False

def walk(root, file_list):
    lst = os.listdir(root)
    dirs = [os.path.join(root,d) for d in lst if os.path.isdir(os.path.join(root,d))]
    files = [f for f in lst if re.match('.*(.mp3|.ogg|.wma)', f)]
    if len(dirs) > 0 or len(files) > 0:
        file_list.append(root)
        file_list.append(files)
        global total_files
        total_files += len(files)
        if len(dirs) == 0:
            global total_albums
            total_albums += 1
        for d in dirs:
            sub_lst = []
            file_list.append(sub_lst)
            walk(d, sub_lst)

def print_html(tgt, html_file):
    if len(tgt) > 0:
        html_file.write((u'<li>' + tgt[0] + u'</li><ul>').encode('utf8'))
        global show_files
        if show_files:
            try:
                files = tgt[1]
                for f in files:
                    html_file.write((u'<li>' + f + u'</li>').encode('utf8'))
            except IndexError:
                pass
        try:
            for i in range(2, len(tgt)):
                sub_lst = tgt[i]
                print_html(sub_lst, html_file)
        except IndexError:
            pass
        html_file.write(u'</ul>'.encode('utf8'))

def main():
    if len(sys.argv) < 3:
        print 'Usage: python mp3list [-f] <root> <target>'
        exit()
    arg_idx = 1
    if sys.argv[1] == '-f':
        global show_files
        show_files = True
        arg_idx = 2
    walk(unicode(sys.argv[arg_idx]), main_list)
    f = open(sys.argv[arg_idx + 1], 'w')
    f.write(u'<html><body><ul>'.encode('utf8'))
    print_html(main_list, f)
    f.write((u'</ul><ul><li>всего альбомов: ' + unicode(total_albums) + u'</li>').encode('utf8'))
    f.write((u'<li>всего записей: ' + unicode(total_files) + u'</li></ul>').encode('utf8'))
    f.write(u'</body></html>'.encode('utf8'))

main()