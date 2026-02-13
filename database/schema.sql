-- PostgreSQL schema for Hotel Property Management System (PMS)

CREATE TABLE users_user (
    id BIGSERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMPTZ NULL,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    username VARCHAR(150) UNIQUE NOT NULL,
    first_name VARCHAR(150) NOT NULL DEFAULT '',
    last_name VARCHAR(150) NOT NULL DEFAULT '',
    email VARCHAR(254) NOT NULL DEFAULT '',
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin','manager','front_desk','housekeeping','accountant','guest')),
    phone VARCHAR(20) NOT NULL DEFAULT ''
);

CREATE TABLE staff_staffprofile (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT UNIQUE NOT NULL REFERENCES users_user(id) ON DELETE CASCADE,
    specialization VARCHAR(120) NOT NULL DEFAULT '',
    license_number VARCHAR(80) NOT NULL DEFAULT '',
    shift_start TIME NULL,
    shift_end TIME NULL
);

CREATE TABLE patients_patient (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT UNIQUE NULL REFERENCES users_user(id) ON DELETE SET NULL,
    first_name VARCHAR(80) NOT NULL,
    last_name VARCHAR(80) NOT NULL,
    email VARCHAR(254) NOT NULL DEFAULT '',
    phone VARCHAR(20) NOT NULL DEFAULT '',
    date_of_birth DATE NOT NULL,
    gender VARCHAR(20) NOT NULL,
    blood_group VARCHAR(5) NOT NULL DEFAULT '',
    address TEXT NOT NULL DEFAULT '',
    emergency_contact VARCHAR(120) NOT NULL DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE appointments_room (
    id BIGSERIAL PRIMARY KEY,
    number VARCHAR(20) UNIQUE NOT NULL,
    room_type VARCHAR(20) NOT NULL CHECK (room_type IN ('standard','deluxe','suite')),
    floor INTEGER NOT NULL DEFAULT 1,
    nightly_rate NUMERIC(10,2) NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('available','occupied','maintenance'))
);

CREATE TABLE appointments_roomavailability (
    id BIGSERIAL PRIMARY KEY,
    room_id BIGINT NOT NULL REFERENCES appointments_room(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    is_available BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE (room_id, date)
);

CREATE TABLE appointments_appointment (
    id BIGSERIAL PRIMARY KEY,
    guest_id BIGINT NOT NULL REFERENCES patients_patient(id) ON DELETE CASCADE,
    room_id BIGINT NOT NULL REFERENCES appointments_room(id) ON DELETE CASCADE,
    assigned_staff_id BIGINT NULL REFERENCES staff_staffprofile(id) ON DELETE SET NULL,
    check_in TIMESTAMPTZ NOT NULL,
    check_out TIMESTAMPTZ NOT NULL,
    notes TEXT NOT NULL DEFAULT '',
    status VARCHAR(20) NOT NULL CHECK (status IN ('booked','checked_in','checked_out','cancelled')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE records_medicalrecord (
    id BIGSERIAL PRIMARY KEY,
    patient_id BIGINT NOT NULL REFERENCES patients_patient(id) ON DELETE CASCADE,
    record_type VARCHAR(30) NOT NULL CHECK (record_type IN ('room_service','housekeeping','maintenance')),
    title VARCHAR(200) NOT NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    encrypted_notes TEXT NOT NULL DEFAULT '',
    current_version INTEGER NOT NULL DEFAULT 1,
    created_by_id BIGINT NULL REFERENCES users_user(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE records_medicalrecordversion (
    id BIGSERIAL PRIMARY KEY,
    record_id BIGINT NOT NULL REFERENCES records_medicalrecord(id) ON DELETE CASCADE,
    version_number INTEGER NOT NULL,
    payload_snapshot JSONB NOT NULL DEFAULT '{}'::jsonb,
    encrypted_notes_snapshot TEXT NOT NULL DEFAULT '',
    updated_by_id BIGINT NULL REFERENCES users_user(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (record_id, version_number)
);

CREATE TABLE billing_bill (
    id BIGSERIAL PRIMARY KEY,
    appointment_id BIGINT UNIQUE NOT NULL REFERENCES appointments_appointment(id) ON DELETE CASCADE,
    subtotal NUMERIC(10,2) NOT NULL DEFAULT 0,
    tax NUMERIC(10,2) NOT NULL DEFAULT 0,
    total NUMERIC(10,2) NOT NULL DEFAULT 0,
    status VARCHAR(20) NOT NULL CHECK (status IN ('draft','issued','paid')),
    generated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE billing_billlineitem (
    id BIGSERIAL PRIMARY KEY,
    bill_id BIGINT NOT NULL REFERENCES billing_bill(id) ON DELETE CASCADE,
    description VARCHAR(200) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    unit_price NUMERIC(10,2) NOT NULL,
    amount NUMERIC(10,2) NOT NULL
);

CREATE TABLE notifications_notificationlog (
    id BIGSERIAL PRIMARY KEY,
    recipient VARCHAR(150) NOT NULL,
    channel VARCHAR(20) NOT NULL CHECK (channel IN ('email','sms')),
    message TEXT NOT NULL,
    appointment_id BIGINT NULL REFERENCES appointments_appointment(id) ON DELETE CASCADE,
    created_by_id BIGINT NULL REFERENCES users_user(id) ON DELETE SET NULL,
    sent_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_bookings_status_dates ON appointments_appointment(status, check_in, check_out);
CREATE INDEX idx_guests_name ON patients_patient(last_name, first_name);
CREATE INDEX idx_room_status ON appointments_room(status);
CREATE INDEX idx_services_guest_type ON records_medicalrecord(patient_id, record_type);
CREATE INDEX idx_invoice_status ON billing_bill(status);
