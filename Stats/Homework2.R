library(readxl)
library(ggplot2)
library(tidyverse)
  library(lubridate)
library(lattice)
library(scales)
library(hash)

# 2.44
master_dir = "/Users/naveenailawadi/Desktop/OPIM\ 173/Homework\ 2"
setwd(master_dir)

# create a folder for exports and set it to current
dir.create('2.44')
setwd('2.44')

# load data
minimum_wage_data = read_excel("Minimum_wage_workers.xlsx")
women_data = minimum_wage_data$'Hourly Workers -- Women'
age_labels = minimum_wage_data$Age

# process for pie chart labels
percent_labels = round(women_data/sum(women_data)*100)
percent_labels = paste("(", percent_labels, "%)", sep = '')
women_labels = paste(age_labels, percent_labels)

# set a title
women_title = "Women Hourly Workers by Age"

# export pie chart
jpeg(filename = "PieChart.jpg", width=520, height=480)
pie(women_data, labels = women_labels, col=rainbow(length(women_data)),
    main=women_title)
dev.off()

# export bar plot with same data
jpeg(filename = "Barplot.jpg", width=520, height=480)
barplot(women_data, main=women_title, xlab="Age Ranges", names.arg=age_labels,
    col=rainbow(length(women_data)))
dev.off()

# load data for women and men at or below minimum wage
men_below_minimum_wage = minimum_wage_data$'At or Below Minimum Wage -- Men'
men_below_minimum_wage = round(men_below_minimum_wage/sum(men_below_minimum_wage)*100)
women_below_minimum_wage = minimum_wage_data$'At or Below Minimum Wage -- Women'
women_below_minimum_wage = round(women_below_minimum_wage/sum(women_below_minimum_wage)*100)

# create a side by side barplot with mens and womens data
jpeg(filename = "SideBySide.jpg", width=520, height=480)
side_by_side = rbind(men_below_minimum_wage, women_below_minimum_wage)
barplot(side_by_side, beside=T, xlab="Age Ranges", ylab = "Percent (%)",
        names.arg = age_labels, col = c("blue", "red"), 
        main="Men And Women Working At or Below Minimum Wage")
legend("topright", c("Men","Women"), pch=15,
       col=c("blue", "red"),
       bty="n")
dev.off()


# 3.2

# create and set new directory
setwd(master_dir)
dir.create('3.2')
setwd('3.2')

# load in purchases data
purchases = c(39.05, 2.73, 32.92, 47.51, 37.91, 34.35, 64.48, 51.96, 56.95, 81.58, 
              47.8, 11.72, 21.57, 40.83, 38.24, 32.98, 75.16, 74.3, 47.54, 65.62)
purchases = sort(purchases)
purchases_df = as.data.frame(purchases)

# create the histogram with bar width 20
jpeg(filename = "Histogram Bar Width 20.jpg", width=520, height=480)
ggplot(data=purchases_df, aes(purchases)) + theme_classic() + 
  theme(plot.title = element_text(hjust = 0.5)) + 
  geom_histogram(bins = 5, breaks=c(0, 20, 40, 60, 80, 100),
                 col="black", 
                 fill="red") + 
  labs(title="Consumer Spending Patterns (5 Bins)", x="Purchase Amount", y="Count") +
  scale_x_continuous(breaks = c(0, 20, 40, 60, 80, 100))
dev.off()

# create the histogram with bar width 10
jpeg(filename = "Histogram Bar Width 10.jpg", width=520, height=480)
ggplot(data=purchases_df, aes(purchases)) + theme_classic() + 
  theme(plot.title = element_text(hjust = 0.5)) + 
  geom_histogram(bins = 10, breaks=seq(0, 100, by = 10),
                 col="black", 
                 fill="red") + 
  labs(title="Consumer Spending Patterns (10 Bins)", x="Purchase Amount", y="Count") + 
  scale_x_continuous(breaks = seq(0, 100, by = 10))
dev.off()

# create a relative frequency list (all in decimal values, not percents)
# get rid of line in middle of it
jpeg(filename = "Relative Frequency Histogram.jpg", width=520, height=480)
purchases_percent = round(purchases/sum(purchases)*100)
purchases_df_percent = as.data.frame(purchases_percent)
ggplot(data=purchases_df_percent, aes(purchases_percent)) + theme_classic() + 
  theme(plot.title = element_text(hjust = 0.5)) + 
  geom_histogram(aes(y = stat(purchases_percent) / sum(purchases_percent)), 
                 breaks=seq(0, 100, by = 10),
                 col="black", 
                 fill="red") + 
  labs(title="Consumer Spending Patterns", x="Purchase Amount", y="Count") +
  scale_y_continuous(labels = scales::percent)
dev.off()




ggplot(data=purchases_df, aes(purchases)) + theme_classic() + 
  theme(plot.title = element_text(hjust = 0.5)) + 
  geom_histogram(bins = 10, breaks=seq(0, 100, by = 10),
                 col="black", 
                 fill="red") + 
  labs(title="Consumer Spending Patterns (10 Bins)", x="Purchase Amount", y="Percent (%)") + 
  scale_x_continuous(breaks = seq(0, 100, by = 10))



# stem and leaf plot
purchases_rounded = round(purchases)

# output (did not save.,,)
jpeg(filename="stem.jpeg",width=480,height=480,
     units="px",pointsize=12)
stem(purchases_rounded, scale = 2)
dev.off()

setwd(master_dir)

# 3.4

# Create the modefunction.
getmode <- function(v) {
   uniqv <- unique(v)
   uniqv[which.max(tabulate(match(v, uniqv)))]
}

purchases_mode = getmode(purchases)

