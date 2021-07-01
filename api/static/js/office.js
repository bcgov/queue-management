console.log('office.js loaded from api/static/js');

$(document).ready(function() {
    // Smartboard
    var sb = $("[id='sb']"); 
    if (sb.val() === "3") { // if nocallonsmartboard
        toggleSmartboardFields(false);
    }
    sb.on('change', function (e) {        
        if (e.val === "3") { // if nocallonsmartboard
            console.log('smartboard value is nocallonsmartboard');
            toggleSmartboardFields(false);     
        } else {            
            console.log('smartboard value is NOT nocallonsmartboard');
            toggleSmartboardFields(true);
        }
    })

    // Appointments Enabled
    var appointments_enabled_ind = $("[id='appointments_enabled_ind']");
    if (appointments_enabled_ind.val() === "0") {
        toggleAppointmentFields(false);
    }        
    appointments_enabled_ind.on('change', function (e) {        
        if (e.val === "0") { // if disabled
            console.log('appointments disabled')
            toggleAppointmentFields(false);
        } else { // if enabled
            console.log('appointments enabled')
            toggleAppointmentFields(true);
        }
    });    

    // Digital Signage
    var digital_signage_message = $("[id='digital_signage_message']");
    if (digital_signage_message.val() === "__None" || digital_signage_message.val() === "0") {
        toggleDigitalSignageFields(false);
    }
    digital_signage_message.on('change', function(e) {
        if (e.val === "0") { // if disabled
            toggleDigitalSignageFields(false);
        } else {
            toggleDigitalSignageFields(true);
        }
    });
});

function toggleSmartboardFields(flag) {
    if (flag) {
        $("label[for='currently_waiting']").parent().show();
        $("label[for='show_currently_waiting_bottom']").parent().show();
    } else {
        $("label[for='currently_waiting']").parent().hide();
        $("label[for='show_currently_waiting_bottom']").parent().hide();
    }
}

function toggleAppointmentFields(flag) {
    if (flag) {
        $("label[for='appointment_duration']").parent().show();
        $("label[for='office_email_paragraph'").parent().show();
    } else {
        $("label[for='appointment_duration']").parent().hide();
        $("label[for='office_email_paragraph'").parent().hide();
    }
}

function toggleDigitalSignageFields(flag) {
    if (flag) {
        $("label[for='digital_signage_message_1']").parent().show();
        $("label[for='digital_signage_message_2']").parent().show();
        $("label[for='digital_signage_message_3']").parent().show();
    } else {
        $("label[for='digital_signage_message_1']").parent().hide();
        $("label[for='digital_signage_message_2']").parent().hide();
        $("label[for='digital_signage_message_3']").parent().hide();
    }
}