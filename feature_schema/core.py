import pandas as pd

class FeatureSchema:
    def __init__(self, df: pd.DataFrame = None):
        self.df = df
        self.schema = self._extract_schema(df)

    def __str__(self):
        summary = ["FeatureSchema Summary:"]
        for feat in self.schema:
            line = f"- {feat['column_name']} (type: {feat['type']}, dtype: {feat['dtype']})"

            if feat['type'] in ["int", "float"]:
                line += f", range: [{feat['min']}, {feat['max']}]"
            elif feat['type'] == "string":
                if "unique_list" in feat:
                    choices_preview = feat['unique_list'][:5]  # show first 5 unique values
                    line += f", choices: {choices_preview}"
                    if len(feat['unique_list']) > 5:
                        line += f" ... (+{len(feat['unique_list'])-5} more)"
            elif feat['type'] == "bool":
                line += ", values: [True, False]"
            elif feat['type'] == "datetime":
                line += f", min: {feat['min']}, max: {feat['max']}"

            if feat["nullable"]:
                line += " (nullable)"

            summary.append(line)

        return "\n".join(summary)



    def _extract_schema(self, df: pd.DataFrame):
        schema = []
        for col in df.columns:
            series = df[col]
            dtype = str(series.dtype)
            ftype = self._get_type(series)

            feature_info = {
                "column_name": col,
                "dtype": dtype,
                "type": ftype,
                "nullable": series.isnull().any()
            }

            if ftype in ["int", "float"]:
                feature_info.update({
                    "min": float(series.min(skipna=True)),
                    "max": float(series.max(skipna=True)),
                    "unique_values": int(series.nunique(dropna=True))
                })
            elif ftype == "string":
                unique_vals = series.dropna().unique().tolist()
                feature_info.update({
                    "unique_values": len(unique_vals),
                    "unique_list": unique_vals  # <-- store all unique string values
                })
            else:
                feature_info.update({
                    "unique_values": int(series.nunique(dropna=True))
                })

            schema.append(feature_info)

        return schema

    def _get_type(self, series: pd.Series):
        if pd.api.types.is_float_dtype(series):
            return "float"
        elif pd.api.types.is_integer_dtype(series):
            return "int"
        elif pd.api.types.is_object_dtype(series) or pd.api.types.is_categorical_dtype(series):
            return "string"
        elif pd.api.types.is_bool_dtype(series):
            return "bool"
        elif pd.api.types.is_datetime64_any_dtype(series):
            return "datetime"
        else:
            return "unknown"

    def to_dict(self):
        return self.schema

    def to_dataframe(self):
        return pd.DataFrame(self.schema)

    
    def __help__(self):
        """
        Display documentation and a summary of the feature schema.
        """
        doc = """
            Feature_Schema: 
            ----------------
            A class to extract and describe feature schemas from a pandas DataFrame.

            Attributes:
            - df: pandas DataFrame used to extract schema
            - schema: list of dictionaries containing metadata for each feature

            Schema dictionary contains:
            - column_name: column name
            - dtype: pandas dtype
            - type: simplified type ('int', 'float', 'string', 'bool', 'datetime', 'unknown')
            - nullable: True if the column has missing values
            - min / max: min/max values for numeric columns
            - unique_values: number of unique values
            - unique_list: list of unique values (for string/categorical columns)

            Methods:
            - to_dict(): returns schema as a list of dictionaries
            - to_dataframe(): returns schema as a pandas DataFrame
            - __str__(): human-readable summary of the schema
            - __help__(): print this documentation
            """
        print(doc)

