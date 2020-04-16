sd_mean <- function(sd, population)  # same as the standard error of a mean
{
  mean_sd = sd / sqrt(population)

  return(mean_sd)
}


standard_deviation <- function(proportion, population)
{
  sd = sqrt( proportion * (1 - proportion) / population)

  return(sd)
}


standardize <- function(value, mean, sd)
{
  z = (value - mean) / sd

  return(z)
}


# create a function that returns the p-value of a certain test
t_value <- function(value, mean, sd, population)
{
  t = (value - mean) / sd_mean(sd, population)

  return(t)
}


# function for one sided p-value (the type parameter is whether you are computing z or p stats)
print_p_os <- function(sample_proportion, old_proportion, sd, population, type)
{
  # make calculations
  se = sd_mean(sd, population)
  z = (sample_proportion - old_proportion) / se

  # handle p value for greater than and less than
  if ('z' == type) { p = pnorm(-1 * z) }
  else if ('t' == type)
  {
    t = t_value(sample_proportion, old_proportion, sd, population)
    p = 1 - pt(t, population - 1)
  }
  else { return('Only use "z" or "t" as types') }


  # print the calculations and inputs
  print("One-Sided Test")
  print(sprintf("Old Proportion: %s", old_proportion))
  print(sprintf("New Proportion: %s", sample_proportion))
  print(sprintf("Population: %s", population))

  print('\n')

  # print hypotheses
  print(sprintf("Null Hypothesis: p = %s", old_proportion))
  if (sample_proportion > old_proportion)
  {
    print(sprintf("Alternative Hypothesis p > %s", old_proportion))
  }
  else
  {
    print(sprintf("Alternative Hypothesis p < %s", old_proportion))
  }

  print("\n")

  print(sprintf("Standard Error: %s", se))

  if ('z' == type) {print(sprintf("z-statistic: %s", z)) }
  else if ('t' == type) { {print(sprintf("t-statistic: %s", z)) } }

  print(sprintf("P-value: %s", p))
}


# returns the difference in probability given a start and end value (not proportion)
probdiff <- function(start, end, mean, sd, df)
{
  p_start = pt(t_value(start, mean, sd, df), df=df)
  p_end = pt(t_value(end, mean, sd, df), df=df)

  pdiff = p_end - p_start

  return(pdiff)

}


# create a function to get the confidence interval (handles for one-sided or not)
mean_confidence_interval <- function(mean, sd, population, alpha, one_sided)
{

  # subtract 1 from population to get the correct t-value for computing the mean confidence interval
  if (one_sided){ t = qt(alpha, population) }
  else { t = qt(alpha / 2, population) }


  se = sd_mean(sd, population)

  lower = mean - (se * abs(t))

  higher = mean + (se * abs(t))

  print(sprintf("t-value: %s", t))
  print(sprintf("Standard Error: %s", se))
  print(sprintf("Lower End: %s", lower))
  print(sprintf("Higher End: %s", higher))
}


sample_sizer <- function(mean, current_sd, target_me, alpha, one_sided)
{
  if (one_sided) { z = qnorm(alpha) }
  else { z = qnorm(alpha/2) }


  population = (z * current_sd / target_me)**2

  print(sprintf("z-statistic: %s", z))
  print(sprintf("Sample size needed: %s", population))
}


sd_diff_means <- function(sd1, sd2, n1, n2)
{
  var1 = (sd1**2) / n1
  var2 = (sd2**2) / n2

  sd = sqrt(var1 + var2)

  return(sd)
}


# get degrees of freedom for difference of means
diff_df <- function(n1, n2, sd1, sd2, se)
{
  df = (se ** 4) / ( ( (sd1**4 / n1**2) / (n1 - 1) ) + ( (sd2**4 / n2**2) / (n2 - 1) ) )

  return(df)
}


# array format: c(mean, sd, population)
t_value_diff_means <- function(array1, array2, delta)
{
  # unpack the arrays
  mean1 = array1[1]
  sd1 = array1[2]
  n1 = array1[3]

  mean2 = array2[1]
  sd2 = array2[2]
  n2 = array2[3]

  se = sd_diff_means(sd1, sd2, n1, n2)

  t = (mean1 - mean2 - delta) / se

  df = diff_df(n1, n2, sd1, sd2, se)

  p = pt(-abs(t), df) * 2

  print(sprintf("Degrees of Freedom: %s", df))
  print(sprintf("Standard Error: %s", se))
  print(sprintf("t-value: %s", t))
  print(sprintf("P-value: %s", p))

}

