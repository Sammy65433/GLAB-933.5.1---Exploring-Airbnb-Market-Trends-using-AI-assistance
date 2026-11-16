# Insights — NYC Airbnb Market Trends (2019)

Data: 25,209 NYC Airbnb listings joined from `airbnb_price.csv`,
`airbnb_room_type.xlsx`, and `airbnb_last_review.tsv`.

## 1. Pricing distribution
- **Median nightly price: $105** (Q1 = $69, Q3 = $175, IQR = $106).
- Mean ($141.78) is well above the median, indicating a right-skewed
  distribution driven by a long tail of high-priced listings.
- **1,326 listings (≈5.3%) are IQR outliers**, all above the $334 upper
  bound; a handful reach $5,000–$7,500. These likely represent luxury
  properties or data entry errors and should be investigated before
  modeling.

## 2. Room-type mix & pricing
- **Entire home/apt: 52.6%** of listings, avg. $197 (median $159).
- **Private room: 45.1%**, avg. $82 (median $70).
- **Shared room: 2.3%**, avg. $53 (median $41).
- Price ordering is consistent across the distribution: entire homes >
  private rooms > shared rooms. Private rooms dominate the $50–$100 band,
  while entire homes dominate everything above $150.

## 3. Review recency & activity
- Reviews span **2019-01-01 to 2019-07-09**.
- Activity ramps through spring and peaks in **June 2019 (12,601
  reviews)**, remaining strong in July (4,725). This suggests demand was
  heating up heading into summer, not cooling.
- The dataset is a 2019 snapshot, so recency is bounded by July 2019.

## 4. Data quality notes
- 10 listings are missing `description`; 8 are missing `host_name`.
- A small number of listings show a price of $0 (private/shared rooms) —
  likely placeholders or errors; treat with caution in any downstream model.
- `listing_id` and `price` are essentially uncorrelated (r ≈ 0.023), so
  ID carries no pricing signal.

## 5. Takeaways for the real-estate startup
- NYC short-term rental supply is split almost evenly between entire homes
  and private rooms; shared rooms are a niche (≈2%).
- Private rooms are the value segment (~$70–$82/night) and make up ~45%
  of inventory — attractive for budget-conscious travelers.
- High-end outliers (> $334) are a distinct segment worth targeting
  separately (luxury positioning).
- Summer 2019 shows peak review activity, consistent with seasonal
  tourism demand; pricing and availability strategies should account for
  this seasonality.
- Before building predictive models, clean $0/placeholder prices and
  consider capping or separately modeling the high-price tail.
