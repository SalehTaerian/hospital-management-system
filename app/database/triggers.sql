CREATE OR REPLACE FUNCTION check_parameter_warning()
RETURNS TRIGGER AS $$
DECLARE
    p_min DECIMAL(10,5);
    p_max DECIMAL(10,5);
    p_name VARCHAR(25);
BEGIN
    SELECT min, max, parameterName 
    INTO p_min, p_max, p_name
    FROM parameterList 
    WHERE parameterID = NEW.parameterID;
    
    IF p_min IS NULL OR p_max IS NULL THEN
        RETURN NEW;
    END IF;
    
    IF NEW.parameterValue < p_min OR NEW.parameterValue > p_max THEN
        
        INSERT INTO warning (
            logID, 
            importance, 
            occuredTime, 
            checkedStatus
        ) VALUES (
            NEW.logID,
            CASE 
                WHEN NEW.parameterValue < p_min THEN 'Low'
                WHEN NEW.parameterValue > p_max THEN 'High'
            END,
            NEW.createdAt,
            'Unchecked'
        );
        
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_check_parameter_warning ON log;

CREATE TRIGGER trigger_check_parameter_warning
AFTER INSERT ON log
FOR EACH ROW
EXECUTE FUNCTION check_parameter_warning();

CREATE OR REPLACE FUNCTION get_patient_id_from_admission(adm_id INTEGER)
RETURNS INTEGER AS $$
DECLARE
    patient_id INTEGER;
BEGIN
    SELECT p.pID INTO patient_id
    FROM patient p
    JOIN medicalRecord mr ON p.pID = mr.pID
    JOIN admission a ON mr.mID = a.mID
    WHERE a.admID = adm_id;
    RETURN patient_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_patient_id_from_appointment(appo_id INTEGER)
RETURNS INTEGER AS $$
DECLARE
    patient_id INTEGER;
BEGIN
    SELECT p.pID INTO patient_id
    FROM patient p
    JOIN medicalRecord mr ON p.pID = mr.pID
    JOIN appointment a ON mr.mID = a.mID
    WHERE a.appoID = appo_id;
    RETURN patient_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_patient_id_from_request(req_id INTEGER)
RETURNS INTEGER AS $$
DECLARE
    patient_id INTEGER;
BEGIN
    SELECT p.pID INTO patient_id
    FROM patient p
    JOIN medicalRecord mr ON p.pID = mr.pID
    JOIN request r ON mr.mID = r.mID
    WHERE r.reqID = req_id;
    RETURN patient_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_patient_id_from_surgery(surg_id INTEGER)
RETURNS INTEGER AS $$
DECLARE
    patient_id INTEGER;
BEGIN
    SELECT pID INTO patient_id
    FROM surgery
    WHERE surgeryID = surg_id;
    RETURN patient_id;
END;
$$ LANGUAGE plpgsql;

-- Function to get insurance coverage
CREATE OR REPLACE FUNCTION get_patient_insurance_coverage(patient_id INTEGER)
RETURNS DECIMAL AS $$
DECLARE
    coverage DECIMAL;
BEGIN
    SELECT coveragePercentage INTO coverage
    FROM insurance
    WHERE pID = patient_id
    ORDER BY createdAt DESC
    LIMIT 1;
    RETURN COALESCE(coverage, 0);
END;
$$ LANGUAGE plpgsql;

-- Function to calculate invoice amounts
CREATE OR REPLACE FUNCTION calculate_invoice_amounts(patient_id INTEGER, total_cost DECIMAL)
RETURNS TABLE(
    total_amount DECIMAL,
    insurance_share DECIMAL,
    patient_share DECIMAL
) AS $$
DECLARE
    coverage DECIMAL;
BEGIN
    coverage := get_patient_insurance_coverage(patient_id);
    total_amount := total_cost;
    insurance_share := total_cost * (coverage / 100);
    patient_share := total_cost - insurance_share;
    RETURN NEXT;
