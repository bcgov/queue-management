$(document).ready(function() {
    // Smartboard
    var sb = $("#sb"); 
    if (sb.val() === "__None" || sb.val() === "3") { // if not selected or nocallonsmartboard
        toggleSmartboardFields(false);
    }
    sb.on('change', (e) => {        
        if (e.val === "__None" || e.val === "3") { // if not selected or nocallonsmartboard
            toggleSmartboardFields(false);     
        } else { // if selected and NOT nocallonsmartboard            
            toggleSmartboardFields(true);
        }
    })

    // Digital Signage
    var digital_signage_message = $("#digital_signage_message");
    if (digital_signage_message.val() === "__None" || digital_signage_message.val() === "0") { // if not selected or disabled
        toggleDigitalSignageFields(false);
    }
    digital_signage_message.on('change', (e) => {
        if (e.val  === "__None" || e.val === "0") { // if not selected or disabled
            toggleDigitalSignageFields(false);
        } else { // if enabled
            toggleDigitalSignageFields(true);
        }
    });

    // Check-In Notifications
    var check_in_notification = $("#check_in_notification");
    if (check_in_notification.val() === "__None" || check_in_notification.val() === "0") { // if not selected or disabled
        toggleCheckInNotificationFields(false);
    }
    check_in_notification.on('change', (e) => { 
        if (e.val === "__None" || e.val === "0") { // if not selected or disabled
            toggleCheckInNotificationFields(false);
        } else { // if enabled
            toggleCheckInNotificationFields(true);
        }
    });
    
    // Appointments Enabled
    var appointments_enabled_ind = $("#appointments_enabled_ind");
    if (appointments_enabled_ind.val() === "0") { // if disabled
        toggleAppointmentFields(false);
        toggleOnlineStatusFields(false);
    }        
    appointments_enabled_ind.on('change', (e) => {        
        if (e.val === "0") { // if disabled            
            toggleAppointmentFields(false);
            toggleOnlineStatusFields(false);
        } else { // if enabled            
            toggleAppointmentFields(true);
        }
    });
    
    // Online Status
    var online_status = $("#online_status");
    if (online_status.val() === "__None" || online_status.val() === "HIDE") { // if not selected or HIDE
        toggleOnlineStatusFields(false);
    }        
    online_status.on('change', (e) => {        
        if (e.val === "__None" || e.val === "HIDE") { // if not selected or HIDE
            toggleOnlineStatusFields(false);
        } else { // if SHOW
            if (appointments_enabled_ind.val() === "0") { // if appointment is disabled, hide Online Status fields still
                toggleOnlineStatusFields(false);
            } else { // if appointment is enabled, show Online Status fields
                toggleOnlineStatusFields(true);
            }            
        }
    });
});

function toggleParentContainer(el, flag) {
    if (flag)
        el.parent().show();
    else
        el.parent().hide();
}

function toggleParentContainers(arr, flag) {
    arr.forEach((el, index) => {  
        toggleParentContainer(el, flag);
    });
}

function toggleSmartboardFields(flag) {
    var arr = [];
    arr.push($("label[for='currently_waiting']"));
    arr.push($("label[for='show_currently_waiting_bottom']"));
    toggleParentContainers(arr, flag);
}

function toggleDigitalSignageFields(flag) {
    var arr = [];
    arr.push($("label[for='digital_signage_message_1']"));
    arr.push($("label[for='digital_signage_message_2']"));
    arr.push($("label[for='digital_signage_message_3']"));
    toggleParentContainers(arr, flag);
}

function toggleCheckInNotificationFields(flag) {
    var arr = [];
    arr.push($("label[for='check_in_reminder_msg']"));
    arr.push($("label[for='automatic_reminder_at']"));
    toggleParentContainers(arr, flag);
}

function toggleAppointmentFields(flag) {
    var arr = [];
    arr.push($("label[for='appointment_duration']"));
    arr.push($("label[for='office_email_paragraph']"));
    arr.push($("label[for='online_status']"));
    toggleParentContainers(arr, flag);
}

function toggleOnlineStatusFields(flag) {
    var arr = [];
    arr.push($("label[for='office_appointment_message']"));
    arr.push($("label[for='latitude']"));
    arr.push($("label[for='longitude']"));
    arr.push($("label[for='civic_address']"));
    arr.push($("label[for='telephone']"));
    arr.push($("label[for='external_map_link']"));
    arr.push($("label[for='appointments_days_limit']"));
    arr.push($("label[for='soonest_appointment']"));
    arr.push($("label[for='max_person_appointment_per_day']"));
    arr.push($("label[for='number_of_dlkt']"));
    arr.push($("label[for='timeslots']"));
    toggleParentContainers(arr, flag);
}