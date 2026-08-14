from collections.abc import Callable
from collections.abc import Sequence as RecordSequence
from typing import Any
from uuid import UUID

import psycopg
from psycopg.types.json import Jsonb

from ingestion.crm.schema import CRMCustomer

INSERT_CRM_STAGING_SQL = """
INSERT INTO staging.crm_customers (
  batch_id, source_record_id, external_id, full_name, email, phone,
  date_of_birth, gender, address_line_1, address_line_2, city,
  state_province, postal_code, country_code, customer_status,
  marketing_consent, source_system, source_payload, source_updated_at
) VALUES (
  %(batch_id)s, %(source_record_id)s, %(external_id)s, %(full_name)s,
  %(email)s, %(phone)s, %(date_of_birth)s, %(gender)s,
  %(address_line_1)s, %(address_line_2)s, %(city)s, %(state_province)s,
  %(postal_code)s, %(country_code)s, %(customer_status)s,
  %(marketing_consent)s, 'crm', %(source_payload)s, %(source_updated_at)s
)
ON CONFLICT (batch_id, source_record_id) DO UPDATE SET
  external_id = EXCLUDED.external_id,
  full_name = EXCLUDED.full_name,
  email = EXCLUDED.email,
  phone = EXCLUDED.phone,
  date_of_birth = EXCLUDED.date_of_birth,
  gender = EXCLUDED.gender,
  address_line_1 = EXCLUDED.address_line_1,
  address_line_2 = EXCLUDED.address_line_2,
  city = EXCLUDED.city,
  state_province = EXCLUDED.state_province,
  postal_code = EXCLUDED.postal_code,
  country_code = EXCLUDED.country_code,
  customer_status = EXCLUDED.customer_status,
  marketing_consent = EXCLUDED.marketing_consent,
  source_payload = EXCLUDED.source_payload,
  source_updated_at = EXCLUDED.source_updated_at,
  ingested_at = NOW(),
  validation_status = 'valid',
  validation_errors = '[]'::JSONB
"""


def load_crm_staging(
    dsn: str,
    batch_id: UUID,
    records: RecordSequence[tuple[CRMCustomer, dict[str, Any]]],
    *,
    connect: Callable[..., Any] = psycopg.connect,
) -> int:
    """Atomically upsert one validated CRM batch into PostgreSQL staging."""
    if not records:
        return 0

    parameters = []
    for record, source_payload in records:
        values = record.model_dump()
        values.update(
            batch_id=batch_id,
            source_record_id=record.source_record_id,
            email=str(record.email) if record.email else None,
            source_payload=Jsonb(source_payload),
        )
        parameters.append(values)

    with connect(dsn) as connection, connection.cursor() as cursor:
        cursor.executemany(INSERT_CRM_STAGING_SQL, parameters)
    return len(parameters)
