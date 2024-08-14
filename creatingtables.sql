-- Create the Device table
CREATE TABLE Device (
    device_id VARCHAR(50) NOT NULL,
    device_name VARCHAR(50) NOT NULL,
    vref INT NOT NULL
	CONSTRAINT PK_Device PRIMARY KEY (device_id)
);

-- Create the SampleResult table
CREATE TABLE SampleResult (
    test_id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    device_id VARCHAR(50) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT GETDATE(),
    operator_first_name VARCHAR(50) NULL,
    project_id VARCHAR(50) NULL,
    panel_id VARCHAR(50) NULL,
    shift_id VARCHAR(50) NULL,
    sample_date INT NULL,
    sample_time INT NULL,
    specie VARCHAR(50) NULL,
    grade VARCHAR(50) NULL,
    dimension VARCHAR(50) NULL,
    mc_right INT NULL,
    mc_left INT NULL,
    max_psi_reading FLOAT NULL,
    max_load_reading FLOAT NULL,
    wood_failure_mode INT NULL,
    min_ft_psi FLOAT NULL,
    fifth_ft_psi FLOAT NULL,
    min_uts_lbs FLOAT NULL,
    fifth_uts_lbs FLOAT NULL,
    adhesive_application VARCHAR(50) NULL,
    squeeze_out VARCHAR(50) NULL,
    adhesive_batch_test_result VARCHAR(50) NULL,
    finished_joint_appearance VARCHAR(50) NULL,
    positioning_alignment VARCHAR(50) NULL,
    test_result VARCHAR(50) NULL,
	CONSTRAINT PK_SampleResult PRIMARY KEY (test_id),
    CONSTRAINT FK_SampleResult_Device FOREIGN KEY (device_id) 
        REFERENCES Device(device_id)
);

-- Create the Image table
CREATE TABLE Image (
    image_id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    test_id UNIQUEIDENTIFIER NOT NULL,
	created_at DATETIME NOT NULL DEFAULT GETDATE(),
    filename VARCHAR(MAX) NOT NULL,
    filepath VARCHAR(MAX) NOT NULL,
	CONSTRAINT PK_Image PRIMARY KEY (image_id),
    CONSTRAINT FK_Image_SampleResult FOREIGN KEY (test_id) 
        REFERENCES SampleResult(test_id)
);
