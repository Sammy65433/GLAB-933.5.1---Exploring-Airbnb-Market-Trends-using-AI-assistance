# GLAB 933.5.1 - Exploring Airbnb Market Trends (NYC)

Data analysis of 2019 NYC Airbnb listings combining three source files
(`airbnb_price.csv`, `airbnb_room_type.xlsx`, `airbnb_last_review.tsv`).

## Run

```bash
uv sync
uv run python airbnb_analysis.py
```

Outputs (charts + cleaned CSV) are written to `output/`.

## Key findings

- ~25k listings joined across the three sources.
- Median nightly price: $105 (Q1=$69, Q3=$175, IQR=$106); 1,326 IQR outliers.
- Room mix: Entire home/apt 52.5%, Private room 45.0%, Shared room 2.3%.
- Average price: Entire home/apt $197, Private room $82, Shared room $53.
- Private rooms make up ~45% of listings.
- Reviews span 2019-01-01 to 2019-07-09, peaking in June 2019 (12,601 reviews).
- Price and listing_id are essentially uncorrelated (r=0.023).

## Files

- `airbnb_analysis.py` - full analysis script
- `data/` - source files
- `output/` - generated charts and cleaned CSV
