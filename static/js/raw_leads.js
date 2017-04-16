var csrftoken = getCookie('csrftoken');
var lastChecked = null;

function load() {
    var date = $("#datepicker").val();
    window.location.href=('/raw_leads/?date=' + date);
};

function truncate_raw() {
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
            data: "date=" + date + "&activated=0",
            success: function (msg) {
                $("#cover").fadeOut(100);
                alert("It's Done!");
                window.location.href=('/raw_leads/?date=' + date);
            }
        });
    } else {
        alert('Incorrect password');
    }
};

function show (i) {
    var date = $("#datepicker").val();
    window.location.href=('/raw_leads/?date=' + date + '&page=' + i);
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

function find_active() {
    var date = $("#datepicker").val();
    $("#cover").fadeIn(100);
    $.ajax({
        type: "POST",
        url: "/find_active/",
        data: "date=" + date,
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function(msg){
            $("#cover").fadeOut(100);
            window.location.href=('/raw_leads/?date=' + date);
        },
        statusCode: {
            400: function() {
              alert('400 status code! user error, reload page');
            },
            500: function() {
              alert('500 status code! server error, reload page');
            }
        }
    });
};

function changestate(id, e) {
    var $chkboxes = $(':checkbox');

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
            url: "/reverse_state/",
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: {'ids': JSON.stringify(ids), 'foo': lastChecked.checked},
        });
    } else {
        $.ajax({
            type: "POST",
            url: "/reverse_state/",
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: "id=" + id,
        });
    }
    lastChecked = e.target;
};

function add_this_name(name_redemption, page) {
    var date = $("#datepicker").val(), i;
    var ids = [];
    var items = document.getElementsByClassName("r_" + name_redemption + page);

    for (i = 0; i < items.length; i += 1) {
        ids.push(items[i].id);
    };

    $.ajax({
        type: "POST",
        url: "/add_this_name/",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: {
            'ids': JSON.stringify(ids),
            'redemption': name_redemption,
            'page': page,
            'date': date,
        },
        success: function (msg) {
        	for (i = 0; i < items.length; i += 1) {
    			items[i].checked = true;
        	}
        }
    });
};

function rem_this_name(name_redemption, page) {
    var date = $("#datepicker").val(), i;
    var ids = [];
    var items = document.getElementsByClassName("r_" + name_redemption + page);

    for (i = 0; i < items.length; i += 1) {
        ids.push(items[i].id);
    };

    $.ajax({
        type: "POST",
        url: "/rem_this_name/",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: {
            'ids': JSON.stringify(ids),
            'redemption': name_redemption,
            'page': page,
            'date': date,
        },
        success: function (msg) {
            for (i = 0; i < items.length; i += 1) {
                items[i].checked = false;
            }
        }
    });
};

function find_mails() {
    $("#cover").fadeIn(100);
    var date = $("#datepicker").val();
    $.ajax({
        type: "POST",
        url: "/find_mails/",
        data: "date=" + date + "&submit=1",
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function(msg){
            $("#cover").fadeOut(100);
            window.location='/active_leads/'
        },
        statusCode: {
            400: function() {
              alert('400 status code! user error, reload page');
            },
            500: function() {
              alert('500 status code! server error, reload page');
            }
        }
    });
};