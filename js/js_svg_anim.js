        var R;
        window.onload = function () {
            R = Raphael("paper", 300, 300);
            var attr = {
                fill: "#BEC1C3",
                stroke: "#666",
                "stroke-width": 1,
                "stroke-linejoin": "round"
            };

var descriptions = {};

$.ajax({
      async: false,
      type: "POST",
    dataType: "json",
        url: "attributes",
        success: function(data){
            //addLetter(R, data);
            for (i in data){
                descriptions[data[i]['nom_dept_clean']] = {"description_wikipedia" : data[i]['description_wikipedia'], "nom_dept_title" : data[i]['nom_dept_title'] }
            }
            console.log(descriptions);
        }
});

$.ajax({
      async: false,
      type: "POST",
    dataType: "json",
        url: "raw_svg",
        success: function(data){
            colorAnalyse(R, data);
        }
});

$.ajax({
      async: false,
      type: "POST",
    dataType: "json",
        url: "raw_svg_letters",
        success: function(data){
            addLetter(R, data);
        }
});

function description_dept(jsonobject){
    var template = "<h2>{{nom_dept_title}}</h2>{{{description_wikipedia}}}";
    var html = Mustache.to_html(template, jsonobject);
    $('#rightdescription').html(html);
}

function colorAnalyse(raphaelobject, jsonobject) {

    var regions = {};

    for (i in jsonobject){
        regions[jsonobject[i]['nom_dept_clean']] = raphaelobject.path(jsonobject[i].svg).attr(attr);
    }

    var current = null;
    for (var region in regions) {
        regions[region].color = Raphael.getColor();
        (function (st, region) {
            st[0].style.cursor = "pointer";
            st[0].onmouseover = function () {
                current && regions[current].animate({fill: "#BEC1C3", stroke: "#666"}, 500)// && (document.getElementById(current).style.display = "");
                st.animate({fill: st.color, stroke: "#ccc"}, 500);
                st.toFront();
                raphaelobject.safari();
                //document.getElementById(region).style.display = "block";
                current = region;
                description_dept(descriptions[current]);
                //console.log(descriptions[current]);

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
}

function addLetter(raphaelobject, jsonobject){
    for (i in jsonobject){
        raphaelobject.path(jsonobject[i].svg).translate( jsonobject[i].x, jsonobject[i].y);
    }
}

        };

