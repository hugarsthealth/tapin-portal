CREATE TABLE IF NOT EXISTS patients(
    patient_id INTEGER PRIMARY KEY,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    nhi TEXT NOT NULL,
    occupation TEXT,
    citizen_resident BOOL,
    contact_num TEXT,
    gender TEXT NOT NULL,
    dob DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS vitalinfos(
    vital_info_id INTEGER PRIMARY KEY ASC,
    patient_id INTEGER NOT NULL,
    weight INTEGER,
    weight_units TEXT,
    height INTEGER,
    height_units TEXT,
    check_in_time DATETIME,
    drinker BOOL,
    smoker BOOL,
    blood_type TEXT,
    overseas_recently BOOL,
    overseas_dests TEXT,
    medical_conditions TEXT,
    allergies TEXT,
    family_hist TEXT,

    FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
);
