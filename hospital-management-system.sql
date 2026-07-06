CREATE TABLE department (
    dId SERIAL PRIMARY KEY,
    hId REFERENCES hospital (hId),
    name VARCHAR(30),
    score int
);

CREATE Table employee (
    employeeId SERIAL,
    dId int REFERENCES department (dId),
    firstName VARCHAR(50),
    lastName VARCHAR(50),
    nationalCode VARCHAR(10),
    contractType VARCHAR(20),
    hireDate TIMESTAMP,
    accessLevel VARCHAR(50),
    sallary NUMERIC(15, 0)
);

CREATE TABLE OfficeStaff (
    employeeId int REFERENCES employee (employeeId),
    role VARCHAR(30)
);

CREATE TABLE nurse (
    employeeId int REFERENCES employee (employeeId),
    medicalNumber VARCHAR(20),
    grade VARCHAR(30)
);

CREATE TABLE surgeon (
    employeeId int REFERENCES employee (employeeId),
    medicalNumber VARCHAR(20),
    surgicalField VARCHAR(30)
);

CREATE TABLE doctor (
    employeeId int REFERENCES employee (employeeId),
    medicalNumber VARCHAR(20),
    specialization VARCHAR(30),
    visitCost NUMERIC(15, 0)
);

CREATE TABLE specilizationIFields (
    specId int REFERENCES doctor (employeeId),
    name VARCHAR(20)
);

CREATE TABLE surgicalFields (
    surgId int REFERENCES surgeon (employeeId),
    name VARCHAR(20)
);

CREATE TABLE shift (
    shiftId int PRIMARY KEY,
    shiftDate TIMESTAMP, --?????
    startTime TIMESTAMP,
    endTime TIMESTAMP
);

CREATE TABLE employeeShift (
    employeeId int REFERENCES employee (employeeId),
    shiftId int REFERENCES shift (shiftId)
);

CREATE TABLE hospital (
    hId SERIAL PRIMARY KEY,
    name VARCHAR(30),
    city VARCHAR(20),
    province VARCHAR(20),
    street VARCHAR(20) alley VARCHAR(20),
    postalCode VARCHAR(15)
);

CREATE TABLE ICDMCode (
    ICDMId SERIAL PRIMARY KEY,
    ICDId int REFERENCES / /,
    medicineName VARCHAR(20)
);

CREATE TABLE storage (
    storageId SERIAL PRIMARY KEY,
    departId int REFERENCES department (dId),
    medId int REFERENCES ICDMCode (ICDMId),
    name VARCHAR(30),
    type VARCHAR(20),
    enterDate TIMESTAMP,
    exitDate TIMESTAMP,
    cost NUMERIC(15, 0)
);

CREATE TABLE medicineConflict (
    medconfId SERIAL PRIMARY KEY,
    departId int REFERENCES department (dId),
    ICDM1Id int REFERENCES ICDMCode (ICDMId),
    ICDM2Id int REFERENCES ICDMCode (ICDMId)
);

CREATE TABLE room (
    roomId SERIAL PRIMARY KEY,
    dId int REFERENCES department (dId),
    name VARCHAR(20),
    description TEXT
);

CREATE TABLE ICDSCode (
    ICDSId SERIAL PRIMARY KEY,
    SurgeryName VARCHAR(20),
    cost NUMERIC(15, 0)
);

CREATE TABLE surgery (
    surgeryId SERIAL PRIMARY KEY,
    surgeryCode int REFERENCES ICDSCode (ICDSId),
    patientId int REFERENCES / /,
    chiefSurgeonId int REFERENCES / /,
    roomID int REFERENCES room (roomId),
    surgeryDate TIMESTAMP,
    status VARCHAR(20),
    finalReport TEXT
);

CREATE TABLE surgeryTeam (
    surgeryId int REFERENCES surgery (surgeryId),
    surgeonId int REFERENCES surgeon (employeeId)
);

CREATE TABLE bed ( bedId SERIAL PRIMARY KEY, cost NUMERIC(15, 0) );

CREATE TABLE bedInfo (
    biId SERIAL PRIMARY KEY,
    bedId int REFERENCES bed (bedId),
    roomId int REFERENCES room (roomId),
    asgAdmId int REFERENCES / /,
    startTimestamp TIMESTAMP status VARCHAR(20)
);

CREATE TABLE signType (
    sTypeId SERIAL PRIMARY KEY,
    signName VARCHAR(20) --???
);

CREATE TABLE equipment (
    equipId SERIAL PRIMARY KEY,
    sTypeId int REFERENCES signType (sTypeId),
    name VARCHAR(30),
    MACAddress VARCHAR(30),
    description TEXT
);

CREATE TABLE equipInfo (
    eiId SERIAL PRIMARY KEY,
    equipId int REFERENCES equipment (equipId),
    roomId int REFERENCES room (roomId),
    asgAdmId int REFERENCES / /,
    startTimestamp TIMESTAMP,
    status VARCHAR(20)
);

CREATE TABLE warning (
    warnId SERIAL PRIMARY KEY,
    logId int REFERENCES / /,
    importance  VARCHAR(20) ,
    occuredTime TIMESTAMP ,
    checkedStatus VARCHAR(20),
    checkedTime TIMESTAMP
);