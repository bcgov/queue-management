archive_data() function

Name:         archive_data
Owner:        postgres
Schema:       public
Comment:

Archives and deletes records that are older than 2 days from the tables:
- period
- servicereq
- citizen

Arguments:    None
Return Type:  character varying
Language:     plpgsql

Code:

/*  Declare variables  */
declare    max_citizen_id             integer;
declare    min_citizen_id             integer;
declare    count_citizen              integer;
declare    start_citizen_count        integer;
declare    end_citizen_count          integer;
declare    copied_citizen_count       integer;
declare    max_sr_id                  integer;
declare    min_sr_id                  integer;
declare    count_sr                   integer;
declare    start_sr_count             integer;
declare    end_sr_count               integer;
declare    copied_sr_count            integer;
declare    max_period_id              integer;
declare    min_period_id              integer;
declare    count_period               integer;
declare    start_period_count         integer;
declare    end_period_count           integer;
declare    copied_period_count        integer;
declare    exists_citizen_archive     boolean;
declare    exists_sr_archive          boolean;
declare    exists_period_archive      boolean;
declare    exists_archive             boolean;
declare    yes_no_citizen             character varying;
declare    copy_citizen               character varying;
declare    yes_no_sr                  character varying;
declare    copy_sr                    character varying;
declare    yes_no_period              character varying;
declare    copy_period                character varying;
declare    msg_citizen                character varying;
declare    msg_sr                     character varying;
declare    msg_period                 character varying;
declare    return_message             character varying;

/*  Start the function.  */
begin

  /*  See if the archive table exists.  */
  exists_archive          = (SELECT EXISTS (
                              SELECT 1 
                              FROM   pg_tables
                              WHERE  schemaname = 'public'
                              AND    tablename = 'archive'
                             ));

  /*  If the table doesn't exist, create it.  */
  if not exists_archive then
    CREATE TABLE archive (archive_id   serial primary key,
                          table_name   character varying(255) NOT NULL,
                          archive_date timestamptz NOT NULL,
	  					  id_min       integer NOT NULL,
		  				  id_max       integer NOT NULL,
			  	          count        integer NOT NULL
                         );
  end if;
  
  /*  Get the maximum citizen ID from two days ago.  */
  count_citizen  =  (select     count(*)
					 from       citizen
					 where      (start_time::date) <= (now() - INTERVAL '2 DAYS')::date);
  if (count_citizen = 0) THEN
    max_citizen_id = 0;
	min_citizen_id = 0;
  else
    max_citizen_id =  (select     max(citizen_id)
                       from       citizen
                       where      (start_time::date) <= (now() - INTERVAL '2 DAYS')::date);
    min_citizen_id =  (select     min(citizen_id)
	                   from       citizen);
	/*  Recalculate count_citizen, in case new citizens added.     */
	/*  Not needed when archiving citizens older than 2 days ago.  */
	count_citizen  =  (select     count(*)
					   from       citizen
					   where      citizen_id >= min_citizen_id
					   and        citizen_id <= max_citizen_id);			   
  end if;

  /*  See if the citizen archive table exists.  */
  exists_citizen_archive = (SELECT EXISTS (
                              SELECT 1 
                              FROM   pg_tables
                              WHERE  schemaname = 'public'
                              AND    tablename = 'citizen_archive'
                             ));

  /*  Table does not exist.  Create it like the citizen table.  */
  if not exists_citizen_archive THEN
    create table citizen_archive (
      like citizen
    );
  end if;
  
  /*  Get record count before the copy. */
  start_citizen_count = (select count(*) from citizen_archive);
  
  /*  Now table exists.  Append records you want to copy.  */
  INSERT INTO  citizen_archive
  SELECT       *
  FROM         citizen
  WHERE        citizen_id <= max_citizen_id;

  /*  Get record count after the copy. */
  end_citizen_count = (select count(*) from citizen_archive);
  copied_citizen_count = end_citizen_count - start_citizen_count;

  /*  If right number of records copied, all OK. Create message, delete records. */
  if (count_citizen = copied_citizen_count) THEN
    copy_citizen = 'Copy successful.  ';
  else
    copy_citizen = 'Copy NOT successful. ' || copied_citizen_count::text || ' records copied. Expected '
	  || count_citizen::text || '.  ';
  end if;

  /*  Set a citizen message for now.  */
  if (exists_citizen_archive) then yes_no_citizen = 'Yes';
  else yes_no_citizen = 'No';
  end if;
  
  msg_citizen = '==> Citizen Min: ' || min_citizen_id::text
			   || '; Max: ' || max_citizen_id::text
			   || '; Count: ' || count_citizen::text
			   || '; Backup existed: ' || yes_no_citizen || '. '
			   || copy_citizen;

  /*  Get the maximum service request ID for maximum citizen id.  */
  count_sr       =  (select     count(*)
					 from       servicereq
					 where      citizen_id <= max_citizen_id);
  if (count_sr = 0) then
    max_sr_id = 0;
	min_sr_id = 0;
  else
    max_sr_id =       (select     max(sr_id)
                       from       servicereq
                       where      citizen_id <= max_citizen_id);
    min_sr_id =       (select     min(sr_id)
                       from       servicereq);
	/*  Recalculate count_sr, in case new service requests added.  */
	/*  Not needed when archiving data older than 2 days ago.      */
	count_sr       =  (select     count(*)
					   from       servicereq
					   where      sr_id >= min_sr_id
					   and        sr_id <= max_sr_id);			   
  end if;

  /*  See if the sr archive table exists.  */
  exists_sr_archive        = (SELECT EXISTS (
                              SELECT 1 
                              FROM   pg_tables
                              WHERE  schemaname = 'public'
                              AND    tablename = 'servicereq_archive'
                             ));

  /*  Table does not exist.  Create it like the servicereq table.  */
  if not exists_sr_archive THEN
    create table servicereq_archive (
      like servicereq
    );
  end if;

  /*  Get record count before the copy. */
  start_sr_count = (select count(*) from servicereq_archive);
  
  /*  Now table exists.  Append records you want to copy.  */
  INSERT INTO  servicereq_archive
  SELECT       *
  FROM         servicereq
  WHERE        sr_id <= max_sr_id;

  /*  Get record count after the copy. */
  end_sr_count = (select count(*) from servicereq_archive);
  copied_sr_count = end_sr_count - start_sr_count;

  /*  If right number of records copied, all OK.  */
  if (count_sr = copied_sr_count) THEN
    copy_sr = 'Copy successful.  ';
  else
    copy_sr = 'Copy NOT successful. ' || copied_sr_count::text || ' records copied. Expected '
	  || count_sr::text || '.  ';
  end if;

  /*  Set sr return a message for now.  */
  if (exists_sr_archive) then yes_no_sr = 'Yes';
  else yes_no_sr = 'No';
  end if;
  
  msg_sr     = '==> Servicereq Min: ' || min_sr_id::text
			   || '; Max: ' || max_sr_id::text
			   || '; Count: ' || count_sr::text
			   || '; Backup existed: ' || yes_no_sr || '. '
			   || copy_sr;

  /*  Get the maximum period ID for maximum service request id.  */
  count_period   =  (select     count(*)
					 from       period
					 where      sr_id <= max_sr_id);
  if (count_period = 0) then
    max_period_id = 0;
	min_period_id = 0;
  else
    max_period_id =   (select     max(period_id)
                       from       period
                       where      sr_id <= max_sr_id);
    min_period_id =   (select     min(period_id)
                       from       period);
	/*  Recalculate count_period, in case new service requests added.  */
	/*  Not needed when archiving data older than 2 days ago.          */
	count_period   =  (select     count(*)
					   from       period
					   where      period_id >= min_period_id
					   and        period_id <= max_period_id);		   
  end if;

  /*  See if the period archive table exists.  */
  exists_period_archive    = (SELECT EXISTS (
                              SELECT 1 
                              FROM   pg_tables
                              WHERE  schemaname = 'public'
                              AND    tablename = 'period_archive'
                             ));

