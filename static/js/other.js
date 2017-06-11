var csrftoken = getCookie('csrftoken');
//BASE
function confirm () {
    var defer = $.Deferred();
    $('<div>Delete for selected date?</div>').dialog({
            close: function () {
                $(this).dialog('destroy');
            },
            buttons: {
                "Yes": function() {
                    defer.resolve("yes");
                    $( this ).dialog( "close" );
                },
                "No": function() {
                    defer.resolve("no");
                    $( this ).dialog( "close" );
                },
                "Cancel": function() {
                    defer.resolve("cancel");
                    $( this ).dialog( "close" );
                }
            }
        });
    return defer.promise();
}

function save_zone_files() {
    var org = $("#org_file_name").val()
    var com = $("#com_file_name").val()
    var net = $("#net_file_name").val()
    var info = $("#info_file_name").val()

    var us = $("#us_file_name").val()
    var biz = $("#biz_file_name").val()
    var mobi = $("#mobi_file_name").val()

    $.ajax({
        type: "POST",
        url: "/save_zone_files/",
        data: "org=" + org + "&net=" + net +
        "&com=" + com + "&info=" + info +
        "&us=" + us + "&mobi=" + mobi +
        "&biz=" + biz,
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function(msg) {
            if (msg.status === "success") {
                alert('Saved!');
                location.reload();
            } else {
                alert('Something went wrong!');
            }
        },
        error: function(ts) {
            alert(ts.responseText)
        },
        statusCode: {
            400: function() {
              alert('400 status code! user error, reload page');
            },
            404: function() {
              alert('404 error, reload the page');
            },
            403: function() {
              alert('403 error, reload the page');
            },
            500: function() {
              alert('500 status code! server error, reload page');
            },
            502: function() {
                alert('gateway timeout!');
            },
            504: function() {
                alert('gateway timeout!');
            }
        }
    });   
}

function run_script(arg) {
    var redempt = $("#red_file_name").val()
    var redempt2 = $("#red_file_name2").val()
    var redempt3 = $("#red_file_name3").val()
    var date = $("#datepicker").val()
    var len  = date.split("-").length;
    if (redempt && (len === 3)) {
        confirm().then(function (answer) {
            if (answer !== "cancel") {
                $("#cover").fadeIn(100);
                $.ajax({
                    type: "POST",
                    url: "/run_script/",
                    data: "redempt=" + redempt +
                    "&redempt2=" + redempt2 +
                    "&redempt3=" + redempt3 +
                    "&answer=" + answer +
                    "&date=" + date + "&arg=" + arg,
                    headers: {
                        'X-CSRFToken': csrftoken,
                    },
                    success: function(msg) {
                        if (msg.status === "success") {
                            $("#cover").fadeOut(100);
                            window.location='/raw_leads/'
                        } else {
                            $("#cover").fadeOut(100);
                            alert('Something went wrong!')
                        }
                    },
                    error: function(ts) {
                        alert(ts.responseText)
                    },
                    statusCode: {
                        400: function() {
                          alert('400 status code! user error, reload page');
                        },
                        404: function() {
                          alert('404 error, reload the page');
                        },
                        403: function() {
                          alert('403 error, reload the page');
                        },
                        500: function() {
                          alert('500 status code! server error, reload page');
                        },
                        502: function() {
                            alert('gateway timeout!');
                        },
                        504: function() {
                            alert('gateway timeout!');
                        }
                    }
                });
            }
        })
    } else {
        alert("Something is wrong, check entries!");
    }
};

function changeSetting(id, value) {
    $.ajax({
        type: "POST",
        url: "/change_setting/",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: "id=" + id + '&value=' + value,
        error: function(ts) {
            alert(ts.responseText)
        },
    });
};
//SEARCH
function restore_lead(id) {
    var r = confirm("Are you sure that you want to restore this deleted lead?");
    if (r == true) {
        $.ajax({
            type: "POST",
            url: "/restore_lead/",
            data: "id=" + id,
            headers: {
                'X-CSRFToken': csrftoken,
            },
            success: function(msg) {
                $('#forma_za_pretragu').submit();
            },
            error: function(ts) {
                alert(ts.responseText)
            },
        });
    }
}
//SUPERBLACKLISTING
function super_blacklist() {
    var domain = $("#super_blacklist").val()
    $.ajax({
        type: "POST",
        url: "/super_blacklist/",
        data: "domain=" + domain,
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function(msg){
            $("#super_blacklist").val('');
            location.reload();
        },
        error: function(ts) {
            alert(ts.responseText)
        },
    });
}

function regular_blacklist() {
    var email = $("#super_blacklist").val()
    $.ajax({
        type: "POST",
        url: "/regular_blacklist/",
        data: "email=" + email,
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function(msg){
            $("#super_blacklist").val('');
            location.reload();
        },
        error: function(ts) {
            alert(ts.responseText)
        },
    });
}

