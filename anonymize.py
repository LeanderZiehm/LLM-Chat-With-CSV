import pandas as pd

# Define generalization functions
def age_range(age):
    """
    Group ages into decade ranges.
    For example, 23 -> "20-29"
    """
    lower = (age // 10) * 10
    upper = lower + 9
    return f"{lower}-{upper}"

def generalize_zip(zipcode):
    """
    Generalize zip code by taking the first three characters.
    """
    return zipcode[:3]

def generalize_birthdate(birthdate):
    """
    Convert a full date (YYYY-MM-DD) to just the year or year-month.
    Here we return the year.
    """
    return birthdate.split("-")[0]

# Check l-diversity within a group
def check_l_diversity(group, sensitive_key, l):
    """
    Returns True if the group has at least 'l' unique sensitive values.
    """
    sensitive_values = {record[sensitive_key] for record in group}
    return len(sensitive_values) >= l

def anonymizeDataframe(df, k, l, sensitive_key="sensitive"):
    """
    Anonymize a dataframe to achieve k-anonymity and l-diversity.
    
    Steps:
    1. Generalize quasi-identifiers.
    2. Group records by quasi-identifiers.
    3. For groups that fail l-diversity, suppress the sensitive attribute.
    """
    # Step 1: Generalize quasi-identifiers
    # df["age_range"] = df["age"].apply(age_range)
    # df["gen_zip"] = df["zip"].apply(generalize_zip)
    # df["gen_birthyear"] = df["birthdate"].apply(generalize_birthdate)
    
    # # Step 2: Group by the quasi-identifiers (age_range, gen_zip, gen_birthyear)
    # grouped = df.groupby(["age_range", "gen_zip", "gen_birthyear"])

    # # Step 3: Apply k-anonymity and l-diversity
    # final_records = []
    # for _, group in grouped:
    #     if len(group) < k:
    #         # For simplicity, we suppress sensitive attribute in groups that do not meet k-anonymity.
    #         group[sensitive_key] = "SUPPRESSED"
    #         final_records.append(group)
    #     else:
    #         if not check_l_diversity(group, sensitive_key, l):
    #             # If l-diversity is not met, suppress sensitive attribute in this group.
    #             group[sensitive_key] = "SUPPRESSED"
    #         final_records.append(group)

    # # Combine all the modified groups back into a single DataFrame
    # anonymized_df = pd.concat(final_records, ignore_index=True)

    # # Drop the generalized columns to return the anonymized dataset
    # anonymized_df.drop(columns=["age_range", "gen_zip", "gen_birthyear"], inplace=True)

    anonymized_df = df 

    return anonymized_df

if __name__ == "__main__":
    data = {
        "id": [1, 2, 3, 4, 5, 6],
        "age": [23, 27, 31, 24, 29, 33],
        "zip": ["12345", "12346", "12347", "12345", "12346", "12347"],
        "birthdate": ["1999-04-15", "1995-08-20", "1991-12-01", "1998-03-10", "1993-07-25", "1989-11-30"],
        "sensitive": ["A", "A", "B", "B", "A", "B"]
    }

    # Create DataFrame
    df = pd.DataFrame(data)

    # Desired k and l
    k = 2
    l = 2

    # Anonymize the DataFrame
    anonymized_df = anonymizeDataframe(df, k, l)

    # Display the result
    print(anonymized_df)
