#!/usr/bin/env python3
import sys

from pandas import DataFrame, read_csv


def analysis(chat_id: int):
    history_df: DataFrame = read_csv("data/%s-history.csv" % chat_id)
    members_df: DataFrame = read_csv("data/%s-members.csv" % chat_id)

    grouped_df: DataFrame = history_df.groupby("User ID") \
        .size() \
        .reset_index(name="Count") \
        .merge(members_df, on="User ID", how="inner") \
        .sort_values("Count", ascending=False)
    grouped_df.to_csv("data/%s-grouped.csv" % chat_id, index=False)

    keep_df = grouped_df[grouped_df["Count"] > 3]
    diff = (members_df["Status"] == "member") & \
           (~members_df["User ID"].isin(keep_df["User ID"]))
    members_df[diff] \
        .to_csv("data/%s-removable.csv" % chat_id, index=False)


def main():
    for chat_id in sys.argv[1:]:
        analysis(int(chat_id))


if __name__ == "__main__":
    main()
