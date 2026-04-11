CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name) THEN
        UPDATE contacts SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO contacts(name, phone) VALUES(p_name, p_phone);
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    IN p_names VARCHAR[],
    IN p_phones VARCHAR[],
    OUT failed_names VARCHAR[],
    OUT failed_phones VARCHAR[]
)
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    failed_names := ARRAY[]::VARCHAR[];
    failed_phones := ARRAY[]::VARCHAR[];

    FOR i IN 1 .. array_length(p_names, 1) LOOP
        IF length(p_phones[i]) < 5 THEN
            failed_names := array_append(failed_names, p_names[i]);
            failed_phones := array_append(failed_phones, p_phones[i]);
        ELSE
            CALL upsert_contact(p_names[i], p_phones[i]);
        END IF;
    END LOOP;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact(p_identifier VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts 
    WHERE name = p_identifier OR phone = p_identifier;
END;
$$;