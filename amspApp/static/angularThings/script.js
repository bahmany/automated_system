'use strict';

// if (location.protocol !== "https:") {
//     location.replace("https://app.******.com");
// }


jQuery.browser = {};
(function () {
    jQuery.browser.msie = false;
    jQuery.browser.version = 0;
    if (navigator.userAgent.match(/MSIE ([0-9]+)\./)) {
        jQuery.browser.msie = true;
        jQuery.browser.version = RegExp.$1;
    }
})();

Array.prototype.pushArray = function (arr) {
    this.push.apply(this, arr);
};


function getCurrentTime() {
    var d = new Date();
    var h = d.getHours().toString();
    var m = d.getMinutes().toString();
    if (h.length == 1) {
        h = "0" + h;
    }
    if (m.length == 1) {
        m = "0" + m;
    }

    return h + ":" + m;
}


$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("rahsoon-csrftoken", getCookie('rahsoon-CSRF-TOKEN'));
        }
    }
});

function getClass(obj) {
    if (typeof obj === "undefined")
        return "undefined";
    if (obj === null)
        return "null";
    return Object.prototype.toString.call(obj)
        .match(/^\[object\s(.*)\]$/)[1];
}

Date.prototype.today = function () {
    return this.getFullYear() + "/" + (((this.getMonth() + 1) < 10) ? "0" : "") + (this.getMonth() + 1) + "/" + ((this.getDate() < 10) ? "0" : "") + this.getDate();
};
// For the time now
Date.prototype.timeNow = function () {
    return ((this.getHours() < 10) ? "0" : "") + this.getHours() + ":" + ((this.getMinutes() < 10) ? "0" : "") + this.getMinutes() + ":" + ((this.getSeconds() < 10) ? "0" : "") + this.getSeconds();
};

function currentDatetime() {
    var newDate = new Date();
    return newDate.today() + " " + newDate.timeNow();
}

function getByNumber(num) {
    //debugger;
    return new Array(num);
}

(function ($) {
    var methods = {
        init: function (options) {
            var settings = $.extend(true, {}, $.fn.autoFit.defaults, options);
            var $this = $(this);

            $this.keydown(methods.fit);

            methods.fit.call(this, null);

            return $this;
        },

        fit: function (event) {
            var $this = $(this);

            var val = $this.val().replace(' ', '-');
            var fontSize = $this.css('font-size');
            var padding = $this.outerWidth() - $this.width();
            var contentWidth = $('<span style="font-size: ' + fontSize + '; padding: 0 ' + padding / 2 + 'px; display: inline-block; position: absolute; visibility: hidden;">' + val + '</span>').insertAfter($this).outerWidth();

            $this.width((contentWidth + padding) + 'px');

            return $this;
        }
    };

    $.fn.autoFit = function (options) {
        if (typeof options == 'string' && methods[options] && typeof methods[options] === 'function') {
            return methods[options].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof options === 'object' || !options) {
            // Default to 'init'
            return this.each(function (i, element) {
                methods.init.apply(this, [options]);
            });
        } else {
            $.error('Method ' + options + ' does not exist on jquery.auto-fit.');
            return null;
        }
    };

    $.fn.autoFit.defaults = {};

})(this['jQuery']);

function PrintElem(elem, json, data) {

    Popup($(elem).html(), json, data);
}

function isJson(str) {

    try {
        JSON.parse(str);
    } catch (e) {
        return false;
    }
    return true;
}


// function OpenPopupForPrintBarcode(imageBase46) {
//     var mywindow = window.open('', 'print2' + Math.floor((Math.random() * 100) + 1), 'width=750,height=auto');
//
// }

