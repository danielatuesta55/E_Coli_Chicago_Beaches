# E. coli Beach Predictions

# Can we use previously recorded levels of precipitation and instances of e. coli to predict the safety of a beach?

Inspired by [these](https://www.chicagoriver.org/issues/policy/climate-change) [articles](https://www.nytimes.com/interactive/2021/07/07/climate/chicago-river-lake-michigan.html) concerning precipitation effects on the Chicago river and Lake Michigan, we set out to predict one serious consequence of a changing climate. By training a machine algorithm to analyze precipitation levels and incidence of e. coli in beaches, we hope to better predict how precipitation can affect waterborne diseases as well as protect beachgoers.

# Predicted Workflow

1. Acquire [beach](https://data.cityofchicago.org/Parks-Recreation/Beach-Lab-Data/2ivx-z93u) and precipitation data.
2. Clean data as needed (renaming headers, changing datatypes, organizing dates, etc).
3. Merge datasets on location.
4. Split data into training and testing sets.
5. Train machine on training set.
6. Form regression model.
7. Test model and analyze accuracy.
8. Tune model as necessary.
9. Use model to predict e. coli levels.
10. Visualize predictions on deployed app.
