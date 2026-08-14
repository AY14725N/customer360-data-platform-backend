"""CRM source ingestion and PostgreSQL staging."""

from ingestion.crm.pipeline import CRMIngestionResult, ingest_crm

__all__ = ["CRMIngestionResult", "ingest_crm"]
