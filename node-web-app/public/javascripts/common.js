function getProductData(productID) {
    var xmlhttp = new XMLHttpRequest();
    var url = "/product/" + productID + "/data";
    xmlhttp.onreadystatechange = function() {
      if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
      }
    };
    xmlhttp.open("GET", url, false);
    xmlhttp.send();
    return JSON.parse(xmlhttp.responseText);
}

function getUserData(email) {
    var xmlhttp = new XMLHttpRequest();
    var url = "/" + email + "/data";
    xmlhttp.onreadystatechange = function() {
      if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
      }
    };
    xmlhttp.open("GET", url, false);
    xmlhttp.send();
    return JSON.parse(xmlhttp.responseText);
}

function getSearchData(productID) {
    var xmlhttp = new XMLHttpRequest();
    var url = "/search/" + query + "/data";
    xmlhttp.onreadystatechange = function() {
      if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
      }
    };
    xmlhttp.open("GET", url, false);
    xmlhttp.send();
    return xmlhttp.responseText;
}

function getQueryVariable(index) {
  var query = window.location.href;
  var vars = query.split("/");
  return vars[vars.length - index];
}

function search() {
    var query = document.getElementById("search_bar").value
    console.log(query)
    window.location.href="/search/" + query
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length,c.length);
        }
    }
    return "";
}
