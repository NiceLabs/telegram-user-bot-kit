#!/usr/bin/env python3
import sys

from pandas import DataFrame, Series, read_csv


def main():
    chat_id = int(sys.argv[1])
    history_df: DataFrame = read_csv("data/%s-history.csv" % chat_id)
    members_df: DataFrame = read_csv("data/%s-members.csv" % chat_id)
    members_df = members_df[members_df["Status"] == "member"]
    merged: DataFrame = history_df.merge(members_df, on="User ID", how="inner")
    grouped: DataFrame = merged \
        .groupby("User ID") \
        .size() \
        .reset_index(name="Count") \
        .sort_values("Count", ascending=False)
    grouped = grouped[grouped["Count"] > 3]
    grouped.to_csv("data/%s-grouped.csv" % chat_id, index=False)

    removable = Series(list(set(members_df["User ID"]) - set(grouped["User ID"])), name="User ID") \
        .sort_values(ascending=False)
    removable.to_csv("data/%s-removable.csv" % chat_id, index=False)


if __name__ == "__main__":
    main()
