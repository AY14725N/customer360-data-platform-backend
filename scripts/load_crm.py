import argparse
import json
from pathlib import Path

from config.settings import get_settings
from ingestion.crm.pipeline import CRMValidationError, ingest_crm
from ingestion.crm.reader import read_crm_api, read_crm_csv


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate CRM data and load PostgreSQL staging")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--csv", type=Path, help="path to a UTF-8 CRM CSV file")
    source.add_argument("--api-url", help="CRM HTTP API endpoint")
    parser.add_argument("--api-token", help="Bearer token; defaults to CRM_API_TOKEN")
    parser.add_argument("--records-key", default="customers", help="API response list field")
    parser.add_argument("--page-size", type=int, default=100)
    parser.add_argument(
        "--allow-invalid",
        action="store_true",
        help="load valid rows and report rejected rows instead of rejecting the batch",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    settings = get_settings()

    if args.csv:
        records = read_crm_csv(args.csv)
    else:
        records = read_crm_api(
            args.api_url,
            api_token=args.api_token or settings.crm_api_token,
            records_key=args.records_key,
            page_size=args.page_size,
        )

    try:
        result = ingest_crm(records, settings.postgres_dsn, fail_on_invalid=not args.allow_invalid)
    except CRMValidationError as exc:
        report = {
            "passed": False,
            "records_rejected": len(exc.rejected),
            "rejected": [
                {"row_number": item.row_number, "errors": item.errors}
                for item in exc.rejected
            ],
        }
        print(json.dumps(report, indent=2))
        raise SystemExit(2) from exc

    print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    main()
