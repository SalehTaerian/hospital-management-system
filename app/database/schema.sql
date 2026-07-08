CREATE TABLE patient (
    pID SERIAL PRIMARY KEY,
    firstName VARCHAR(35) NOT NULL,
    lastName VARCHAR(35) NOT NULL,
    nationalCode VARCHAR(10) UNIQUE NOT NULL,
    password VARCHAR(30) NOT NULL,
    gender VARCHAR(6),
    dateOfBirth DATE,
    phoneNumber VARCHAR(13),
    homeNumber VARCHAR(13),
    city VARCHAR(15),
    province VARCHAR(15),
    street VARCHAR(100),
    alley VARCHAR(100),
    houseCode VARCHAR(10),
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE medicalRecord (
    mID SERIAL PRIMARY KEY,
    pID INTEGER NOT NULL REFERENCES patient(pID) ON DELETE CASCADE,
    bloodType VARCHAR(5),
    smokingHistory VARCHAR(50)
);


CREATE TABLE insurance (
    insuranceID SERIAL PRIMARY KEY,
    pID INTEGER NOT NULL REFERENCES patient(pID) ON DELETE CASCADE,
    name VARCHAR(35) NOT NULL,
    coveragePercentage DECIMAL(4,2),
    policyNumber VARCHAR(20) UNIQUE,
    startDate DATE,
    endDate DATE,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE hospital (
    hospitalID SERIAL PRIMARY KEY,
    name VARCHAR(30),
    city VARCHAR(20),
    province VARCHAR(20),
    street VARCHAR(20),
    alley VARCHAR(20),
    postalCode VARCHAR(15)
);


CREATE TABLE department (
    departID SERIAL PRIMARY KEY,
    hospitalID INTEGER NOT NULL REFERENCES hospital (hospitalID) ON DELETE CASCADE,
    name VARCHAR(30),
    score INTEGER
);


CREATE Table employee (
    employeeID SERIAL PRIMARY KEY,
    departID INTEGER NOT NULL REFERENCES department (departID) ON DELETE CASCADE,
    firstName VARCHAR(50),
    lastName VARCHAR(50),
    nationalCode VARCHAR(10) UNIQUE NOT NULL,
    password VARCHAR(30) NOT NULL,
    contractType VARCHAR(20),
    hireDate TIMESTAMP,
    accessLevel VARCHAR(50),
    salary NUMERIC(15, 0)
);


CREATE TABLE officeStaff (
    employeeID INTEGER NOT NULL PRIMARY KEY REFERENCES employee (employeeID) ON DELETE CASCADE,
    role VARCHAR(30)
);


CREATE TABLE nurse (
    employeeID INTEGER NOT NULL PRIMARY KEY REFERENCES employee (employeeID) ON DELETE CASCADE,
    medicalNumber VARCHAR(20),
    grade VARCHAR(30)
);


CREATE TABLE surgeon (
    employeeID INTEGER NOT NULL PRIMARY KEY REFERENCES employee (employeeID) ON DELETE CASCADE,
    medicalNumber VARCHAR(20),
    surgicalField VARCHAR(30)
);


CREATE TABLE doctor (
    employeeID INTEGER NOT NULL PRIMARY KEY REFERENCES employee (employeeID) ON DELETE CASCADE,
    medicalNumber VARCHAR(20),
    specialization VARCHAR(30),
    visitCost NUMERIC(15, 0)
);


CREATE TABLE specializationFields (
    specID INTEGER NOT NULL REFERENCES doctor (employeeID) ON DELETE CASCADE,
    name VARCHAR(20)
);


CREATE TABLE surgicalFields (
    surgID INTEGER NOT NULL REFERENCES surgeon (employeeID) ON DELETE CASCADE,
    name VARCHAR(20)
);


CREATE TABLE shift (
    shiftID SERIAL PRIMARY KEY,
    shiftDate TIMESTAMP, --?????
    startTime TIMESTAMP,
    endTime TIMESTAMP
);


CREATE TABLE employeeShift (
    employeeID INTEGER NOT NULL REFERENCES employee (employeeID) ON DELETE CASCADE,
    shiftID INT NOT NULL REFERENCES shift (shiftID) ON DELETE CASCADE
);


CREATE TABLE admission (
    admID SERIAL PRIMARY KEY,
    mID INTEGER NOT NULL REFERENCES medicalRecord(mID) ON DELETE CASCADE,
    doctorID INTEGER NOT NULL REFERENCES doctor(employeeID) ON DELETE CASCADE,
    officeStaffID INTEGER NOT NULL REFERENCES officeStaff(employeeID) ON DELETE CASCADE,
    cost NUMERIC(15, 0)
);


CREATE TABLE parameterList (
    parameterID SERIAL PRIMARY KEY,
    parameterName VARCHAR(25),
    min DECIMAL(10,5),
    max DECIMAL(10,5),
    average DECIMAL(10,5)
);


CREATE TABLE icdCode (
    icdID SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    diseaseName VARCHAR(50) NOT NULL
);


CREATE TABLE icdmCode (
    icdmID SERIAL PRIMARY KEY,
    icdID INTEGER NOT NULL REFERENCES icdCode(icdID) ON DELETE CASCADE,
    medicineName VARCHAR(20) NOT NULL
);


CREATE TABLE icdsCode (
    icdsID SERIAL PRIMARY KEY,
    surgeryName VARCHAR(20),
    cost NUMERIC(15, 0)
);

CREATE TABLE icdtCode (
    icdtID SERIAL PRIMARY KEY,
    testName VARCHAR(50),
    cost NUMERIC(15, 0)
);


CREATE TABLE storage (
    storageID SERIAL PRIMARY KEY,
    departID INTEGER NOT NULL REFERENCES department (departID) ON DELETE CASCADE,
    medID INTEGER NOT NULL REFERENCES icdmCode (icdmID) ON DELETE CASCADE,
    name VARCHAR(30),
    type VARCHAR(20),
    enterDate TIMESTAMP,
    exitDate TIMESTAMP,
    cost NUMERIC(15, 0)
);

CREATE TABLE medicineConflict (
    medconfID SERIAL PRIMARY KEY,
    departID INTEGER NOT NULL REFERENCES department (departID) ON DELETE CASCADE,
    icdm1ID INTEGER NOT NULL REFERENCES icdmCode (icdmID) ON DELETE CASCADE,
    icdm2ID INTEGER NOT NULL REFERENCES icdmCode (icdmID) ON DELETE CASCADE
);

CREATE TABLE room (
    roomID SERIAL PRIMARY KEY,
    departID INTEGER NOT NULL REFERENCES department (departID) ON DELETE CASCADE,
    name VARCHAR(20),
    description TEXT
);


CREATE TABLE surgery (
    surgeryID SERIAL PRIMARY KEY,
    surgeryCode INTEGER NOT NULL REFERENCES icdsCode (icdsID) ON DELETE CASCADE,
    pID INTEGER NOT NULL REFERENCES patient(pID) ON DELETE CASCADE,
    chiefSurgeonId INTEGER NOT NULL REFERENCES surgeon(employeeID) ON DELETE CASCADE,
    roomID INTEGER NOT NULL REFERENCES room (roomID),
    surgeryDate TIMESTAMP,
    status VARCHAR(20),
    finalReport TEXT
);

CREATE TABLE surgeryTeam (
    surgeryID INTEGER NOT NULL REFERENCES surgery (surgeryID) ON DELETE CASCADE,
    surgeonID INTEGER NOT NULL REFERENCES surgeon (employeeID) ON DELETE CASCADE
);

CREATE TABLE bed ( 
    bedID SERIAL PRIMARY KEY,
    cost NUMERIC(15, 0) 
);

CREATE TABLE bedInfo (
    biID SERIAL PRIMARY KEY,
    bedID INTEGER NOT NULL REFERENCES bed (bedID) ON DELETE CASCADE,
    roomID INTEGER NOT NULL REFERENCES room (roomID) ON DELETE CASCADE,
    asgAdmID INTEGER REFERENCES admission (admID) ON DELETE CASCADE,
    startTimestamp TIMESTAMP,
    status VARCHAR(20)
);

CREATE TABLE transfer (
    transferID SERIAL PRIMARY KEY,
    admID INTEGER NOT NULL REFERENCES admission(admID) ON DELETE CASCADE,
    destBedID INTEGER NOT NULL REFERENCES bed(bedID) ON DELETE CASCADE,
    transferedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cost NUMERIC(15, 0)
);


CREATE TABLE signType (
    sTypeID SERIAL PRIMARY KEY,
    signName VARCHAR(20) --???
);

CREATE TABLE equipment (
    equipID SERIAL PRIMARY KEY,
    sTypeID INTEGER NOT NULL REFERENCES signType (sTypeID) ON DELETE CASCADE,
    name VARCHAR(30),
    MACAddress VARCHAR(30),
    description TEXT
);

CREATE TABLE equipInfo (
    eiID SERIAL PRIMARY KEY,
    equipID INTEGER NOT NULL REFERENCES equipment (equipID) ON DELETE CASCADE,
    roomID INTEGER NOT NULL REFERENCES room (roomID) ON DELETE CASCADE,
    asgAdmID INTEGER NOT NULL REFERENCES admission(admID) ON DELETE CASCADE,
    startTimestamp TIMESTAMP,
    status VARCHAR(20)
);

CREATE TABLE log (
    logID SERIAL PRIMARY KEY,
    equipID INTEGER NOT NULL REFERENCES equipment(equipID) ON DELETE CASCADE,
    parameterID INTEGER NOT NULL REFERENCES parameterList(parameterID) ON DELETE CASCADE,
    asgAdmID INTEGER NOT NULL REFERENCES admission(admID) ON DELETE CASCADE,
    parameterValue DECIMAL(10,5),
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE warning (
    warnID SERIAL PRIMARY KEY,
    logID INTEGER NOT NULL REFERENCES log(logID) ON DELETE CASCADE,
    importance  VARCHAR(20) ,
    occuredTime TIMESTAMP ,
    checkedStatus VARCHAR(20),
    checkedTime TIMESTAMP
);


CREATE TABLE appointment (
    appoID SERIAL PRIMARY KEY,
    mID INTEGER NOT NULL REFERENCES medicalRecord(mID) ON DELETE CASCADE,
    doctorID INTEGER NOT NULL REFERENCES doctor(employeeID),
    date DATE NOT NULL,
    time TIME NOT NULL,
    status VARCHAR(20),
    isOnlineReserved BOOLEAN,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE medicineDiag (
    appoID INTEGER NOT NULL REFERENCES appointment(appoID) ON DELETE CASCADE,
    icdmID INTEGER NOT NULL REFERENCES icdmCode(icdmID) ON DELETE CASCADE,
    description TEXT
);


CREATE TABLE diseaseDiag (
    appoID INTEGER NOT NULL REFERENCES appointment(appoID) ON DELETE CASCADE,
    icdID INTEGER NOT NULL REFERENCES icdCode(icdID) ON DELETE CASCADE,
    description TEXT
);


CREATE TABLE vitalSign (
    vitalID SERIAL PRIMARY KEY,
    appoID INTEGER NOT NULL REFERENCES appointment(appoID) ON DELETE CASCADE,
    parameterID INTEGER NOT NULL REFERENCES parameterList(parameterID) ON DELETE CASCADE,
    parameterValue DECIMAL(10,5)
);


CREATE TABLE diseaseRecord (
    diseaseID SERIAL PRIMARY KEY,
    mID INTEGER NOT NULL REFERENCES medicalRecord(mID) ON DELETE CASCADE,
    icdID INTEGER NOT NULL REFERENCES icdCode(icdID) ON DELETE CASCADE,
    description TEXT
);


CREATE TABLE drugRecord (
    drugID SERIAL PRIMARY KEY,
    mID INTEGER NOT NULL REFERENCES medicalRecord(mID) ON DELETE CASCADE,
    description TEXT
);


CREATE TABLE medicineRecord (
    medicineID SERIAL PRIMARY KEY,
    mID INTEGER NOT NULL REFERENCES medicalRecord(mID) ON DELETE CASCADE,
    icdmID INTEGER NOT NULL REFERENCES icdmCode(icdmID) ON DELETE CASCADE,
    description TEXT
);


CREATE TABLE request (
    reqID SERIAL PRIMARY KEY,
    mID INTEGER NOT NULL REFERENCES medicalRecord(mID) ON DELETE CASCADE,
    doctorID INTEGER NOT NULL REFERENCES doctor(employeeID) ON DELETE CASCADE,
    departID INTEGER NOT NULL REFERENCES department(departID) ON DELETE CASCADE,
    medID INTEGER REFERENCES icdmCode(icdmID) ON DELETE CASCADE,
    testID INTEGER REFERENCES icdtCode(icdtID) ON DELETE CASCADE,
    name VARCHAR(50),
    description TEXT,
    status VARCHAR(20),
    isPatientConfirmed BOOLEAN,
    cost NUMERIC(15, 0)
);


CREATE TABLE parameterResult (
    resultID SERIAL PRIMARY KEY,
    reqID INTEGER NOT NULL REFERENCES request(reqID) ON DELETE CASCADE,
    parameterID INTEGER NOT NULL REFERENCES parameterList(parameterID) ON DELETE CASCADE,
    parameterValue INTEGER
);


CREATE TABLE receptionReserve (
    reserveID SERIAL PRIMARY KEY,
    officeStaffID INTEGER NOT NULL REFERENCES officeStaff(employeeID) ON DELETE CASCADE,
    pID INTEGER NOT NULL REFERENCES patient(pID) ON DELETE CASCADE,
    appoID INTEGER REFERENCES appointment(appoID) ON DELETE CASCADE,
    surgeryID INTEGER REFERENCES surgery(surgeryID) ON DELETE CASCADE,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE invoice (
    invID SERIAL PRIMARY KEY,
    pID INTEGER NOT NULL REFERENCES patient(pID) ON DELETE CASCADE,
    appoID INTEGER REFERENCES appointment(appoID) ON DELETE CASCADE,
    reqID INTEGER REFERENCES request(reqID) ON DELETE CASCADE,
    surgeryID INTEGER REFERENCES surgery(surgeryID) ON DELETE CASCADE,
    admID INTEGER REFERENCES admission(admID) ON DELETE CASCADE,
    issueDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    totalAmount NUMERIC(15, 0),
    insuranceShare NUMERIC(15, 0),
    patientShare NUMERIC(15, 0),
    isPaid BOOLEAN
);


CREATE TABLE allItems (
    itemID SERIAL PRIMARY KEY,
    itemType VARCHAR(20),
    description TEXT
);


CREATE TABLE invoiceItem (
    itemID INTEGER NOT NULL REFERENCES invoice(invID) ON DELETE CASCADE,
    invoiceID INTEGER NOT NULL REFERENCES allItems(itemID) ON DELETE CASCADE,
    description TEXT
);