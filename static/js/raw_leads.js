var csrftoken = getCookie('csrftoken');
var lastChecked = null;

function load() {
    var list_no = $("#filter_by_list_no").val();
    var date = $("#datepicker").val();
    window.location.href=('/raw_leads/?date=' + date + '&pages=1&list_no=' + list_no);
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
            },
            error: function(ts) {
                alert(ts.responseText)
            },
        });
    } else {
        alert('Incorrect password');
    }
};

function show (i) {
    var date = $("#datepicker").val();
    window.location.href=('/raw_leads/?date=' + date + '&pages=' + i);
};

function filter_by_list_no() {
    var list_no = $("#filter_by_list_no").val();
    var date = $("#datepicker").val();
    window.location.href=('/raw_leads/?date=' + date + '&pages=1&list_no=' + list_no);
}

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
        error: function(ts) {
            alert(ts.responseText)
        },
        statusCode: {
            200: function() {
                $("#cover").fadeOut(100);
                window.location.href=('/raw_leads/?date=' + date);
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
            success: function (msg) {
                var count = $(":checkbox:checked").length;
                $("#counter").html(count);
            },
            error: function(ts) {
                alert(ts.responseText)
            },
        });
    } else {
        $.ajax({
            type: "POST",
            url: "/reverse_state/",
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: "id=" + id,
            success: function (msg) {
                var count = $(":checkbox:checked").length;
                $("#counter").html(count);
            },
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
            var count = $(":checkbox:checked").length;
            $("#counter").html(count);
        },
        error: function(ts) {
            alert(ts.responseText)
        },
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
            var count = $(":checkbox:checked").length;
            $("#counter").html(count);
        },
        error: function(ts) {
            alert(ts.responseText)
        },
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
        error: function(ts) {
            alert(ts.responseText)
        },
        statusCode: {
            200: function() {
                $("#cover").fadeOut(100);
                window.location='/active_leads/'
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
};
