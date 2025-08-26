# feature_schema

`feature_schema` is a lightweight Python package that automatically extracts and documents **feature metadata** from a pandas DataFrame.  
It’s designed for **machine learning workflows** where you need to understand, validate, or dynamically generate user inputs for model features.  

---

## Features

- Extract feature name
- Auto-detect feature types (`int`, `float`, `string`, `bool`, `datetime`)  
- Numeric metadata: min, max, range  
- Categorical metadata: unique values & counts  
- Nullability check: detect if features contain missing values  
- Human-readable docs (`__str__`) for quick schema inspection  
- Exportable schema to dict / DataFrame for further use  

---

## Installation

```bash
pip install feature_schema
```

## Usage

### 1. Create the Schema for a DataFrame

```python
import pandas as pd
from feature_schema import FeatureSchema

# Sample dataset
df = pd.DataFrame({
    "age": [25, 30, 40, 22],
    "salary": [50000.0, 60000.5, 80000.2, 45000.0],
    "city": ["NY", "SF", "LA", "NY"]
})

# Create Feature schema object
fs = FeatureSchema(df)

# Print schema (human readable)
print(fs.to_dict())

```
### Output:
```json
[
    {'column_name': 'age', 'dtype': 'int64', 'type': 'int', 'nullable': np.False_, 'min': 22.0, 'max': 40.0, 'unique_values': 4}, {'column_name': 'salary', 'dtype': 'float64', 'type': 'float', 'nullable': np.False_, 'min': 45000.0, 'max': 80000.2, 'unique_values': 4}, {'column_name': 'city', 'dtype': 'object', 'type': 'string', 'nullable': np.False_, 'unique_values': 3, 'unique_list': ['NY', 'SF', 'LA']}
]
```

### 2. Export Schema as Dictionary / DataFrame

```python
# As dictionary
schema_dict = fs.to_dict()
print(schema_dict)

# As DataFrame
schema_df = fs.to_dataframe()
print(schema_df)
```

## Why Use feature_schema?
- No more hardcoding feature names, types, and ranges
- Auto-generate Streamlit forms or FastAPI validation schemas
- Save schema along with ML models for reproducibility
- Helps teams document datasets automatically
- Helps to validate input