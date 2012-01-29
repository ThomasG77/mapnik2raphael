#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from spatialite_sqlite import *
from download_and_zip import *
from variables_config import * # Contains shared variables (See http://docs.python.org/faq/programming.html#how-do-i-share-global-variables-across-modules)

cur = conn.cursor()
from Cheetah.Template import Template

with closing(cur):

    html = showquery(cur, 'SELECT code_dept, lower(nom_dept) as nom_dept, substr(upper(nom_dept),1,1) || substr(lower(nom_dept),-length(nom_dept)+1) as nom_dept_title, replace(replace(lower(nom_dept),"-",""),"\'","") as nom_dept_clean, description_wikipedia, svg FROM "departements"')

    print html

    tpl_dir = "tpl_cheetah"
    css_dir = "css"
    js_dir = "js"
    sep = "/"

    t = Template(open(tpl_dir + sep + 'template_html.tmpl').read(), searchList=[{'data': html}])
    #print t
    open('france.html','w').write(str(t))

    t = Template(open(tpl_dir + sep + 'screen_style.tmpl').read(), searchList=[{'data': html}])
    #print t
    open(css_dir + sep + 'screen_style.css','w').write(str(t))

    htmlletters = showquery(cur, 'SELECT path, x, y FROM "letters"')

    t = Template(open(tpl_dir + sep +'js_svg_anim.tmpl').read(), searchList=[{'data': html, 'letters': htmlletters}])
    #print t
    open(js_dir + sep + 'js_svg_anim.js','w').write(str(t))

