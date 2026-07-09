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