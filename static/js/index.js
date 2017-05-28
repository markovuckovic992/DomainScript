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