END;
$$ LANGUAGE plpgsql;

-- Function to get allItems ID by type
CREATE OR REPLACE FUNCTION get_allitem_id(item_type VARCHAR)
RETURNS INTEGER AS $$
DECLARE
    item_id INTEGER;
BEGIN
    SELECT itemID INTO item_id
    FROM allItems
    WHERE itemType = item_type;
    RETURN item_id;
END;
$$ LANGUAGE plpgsql;

-- ==========================================
-- TRIGGER: Auto-create invoice for admission
-- ==========================================

CREATE OR REPLACE FUNCTION create_invoice_for_admission()
RETURNS TRIGGER AS $$
DECLARE
    patient_id INTEGER;
    inv_id INTEGER;
    item_id INTEGER;
    amounts RECORD;
    total_cost DECIMAL;
BEGIN
    patient_id := get_patient_id_from_admission(NEW.admID);
    
    IF patient_id IS NULL THEN
        RETURN NEW;
    END IF;
    
    total_cost := COALESCE(NEW.cost, 0);
    
    SELECT * INTO amounts FROM calculate_invoice_amounts(patient_id, total_cost);
    
    INSERT INTO invoice (
        pID, admID, issueDate, totalAmount, insuranceShare, patientShare, isPaid
    ) VALUES (
        patient_id,
        NEW.admID,
        CURRENT_TIMESTAMP,
        amounts.total_amount,
        amounts.insurance_share,
        amounts.patient_share,
        FALSE
    ) RETURNING invID INTO inv_id;
    
    item_id := get_allitem_id('admission');
    IF item_id IS NOT NULL AND inv_id IS NOT NULL THEN
        INSERT INTO invoiceItem (itemID, invoiceID, description)
        VALUES (inv_id, item_id, 'Admission #' || NEW.admID);
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_create_invoice_admission ON admission;

CREATE TRIGGER trigger_create_invoice_admission
AFTER INSERT ON admission
FOR EACH ROW
EXECUTE FUNCTION create_invoice_for_admission();

-- ==========================================
-- TRIGGER: Update invoice when admission cost changes
-- ==========================================

CREATE OR REPLACE FUNCTION update_invoice_for_admission()
RETURNS TRIGGER AS $$
DECLARE
    patient_id INTEGER;
    inv_id INTEGER;
    amounts RECORD;
    total_cost DECIMAL;
BEGIN
    patient_id := get_patient_id_from_admission(NEW.admID);
    
    IF patient_id IS NULL THEN
        RETURN NEW;
    END IF;
    
    SELECT invID INTO inv_id
    FROM invoice
    WHERE admID = NEW.admID AND isPaid = FALSE
    ORDER BY issueDate DESC
    LIMIT 1;
    
    IF inv_id IS NULL THEN
        RETURN NEW;
    END IF;
    
    total_cost := COALESCE(NEW.cost, 0);
    
    SELECT * INTO amounts FROM calculate_invoice_amounts(patient_id, total_cost);
    
    UPDATE invoice
    SET totalAmount = amounts.total_amount,
        insuranceShare = amounts.insurance_share,
        patientShare = amounts.patient_share
    WHERE invID = inv_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_update_invoice_admission ON admission;

CREATE TRIGGER trigger_update_invoice_admission
AFTER UPDATE OF cost ON admission
FOR EACH ROW
WHEN (OLD.cost IS DISTINCT FROM NEW.cost)
EXECUTE FUNCTION update_invoice_for_admission();

-- ==========================================
-- TRIGGER: Auto-create invoice for appointment
-- ==========================================

CREATE OR REPLACE FUNCTION create_invoice_for_appointment()
RETURNS TRIGGER AS $$
DECLARE
    patient_id INTEGER;
    inv_id INTEGER;
    item_id INTEGER;
    amounts RECORD;
    total_cost DECIMAL;
    doctor_employee_id INTEGER;
