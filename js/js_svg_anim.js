
var elements;
window.onload = function () {

    //Declare Raphael object
    var R = Raphael("paper", 300, 300);

    m2r = {};

    m2r.exchange = {
        options: {},
        regiondata: null,
        attributes: null,
        jsonAjax: function jsonAjax(url, callback, options) {
            //Create var to get var in scope
            var self;
            $.ajax({
            async: false,
            type: "POST",
            dataType: "json",
            url: url,
            success: function(data){
                // Retrieve callback return
                self = callback(data, options);
            }});
            // Return function callback result
            return self;
        },
        attributeData: function attributeData(datas, optionsObj) {
            var descriptions = {};
            for (line in datas){
                descriptions[datas[line]['nom_dept_clean']] = {"description_wikipedia" : datas[line]['description_wikipedia'], "nom_dept_title" : datas[line]['nom_dept_title'] }
            }
            return descriptions;
        },
        regionData: function regionData(datas, optionsStr) {

            elements = colorAnalyse(optionsStr, datas);
        },
        letterData: function letterData(datas, optionsStr){
            for (i in datas){
                optionsStr.path(datas[i].svg).translate( datas[i].x, datas[i].y);
            }
        },
        classification : function classification(datas, options){
            console.log(datas);
        }
    };

m2r.render = {
    htmlMustache: function htmlMustache(datas) {
        var template = "<h2>{{nom_dept_title}}</h2>{{{description_wikipedia}}}";
        var html = Mustache.to_html(template, datas);
        $('#rightdescription').html(html);
    }
}

    function setattr(fillcolor){
        var attr = {
            fill: fillcolor,
            stroke: "#666",
            "stroke-width": 1,
            "stroke-linejoin": "round"
        };
        return attr;
    }

    //descriptions = {};
    test = m2r.exchange.jsonAjax("attributes", m2r.exchange.attributeData, {"abc": 123, "def": 456});
    m2r.exchange.jsonAjax("raw_svg", m2r.exchange.regionData, R);
    m2r.exchange.jsonAjax("classification", m2r.exchange.classification);
    m2r.exchange.jsonAjax("raw_svg_letters", m2r.exchange.letterData, R);

    function colorAnalyse(raphaelobject, jsonobject) {

        var regions = {};

        for (i in jsonobject){
            var attr = setattr("#000000");
            regions[jsonobject[i]['nom_dept_clean']] = raphaelobject.path(jsonobject[i].svg).attr(attr);
            regions[jsonobject[i]['nom_dept_clean']]['identifier'] = jsonobject[i].nom_dept_clean;
        }

        var current = null;
        for (var region in regions) {
            regions[region].color = Raphael.getColor();

            (function (st, region) {
                st[0].style.cursor = "pointer";
                st[0].onmouseover = function () {
                    current && regions[current].animate({fill: "#BEC1C3", stroke: "#666"}, 500)
                    st.animate({fill: st.color, stroke: "#ccc"}, 500);
                    st.toFront();
                    raphaelobject.safari();
                    current = region;
                    if (regions.identifier === "hautecorse"){
                        //regions.attr({fill :"#64bf68"});
                        regions.attr({fill: "#64bf68"});
                    }
                    m2r.render.htmlMustache(test[current]);

                };
                st[0].onmouseout = function () {
                    st.animate({fill: "#BEC1C3", stroke: "#666"}, 500);
                    st.toBack();
                    raphaelobject.safari();
                };
                if (region == "ain") {
                    st[0].onmouseover();
                }
            })(regions[region], region);
        }
        return regions;
    }

};

// Test to change color

for (element in elements){
    //console.log(elements[element].identifier);
    elements[element].attr({fill: "#64bf68"});
}

