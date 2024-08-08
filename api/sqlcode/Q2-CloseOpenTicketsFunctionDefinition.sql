close_open_tickets() function

Name:         close_open_tickets
Owner:        postgres
Schema:       public
Comment:

This procedure deletes any open tickets defined as:
(1) A ticket which has a period with a null ending time
(2) A service request which does not have a status of complete
(3) A citizen who has a status of Active

Arguments:    None
Return Type:  character varying
Language:     plpgsql

Code:

/*  Declare variables  */

declare     return_message     character varying;
declare     date_utc           timestamptz;
declare     date_van           timestamptz;
declare     var_time_start     time;
declare     var_time_end       time;
declare     var_time_van       time;
declare     time_string_van    character varying;
declare     time_string_start  character varying;
declare     time_string_end    character varying;
declare     rows_affected      integer;
declare     update_citizen     integer;
declare     update_active      integer;
declare     update_period      integer;
declare     update_sr          integer;
declare     id_got_services    bigint;

/*  Start the function  */
begin

  /*  Get the current time in Vancouver timezone */
  date_utc = current_timestamp;
  date_van = timezone('America/Vancouver', date_utc);
  var_time_van = date_van::time;

  /*  Set the start and end times where closing tickets is not allowed */
  var_time_start = to_timestamp('07:00:00', 'HH24:MI.SS')::time;
  var_time_end = to_timestamp('17:30:00', 'HH24:MI.SS')::time;

  /*  Turn times into strings, for messages  */
  time_string_van = to_char(var_time_van, 'HH24:MI');
  time_string_start = to_char(var_time_start, 'HH24:MI');
  time_string_end = to_char(var_time_end, 'HH24:MI');
  
  /*  If you are before start time, or after end time, you can close tickets */
  if (var_time_van < var_time_start or var_time_van > var_time_end) then
  
    /*  Get the id for a citizen state of 'Received Services'. */
	id_got_services = (select cs_id from citizenstate where cs_state_name = 'Received Services');
  
    /*  Set inaccurate time, clear comments for citizens where time_end of a period is null */
    /*  Set inaccurate time flag, clear comments for citizens, where service request is not complete.  */
    /*  NOTE!!  Need double subquery to get around MySQL limitation about updates in subqueries */
    update      citizen
    set         cs_id = id_got_services,
	            accurate_time_ind = 0,
	    		citizen_comments = ''
    where   office_id in (select office_id from office where optout_status = 0) and citizen.citizen_id in
    (
      select    distinct f.cid
      from
      (
        select  c2.citizen_id cid
        from    period p,
	  	        citizen c2,
                servicereq sr
        where   p.time_end is null
        and     p.sr_id = sr.sr_id
        and     c2.citizen_id = sr.citizen_id
		union
        SELECT   c.citizen_id cid
        FROM     servicereq sr,
                 srstate srs,
                 citizen c
        where    sr.sr_state_id = srs.sr_state_id
        and      c.citizen_id = sr.citizen_id
        and      sr_code != 'Complete'
      ) f
    );
    get diagnostics update_citizen = ROW_COUNT;

    /*  Set all citizen's state to be received services, inaccurate time, */
    /*  clear comments for citizens still active.                         */
    update        citizen
    set           cs_id = id_got_services,
                  accurate_time_ind = 0,
                  citizen_comments = ''
    where         cs_id = (select cs_id from citizenstate where cs_state_name = 'Active') and office_id in (select office_id from office where optout_status = 0);
    get diagnostics update_active = ROW_COUNT;

    /*  Set period time_end to be now for all periods with null ending time. */
  
    UPDATE period
    SET time_end = NOW()
    WHERE time_end IS NULL
    AND sr_id IN (
        SELECT sr_id
        FROM servicereq
        WHERE citizen_id IN (
            SELECT citizen_id
            FROM citizen
            WHERE office_id in (select office_id from office where optout_status = 0)
        ));
    get diagnostics update_period = ROW_COUNT;

    /*  Set all service requests to be complete, for those that aren't marked as complete. */
    update        servicereq
    set           sr_state_id = (select sr_state_id from srstate where sr_code = 'Complete')
    where         sr_state_id != (select sr_state_id from srstate where sr_code = 'Complete') and
                  citizen_id in (
                  SELECT citizen_id
                  FROM citizen
                  WHERE office_id  in (select office_id from office where optout_status = 0));

    get diagnostics update_sr = ROW_COUNT;

    return_message = 'Tickets closed first pass: ' || update_citizen::text
	              || ', Tickets closed second pass: ' || update_active::text
                  || ', Closed Service Requests: ' || update_sr::text
  	              || ', Closed Periods: ' || update_period::text;

/*  You are trying to close tickets during office hours.  Display a message. */
  else
    return_message = 'Please close tickets after hours, before ' || time_string_start
	                 || ' or after ' || time_string_end || '. Time is now ' || time_string_van;
  end if;
  
  /*
  '{ "projectFriendlyName": "Close Open Tickets","projectName": "COT", "statusCode": "INFO", "message": "Hi"}'
  */
  /*  Return the message in the format that Rocket Chat webhook wants it. */
  /*
  return '{"text": "' || return_message || '"}';
  */
  return '{"projectFriendlyName": "Customer Flow System (Prod)", ' 
         || '"projectName": "Close Open Tickets", '
		 || '"statusCode": "OK", '
         || '"message": "' || return_message || '"}';
  
end