BEGIN
    patient_id := get_patient_id_from_appointment(NEW.appoID);
    
    IF patient_id IS NULL THEN
        RETURN NEW;
    END IF;
    
    SELECT visitCost INTO total_cost
    FROM doctor
    WHERE employeeID = NEW.doctorID;
    
    total_cost := COALESCE(total_cost, 0);
    
    SELECT * INTO amounts FROM calculate_invoice_amounts(patient_id, total_cost);
    
    INSERT INTO invoice (
        pID, appoID, issueDate, totalAmount, insuranceShare, patientShare, isPaid
    ) VALUES (
        patient_id,
        NEW.appoID,
        CURRENT_TIMESTAMP,
        amounts.total_amount,
        amounts.insurance_share,
        amounts.patient_share,
        FALSE
    ) RETURNING invID INTO inv_id;
    
    item_id := get_allitem_id('appointment');
    IF item_id IS NOT NULL AND inv_id IS NOT NULL THEN
        INSERT INTO invoiceItem (itemID, invoiceID, description)
        VALUES (inv_id, item_id, 'Appointment #' || NEW.appoID);
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_create_invoice_appointment ON appointment;

CREATE TRIGGER trigger_create_invoice_appointment
AFTER INSERT ON appointment
FOR EACH ROW
EXECUTE FUNCTION create_invoice_for_appointment();

-- ==========================================
-- TRIGGER: Auto-create invoice for surgery
-- ==========================================

CREATE OR REPLACE FUNCTION create_invoice_for_surgery()
RETURNS TRIGGER AS $$
DECLARE
    patient_id INTEGER;
    inv_id INTEGER;
    item_id INTEGER;
    amounts RECORD;
    total_cost DECIMAL;
BEGIN
    patient_id := NEW.pID;
    
    IF patient_id IS NULL THEN
        RETURN NEW;
    END IF;
    
    SELECT cost INTO total_cost
    FROM icdsCode
    WHERE icdsID = NEW.surgeryCode;
    
    total_cost := COALESCE(total_cost, 0);
    
    SELECT * INTO amounts FROM calculate_invoice_amounts(patient_id, total_cost);
    
    INSERT INTO invoice (
        pID, surgeryID, issueDate, totalAmount, insuranceShare, patientShare, isPaid
    ) VALUES (
        patient_id,
        NEW.surgeryID,
        CURRENT_TIMESTAMP,
        amounts.total_amount,
        amounts.insurance_share,
        amounts.patient_share,
        FALSE
    ) RETURNING invID INTO inv_id;
    
    item_id := get_allitem_id('surgery');
    IF item_id IS NOT NULL AND inv_id IS NOT NULL THEN
        INSERT INTO invoiceItem (itemID, invoiceID, description)
        VALUES (inv_id, item_id, 'Surgery #' || NEW.surgeryID);
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_create_invoice_surgery ON surgery;

CREATE TRIGGER trigger_create_invoice_surgery
AFTER INSERT ON surgery
FOR EACH ROW
EXECUTE FUNCTION create_invoice_for_surgery();

-- ==========================================
-- TRIGGER: Auto-create invoice for medicine request
-- ==========================================

CREATE OR REPLACE FUNCTION create_invoice_for_medicine_request()
RETURNS TRIGGER AS $$
DECLARE
    patient_id INTEGER;
    inv_id INTEGER;
    item_id INTEGER;
    amounts RECORD;
    total_cost DECIMAL;
BEGIN
    IF NEW.medID IS NULL THEN
        RETURN NEW;
    END IF;
    
    patient_id := get_patient_id_from_request(NEW.reqID);
    
    IF patient_id IS NULL THEN
        RETURN NEW;
    END IF;
    
    total_cost := COALESCE(NEW.cost, 0);
    
    SELECT * INTO amounts FROM calculate_invoice_amounts(patient_id, total_cost);
    
    INSERT INTO invoice (
        pID, reqID, issueDate, totalAmount, insuranceShare, patientShare, isPaid
    ) VALUES (
        patient_id,
        NEW.reqID,
        CURRENT_TIMESTAMP,
        amounts.total_amount,
        amounts.insurance_share,
        amounts.patient_share,
        FALSE
    ) RETURNING invID INTO inv_id;
    
    item_id := get_allitem_id('medicine');
    IF item_id IS NOT NULL AND inv_id IS NOT NULL THEN
        INSERT INTO invoiceItem (itemID, invoiceID, description)
        VALUES (inv_id, item_id, 'Medicine Request #' || NEW.reqID);
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_create_invoice_medicine ON request;

