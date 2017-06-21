var csrftoken = getCookie('csrftoken');
var lastChecked = null;

function load_send() {
    var date = $("#datepicker").val();
    window.location.href=('/active_leads/?date=' + date);
};

function load_send2() {
    var date = $("#datepicker").val();
    window.location.href=('/active_leads_tld/?date=' + date);
};

function Confirm () {
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

function find_mails_again() {
    Confirm().then(function (mode) {
        if (mode !== "cancel") {
            $("#cover").fadeIn(100);
            var date = $("#datepicker").val();
            $.ajax({
                type: "POST",
                url: "/find_mails/",
                data: "date=" + date + "&mode=" + mode,
                headers: {
                    'X-CSRFToken': csrftoken
                },
                success: function(msg){
                    $("#cover").fadeOut(100);
                    location.reload();
                },
                error: function(ts) {
                    location.reload();
                },
                statusCode: {
                    200: function() {
                        $("#cover").fadeOut(100);
                        location.reload();
                    },
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

function select_all(activated) {
    var date = $("#datepicker").val()
    $.ajax({
        type: "POST",
        url: "/mark_to_send/",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: "date=" + date + "&activated=" + activated,
        success: function(msg){
            $('input:checkbox.prim').prop('checked', true);
        },
        error: function(ts) {
            alert(ts.responseText)
        },
    });
};

function un_select_all(activated) {
    var date = $("#datepicker").val()
    $.ajax({
        type: "POST",
        url: "/un_mark_to_send/",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: "date=" + date + "&activated=" + activated,
        success: function(msg){
            $('input:checkbox.prim').prop('checked', false);
        },
        error: function(ts) {
            alert(ts.responseText)
        },
    });
};

function blacklist_selected() {
    var date = $("#datepicker").val()
    $.ajax({
        type: "POST",
        url: "/blacklist_selected/",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: "date=" + date,
        success: function (msg) {
            $(':checkbox.blacklist').each(function() {
                this.checked = false;
            });
            location.reload()
        },
        error: function(ts) {
            alert(ts.responseText)
        },
    });
};

function filter_by_dom() {
    var rows = $('#mytable tbody tr');
    var temp = $('#filter_by_dom').val().toLowerCase();
    var n, text;
    rows.show().filter(function() {
        text = $(this).find('td.redemption').text().toLowerCase();
        n = text.indexOf(temp);
        return n === -1;
    }).hide();
};

function add_multiple() {
    var dict = [];
    $("input[type='text'].email_entries").each(function(index, elem) {
        if($(elem).val()) {
            dict.push({
                id:   $(elem).attr('id').replace('mail_entry_', ''),
                value: $(elem).val()
            });
        }
    });
    if(dict.length) {
        $.ajax({
            type: "POST",
            url: "/add_multiple/",
            data: {'dict': JSON.stringify(dict)},
            headers: {
                'X-CSRFToken': csrftoken,
            },
            success: function(msg){
                window.location.reload()
            },
            error: function(ts) {
                alert(ts.responseText)
            },
        });
    }
};

function truncate_active() {
    var passwd = prompt("Enter Password : ", "your password here");
    if (passwd == 2011) {
        $("#cover").fadeIn(100);
        var date = $("#datepicker").val();
        $.ajax({
            type: "POST",
            url: "/truncate/",
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: "date=" + date + "&activated=1",
            success: function (msg) {
                $("#cover").fadeOut(100);
                alert("It's Done!");
                window.location.href=('/active_leads/?date=' + date);
            },
            error: function(ts) {
                alert(ts.responseText)
            },
        });
    } else {
        alert('Incorrect password');
    }
};

function send_pending(argument) {
    var passwd = prompt("Enter Password : ", "your password here");
    if (passwd == 2011) {
        $("#cover").fadeIn(100);
        $.ajax({
        type: "POST",
        url: "/send_pending/",
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function(msg){
            $("#cover").fadeOut(100);
            window.location.reload();
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
        },
        error: function(ts) {
            $("#cover").fadeOut(100);
            // alert(ts.responseText)
        },
    });
    } else {
        alert('Incorrect password');
    }
};

function mark_to_send(id, e, activated) {
    var $chkboxes = $(':checkbox.prim');

    if(e.shiftKey) {
        var start = $chkboxes.index(e.target);
        var end = $chkboxes.index(lastChecked);
        var checks = $chkboxes.slice(Math.min(start,end), Math.max(start,end)+ 1)
        checks.prop('checked', lastChecked.checked);
        var ids = [];
        for (var i = 0; i < checks.length; i += 1) {
            ids.push($(checks[i]).attr('id'))
        }
        $.ajax({
            type: "POST",
            url: "/mark_to_send/",
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: {'ids': JSON.stringify(ids), 'foo': lastChecked.checked, 'activated': activated},
            error: function(ts) {
                alert(ts.responseText)
            },
        });
    } else {
        $.ajax({
            type: "POST",
            url: "/mark_to_send/",
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: "id=" + id + "&activated=" + activated,
            error: function(ts) {
                alert(ts.responseText)
            },
        });
    }
    lastChecked = e.target;
};

function rem_mail(id, name_zone) {
    var zone = "'" + name_zone + "'"
    var html = 'email not found <input type="text" class="email_entries" id="mail_entry_' + id + '"/><button onclick="add_mail_man(' + id + ', ' + zone + ')">Add</button>';
    $.ajax({
        type: "POST",
        url: "/rem_mail/",
        data: "id=" + id,
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function(msg){
            for (i = 0; i < msg.ids.length; i += 1) {
                $("#mail_field_" + msg.ids[i]).html(html + '<a href="http://bgp.he.net/dns/' + name_zone + '#_whois" target="_blank">bgd.he.net</a>'
);
            }
        },
        error: function(ts) {
            alert(ts.responseText)
        },
    });
};

function add_mail_man(id, name_zone) {
    var email = $("#mail_entry_" + id).val(), i;
    var zone = "'" + name_zone + "'"
    var html = email + '<button onclick="rem_mail(' + id + ', ' + zone + ')">Rewrite</button>'
    $.ajax({
        type: "POST",
        url: "/add_mail_man/",
        data: "id=" + id + "&email=" + email,
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function(msg) {
            for (i = 0; i < msg.ids.length; i += 1) {
                $("#mail_field_" + msg.ids[i]).html(html);
            }
        },
        error: function(ts) {
            alert(ts.responseText)
        },
    });
};

function active_manual_hash(id, number, hash) {
    var r = confirm("Are you sure that you want to generate hash for entry number: " + number);
    var link = 'http://www.webdomainexpert.pw/offer/?id='
    if (r == true) {
        $.ajax({
            type: "POST",
            url: "/active_manual/",
            data: "id=" + id,
            headers: {
                'X-CSRFToken': csrftoken,
            },
            success: function(msg) {
                var person = prompt("Your link is:", link + hash);
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
            },
            error: function(ts) {
                alert(ts.responseText)
            },
        });
    }
};

function blacklist(id) {
    var date = $("#datepicker").val();
    $.ajax({
        type: "POST",
        url: "/blacklist/",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: "id=" + id + "&date=" + date,
        success: function (msg) {
            for (i = 0; i < msg.ids.length; i += 1) {
                $("#blacklist_" + msg.ids[i]).prop('checked', msg.command);
            }
        },
        error: function(ts) {
            alert(ts.responseText);
        },
    });
};

function to_delete(id, e) {
    var $chkboxes = $(':checkbox.delete__');
    if(e.shiftKey) {
        var start = $chkboxes.index(e.target);
        var end = $chkboxes.index(lastChecked);
        var checks = $chkboxes.slice(Math.min(start,end), Math.max(start,end)+ 1)
        checks.prop('checked', lastChecked.checked);
        var ids = [];
        for (var i = 0; i < checks.length; i += 1) {
            ids.push($(checks[i]).attr('id').replace('_del', ''))
        }
        $.ajax({
            type: "POST",
            url: "/delete/",
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: {'ids': JSON.stringify(ids), 'foo': lastChecked.checked},
            error: function(ts) {
                alert(ts.responseText)
            },
        });
    } else {
        $.ajax({
            type: "POST",
            url: "/delete/",
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: "id=" + id,
            error: function(ts) {
                alert(ts.responseText)
            },
        });
    }
    lastChecked = e.target;
};

function send_mails() {
    $("#cover").fadeIn(100);
    var date = $("#datepicker").val()
    $.ajax({
        type: "POST",
        url: "/send_mails/",
        data: "date=" + date,
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function(msg) {
            $("#cover").fadeOut(100);
            location.reload();
            $('input:checkbox').removeAttr('checked');
        },
        error: function(ts) {
            // alert(ts.responseText);
            $("#cover").fadeOut(100);
        },
        statusCode: {
            200: function() {
                $("#cover").fadeOut(100);
                location.reload();
                $('input:checkbox').removeAttr('checked');
            },
            400: function() {
                alert('400 status code! user error, reload page');
                $("#cover").fadeOut(100);
            },
            404: function() {
              alert('404 error, reload the page');
              $("#cover").fadeOut(100);
            },
            403: function() {
              alert('403 error, reload the page');
              $("#cover").fadeOut(100);
            },
            500: function() {
              alert('500 status code! server error, reload page');
              $("#cover").fadeOut(100);
            },
            502: function() {
                alert('gateway timeout!');
                $("#cover").fadeOut(100);
            },
            504: function() {
                alert('gateway timeout!');
                $("#cover").fadeOut(100);
            }
        }
    });
};

function whois_he_net() {
    var date = $("#datepicker").val();
    $("#cover").fadeIn(100);
    $.ajax({
        type: "POST",
        url: "/whois_he_net/",
        headers: {
            'X-CSRFToken': csrftoken,
        },
        data: "date=" + date,
        success: function(msg){
            $("#cover").fadeOut(100);
            alert("Whois will start soon!");
            location.reload();
        },
        error: function(ts) {
            $("#cover").fadeOut(100);
            // alert(ts.responseText)
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
