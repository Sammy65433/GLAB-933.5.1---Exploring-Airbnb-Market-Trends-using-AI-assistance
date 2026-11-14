"""GLAB 933.5.1 - Exploring Airbnb Market Trends (NYC).

Analysis script: loads, joins, cleans, and explores the Airbnb listings data.
Run:  uv run python airbnb_analysis.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # headless
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent / "data"
OUT_DIR = Path(__file__).resolve().parent / "output"
OUT_DIR.mkdir(exist_ok=True)


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    price = pd.read_csv(DATA_DIR / "airbnb_price.csv")
    room = pd.read_excel(DATA_DIR / "airbnb_room_type.xlsx")
    review = pd.read_csv(DATA_DIR / "airbnb_last_review.tsv", sep="\t")
    return price, room, review


def join_data(price, room, review) -> pd.DataFrame:
    listings = pd.merge(price, room, on="listing_id", how="inner")
    listings = pd.merge(listings, review, on="listing_id", how="inner")
    return listings


def clean_data(listings: pd.DataFrame) -> pd.DataFrame:
    # Clean price: strip '$' and commas, convert to numeric
    listings = listings.copy()
    listings["price"] = (
        listings["price"].astype(str).str.extract(r"(\d[\d,]*)", expand=False)
        .str.replace(",", "", regex=False)
    )
    listings["price"] = pd.to_numeric(listings["price"], errors="coerce")

    # Normalize room_type capitalization
    listings["room_type"] = listings["room_type"].astype(str).str.strip().str.lower()

    # Parse last review date
    listings["last_review_date"] = pd.to_datetime(
        listings["last_review"], format="%B %d %Y", errors="coerce"
    )

    return listings


def main() -> None:
    price, room, review = load_data()
    print("Shapes:", price.shape, room.shape, review.shape)

    listings = join_data(price, room, review)
    listings = clean_data(listings)
    print("\nJoined shape:", listings.shape)
    print("\nColumns:", list(listings.columns))

    # Missingness
    print("\nMissing values per column:")
    print(listings.isna().sum())

    # Price distribution
    print("\nPrice summary:")
    print(listings["price"].describe())
    print("Median:", listings["price"].median())
    q1, q3 = listings["price"].quantile([0.25, 0.75])
    iqr = q3 - q1
    print(f"Q1={q1}, Q3={q3}, IQR={iqr}")
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    outliers = listings[(listings["price"] < lower) | (listings["price"] > upper)]
    print(f"IQR outlier bounds: [{lower}, {upper}]  -> {len(outliers)} outliers")

    # Room type counts & average price
    print("\nRoom type counts:")
    print(listings["room_type"].value_counts())
    print("\nAverage price by room type:")
    print(listings.groupby("room_type")["price"].agg(["count", "mean", "median"]).round(2))

    # Private room count
    private_count = (listings["room_type"] == "private room").sum()
    print(f"\nPrivate rooms: {private_count} ({private_count/len(listings):.1%})")

    # Review recency
    print("\nEarliest review:", listings["last_review_date"].min())
    print("Most recent review:", listings["last_review_date"].max())
    listings["review_month"] = listings["last_review_date"].dt.to_period("M")
    monthly = listings.groupby("review_month").size()
    print("\nReviews by month (last 12):")
    print(monthly.tail(12))

    # Correlation (numeric)
    numeric = listings.select_dtypes(include=[np.number])
    if numeric.shape[1] > 1:
        print("\nCorrelation matrix:")
        print(numeric.corr().round(3))

    # ---- Charts ----
    # Price distribution
    fig, ax = plt.subplots(figsize=(8, 5))
    listings["price"].clip(upper=upper).hist(bins=40, ax=ax, color="#6366f1", edgecolor="white")
    ax.set_title("Distribution of Listing Prices (capped at IQR upper bound)")
    ax.set_xlabel("Price (USD)")
    ax.set_ylabel("Count")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "price_distribution.png", dpi=120)
    plt.close(fig)

    # Price by room type (boxplot)
    fig, ax = plt.subplots(figsize=(8, 5))
    data = [listings.loc[listings["room_type"] == rt, "price"].dropna().clip(upper=upper)
            for rt in sorted(listings["room_type"].unique())]
    ax.boxplot(data, tick_labels=sorted(listings["room_type"].unique()), showfliers=False)
    ax.set_title("Price by Room Type")
    ax.set_ylabel("Price (USD)")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "price_by_room_type.png", dpi=120)
    plt.close(fig)

    # Room type share
    fig, ax = plt.subplots(figsize=(6, 6))
    counts = listings["room_type"].value_counts()
    ax.pie(counts, labels=counts.index, autopct="%1.1f%%", startangle=90,
           colors=["#6366f1", "#ec4899", "#f59e0b"])
    ax.set_title("Room Type Share")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "room_type_share.png", dpi=120)
    plt.close(fig)

    # Reviews by month
    fig, ax = plt.subplots(figsize=(10, 5))
    monthly.plot(ax=ax, color="#10b981")
    ax.set_title("Listings Reviewed by Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Count")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "reviews_by_month.png", dpi=120)
    plt.close(fig)

    # Save cleaned data
    listings.to_csv(OUT_DIR / "listings_cleaned.csv", index=False)
    print(f"\nCharts and cleaned CSV saved to: {OUT_DIR}")


if __name__ == "__main__":
    main()