function Popup(data, json, bigArchive) {
    var mywindow = window.open('', 'print2' + Math.floor((Math.random() * 100) + 1), 'width=750,height=auto');
    mywindow.document.write('<html><head><title>print</title>');
    mywindow.document.write('<link rel="stylesheet" href="/static/styles/printable.css" type="text/css" />');
    mywindow.document.write('</head><body >');
    mywindow.document.write(data);
    $('.panel-title', mywindow.document).html($('.lp-inbox-item.active .firstRow h4').html());
    mywindow.document.write('<p style="text-align:left">' + json.id + "-" + json.position_id + '</p>');
    mywindow.document.write('</body></html>');
    mywindow.document.write('<div id="signs"></div></body></html>');
    $(mywindow.document).find(".panel-title").append('<div id="qrcode"></div>');
    $(mywindow.document).find(".lbcheckboxlist").each(function (index, value) {
        var ftext = "";
        $(value).parent().find('input[aria-checked=true]').each(function (index, valueee) {
            if (ftext != "") {
                ftext = ftext + " - ";
            }
            ftext = ftext + $(valueee).parent().text();
        });
        $(value).next().replaceWith(function () {
            return "<div class='selected-options'>" + ftext + "</div>";
        })
    });
    $(mywindow.document).find("textarea").each(function (index, value) {
        var obj = jQuery(value);
        var tmp = obj.val().replace(/[\r\n]/g, "&lt;br /&gt;");
        var newTag = jQuery("<div class='thisistextarea'></div>").html(tmp);
        newTag.addClass("plain-text");
        obj.replaceWith(newTag);
    });
    $(mywindow.document).find(".plain-text").each(function (index, value) {
        $(value).parent().parent().parent().parent().addClass("hasTextArea");
    });
    $(mywindow.document).find("input[type=radio]").each(function (index, value) {
        $(value).parent().parent().parent().parent().parent().parent().addClass("hasRadio");
    });
    $(mywindow.document).find(".hasRadio").each(function (index, value) {
        var result = $($(value).find('input[aria-checked=true]').parent().find('span')[0]).html();
        $(value).find("div > div").css("display", "none");
        $(value).append("<span class='radiolblspan'>" + result + "</span>");
    });
    $(mywindow.document).find(".lbchartPositionselectlist").each(function (index, value) {
        var first_value = $($(value).parent().parent().find('select')[0]).find("option:selected").text();
        var second_value = $($(value).parent().parent().find('select')[1]).find("option:selected").text();
        var lbl = $(value).text();
        $(value).parent().parent().html("<label class='control-label lbnumber'>" + lbl + "</label><div class='selected-options'>" + first_value + " - " + second_value + "</div>");
    });
    $(mywindow.document).find(".lbselectlist").each(function (index, value) {
        var first_value = $($(value).parent().parent().find('select')[0]).find("option:selected").text();
        var lbl = $(value).text();
        $(value).parent().parent().html("<label class='control-label lbnumber'>" + lbl + "</label><div class='selected-options'>" + first_value + "</div>");
    });
    $(mywindow.document).find("input").each(function (index, value) {
        $(value).replaceWith(function () {
            return ("<div class='selected-options'>" + $(value).val() + "</div>")
        });
    });
    $(mywindow.document).find(".lbamflabel").each(function (index, value) {
        $(value).parent().parent().css("display", "none");
    });
    $(mywindow.document).find(".lbamffile").each(function (index, value) {
        $(value).parent().parent().css("width", "100%").addClass("thisIsFullWith");
        $(value).parent().parent().find("img").each(function (index, valueee) {
            $(valueee).parent().css("float", "right");
            $(valueee).parent().css({
                width: "25px",
                height: "30px",
                margin: "3px",
                padding: "3px"
            });
            $(valueee).css({
                width: "23px",
                height: "28px",
                margin: "0",
                padding: "0"
            }).parent().find("br").remove();

        })
    });
    $(mywindow.document).find("table").each(function (index, value) {
        $(value).parent().parent().parent().parent().css("width", "100%").addClass("thisIsFullWith").find("table").each(function (index, value) {
            $(value).css("width", "100%");
        });
        $(value).find("tbody td").each(function (index, vvalue) {
            divValue = $($(vvalue).find("div")[0]).text();
            if (divValue != "") {
                if (isJson($(vvalue).text())) {
                    cellID = $(vvalue).closest("tr").index().toString() + "_" + $(vvalue).index().toString();
                    var jj = JSON.parse($(vvalue).text());
                    $(vvalue).text(jj[cellID]);
                }
            }
        });
    });
    //console.log(json);
    $(mywindow.document).find("h3").html("<img style='display:initial; width:55px' src='" + companyLogo + "'/><br/><span class='header_top'>" + json.bpmnName + "</span> <br/> " + json.curAndPrevSteps.current);
    $(mywindow.document).find("body").append("<div id='sings'></div>");
    for (var i = 0; bigArchive.length > i; i++) {
        var taskName = "<div class='repo_taskName'>" + bigArchive[i].taskName + "</div>";
        var thisPerformerName = "<div class='repo_thisPerformerName'>" + bigArchive[i].thisPerformerName + "</div>";
        var thisPerformerChartName = "<div class='repo_thisPerformerChartName'>" + bigArchive[i].thisPerformerChartName + "</div>";
        var doneDate = "<div class='repo_doneDate'>" + bigArchive[i].doneDate + "</div>";
        $(mywindow.document).find("#signs").append("<div class='signs'>"
            + "<div style='float:right; margin:5px;' id='sing" + i.toString() + "'></div>" +
            taskName +
            thisPerformerName +
            thisPerformerChartName +
            doneDate + "</div>"
        );
        $($(mywindow.document).find('#sing' + i.toString())[0]).qrcode({
            text: bigArchive[i].id,
            width: 75, height: 75
        });
    }
    mywindow.document.close(); // necessary for IE >= 10
    mywindow.focus(); // necessary for IE >= 10
    return true;
}

