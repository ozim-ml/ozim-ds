$(document).ready(function() {
    $(".content-section").hide();
    $("#section2").show();

    $("[data-section='#section1']").click(function() {
        $(".content-section").hide();
        $("#section2").show();
    });

    $("[data-section='#section1']").click(function() {
        window.location.href = '/data_selection.html';
    });
    
    $(".section-btn").click(function() {
        $(".content-section").hide();
        var sectionToShow = $(this).data("section");
        $(sectionToShow).show();
    });
});