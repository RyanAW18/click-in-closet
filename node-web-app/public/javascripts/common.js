function getData(productID) {
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