function PopupLetter(json) {
    //console.log(json);
    var mywindow = window.open('', 'print2' + Math.floor((Math.random() * 100) + 1), 'width=750,height=auto');
    mywindow.document.write('<html><head><title>print</title>');
    mywindow.document.write('<link rel="stylesheet" href="/static/styles/fonts.css" type="text/css" />');
    mywindow.document.write('<link rel="stylesheet" href="/static/styles/printable.css" type="text/css" />');
    mywindow.document.write('</head><body class="letter">');
    mywindow.document.write("<div class='letterTop'>" +
        "<img class='companylogo' src='" + companyLogo + "'/>" +
        '<span  class="number"> شماره نامه : ' + "<img src='" + json.letter.sign.generatedFileAddr + "' />" + // letterNoandDate
        '<br><span>تاریخ : ' + json.LetterShDate + '</span>' +
        '</span>' +
        '</div>');

    if (json.letter.recievers) {
        for (let i = 0; json.letter.recievers.length > i; i++) {
            mywindow.document.write('<div> به : ' + json.letter.recievers[i].profileName + ' ' + json.letter.recievers[i].chartName + ' ' + ' </div>')
        }
    }

    if (json.reciever) {

        if (json.reciever.option) {
            if (json.reciever.option.hamesh) {
                mywindow.document.write('<div class="hamesh">هامش : ' + json.reciever.option.hamesh + ' توسط' + ' (' +
                    json.sender.profileName + ' ' + json.sender.chartName +
                    ')</div>');

            }
        }
    }
    mywindow.document.write('<div class="letterBody">' + json.letter.body + '</div>');
    mywindow.document.write('<div class="senderBody">' + json.letter.creatorPosition.profileName + '<br><span>(' + json.letter.creatorPosition.chartName + ')</span></div>');
    mywindow.document.write('<div class="letterSign" style="float:left; margin:5px;"></div>');

    if (json.hameshHistory) {


        if (json.hameshHistory.length > 0) {
            for (let j = 0; json.hameshHistory.length > j; j++) {


                mywindow.document.write(
                    '<div> هامش :  ' + json.hameshHistory[j].message +
                    ' - مورخه ' + json.hameshHistory[j].dateOf +
                    '  - توسط  ' + json.hameshHistory[j].sender +
                    ' </div>');

            }
        }
    }

    $($(mywindow.document).find('.letterSign')[0]).qrcode({
        text: "http://app.****.ir/qr/1_" + json.id + "/",
        width: 75, height: 75
    });
    mywindow.document.write('</body ></html>');

    mywindow.document.close(); // necessary for IE >= 10
    mywindow.focus(); // necessary for IE >= 10
    return true;
}


function downloadURL(url) {
    if ($('#idown').length) {
        $('#idown').attr('src', url);
    } else {
        $('<iframe>', {id: 'idown', src: url}).hide().appendTo('body');
    }
}


function checkUknownDictionsy() {
    if (UnknowGlobalDicKeys.length != 0) {
        $.ajax({
            url: '/api/v1/translate',
            type: 'post',
            dataType: 'json',
            success: function (data) {
                setTimeout(checkUknownDictionsy, 90000)
            },
            data: {items: UnknowGlobalDicKeys.join("____")}
        })


    } else {
        setTimeout(checkUknownDictionsy, 6000)
    }


}

// checkUknownDictionsy();


function len(arr) {
    return arr.length
}