IQR = quantile(purchases, prob=.75)-quantile(purchases, prob=.25)
min_q = quantile(purchases, prob=0.25) - 1.5*IQR
max_q = quantile(purchases, prob=0.75) + 1.5*IQR
OutVals = boxplot(purchases, plot=F)$out

# 3.6

# 6a --> expect the mean purchase to be greater than the median because
# the data is right skewed

mean_purchase = mean(purchases)

median_purchase = median(purchases)


# 3.8

# load data into calculator
count = 1
for (i in purchases) {
  print(i)
  input = readline(prompt="")
  count = count + 1
  if (count == 1) {break}
}

# tukey's method by hand
q1_tukey = median(append(purchases[1 : 10], median_purchase))
q3_tukey = median(append(median_purchase, purchases[10:20]))
tukey_IQR = q3_tukey - q1_tukey



# 3.12

# standardize minimum and maximum purchase

# find stdev, min, and max
min_purchase = purchases[1]
max_purchase = purchases[20]
stdev = sd(purchases)


# calculate z scores

get_z_score <- function(value, mean, stdev) {
  z_score = (value - mean) / stdev
  return(z_score)
}

min_z_score = get_z_score(min_purchase, mean_purchase, stdev)
max_z_score = get_z_score(max_purchase, mean_purchase, stdev)


# 3.14

# load correct directories
setwd(master_dir)
dir.create('3.14')
setwd('3.14')

# create boxplot and output to a jpeg
jpeg(filename = "PurchasesBoxplot.jpg", width=520, height=480)
boxplot(purchases, col="green", cex.main = 2, 
        ylab = "Purchase amount in $", main = "Purchases")
dev.off()



# 3.22

IQR22 = 49 - 24
min_q22 = 24 - 1.5*IQR22
max_q22 = 49 + 1.5*IQR22


# 3.34

# get correct directory
setwd(master_dir)
setwd('3.34')

# read in data
car_discount_data = read_excel('Car_discounts.xlsx')

# create a five number summary for the data
car_discounts = car_discount_data$'Discount'
car_ages = car_discount_data$'Age'
car_incomes = car_discount_data$'Income'

# make a function to create five number summaries
five_number_summary <- function(data) {
  data = sort(data)
  data_min = min(data)
  data_max = max(data)
  Q1 = quantile(data, prob = 0.25)
  Q3 = quantile(data, prob = 0.75)
  median = median(data)
  
  # format: min, Q1, median, Q2, max
  print("Summary format: Min   Q1   Med   Q3   Max")
  summary = c(data_min, Q1, median, Q3, data_max)
  return(summary)
}

# run the function to create the summaries
discount_summary = five_number_summary(car_discounts)
age_summary = five_number_summary(car_ages)
income_summary = five_number_summary(car_incomes)

# create discount boxplot
jpeg(filename = "DiscountsBoxplot.jpg", width=520, height=480)
boxplot(car_discounts, col="red", cex.main = 2, 
        ylab = "Amount in $", main = "Discounts")
dev.off()

# create ages boxplot
jpeg(filename = "AgesBoxplot.jpg", width=520, height=480)
boxplot(car_ages, col="blue", cex.main = 2, 
        ylab = "Age in Years", main = "Ages")
dev.off()

# create incomes boxplot
jpeg(filename = "IncomesBoxplot.jpg", width=520, height=480)
boxplot(car_discounts, col="green", cex.main = 2, 
        ylab = "Income in $", main = "Incomes")
dev.off()


# 3.36
setwd(master_dir)
setwd('3.36')

price_per_gallon_data = read_excel("Gas_Prices_2013.xlsx")
price_per_gallon = price_per_gallon_data$'Price/Gal($)'

# create stem and leaf plot
stem(price_per_gallon, scale = .5, width = 100)


# 3.46

# compute range
real_estate_min = 672
real_estate_max = 5228
real_estate_range = real_estate_max - real_estate_min

# compute distribution
real_estate_Q1 = 1342
real_estate_Q3 = 2223
real_estate_IQR = real_estate_Q3 - real_estate_Q1


# 3.48

# set correct directory
setwd(master_dir)
setwd('3.48')

# load dataset
insurance_data = read_excel('Insurance_profits.xlsx')
insurance_profit = insurance_data$'Profit'

# create a boxplot with a summary of the profits
jpeg(filename = "ProfitsBoxplot.jpg", width=520, height=480)
boxplot(insurance_profit, col="green", cex.main = 2, 
        ylab = "Profit in $", main = "Profits")
dev.off()

# get the five number summary for the data
profit_summary = five_number_summary(insurance_profit)

# get info on the center of the data
profit_median = profit_summary[3]
profit_mean = mean(insurance_profit)

# get info on the spread of the data

profit_stdev = sd(insurance_profit)
profit_Q1 = profit_summary[2]
profit_Q3 = profit_summary[4]
profit_IQR =profit_Q3 - profit_Q1 


# find any outliers
min_profit_outlier = profit_Q1 - 1.5*profit_IQR
max_profit_outlier = profit_Q3 + 1.5*profit_IQR

# create lists to add outliers to
high_outliers = c()
low_outliers = c()

# check for outliers
no_outliers = TRUE
for (profit in insurance_profit) {
  if (profit > max_profit_outlier) {
    high_outliers = append(high_outliers, profit)
    no_outliers = FALSE
    
  }
  else if (profit < min_profit_outlier) {
    low_outliers = append(low_outliers, profit)
    no_outliers = FALSE
  }
}

if (no_outliers) {
  print("No outliers found.")
  } else {
  print("High Outliers: ")
  print(high_outliers)
  print("Low Outliers: ")
  print(low_outliers)
}







