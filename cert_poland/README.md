# Polish CERT Phishing Statistics Analysis

This dataset contains phishing statistics from CERT Poland (CERT.PL), analyzing trends in phishing incidents reported and handled by the Polish national CERT team from 2009-2023.

## Overview

The analysis examines yearly phishing incident data reported to CERT Poland, providing insights into:

- Total phishing incidents reported
- Year-over-year growth trends
- Impact on Polish internet users and organizations

## Generated Graphs

The script generates the following visualizations in the `graphs/` directory:

- `total_incidents.png` - Yearly phishing incidents over time
- `yearly_growth.png` - Year-over-year growth rates in phishing incidents

## Data Source

The data is sourced from official CERT Poland annual reports available at: https://www.cert.pl/

The raw data is stored in `datasets/cert_cp.json` and contains yearly phishing statistics compiled from these reports.

## Usage

To generate the graphs and statistics:

```
python generate_graphs.py
```