var horizonalLinePlugin = {
    afterDraw: function (chartInstance) {
        var yScale = chartInstance.scales["y-axis-0"];
        var canvas = chartInstance.chart;
        var ctx = canvas.ctx;
        var index;
        var line;
        var style;

        if (chartInstance.options.horizontalLine) {
            for (index = 0; index < chartInstance.options.horizontalLine.length; index++) {
                line = chartInstance.options.horizontalLine[index];

                if (!line.style) {
                    style = "rgba(169,169,169, .6)";
                } else {
                    style = line.style;
                }

                if (line.y) {
                    yValue = yScale.getPixelForValue(line.y);
                } else {
                    yValue = 0;
                }

                ctx.lineWidth = 1.5;

                if (yValue) {
                    ctx.beginPath();
                    ctx.moveTo(0, yValue);
                    ctx.lineTo(canvas.width, yValue);
                    ctx.strokeStyle = style;
                    ctx.stroke();
                }

                if (line.text) {
                    ctx.fillStyle = style;
                    ctx.fillText(line.text, 0, yValue + ctx.lineWidth);
                }
            }
            return;
        }
        ;
    }
};
// Chart.pluginService.register(horizonalLinePlugin);


if (!window.XMLHttpRequest)
    XMLHttpRequest = function () {
        return new ActiveXObject("Microsoft.XMLHTTP");
    };

function setActiveStyleSheet(title) {
    var i, a, main;
    for (i = 0; (a = document.getElementsByTagName("link")[i]); i++) {
        if (a.getAttribute("rel").indexOf("style") != -1 && a.getAttribute("title")) {
            a.disabled = true;
            if (a.getAttribute("title") == title) a.disabled = false;
        }
    }
}

function changeLanguage(lang) {
    var req = new XMLHttpRequest();
    req.open('get', '/static/bower_components/jalalijscalendar/lang/calendar-' + lang + '.js', true);
    req.onreadystatechange = function () {
        if (req.readyState == 4 && req.status == 200) {
            eval(req.responseText + "\nflatCal.recreate();popupCal.recreate();");
        }
    };
    req.send(null);
}

function changeType(type) {
    document.getElementById('flat_calendar').style.display = type == 'flat' ? 'block' : 'none';
}


function changeDateType(dateType) {
    flatCal.setDateType(dateType);
}


function changeLangNumbers(value) {
    flatCal.setLangNumbers(value);
}

function showWeekNumbers(value) {
    flatCal.setWeekNumbers(value);

}

function showOtherMonths(value) {
    flatCal.setOtherMonths(value);
}

function changeDateFormat(format) {
    flatCal.setDateFormat(format);
}

function changeShowTime(value) {
    flatCal.setShowsTime(value);
}

function setTime24(value) {
    flatCal.setTime24(value);
}


function showDeleteConfirm(Question_msg, Pass_msg, Callback) {
    swal({
        title: "Are you sure?",
        text: "You will not be able to recover this imaginary file!",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Yes, delete it!",
        showLoaderOnConfirm: true,
        closeOnConfirm: false
    }, function () {
        bpmnService.getCurrent(0).then(function (res) {
            $scope.current = res.data;
            if (res.positionDocument == LunchedProcessObj.position_id) {
                LunchedProcessService.hideLunchedProcessArchive(LunchedProcessObj.id).then(function (data) {

                    swal("Deleted!", "Your imaginary file has been deleted.", "success");
                    $scope.lunchedProcessArchiveList();
                });
            } else {
                swal("Permission!", "You're nor be able to delete this process.", "error");

            }
        });
    })
}


// $.cookie("domainName", window.location.hostname);
Cookies.set('domainName', window.location.hostname);

$("body").click(function (e) {
    if ($(e.target).hasClass("demo-header-searchbox")) {
        return
    }
    $("._md-select-menu-container").fadeOut();
});


var publicEditorOptions = {
    language: 'fa',
    toolbar: [
        {
            name: 'document',
            items: ['Source', '-', 'Save', 'NewPage', 'DocProps', 'Preview', 'Print', '-', 'Templates']
        },
        {name: 'clipboard', items: ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
        {name: 'editing', items: ['Find', 'Replace', '-', 'SelectAll', '-', 'SpellChecker', 'Scayt']},
        {
            name: 'forms',
            items: ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                'HiddenField']
        },
        '/',
        {
            name: 'basicstyles',
            items: ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']
        },
        {
            name: 'paragraph',
            items: ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv',
                '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl']
        },
        {name: 'links', items: ['Link', 'Unlink', 'Anchor']},
        {
            name: 'insert',
            items: ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']
        },
        '/',
        {name: 'styles', items: ['Styles', 'Format', 'Font', 'FontSize']},
        {name: 'colors', items: ['TextColor', 'BGColor']},
        {name: 'tools', items: ['Maximize', 'ShowBlocks', '-', 'About']}

    ],
    extraPlugins: 'lineutils,notification,uploadwidget,uploadimage',
    removePlugins: 'sourcearea',
    filebrowserUploadUrl: '/api/v1/file/upload',
    resize_maxHeight: 900,
    height: 600

};