CREATE TRIGGER trigger_create_invoice_medicine
AFTER INSERT ON request
FOR EACH ROW
WHEN (NEW.medID IS NOT NULL)
EXECUTE FUNCTION create_invoice_for_medicine_request();

-- ==========================================
-- TRIGGER: Auto-create invoice for test request
-- ==========================================

CREATE OR REPLACE FUNCTION create_invoice_for_test_request()
RETURNS TRIGGER AS $$
DECLARE
    patient_id INTEGER;
    inv_id INTEGER;
    item_id INTEGER;
    amounts RECORD;
    total_cost DECIMAL;
BEGIN
    IF NEW.testID IS NULL THEN
        RETURN NEW;
    END IF;
    
    patient_id := get_patient_id_from_request(NEW.reqID);
    
    IF patient_id IS NULL THEN
        RETURN NEW;
    END IF;
    
    total_cost := COALESCE(NEW.cost, 0);
    
    SELECT * INTO amounts FROM calculate_invoice_amounts(patient_id, total_cost);
    
    INSERT INTO invoice (
        pID, reqID, issueDate, totalAmount, insuranceShare, patientShare, isPaid
    ) VALUES (
        patient_id,
        NEW.reqID,
        CURRENT_TIMESTAMP,
        amounts.total_amount,
        amounts.insurance_share,
        amounts.patient_share,
        FALSE
    ) RETURNING invID INTO inv_id;
    
    item_id := get_allitem_id('test');
    IF item_id IS NOT NULL AND inv_id IS NOT NULL THEN
        INSERT INTO invoiceItem (itemID, invoiceID, description)
        VALUES (inv_id, item_id, 'Test Request #' || NEW.reqID);
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_create_invoice_test ON request;

CREATE TRIGGER trigger_create_invoice_test
AFTER INSERT ON request
FOR EACH ROW
WHEN (NEW.testID IS NOT NULL)
EXECUTE FUNCTION create_invoice_for_test_request();

-- ==========================================
-- TRIGGER: Update invoice when request cost changes
-- ==========================================

CREATE OR REPLACE FUNCTION update_invoice_for_request()
RETURNS TRIGGER AS $$
DECLARE
    patient_id INTEGER;
    inv_id INTEGER;
    amounts RECORD;
    total_cost DECIMAL;
BEGIN
    patient_id := get_patient_id_from_request(NEW.reqID);
    
    IF patient_id IS NULL THEN
        RETURN NEW;
    END IF;
    
    SELECT invID INTO inv_id
    FROM invoice
    WHERE reqID = NEW.reqID AND isPaid = FALSE
    ORDER BY issueDate DESC
    LIMIT 1;
    
    IF inv_id IS NULL THEN
        RETURN NEW;
    END IF;
    
    total_cost := COALESCE(NEW.cost, 0);
    
    SELECT * INTO amounts FROM calculate_invoice_amounts(patient_id, total_cost);
    
    UPDATE invoice
    SET totalAmount = amounts.total_amount,
        insuranceShare = amounts.insurance_share,
        patientShare = amounts.patient_share
    WHERE invID = inv_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_update_invoice_request ON request;

CREATE TRIGGER trigger_update_invoice_request
AFTER UPDATE OF cost ON request
FOR EACH ROW
WHEN (OLD.cost IS DISTINCT FROM NEW.cost)
EXECUTE FUNCTION update_invoice_for_request();