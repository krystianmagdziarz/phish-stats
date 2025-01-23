# APWG Phishing Statistics Dataset

This dataset contains phishing statistics transcribed from reports available on the [APWG Phishing Activity Trends Reports](https://apwg.org/trendsreports/) website.

The data has been manually extracted from quarterly and monthly reports published by the Anti-Phishing Working Group (APWG) and consolidated into JSON format for easier analysis.

## Data Source

All data comes from official APWG Phishing Activity Trends Reports published at: https://apwg.org/trendsreports/

The reports provide detailed statistics about phishing attacks observed by APWG member companies and partners, including:
- Number of unique phishing sites detected
- Most targeted industry sectors
- Countries hosting phishing sites
- And other phishing activity metrics

## Dataset Format

The data is stored in JSON format with the following structure:
- Year as the top level key
- Month as the nested key 
- Number of phishing sites detected as the value


