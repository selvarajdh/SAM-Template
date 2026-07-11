# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repo is a collection of AWS SAM (Serverless Application Model) learning projects, each in its own subdirectory with an independent `template.yaml`, `samconfig.toml`, and Python 3.13 Lambda functions.

## Projects

| Directory | Description |
|---|---|
| `first-lambda/` | Introductory Lambda — demonstrates cold starts, data types, context object, and environment variables |
| `OrderLambda/orders-api/` | REST API backed by API Gateway + DynamoDB. `POST /orders` (create) and `GET /orders/{id}` (read) |
| `AsynchronousPatCheckout/patientcheckout/` | Event-driven pipeline: S3 upload → SNS fan-out → SQS + DLQ. Four Lambda functions (PatientCheckout, BillManagement, ClaimManagement, ErrorHandler) |

## SAM Commands

All commands must be run from inside the project subdirectory (e.g. `cd OrderLambda/orders-api`).

```bash
sam build                          # build (no container)
sam build --use-container          # build inside Lambda-like Docker container
sam deploy --guided                # first-time deploy (saves config to samconfig.toml)
sam deploy                         # subsequent deploys using saved samconfig.toml
sam local invoke <FunctionName> --event events/event.json   # invoke locally
sam local start-api                # run API Gateway locally on port 3000
sam logs -n <FunctionName> --stack-name <stack> --tail      # tail CloudWatch logs
sam delete --stack-name <stack>    # tear down the stack
```

## Tests

```bash
# Unit tests (no AWS needed)
pip install -r tests/requirements.txt
python -m pytest tests/unit -v

# Integration tests (stack must be deployed first)
AWS_SAM_STACK_NAME="<stack-name>" python -m pytest tests/integration -v
```

## Architecture Notes

**AsynchronousPatCheckout flow:**
1. A JSON file is uploaded to `PatientCheckoutBucket` (S3)
2. S3 event triggers `PatientCheckoutFunction`, which reads the file and publishes each record to `PatientCheckoutTopic` (SNS)
3. SNS fans out to `BillManagementFunction` (SNS subscriber) and `ClaimManagementQueue` (SQS subscriber consumed by `ClaimManagementFunction`)
4. Failed invocations on `PatientCheckoutFunction` route to `PatientCheckoutDLQ` (SNS), handled by `ErrorHandlerFunction`

**OrderLambda:**  
`CreateOrderFunction` and `ReadOrderFunction` share the same `orders_api/` code directory. The `ORDERS_TABLE` env var (set globally in `template.yaml`) points to the `OrdersTable` DynamoDB simple table. `read.py` uses `simplejson` (not stdlib `json`) to handle DynamoDB Decimal serialization.

**first-lambda:**  
`datatypes.py` contains multiple handler functions (`cold_start_basics`, `simple_types`, `list_types`, `dict_types`, `lambda_handler`) — the active handler is set via `Handler:` in `template.yaml`.
