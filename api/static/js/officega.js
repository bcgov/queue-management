console.log('officega.js loaded from api/static/js');

$(document).ready(function() {
    var sb = $("select[id$='sb'].form-control"); // Smartboard Original Select
    if (sb !== null) {                
        var sb_selection = sb.find(":selected").val();
        if (sb_selection !== "3") { // If NOT nocallonsmartboard
            console.log("smartboard is NOT nocallonsmartboard");
            $("label[for='currently_waiting']").parent().show();
            $("label[for='show_currently_waiting_bottom']").parent().show();    
        } else {
            console.log("smartboard is nocallonsmartboard");
            $("label[for='currently_waiting']").parent().hide();
            $("label[for='show_currently_waiting_bottom']").parent().hide();
        }
        sb.prop("disabled", true);        
    }
});