# find confidence intervals for a difference of means
# array format: c(mean, sd, population)
mean_diff_confidence_intervals <- function(array1, array2, delta, alpha)
{
  # unpack the arrays
  mean1 = array1[1]
  sd1 = array1[2]
  n1 = array1[3]

  mean2 = array2[1]
  sd2 = array2[2]
  n2 = array2[3]

  diff = abs(mean1 - mean2)

  se = sd_diff_means(sd1, sd2, n1, n2)

  df = diff_df(n1, n2, sd1, sd2, se)

  # need to divide alpha for 2-sided test
  t = abs(qt(alpha/2, df))

  lower = diff - (t * se)
  higher = diff + (t * se)

  print(sprintf("Difference: %s", diff))
  print(sprintf("Degrees of Freedom: %s", df))
  print(sprintf("t-value: %s", t))
  print(sprintf("Standard Error: %s", se))
  print(sprintf("Lower End: %s", lower))
  print(sprintf("Higher End: %s", higher))

}


df_pooled <- function(n1, n2)
{
  df = n1 + n2 - 2

  return(df)
}


sd_pooled <- function(sd1, sd2, n1, n2)
{
  s_squared = ( ( (n1 - 1) * sd1**2 ) + ( (n2 - 1) * sd2**2 ) ) / (df_pooled(n1, n2))

  s = sqrt(s_squared)

  return(s)
}

sd_diff_means_pooled <- function(sd1, sd2, n1, n2)
{
  sd_pooled = sd_pooled(sd1, sd2, n1, n2)

  se = sd_pooled * sqrt((1/n1) + (1/n2))

  return(se)
}


mean_diff_confidence_intervals_pooled <- function(array1, array2, delta, alpha)
{
  # unpack the arrays
  mean1 = array1[1]
  sd1 = array1[2]
  n1 = array1[3]

  mean2 = array2[1]
  sd2 = array2[2]
  n2 = array2[3]

  diff = abs(mean1 - mean2)

  se = sd_diff_means_pooled(sd1, sd2, n1, n2)

  df = df_pooled(n1, n2)

  # need to divide alpha for 2-sided test
  t = abs(qt(alpha/2, df))

  lower = diff - (t * se)
  higher = diff + (t * se)

  print(sprintf("Difference: %s", diff))
  print(sprintf("Degrees of Freedom: %s", df))
  print(sprintf("t-value: %s", t))
  print(sprintf("Standard Error: %s", se))
  print(sprintf("Lower End: %s", lower))
  print(sprintf("Higher End: %s", higher))

}

t_paired <- function(pairwise_differences, sd, population, delta)
{
  # standard deviation for a paired t-value is the same as the standard deviation for 2 means
  se = sd_means(sd, population)

  t = (pairwise_differences - delta) / se

  return(t)
}

mean_diff_confidence_intervals_paired <- function(pairwise_differences, sd, delta, population, alpha)
{
  se = sd_means(sd, population)

  # use n-1 for degrees of freedom
  t = abs(qt(alpha/2, population))

  lower = pairwise_differences - (t * se)
  higher = pairwise_differences + (t * se)

  print(sprintf("t-value: %s", t))
  print(sprintf("Standard Error: %s", se))
  print(sprintf("Lower End: %s", lower))
  print(sprintf("Higher End: %s", higher))

}

# other functions (built in)
# get t-value (from alpha and degrees of freedom) --> qt(alpha, df) --> 1-sided
# qt(alpha/2, df) --> 2-sided
# get the p-value from a t-value and degrees of freedom --> pt(t-value, df)
# get the z-score from an alpha value --> qnorm(alpha) ** make sure to divide by 2 if a 2-sided test
# get alpha from z-score --> pnorm(z-score)


# Chapter 12
# Exercises 2, 4, 6, 8, 10, 12, 14, 18, 20, 24, 28, 40, 46, 48.





