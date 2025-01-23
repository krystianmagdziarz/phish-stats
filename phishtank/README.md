# PhishTank Statistics Analysis

This project analyzes historical data from PhishTank to understand trends in phishing reports, verification times, and community participation from 2009-2017.

## Overview

The analysis examines several key metrics:

- Total phishing submissions
- Valid phishing reports
- Invalid phishing reports  
- Median time to verify reports
- Verification time per submission ratio
- Total community votes

## Generated Graphs

The script generates the following visualizations in the `graphs/` directory:

- `total_submissions.png` - Monthly phishing submissions over time
- `valid_phishes.png` - Valid phishing reports over time
- `invalid_phishes.png` - Invalid phishing reports over time
- `median_time.png` - Median verification time trends
- `median_time_ratio.png` - Ratio of verification time to total submissions
- `total_votes.png` - Community voting participation over time

## Data Source

The raw data is stored in `datasets/phishtank_stats.json` and contains monthly statistics from PhishTank's public data.

## Usage

To generate the graphs and statistics:

```bash
python fetch_datasets.py
python generate_graphs.py
```

This will create the graphs in the `graphs/` directory.
