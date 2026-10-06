def get_value_via_concept(financial_data, concept_name):

    result = financial_data.xb.query().by_concept(concept_name, exact=True).to_dataframe()

    if result.empty:
        return None

    if len(result) > 1:
        undimensioned = result[result["is_dimensioned"] == False]
        if not undimensioned.empty:
            result = undimensioned
        result = result.sort_values("fiscal_year", ascending=False)

    return result.iloc[0]["numeric_value"]