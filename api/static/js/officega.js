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