/*  Table does not exist.  Create it like the servicereq table.  */
  if not exists_period_archive THEN
    create table period_archive (
      like period
    );
  end if;

  /*  Get record count before the copy. */
  start_period_count = (select count(*) from period_archive);

  /*  Now table exists.  Append records you want to copy.  */
  INSERT INTO  period_archive
  SELECT       *
  FROM         period
  WHERE        period_id <= max_period_id;

  /*  Get record count after the copy. */
  end_period_count = (select count(*) from period_archive);
  copied_period_count = end_period_count - start_period_count;

  /*  If right number of records copied, all OK.  */
  if (count_period = copied_period_count) THEN
    copy_period = 'Copy successful.  ';
  else
    copy_period = 'Copy NOT successful. ' || copied_period_count::text || ' records copied. Expected '
	  || count_period::text || '.  ';
  end if;
  
  /*  If all copies were successful, delete records.  */
  if ((count_citizen = copied_citizen_count)
    and (count_sr = copied_sr_count)
	and (count_period = copied_period_count)) THEN
	  delete from period where period_id <= max_period_id;
	  delete from servicereq where sr_id <= max_sr_id;
	  delete from citizen where citizen_id <= max_citizen_id;
  end if;

  /*  Set period return a message for now.  */
  if (exists_period_archive) then yes_no_period = 'Yes';
  else yes_no_period = 'No';
  end if;
  
  msg_period = '==> Period Min: ' || min_period_id::text
			   || '; Max: ' || max_period_id::text
			   || '; Count: ' || count_period::text
			   || '; Backup existed: ' || yes_no_period || '. '
			   || copy_period;

  /*  Update citizen log records. */
  INSERT INTO archive(table_name, archive_date, id_min, id_max, count)
  VALUES ('citizen', now(), min_citizen_id, max_citizen_id, count_citizen);

  /*  Update sr log records. */
  INSERT INTO archive(table_name, archive_date, id_min, id_max, count)
  VALUES ('servicereq', now(), min_sr_id, max_sr_id, count_sr);

  /*  Update period log records. */
  INSERT INTO archive(table_name, archive_date, id_min, id_max, count)
  VALUES ('period', now(), min_period_id, max_period_id, count_period);

  /*  Calculate and return a complete return message.  */
  return_message = msg_citizen || msg_sr || msg_period;

  /*  Return a message that can be sent to Rocket Chat. */
  return '{"projectFriendlyName": "Customer Flow System (Prod)", ' 
         || '"projectName": "Archive Data", '
		 || '"statusCode": "OK", '
         || '"message": "' || return_message || '"}';
end