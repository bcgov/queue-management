console.log('office.js loaded from api/static/js');

$(document).ready(function() {
    var sb = $("[id$='_sb']"); // Smartboard

    if (sb) {
        sb.on('change', (e) => {
            if (e.val !== "3") { // If NOT nocallonsmartboard
                $("label[for='currently_waiting']").parent().show();
                $("label[for='show_currently_waiting_bottom']").parent().show();    
            } else {
                $("label[for='currently_waiting']").parent().hide();
                $("label[for='show_currently_waiting_bottom']").parent().hide();
            }
        })
    }

    // var appointments_enabled_ind = $("[id$='_appointments_enabled_ind']"); // Appointments Enabled       
    // appointments_enabled_ind.on('change', function (e) {
    //     if(e.val === "0") { // Disabled
    //         console.log('appointments disabled')
    //         $("label[for='office_appointment_message']").parent().hide();
    //     } else { // Enabled
    //         console.log('appointments enabled')
    //         $("label[for='office_appointment_message']").parent().show();
    //     }
    // });    
});

