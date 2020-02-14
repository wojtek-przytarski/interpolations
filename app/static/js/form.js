var params_f = document.getElementById('params_f');
var params_a = document.getElementById('params_a');
var params_b = document.getElementById('params_b');
var params_n = document.getElementById('params_n');

function sendData() {
    window.open('/?f=' + encodeURIComponent(params_f.value) + '&a=' + params_a.value +
        '&b=' + params_b.value + '&n=' + params_n.value, "_self");
}