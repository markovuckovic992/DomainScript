//COMMON
function chkDuplicates(arr,justCheck=true) {
    var len = arr.length, tmp = {}, arrtmp = arr.slice(), dupes = [];
    arrtmp.sort();
    while(len--) {
    var val = arrtmp[len];
    if (val) {
       if (/nul|nan|infini/i.test(String(val))){
         val = String(val);
        }
        if (tmp[JSON.stringify(val)]) {
           if (justCheck) {return true;}
           dupes.push(val);
        }
        tmp[JSON.stringify(val)] = true;
      }
    }
    return justCheck ? false : dupes.length ? dupes : null;
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = $.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
//BASE
function run_script(arg) {
    var org = $("#org_file_name").val()
    var com = $("#com_file_name").val()
    var net = $("#net_file_name").val()
    var info = $("#info_file_name").val()
    var redempt = $("#red_file_name").val()
    var date = $("#datepicker").val()
    var len  = date.split("-").length;
    console.log(len);
    if (org && com && net && info && redempt && (len === 3)) {
        if (chkDuplicates([org, net, com, info, redempt])) {
            alert("You have selected some domain list twice");
        } else {
            var r = confirm("Everything for selected date will be deleted");
            if (r == true) {
                $("#cover").fadeIn(100);
                $.ajax({
                    type: "POST",
                    url: "/run_script/",
                    data: "org=" + org + "&net=" + net +
                    "&com=" + com + "&info=" + info +
                    "&redempt=" + redempt + "&date=" + date + "&arg=" + arg,
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
                    statusCode: {
                        400: function() {
                          alert('400 status code! user error, reload page');
                        },
                        500: function() {
                          alert('500 status code! server error, reload page');
                        },
                        502: function() {
                            alert('gateway timeout!')
                        },
                        504: function() {
                            alert('gateway timeout!')
                        }
                    }
                });
            }
        }
    } else {
        alert("Something is wrong, check entries!");
    }
}
//RAW LEADS
function changestate(id) {
    $.ajax({
        type: "POST",
        url: "/reverse_state/",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: "id=" + id,
    });
}

function load() {
    var date = $("#datepicker").val();
    window.location.href=('/raw_leads/?date=' + date);
}

function show (i) {
    var date = $("#datepicker").val();
    window.location.href=('/raw_leads/?date=' + date + '&page=' + i);           
}


function find_mails() {
    $("#cover").fadeIn(100);
    var date = $("#datepicker").val();
    $.ajax({
        type: "POST",
        url: "/find_mails/",
        data: "date=" + date,
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
}

function find_mails_again() {
    $("#cover").fadeIn(100);
    var date = $("#datepicker").val();
    $.ajax({
        type: "POST",
        url: "/find_mails/",
        data: "date=" + date,
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function(msg){
            $("#cover").fadeOut(100);
            location.reload();
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
}

function truncate() {
    var passwd = prompt("Enter Password : ", "your password here");
    if (passwd == 2011) {
        var date = $("#datepicker").val();
        $.ajax({
            type: "POST",
            url: "/truncate/",
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: "date=" + date,
            success: function (msg) {
                alert("It's Done!")
                window.location.href=('/raw_leads/?date=' + date);
            }
        });
    } else {
        alert('Incorrect password');
    }
}

function add_this_name(name_redemption, page) {
    var date = $("#datepicker").val(), i;
    var items = document.getElementsByClassName("r_" + name_redemption);
    $.ajax({
        type: "POST",
        url: "/add_this_name/",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: "redemption=" + name_redemption + "&page=" + page + "&date=" + date,
        success: function (msg) {
        	for (i = 0; i < items.length; i += 1) {
    			items[i].checked = true;
        	}	
        }
    });
}

function rem_this_name(name_redemption, page) {
    var date = $("#datepicker").val(), i;
    var items = document.getElementsByClassName("r_" + name_redemption);
    $.ajax({
        type: "POST",
        url: "/rem_this_name/",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: "redemption=" + name_redemption + "&page=" + page + "&date=" + date,
        success: function (msg) {
            for (i = 0; i < items.length; i += 1) {
                items[i].checked = false;
            }   
        }
    });
}
//ACTIVE LEADS
function load_send() {
    var date = $("#datepicker").val();
    window.location.href=('/active_leads/?date=' + date);
}

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
        }
    });
}

function blacklist_selected() {
    $.ajax({
        type: "POST",
        url: "/blacklist_selected/",
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function (msg) { 
            $(':checkbox.blacklist').each(function() {
                this.checked = false;                        
            });           
            location.reload()  
        }
    });
}

function to_delete(id) {
    $.ajax({
        type: "POST",
        url: "/delete/",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: "id=" + id,
    });
}

function mark_to_send(id) {
    $.ajax({
        type: "POST",
        url: "/mark_to_send/",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: "id=" + id,
    });
}

function select_all() {
    var date = $("#datepicker").val()
    $.ajax({
        type: "POST",
        url: "/mark_to_send/",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: "date=" + date,
        success: function(msg){
            $('input:checkbox.prim').prop('checked', true);
        }
    });
}

function un_select_all() {
    var date = $("#datepicker").val()
    $.ajax({
        type: "POST",
        url: "/un_mark_to_send/",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: "date=" + date,
        success: function(msg){
            $('input:checkbox.prim').prop('checked', false);
        }
    });
}

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
        success: function(msg){
            $("#cover").fadeOut(100);
            location.reload();
            $('input:checkbox').removeAttr('checked');
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
}

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
        success: function(msg){
            for (i = 0; i < msg.ids.length; i += 1) {
                $("#mail_field_" + msg.ids[i]).html(html);
            }
        }
    });
}

function rem_mail(id, name_zone) {
    var zone = "'" + name_zone + "'"
    var html = 'email not found <input type="text" id="mail_entry_' + id + '"/><button onclick="add_mail_man(' + id + ', ' + zone + ')">Add</button>';
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
        }
    });
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
        }
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
        }
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
        }
    });
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
}

// MAN

function search_manual() {
    var zone = $('#manual_input_zone').val();
    var rede = $('#manual_input_redem').val();
    var date = $("#datepicker").val();
    $.ajax({
        type: "POST",
        url: "/search_manual/",
        data: "zone=" + zone + "&rede=" + rede + "&date=" + date,
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function(msg){
            if (msg.hash) {
                $('#search_manual').hide()
                $('#add_manual').show()
                $('#hash_man').show()

                $('#hash_man').html('hash: ' + msg.hash)
            } else {
                alert("Can't find match for inputs!")
            }
        }
    });

}

function add_manual() {
    var hash = $('#hash_man').html().replace('hash: ', '');
    var zone = $('#manual_input_zone').val();
    var rede = $('#manual_input_redem').val();
    var date = $("#datepicker").val();
    var email = $("#manual_input_email").val();
    if (hash && zone && rede && date && email) {
        $.ajax({
            type: "POST",
            url: "/add_manual/",
            data: "zone=" + zone + "&rede=" + rede + "&date=" + date + "&hash=" + hash + "&email=" + email,
            headers: {
                'X-CSRFToken': csrftoken,
            },
            success: function(msg){
                if (msg.link) {
                    $('#add_manual').hide()
                    $('#reload').show()
                    $('#hash_man_link').show()

                    $('#hash_man_link').html('link: ' + msg.link)
                } else {
                    alert("Can't find match for inputs!")
                }
            }
        });
    } else {
        console.log(hash, zone, rede, date, email)
        alert('Some data is missing!');
    }

}