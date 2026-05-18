# Postmortem Analysis

## 1. Incident Overview

An intentional misconfiguration was introduced in the order service database connection settings to simulate production failure conditions.

## 2. Customer Impact

Customers could not access order data while the incident was active. Authentication, product, user, payment, and notification services remained operational.

## 3. Root Cause Analysis

Configuration drift in the order service environment caused it to use an invalid database host.

## 4. Detection and Response Evaluation

- Detection quality: good (dashboard + endpoint checks)
- Time to detect: short
- Time to mitigate: moderate
- Response process: effective, but too manual

## 5. Resolution Summary

The service configuration was corrected and the order container was redeployed, restoring normal behavior.

## 6. Lessons Learned

1. Misconfiguration can be as damaging as code defects.
2. Service-level metrics speed up failure localization.
3. Restart runbooks must be documented and tested.

## 7. Action Items

1. Add startup validation for DB host/connection.
2. Add alerting for order error rate and health endpoint failures.
3. Introduce pre-deploy configuration checks in CI/CD.
4. Use environment templates and secrets management to reduce manual errors.
