# Ask the Data Assistant Report

## Performance
- **Successful Queries:** 13/15
- **Accuracy:** 86.7%
- **Method:** Rule-based patterns + Gemini API (fallback available)

## Test Results
- OK What is the total transaction volume? (1 rows)
- OK What is the average volume per month? (1 rows)
- FAIL What is the maximum volume ever recorded? (Could not generate SQL for this question. Try: gro)
- OK What is the growth rate from start to end? (1 rows)
- OK Which month has the highest average volume? (1 rows)
- OK How many banks were involved at the start and end? (1 rows)
- OK What is the most recent volume? (6 rows)
- OK Show me the trend in the first 10 months (12 rows)
- OK Which periods have anomalies? (2 rows)
- OK What are the market segments? (3 rows)
- OK What is the value per transaction on average? (1 rows)
- OK How many transactions in the latest month? (1 rows)
- FAIL What is the coefficient of variation? (Could not generate SQL for this question. Try: gro)
- OK Which month shows highest variability? (1 rows)
- OK Compare volume and value trends (12 rows)


## Architecture
1. **Input:** Natural language question
2. **Rule Match:** Check 10+ predefined patterns
3. **LLM Fallback:** Gemini 1.5 Flash (if available)
4. **Validation:** Schema check, safety check, SQL syntax
5. **Execution:** DuckDB read-only query
6. **Verification:** Result sanity check

## Limitations
- Rule-based patterns cover ~70% of common questions
- Gemini requires API key (graceful fallback)
- No join queries between tables
- Limited to SELECT operations only

