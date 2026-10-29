# Test Plan

| ID | Scenario | Expected result |
|---|---|---|
| T01 | Valid programming question | Explanation is returned when API credentials are configured |
| T02 | Valid mathematics question | Step-by-step reasoning is requested |
| T03 | ML concept question | Explanation includes definitions and examples |
| T04 | NLP concept question | Explanation uses topic-relevant examples |
| T05 | Empty question and no upload | Validation warning is shown |
| T06 | Question over maximum length | Validation warning is shown |
| T07 | Missing API key | Helpful configuration error is shown |
| T08 | Hint-first mode | Hint is provided without immediately revealing full answer |
| T09 | Verify mode with an attempt | Attempt is reviewed, with caveats where needed |
| T10 | Provider/network failure | A readable error is displayed rather than a silent failure |

Run automated checks using `pytest -q`. Record actual results after running the application and reviewing AI outputs. Do not mark manual AI-quality checks as passed before performing them.