(function (f) {
    f.module("angularTreeview", []).directive("treeModel", function ($compile) {

        return {
            restrict: "A", link: function (b, h, c) {
                var a = c.treeId, g = c.treeModel, e = c.nodeLabel || "label", d = c.nodeChildren || "children",
                    e = '<ul><li data-ng-repeat="node in ' + g + '"><i class="collapsed" data-ng-show="node.' + d + '.length && node.collapsed" data-ng-click="' + a + '.selectNodeHead(node)"></i><i class="expanded" data-ng-show="node.' + d + '.length && !node.collapsed" data-ng-click="' + a + '.selectNodeHead(node)"></i><i class="normal" data-ng-hide="node.' +
                        d + '.length"></i> <span data-ng-class="node.selected" data-ng-click="' + a + '.selectNodeLabel(node)">//node.' + e + '//</span> <button style="font-size:10px;" data-ng-if="(node.selected)&&(node.isEditable)" type="button" class="btn btn-xs btn-danger fa fa-trash" data-ng-click="deleteFolder(node)"></button><button style="font-size:10px;" data-ng-if="(node.selected)&&(node.isEditable)" type="button" class="btn btn-xs btn-info fa fa-pencil" data-ng-click="editFolder(node)"></button><button style="font-size:10px;" data-ng-if="(node.selected)&&(node.isEditable)" type="button" data-ng-click="newFolder(node)" class="btn btn-xs btn-primary fa fa-plus"></button>  <div data-ng-hide="node.collapsed" data-tree-id="' + a + '" data-tree-model="node.' + d + '" data-node-id=' + (c.nodeId || "id") + " data-node-label=" + e + " data-node-children=" + d + "></div></li></ul>";
                a && g && (c.angularTreeview && (b[a] = b[a] || {}, b[a].selectNodeHead = b[a].selectNodeHead || function (a) {
                    a.collapsed = !a.collapsed
                }, b[a].selectNodeLabel = b[a].selectNodeLabel || function (c) {
                    b[a].currentNode && b[a].currentNode.selected &&
                    (b[a].currentNode.selected = void 0);
                    c.selected = "selected";
                    b[a].currentNode = c
                }), h.html('').append($compile(e)(b)))

            }
        }
    })
})(angular);


