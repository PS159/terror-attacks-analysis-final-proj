# Final test

## Important details about the data set
- All dates that did not contain the day of the month, got by default the first day of the month, (it does not harm the analysis since the analysis does not refer to the days of the month).
- All dates that did not contain a month, got by default 'January'. the reason is that there are only a few months missing from the dataset, so that the impact on the analysis is insignificant.

## The logic of the structure
- The region is in a separate table for two reasons, first of all the region does not have a direct relation with the attack, secondly, the countries should be in a table of their own because of their dependence on the regions (3NF). 