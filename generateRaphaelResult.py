#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from download_and_zip import *
url_raphael = "https://raw.github.com/DmitryBaranovskiy/raphael/master/raphael.js"
file_name_raphael = url_raphael.split('/')[-1]
download_file(url_raphael, file_name_raphael)


from pyspatialite import dbapi2 as sqlite

conn = sqlite.connect('france.sqlite')
cur = conn.cursor()

def showquery(request):
    cur.execute(request)
    fieldnames = [name[0] for name in cur.description]
    result = []
    for row in cur.fetchall():
        rowset = []
        for field in zip(fieldnames, row):
            rowset.append(field)
        result.append(dict(rowset))
    return result

html = showquery('SELECT code_dept, lower(nom_dept) as nom_dept, substr(upper(nom_dept),1,1) || substr(lower(nom_dept),-length(nom_dept)+1) as nom_dept_title, replace(replace(lower(nom_dept),"-",""),"\'","") as nom_dept_clean, code_chf, nom_chf, description_wikipedia, svg FROM "departements"')


from Cheetah.Template import Template

t = Template(open('template_html.tmpl').read(), searchList=[{'data': html}])
#print t
open('france.html','w').write(str(t))

t = Template(open('screen_style.tmpl').read(), searchList=[{'data': html}])
#print t
open('screen_style.css','w').write(str(t))

htmlletters = showquery('SELECT path, x, y FROM "letters"')

t = Template(open('js_svg_anim.tmpl').read(), searchList=[{'data': html, 'letters': htmlletters}])
#print t
open('js_svg_anim.js','w').write(str(t))

cur.close()