Date.prototype.timeNow = function () {
    return ((this.getHours() < 10) ? "0" : "") + this.getHours() + ":" + ((this.getMinutes() < 10) ? "0" : "") + this.getMinutes() + ":" + ((this.getSeconds() < 10) ? "0" : "") + this.getSeconds();
};
(function ($) {
    "use strict";

    function getjQueryObject(string) {
        // Make string a vaild jQuery thing
        var jqObj = $("");
        try {
            jqObj = $(string)
                .clone();
        } catch (e) {
            jqObj = $("<span />")
                .html(string);
        }
        return jqObj;
    }

    function printFrame(frameWindow, content, options) {
        // Print the selected window/iframe
        var def = $.Deferred();
        try {
            frameWindow = frameWindow.contentWindow || frameWindow.contentDocument || frameWindow;
            var wdoc = frameWindow.document || frameWindow.contentDocument || frameWindow;
            if (options.doctype) {
                wdoc.write(options.doctype);
            }
            wdoc.write(content);
            wdoc.close();
            setTimeout(function () {
                // Fix for IE : Allow it to render the iframe
                frameWindow.focus();
                try {
                    // Fix for IE11 - printng the whole page instead of the iframe content
                    if (!frameWindow.document.execCommand('print', false, null)) {
                        // document.execCommand returns false if it failed -http://stackoverflow.com/a/21336448/937891
                        frameWindow.print();
                    }
                } catch (e) {
                    frameWindow.print();
                }
                frameWindow.close();
                def.resolve();
            }, options.timeout);
        } catch (err) {
            def.reject(err);
        }
        return def;
    }

    function printContentInIFrame(content, options) {
        var $iframe = $(options.iframe + "");
        var iframeCount = $iframe.length;
        if (iframeCount === 0) {
            // Create a new iFrame if none is given
            $iframe = $('<iframe height="0" width="0" border="0" wmode="Opaque"/>')
                .prependTo('body')
                .css({
                    "position": "absolute",
                    "top": -999,
                    "left": -999
                });
        }
        var frameWindow = $iframe.get(0);
        return printFrame(frameWindow, content, options)
            .done(function () {
                // Success
                setTimeout(function () {
                    // Wait for IE
                    if (iframeCount === 0) {
                        // Destroy the iframe if created here
                        $iframe.remove();
                    }
                }, 100);
            })
            .fail(function (err) {
                // Use the pop-up method if iframe fails for some reason
                console.error("Failed to print from iframe", err);
                printContentInNewWindow(content, options);
            })
            .always(function () {
                try {
                    options.deferred.resolve();
                } catch (err) {
                    console.warn('Error notifying deferred', err);
                }
            });
    }


    function printContentInNewWindow(content, options) {
        // Open a new window and print selected content
        var frameWindow = window.open();
        return printFrame(frameWindow, content, options)
            .always(function () {
                try {
                    options.deferred.resolve();
                } catch (err) {
                    console.warn('Error notifying deferred', err);
                }
            });
    }

    function isNode(o) {
        /* http://stackoverflow.com/a/384380/937891 */
        return !!(typeof Node === "object" ? o instanceof Node : o && typeof o === "object" && typeof o.nodeType === "number" && typeof o.nodeName === "string");
    }

    $.print = $.fn.print = function () {
        // Print a given set of elements
        var options, $this, self = this;
        // ////console.log("Printing", this, arguments);
        if (self instanceof $) {
            // Get the node if it is a jQuery object
            self = self.get(0);
        }
        if (isNode(self)) {
            // If `this` is a HTML element, i.e. for
            // $(selector).print()
            $this = $(self);
            if (arguments.length > 0) {
                options = arguments[0];
            }
        } else {
            if (arguments.length > 0) {
                // $.print(selector,options)
                $this = $(arguments[0]);
                if (isNode($this[0])) {
                    if (arguments.length > 1) {
                        options = arguments[1];
                    }
                } else {
                    // $.print(options)
                    options = arguments[0];
                    $this = $("html");
                }
            } else {
                // $.print()
                $this = $("html");
            }
        }
        // Default options
        var defaults = {
            globalStyles: true,
            mediaPrint: false,
            stylesheet: null,
            noPrintSelector: ".no-print",
            iframe: true,
            append: null,
            prepend: null,
            manuallyCopyFormValues: true,
            deferred: $.Deferred(),
            timeout: 250,
            title: null,
            doctype: '<!doctype html>'
        };
        // Merge with user-options
        options = $.extend({}, defaults, (options || {}));
        var $styles = $("");
        if (options.globalStyles) {
            // Apply the stlyes from the current sheet to the printed page
            $styles = $("style, link, meta, title");
        } else if (options.mediaPrint) {
            // Apply the media-print stylesheet
            $styles = $("link[media=print]");
        }
        if (options.stylesheet) {
            // Add a custom stylesheet if given
            $styles = $.merge($styles, $('<link rel="stylesheet" href="' + options.stylesheet + '">'));
        }
        // Create a copy of the element to print
        var copy = $this.clone();
        // Wrap it in a span to get the HTML markup string
        copy = $("<span/>")
            .append(copy);
        // Remove unwanted elements
        copy.find(options.noPrintSelector)
            .remove();
        // Add in the styles
        copy.append($styles.clone());
        // Update title
        if (options.title) {
            var title = $("title", copy);
            if (title.length === 0) {
                title = $("<title />");
                copy.append(title);
            }
            title.text(options.title);
        }
        // Appedned content
        copy.append(getjQueryObject(options.append));
        // Prepended content
        copy.prepend(getjQueryObject(options.prepend));
        if (options.manuallyCopyFormValues) {
            // Manually copy form values into the HTML for printing user-modified input fields
            // http://stackoverflow.com/a/26707753
            copy.find("input")
                .each(function () {
                    var $field = $(this);
                    if ($field.is("[type='radio']") || $field.is("[type='checkbox']")) {
                        if ($field.prop("checked")) {
                            $field.attr("checked", "checked");
                        }
                    } else {
                        $field.attr("value", $field.val());
                    }
                });
            copy.find("select").each(function () {
                var $field = $(this);
                $field.find(":selected").attr("selected", "selected");
            });
            copy.find("textarea").each(function () {
                // Fix for https://github.com/DoersGuild/jQuery.print/issues/18#issuecomment-96451589
                var $field = $(this);
                $field.text($field.val());
            });
        }
        // Get the HTML markup string
        var content = copy.html();
        // Notify with generated markup & cloned elements - useful for logging, etc
        try {
            options.deferred.notify('generated_markup', content, copy);
        } catch (err) {
            console.warn('Error notifying deferred', err);
        }
        // Destroy the copy
        copy.remove();
        if (options.iframe) {
            // Use an iframe for printing
            try {
                printContentInIFrame(content, options);
            } catch (e) {
                // Use the pop-up method if iframe fails for some reason
                console.error("Failed to print from iframe", e.stack, e.message);
                printContentInNewWindow(content, options);
            }
        } else {
            // Use a new window for printing
            printContentInNewWindow(content, options);
        }
        return this;
    };


    var firebaseConfig = {
        apiKey: "AIzaSyCslK7cJxUGyStpiMNj_uyGaDPAdJbufrE",
        authDomain: "rahsoon-66afd.firebaseapp.com",
        databaseURL: "https://rahsoon-66afd.firebaseio.com",
        projectId: "rahsoon-66afd",
        storageBucket: "rahsoon-66afd.appspot.com",
        messagingSenderId: "731814768196",
        appId: "1:731814768196:web:6d3bfdda9ad31a89db9611"
    };
    firebase.initializeApp(firebaseConfig);
// Add the public key generated from the console here.
    const messaging = firebase.messaging();
    messaging.usePublicVapidKey("BOkMLUdzMSh9r8Tz_HXSy985n4N5s9HcrBdqBGSovFpRUTLpV8lhmupPtCCiQSWx4JK0BPxdtnqt02ex20oDl30");
    makeMsg();
    tokening();


    // console.log("1");


    function tokening() {
        messaging.onTokenRefresh(() => {
            messaging.getToken().then((refreshedToken) => {
                // console.log("11");

                setTokenSentToServer(false);
                sendTokenToServer(refreshedToken);


            }).catch((err) => {
                // console.log('Unable to retrieve refreshed token ', err);
                showToken('Unable to retrieve refreshed token ', err);
            });
        });

    }

    function makeMsg() {
        messaging.onMessage((payload) => {
            // console.log("55");
            if (!(payload.data)) {
                return
            }
            var obj = JSON.parse(payload.data.message);

            var $body = angular.element("#thisisoool");  // 1
            var $scope = $body.scope();        // 2
            $scope.$apply(function () {              // 3
                $scope.showCustomToast(obj.notification);
            });

            // console.log('Message received. ', payload);


        });

    }

    function makeMsgWork() {
        // console.log("2");
        // console.log("3");
        //
        // console.log("4");

        Notification.requestPermission().then((permission) => {
            // console.log("22");
            // console.log(permission);
            if (permission === 'granted') {
                // console.log('Notification permission granted.');
                // TODO(developer): Retrieve an Instance ID token for use with FCM.
                // ...
            } else {
                // console.log('Unable to get permission to notify.');
            }
        }).catch(function (err) {
            // console.log('Service worker registration failed, error:', err);
        });
        // console.log("5");
        messaging.requestPermission().then(function () {
            // console.log("33");

            // console.log('Notification permission granted.');
        });
        // console.log("6");
        messaging.getToken().then((currentToken) => {
            // console.log("44");
            // console.log(currentToken);

            if (currentToken) {

                var dt = {};
                dt['token'] = currentToken;
                dt['dest'] = "web";

                $.ajax({
                    type: "POST",
                    url: "/api/v1/tokens/",
                    data: dt,
                    success: function (data) {


                    },
                    error: function (data) {

                    }
                });


            } else {
                // Show permission request.
                // console.log('No Instance ID token available. Request permission to generate one.');


            }
        }).catch((err) => {
            // console.log('An error occurred while retrieving token. ', err);
        });
        // console.log("7");

    }

    function setTokenSentToServer(sent) {
        // console.log("11");

        window.localStorage.setItem('sentToServer', sent ? '1' : '0');
    }

    function sendTokenToServer(refreshedToken) {
        // console.log("66");
        // console.log(refreshedToken);

        var dt = {};
        dt['token'] = refreshedToken;
        dt['dest'] = "web";

        $.ajax({
            type: "POST",
            url: "/api/v1/tokens/",
            data: dt,
            success: function (data) {


            },
            error: function (data) {

            }
        });
    }


    function deleteToken() {
        // Delete Instance ID token.
        // [START delete_token]
        messaging.getToken().then((currentToken) => {
            messaging.deleteToken(currentToken).then(() => {
                // console.log('Token deleted.');
                setTokenSentToServer(false);
                // [START_EXCLUDE]
                // Once token is deleted update UI.
                resetUI();
                // [END_EXCLUDE]
            }).catch((err) => {
                // console.log('Unable to delete token. ', err);
            });
            // [END delete_token]
        }).catch((err) => {
            // console.log('Error retrieving Instance ID token. ', err);
            showToken('Error retrieving Instance ID token. ', err);
        });
    }


    if ('serviceWorker' in navigator) {
        window.addEventListener('load', function () {


            navigator.serviceWorker.register('./static/firebase-messaging-sw.js').then((registration) => {

                messaging.useServiceWorker(registration);

                makeMsgWork();
                console.log("8");


            }).catch(function (err) {
                // console.log('Service worker registration failed, error:', err);
            });

        })
    }


})(jQuery);


