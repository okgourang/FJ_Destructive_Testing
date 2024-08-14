insert into Device (device_id, device_name, vref)
values ('08:D1:F9:E6:FE:5C', 'FJ Destructive Test Device' ,1128);

select * from Device

select * from SampleResult
order by created_at desc

select * from Image
order by created_at desc

Select * from Device

delete from SampleResult


ALTER TABLE SampleResult ADD sample_date_new DATE;

UPDATE SampleResult
SET sample_date_new = 
    CASE
        WHEN LEN(CAST(sample_date AS VARCHAR(8))) = 8 THEN 
            CAST(
                STUFF(
                    STUFF(CAST(sample_date AS VARCHAR(8)), 5, 0, '-'), 
                    8, 0, '-'
                ) AS DATE
            )
        ELSE NULL
    END;

ALTER TABLE SampleResult DROP COLUMN sample_date;

EXEC sp_rename 'SampleResult.sample_date_new', 'sample_date', 'COLUMN';

