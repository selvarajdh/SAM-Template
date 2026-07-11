# SAM Template

A collection of AWS Serverless Application Model (SAM) learning projects built with Python 3.13.

## Projects

### first-lambda
An introductory Lambda function exploring cold starts, Python data types, the Lambda context object, and environment variables.

### OrderLambda
A REST API using API Gateway and DynamoDB:
- `POST /orders` — create an order
- `GET /orders/{id}` — retrieve an order by ID

### AsynchronousPatCheckout
An event-driven patient checkout pipeline:
- A JSON file uploaded to S3 triggers the checkout Lambda
- Records are published to SNS and fanned out to billing (SNS) and claims (SQS) handlers
- Failed invocations are routed to a dead-letter queue handled by an error handler Lambda

## Prerequisites

- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- Python 3.13
- Docker (for `--use-container` builds)
- AWS credentials configured

## Usage

Navigate into any project subdirectory and run:

```bash
sam build
sam deploy --guided
```

See [CLAUDE.md](CLAUDE.md) for the full command reference.