jQuery(document).ready(function ($) {
    $('[data-toggle="tooltip"]').tooltip();

})

var ws4redis = undefined;
var getNotificationType = undefined;

function startWS() {
    // return

    if (!(ws4redis)) {
        ws4redis = WS4Redis({
            // uri: 'ws://localhost:8000/ws/foobar?subscribe-broadcast&publish-broadcast&echo&token='+token,
            uri: ws_protocol + '://' + domainname + '/ws/foobar?subscribe-user&echo&token=' + token,
            receive_message: receiveMessage,
            heartbeat_msg: '#'
        });

        getNotificationType = function (message) {
            let mmm;
            let msg = message.split('___');
            let msg_type = msg[0];
            let msg_content = msg[1];
            let msg_id = msg[2];
            // از باسکول به انبار
            // msg : 1___barcode_id


            if (msg_type === '123121234' || msg_type === '8974532' || msg_type === '643242' || msg_type === '7' || msg_type === '987897866' || msg_type === '32424246') {
                let appElement = document.querySelector('[ng-controller=MaterialBakolToAnbarCtrl]');
                if (appElement) {
                    let apScope = angular.element(appElement).scope();
                    apScope.removeByNotification(msg_content);
                    mmm = msg.length === 2 ? msg[1] : msg[2];
                    apScope.http.get('/api/v1/notify/' + mmm + '/').then(function (data) {
                        apScope.addToAnbarList(data.data.extra.msg_content);
                    })


                }

                let appElement2 = document.querySelector('[ng-controller=MaterialBaskolCtrl]');
                if (appElement2) {
                    let ap2Scope = angular.element(appElement2).scope();
                    mmm = msg.length === 2 ? msg[1] : msg[2];

                    ap2Scope.http.get('/api/v1/notify/' + mmm + '/').then(function (data) {
                        ap2Scope.updateCellWS(data.data.extra.msg_content);
                    })


                }
            }

            if (msg_type === '1') {
                let appElement = document.querySelector('[ng-controller=InboxListCtrl]');
                if (appElement) {
                    let appScope = angular.element(appElement).scope();
                    setTimeout(function () {
                        appScope.GetInboxList();

                    }, 2000)
                }


            }


            let appElement = document.querySelector('[ng-controller=NotifCtrl]');
            if (appElement) {
                let appScope = angular.element(appElement).scope();
                mmm = msg.length === 2 ? msg[1] : msg[2];
                appScope.getNotif(mmm);
                appScope.list();
            }

            let navElement = document.querySelector('#thisisoool');
            if (navElement) {
                let appScope = angular.element(navElement).scope();

                if (appScope) {

                    appScope.GetNotificationCounts();
                }
            }


        }

        function receiveMessage(msg) {
            getNotificationType(msg)
        }
    }

}

// jQuery(document).ready(function ($) {
//
// });

function makeid(length) {
    var result = '';
    var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for (var i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}


function notifyBrowser(msg) {
    // Let's check if the browser supports notifications
    if (!("Notification" in window)) {
        // alert("This browser does not support desktop notification");
    }

    // Let's check if the user is okay to get some notification
    else if (Notification.permission === "granted") {
        // If it's okay let's create a notification
        var notification = new Notification(msg);
    }

        // Otherwise, we need to ask the user for permission
        // Note, Chrome does not implement the permission static property
    // So we have to check for NOT 'denied' instead of 'default'
    else if (Notification.permission !== 'denied') {
        Notification.requestPermission(function (permission) {

            // Whatever the user answers, we make sure we store the information
            if (!('permission' in Notification)) {
                Notification.permission = permission;
            }

            // If the user is okay, let's create a notification
            if (permission === "granted") {
                var notification = new Notification(msg);
            }
        });
    } else {
        // alert(`Permission is ${Notification.permission}`);
    }
}

function update_notif() {
    let appElement = document.querySelector('[ng-controller=NotifCtrl]');
    if (appElement) {
        let appScope = angular.element(appElement).scope();
        appScope.list();
    }


}



