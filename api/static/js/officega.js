console.log('officega.js loaded from api/static/js');

$(document).ready(function() {
    // Smartboard
    var sb = $("#sb"); 
    if (sb.val() === "3") { // if nocallonsmartboard
        toggleSmartboardFields(false);
    } else {
        toggleSmartboardFields(true);
    }
    $("select[id='sb'].form-control").prop("disabled", true);

    
    // Digital Signage
    var digital_signage_message = $("#digital_signage_message");
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
    
    // Check-In Notifications
    var check_in_notification = $("#check_in_notification");
    if (check_in_notification.val() === "__None" || check_in_notification.val() === "0") {
        toggleCheckInNotificationFields(false);
    }
    check_in_notification.on('change', function(e) {
        if (e.val === "0") { //if disabled
            toggleCheckInNotificationFields(false);
        } else {
            toggleCheckInNotificationFields(true);
        }
    });

    // Appointments Enabled
    var appointments_enabled_ind = $("#appointments_enabled_ind");
    if (appointments_enabled_ind.val() === "0") {
        toggleAppointmentFields(false);
        toggleOnlineStatusFields(false);
    }        
    appointments_enabled_ind.on('change', function (e) {        
        if (e.val === "0") { // if disabled
            console.log('appointments disabled')
            toggleAppointmentFields(false);
            toggleOnlineStatusFields(false);
        } else { // if enabled
            console.log('appointments enabled')
            toggleAppointmentFields(true);
        }
    });

    // Online Status
    var online_status = $("#online_status"); 
    if (online_status.val() === "__None" || online_status.val() === "HIDE") {
        toggleOnlineStatusFields(false);
    } else {
        toggleOnlineStatusFields(true);
    }
    $("select[id='online_status'].form-control").prop("disabled", true);
    
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

function toggleCheckInNotificationFields(flag) {
    if (flag) {
        $("label[for='check_in_reminder_msg']").parent().show();
        $("label[for='automatic_reminder_at']").parent().show();
    } else {
        $("label[for='check_in_reminder_msg']").parent().hide();
        $("label[for='automatic_reminder_at']").parent().hide();
    }
}

function toggleAppointmentFields(flag) {
    if (flag) {
        $("label[for='appointment_duration']").parent().show();
        $("label[for='office_email_paragraph'").parent().show();
        $("label[for='online_status'").parent().show();
    } else {
        $("label[for='appointment_duration']").parent().hide();
        $("label[for='office_email_paragraph'").parent().hide();
        $("label[for='online_status'").parent().hide();
    }
}

function toggleOnlineStatusFields(flag) {
    if (flag) {
        $("label[for='office_appointment_message']").parent().show();
        $("label[for='civic_address']").parent().show();
        $("label[for='telephone']").parent().show();
        $("label[for='external_map_link']").parent().show();
        $("label[for='appointments_days_limit']").parent().show();
        $("label[for='soonest_appointment']").parent().show();
        $("label[for='max_person_appointment_per_day']").parent().show();
        $("label[for='number_of_dlkt']").parent().show();
    } else {
        $("label[for='office_appointment_message']").parent().hide();
        $("label[for='civic_address']").parent().hide();
        $("label[for='telephone']").parent().hide();
        $("label[for='external_map_link']").parent().hide();
        $("label[for='appointments_days_limit']").parent().hide();
        $("label[for='soonest_appointment']").parent().hide();
        $("label[for='max_person_appointment_per_day']").parent().hide();
        $("label[for='number_of_dlkt']").parent().hide();
    }
}