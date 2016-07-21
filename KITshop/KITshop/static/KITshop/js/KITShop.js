/* 
    This JavaScript file is used to request the most helpful/most critical review. 
    Note that - due to the Same-Origin-Policy of JavaScript, we cannot directly contact the RESTful 
    product review service. Instead, we have added two view methods to the django service (which has the same origin
    as this script). From there, we directly obtain the transformed XML (i.e. an HTML fragment) which we inject 
    into the DOM tree via the DOM API
*/


function getReview() {

    // check which model is selected
    var options = document.getElementById("reviewSelection");
    var review_tag = options.options[options.selectedIndex].getAttribute('value');
    var product_id = "123";
    console.log('selected review: ' + review_tag);

    var xhttp = new XMLHttpRequest();

    // this will be executed once a HTTP response is received
    xhttp.onreadystatechange = function () {
        if (xhttp.readyState == 4 && xhttp.status == 200) {            
            changeReview(xhttp.responseText);
        }
    };

    xhttp.onerror = function () {
        console.log('Error sending HTTP request');
    };

    // set request method and resource URI
    uri = "/" + review_tag + "/" + product_id;
    console.log('Requesting: ' + uri);
    xhttp.open('GET', uri, true);
    console.log('Sending HTTP request');
    xhttp.send();
}

function changeReview(review_html) {
    // get review DIV 
    var productDetails = document.getElementById('reviewdiv');

    productDetails.innerHTML = review_html

}