function document_onLoad() {
    var captcha_img = document.getElementsByClassName("captcha")[0];
    captcha_img.onclick = refreshCaptcha;
    captcha_img.style.cursor = "pointer"
}

function refreshCaptcha() {
    var xmlHttp = new XMLHttpRequest();
    if (xmlHttp == null) {
        console.log("xmlHttp is null. What's wrong?");
        return;
    }
    xmlHttp.open("GET", "/captcha/refresh/");
    xmlHttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xmlHttp.send(null);
    xmlHttp.onreadystatechange = function () {
        if ((xmlHttp.readyState == 4) && (xmlHttp.status == 200)) {
            var respJson = eval('(' + xmlHttp.responseText + ')');
            var captcha_img = document.getElementsByClassName("captcha")[0];
            var captcha_input_id_0 = document.getElementById("id_captcha_0");
            captcha_img.src = respJson['image_url'];
            captcha_input_id_0.value = respJson['key'];
        }
    }
}

window.onload = document_onLoad;
