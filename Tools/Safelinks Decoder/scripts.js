function generate_decode_url() {
    var link = document.getElementById("Safelink").value;
    var url_parts = link.split("?")[1];
    var params = url_parts.split("&");
    var target_url = "Error: couldn't find target URL.";
    var parametersList = document.getElementById("parameters");
    parametersList.innerHTML = "";

    for (var n = 0; n < params.length; n++) {
        var namval = params[n].split("=");
        
        var listItem = document.createElement("li");
        listItem.textContent = "Parameter " + (n + 1) + ": " + namval[0] + " = " + decodeURIComponent(namval[1]);
        parametersList.appendChild(listItem);
        if (namval[0] == "url") target_url = namval[1];
    }
    var decode_url = decodeURIComponent(target_url);
    document.getElementById("target_url").value = decode_url;

    var fanged_url = decode_url.replace(/\./g, "[.]");
    document.getElementById("fanged_url").value = fanged_url;
}