function remove_from_blacklist(id, type) {
    $.ajax({
        type: "POST",
        url: "/remove_from_blacklist/",
        data: "id=" + id + "&type=" + type,
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function(msg){
            location.reload()
        },
        error: function(ts) {
            alert(ts.responseText)
        },
    });
}
// MAN
function add_manual_whois() {
    $("#cover").fadeIn(100);
    var file = $("#red_file_name").val();
    $.ajax({
        type: "POST",
        url: "/add_manual_whois/",
        data: "file=" + file,
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function(msg){
            alert("it's uploaded");
            $("#cover").fadeOut(100);
        },
        error: function(ts) {
            alert(ts.responseText)
        },
        statusCode: {
            400: function() {
              alert('400 status code! user error, reload page');
            },
            404: function() {
              alert('404 error, reload the page');
            },
            403: function() {
              alert('403 error, reload the page');
            },
            500: function() {
              alert('500 status code! server error, reload page');
            },
            502: function() {
                alert('gateway timeout!');
            },
            504: function() {
                alert('gateway timeout!');
            }
        }
    });
};
// ADMINS PAGE
function load_logs() {
    var date = $("#datepicker").val();
    window.location.href=('/classified/?date=' + date);
};

function confirm_whois () {
    var defer = $.Deferred();
    $('<div>Internal or External?</div>').dialog({
            close: function () {
                $(this).dialog('destroy');
            },
            buttons: {
                "Internal": function() {
                    defer.resolve("internal");
                    $( this ).dialog( "close" );
                },
                "External": function() {
                    defer.resolve("external");
                    $( this ).dialog( "close" );
                },
                "Cancel": function() {
                    defer.resolve("cancel");
                    $( this ).dialog( "close" );
                }
            }
        });
    return defer.promise();
};


function whois_period() {
    confirm_whois().then(function (mode) {
        if (mode !== "cancel") {
            var interval = $("#whois_period").val();
            if (!interval) {
                interval = 5;
            }

            $("#cover").fadeIn(100);
            $.ajax({
                type: "POST",
                url: "/whois_period/",
                data: "interval=" + interval + "&mode=" + mode,
                headers: {
                    'X-CSRFToken': csrftoken,
                },
                success: function(msg){
                    $("#cover").fadeOut(100);
                    alert("Done!");
                },
                error: function(ts) {
                    alert(ts.responseText)
                },
                statusCode: {
                    400: function() {
                      alert('400 status code! user error, reload page');
                    },
                    404: function() {
                      alert('404 error, reload the page');
                    },
                    403: function() {
                      alert('403 error, reload the page');
                    },
                    500: function() {
                      alert('500 status code! server error, reload page');
                    },
                    502: function() {
                        alert('gateway timeout!');
                    },
                    504: function() {
                        alert('gateway timeout!');
                    }
                }
            });

        }
    })
};

function whois_he_net() {
    $("#cover").fadeIn(100);
    $.ajax({
        type: "POST",
        url: "/whois_he_net/",
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function(msg){
            $("#cover").fadeOut(100);
            alert("Whois will start soon!");
            location.reload();
        },
        error: function(ts) {
            alert(ts.responseText)
        },
        statusCode: {
            400: function() {
              alert('400 status code! user error, reload page');
            },
            404: function() {
              alert('404 error, reload the page');
            },
            403: function() {
              alert('403 error, reload the page');
            },
            500: function() {
              alert('500 status code! server error, reload page');
            },
            502: function() {
                alert('gateway timeout!');
            },
            504: function() {
                alert('gateway timeout!');
            }
        }
    });
}

function remove_unwanted() {
    $("#cover").fadeIn(100);
    $.ajax({
        type: "POST",
        url: "/remove_unwanted/",
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function(msg){
            alert('It\'s cleared!');
            $("#cover").fadeOut(100);
        },
        error: function(ts) {
            alert(ts.responseText)
        },
    });
};

function delete_exception(id) {
    $.ajax({
        type: "POST",
        url: "/delete_exception/",
        data: "id=" + id,
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function(msg){
            location.reload()
        },
        error: function(ts) {
            alert(ts.responseText)
        },
    });
};

function delete_tld(id) {
    $.ajax({
        type: "POST",
        url: "/delete_tld/",
        data: "id=" + id,
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function(msg){
            location.reload()
        },
        error: function(ts) {
            alert(ts.responseText)
        },
    });
};

function add_exception() {
    var name = $('#name_exception').val();
    $.ajax({
        type: "POST",
        url: "/add_exception/",
        data: "name=" + name,
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function(msg){
            location.reload();
        },
        error: function(ts) {
            alert(ts.responseText)
        },
    });
};

function add_tld() {
    var name = $('#name_tld').val();
    $.ajax({
        type: "POST",
        url: "/add_tld/",
        data: "name=" + name,
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function(msg) {
            location.reload();
        },
        error: function(ts) {
            alert(ts.responseText)
        },
    });
}
