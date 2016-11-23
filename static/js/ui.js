function chkDuplicates(arr,justCheck=true){
	var len = arr.length, tmp = {}, arrtmp = arr.slice(), dupes = [];
	arrtmp.sort();
	while(len--) {
	var val = arrtmp[len];
	if (val) {
	   if (/nul|nan|infini/i.test(String(val))){
	     val = String(val);
	    }
	    if (tmp[JSON.stringify(val)]){
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
		}
	});
}


function run_script() {
	var org = $("#org_file_name").val()
	var com = $("#com_file_name").val()
	var net = $("#net_file_name").val()
	var info = $("#info_file_name").val()
	var redempt = $("#red_file_name").val()
	var date = $("#datepicker").val()
	if ((org || com || net || info) && redempt) {
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
					"&redempt=" + redempt + "&date=" + date,
					headers: {
			            'X-CSRFToken': csrftoken,
			        },
					success: function(msg) {
						if (msg.status === "success") {
							window.location='/filtering/'
						} else {
							alert('Something went wrong!')
						}
						$("#cover").fadeOut(100);
					}
				});
			}
		}
	} else {
		alert("It's required to select at least one zone and redemption file");
	}
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
			window.location='/sending/'
		}
	});
}

function check_offer_status () {
    $("#cover").fadeIn(100);
    var date = $("#datepicker").val();
    $.ajax({
        type: "POST",
        url: "/check_offer_status/",
        data: "date=" + date,
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function(msg){
            $("#cover").fadeOut(100);
            location.reload()
        }
    });
}

function add_zone() {
	var zone = $("#zone_file_name").val();
	$("#cover").fadeIn(100);
	$.ajax({
		type: "POST",
		url: "/add_zone/",
		data: "zone=" + zone,
		headers: {
            'X-CSRFToken': csrftoken,
        },
		success: function(msg) {
			$("#cover").fadeOut(100);
			window.location='/filtering/'
		}
	});
}

function return_from_archive(id) {
    $.ajax({
		type: "POST",
		url: "/return_from_archive/",
		headers: {
            'X-CSRFToken': csrftoken
        },
		data: "id=" + id,
	});
}

function do_deleting() {
	$("#cover").fadeIn(100);
	var date = $("#datepicker").val();
	$.ajax({
		type: "POST",
		url: "/do_deleting/",
		data: "date=" + date,
		headers: {
            'X-CSRFToken': csrftoken,
        },
		success: function(msg) {
			$("#cover").fadeOut(100);
			window.location='/sending/'
		}
	})
}

function load() {
	var date = $("#datepicker").val();
	window.location.href=('/filtering/?date=' + date);
}

function load_send() {
	var date = $("#datepicker").val();
	window.location.href=('/sending/?date=' + date);
}

function load_del() {
	var date = $("#datepicker").val();
	window.location.href=('/deleting/?date=' + date);
}

function load_offers() {
	var date = $("#datepicker").val();
	window.location.href=('/offers/?date=' + date);
}

function blacklist(id) {
	$.ajax({
		type: "POST",
		url: "/blacklist/",
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
