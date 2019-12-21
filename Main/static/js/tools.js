$("#tool-res").click(function () {
    window.location.href = "http://localhost/tools/resistance";
});

$("#tool-res-p").click(function () {
    window.location.href = "http://localhost/tools/resistance-par";
});

$("#tool-cap").click(function () {
    window.location.href = "http://localhost/tools/capacitance";
});

$("#tool-cap-p").click(function () {
    window.location.href = "http://localhost/tools/capacitance-par";
});


$("#tool-color").click(function () {
    window.location.href = "http://localhost/tools/resistance-by-color";
});

$("#calc-res").click(function () {
    let mega = $("#mega").val().split(" ");
    let kilo = $("#kilo").val().split(" ");
    let one = $("#one").val().split(" ");
    let milli = $("#milli").val().split(" ");
    let sum = 0;
    if (!isNaN(parseInt(mega[0]))) {
        jQuery.each(mega, function (index, value) {
            sum += parseInt(value) * 1000000;
        });
    }
    if (!isNaN(parseInt(kilo[0]))) {
        jQuery.each(kilo, function (index, value) {
            sum += parseInt(value) * 1000;
        });
    }
    if (!isNaN(parseInt(one[0]))) {
        jQuery.each(one, function (index, value) {
            sum += parseInt(value);
        });
    }
    if (!isNaN(parseInt(milli[0]))) {
        jQuery.each(milli, function (index, value) {
            sum += parseInt(value) * 0.001;
        });
    }
    $("#result-text").text(sum);
});

$("#calc-res-p").click(function () {
    let mega = $("#mega").val().split(" ");
    let kilo = $("#kilo").val().split(" ");
    let one = $("#one").val().split(" ");
    let milli = $("#milli").val().split(" ");
    let sum = 0;
    if (!isNaN(parseInt(mega[0]))) {
        jQuery.each(mega, function (index, value) {
            sum += 1 / (parseInt(value) * 1000000);
        });
    }
    if (!isNaN(parseInt(kilo[0]))) {
        jQuery.each(kilo, function (index, value) {
            sum += 1 / (parseInt(value) * 1000);
        });
    }
    if (!isNaN(parseInt(one[0]))) {
        jQuery.each(one, function (index, value) {
            sum += 1 / (parseInt(value));
        });
    }
    if (!isNaN(parseInt(milli[0]))) {
        jQuery.each(milli, function (index, value) {
            sum += 1 / (parseInt(value) * 0.001);
        });
    }
    $("#result-text").text(1 / sum);
});

$("#calc-cap").click(function () {
    let one = $("#one").val().split(" ");
    let milli = $("#milli").val().split(" ");
    let micro = $("#micro").val().split(" ");
    let nano = $("#nano").val().split(" ");
    let pico = $("#pico").val().split(" ");
    let sum = 0;
    if (!isNaN(parseInt(one[0]))) {
        jQuery.each(one, function (index, value) {
            sum += 1 / (parseInt(value));
        });
    }
    if (!isNaN(parseInt(milli[0]))) {
        jQuery.each(milli, function (index, value) {
            sum += 1 / (parseInt(value) * 0.001);
        });
    }
    if (!isNaN(parseInt(micro[0]))) {
        jQuery.each(micro, function (index, value) {
            sum += 1 / (parseInt(value) * 0.000001);
        });
    }
    if (!isNaN(parseInt(nano[0]))) {
        jQuery.each(nano, function (index, value) {
            sum += 1 / (parseInt(value) * 0.000000001);
        });
    }
    if (!isNaN(parseInt(pico[0]))) {
        jQuery.each(pico, function (index, value) {
            sum += 1 / (parseInt(value) * 0.000000000001);
        });
    }
    $("#result-text").text(1 / sum);
});

$("#calc-cap-p").click(function () {
    let one = $("#one").val().split(" ");
    let milli = $("#milli").val().split(" ");
    let micro = $("#micro").val().split(" ");
    let nano = $("#nano").val().split(" ");
    let pico = $("#pico").val().split(" ");
    let sum = 0;
    if (!isNaN(parseInt(one[0]))) {
        jQuery.each(one, function (index, value) {
            sum += parseInt(value);
        });
    }
    if (!isNaN(parseInt(milli[0]))) {
        jQuery.each(milli, function (index, value) {
            sum += parseInt(value) * 0.001;
        });
    }
    if (!isNaN(parseInt(micro[0]))) {
        jQuery.each(micro, function (index, value) {
            sum += parseInt(value) * 0.000001;
        });
    }
    if (!isNaN(parseInt(nano[0]))) {
        jQuery.each(nano, function (index, value) {
            sum += parseInt(value) * 0.000000001;
        });
    }
    if (!isNaN(parseInt(pico[0]))) {
        jQuery.each(pico, function (index, value) {
            sum += parseInt(value) * 0.000000000001;
        });
    }
    $("#result-text").text(sum);
});

$(".select-color").click(function () {
    let color = $("option:selected", this).attr("style");
    $(this).attr("style", color);
});

$("#calc-res-c").click(function () {
    let sum = 0.0;
    sum += parseFloat($("#c1").val()) * 10;
    sum += parseFloat($("#c2").val());
    sum *= parseFloat($("#c3").val());
    let tol = sum * parseFloat($("#c4").val());
    $("#result-text").text(sum + " ± " + tol + " Ом");
});
