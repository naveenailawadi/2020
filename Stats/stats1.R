# discrete probability functions
# with the arrays, a value can be passed instead (just use a probability of 1)

expected_value <- function(value_array, probability_array)
{
  # join the arrays
  combined_array = value_array * probability_array
  
  # get the mean by adding them
  mean = sum(combined_array)
  
  return(mean)
}

sd_discrete <- function(value_array, probability_array)
{
  mean = expected_value(value_array, probability_array)
  
  difference_array = ((value_array - mean)**2) * probability_array
  
  sd = sqrt(sum(difference_array))
  
  return(sd)
  
}

var_discrete <- function(value_array, probability_array)
{
  sd = sd_discrete(value_array, probability_array)
  
  variance = sd**2
  
  return(variance)
}

cov_discrete <- function(value_array1, probability_array1, value_array2, probability_array2)
{
  discrete_mean1 = expected_value(value_array1, probability_array1)
  discrete_mean2 = expected_value(value_array2, probability_array2)
  
  covariance = expected_value(value_array1 - discrete_mean1, probability_array1) * expected_value(value_array2 - discrete_mean2, probability_array2)
  
  return(covariance)
}

var_dicrete_sum <- function(value_array1, probability_array1, value_array2, probability_array2)
{
  var1 = var_discrete(value_array1, probability_array1)
  var2 = var_discrete(value_array2, probability_array2)
  
  cov = cov_discrete(value_array1, probability_array1, value_array2, probability_array2)
  
  variance = var1 + var2 + 2 * cov
  
  return(variance)
}

var_dicrete_difference <- function(value_array1, probability_array1, value_array2, probability_array2)
{
  var1 = var_discrete(value_array1, probability_array1)
  var2 = var_discrete(value_array2, probability_array2)
  
  cov = cov_discrete(value_array1, probability_array1, value_array2, probability_array2)
  
  variance = var1 + var2 - 2 * cov
  
  return(variance)
}

corr_discrete <- function(value_array1, probability_array1, value_array2, probability_array2)
{
  sd1 = sd_discrete(value_array1, probability_array1)
  sd2 = sd_discrete(value_array2, probability_array2)
  
  cov = cov_discrete(value_array1, probability_array1, value_array2, probability_array2)
  
  corr = cov / (sd1 * sd2)
  
  return(corr)
}


# functions using standardization
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


# function for finding a p-value (the type parameter is whether you are computing z or p stats)
# can use NULL as sd if there is no given standard deviation
# can use proportions or amounts
p_test <- function(old_amount, sample_amount, sd, population, type, one_sided)
{
  
  # convert proportions to amounts
  if (sample_amount < 1) { sample_amount = sample_amount * population }
  if (old_amount < 1) { old_amount = old_amount * population }
  
  # make calculations
  if (length(sd) == 0)
  {
    sample = old_amount / population
    
    se = standard_deviation(sample, population)
    
    sd_new = se * population
    
    z = ((sample_amount / population) - (old_amount/population)) / se
  }
  else
  {
    se = sd_mean(sd, population)
    
    # this z is the same as a t-value for the same thing (se uses population)
    z = (sample_amount - old_amount) / se
  }
  
  
  # handle p value for greater than and less than
  if ('z' == type) { p = pnorm(-1 * abs(z)) }
  else if ('t' == type)
  {
    t = abs(t_value(sample_amount, old_amount, sd, population))
    p = 1 - pt(t, population - 1)
  }
  else { return('Only use "z" or "t" as types') }
  
  if (! one_sided) { p = 2 * p}
  
  
  # print the calculations and inputs
  cat(sprintf("Old Amount: %s\n", old_amount))
  cat(sprintf("New Amount: %s\n", sample_amount))
  if (length(sd) == 0) { cat(sprintf("Standard Deviation: %s\n", sd_new)) }
  cat(sprintf("Population: %s\n", population))
  
  cat('\n')
  
  # print hypotheses
  
  
  cat(sprintf("Null Hypothesis: p = %s\n", old_amount))
  if (! one_sided)
  {
    cat(sprintf("Alternative Hypothesis: p != %s\n", old_amount))
  }
  else if (sample_amount > old_amount)
  {
    cat(sprintf("Alternative Hypothesis: p > %s\n", old_amount))
  }
  else
  {
    cat(sprintf("Alternative Hypothesis: p < %s\n", old_amount))
  }
  
  cat("\n")
  
  cat(sprintf("Standard Error: %s\n", se))
  
  if ('z' == type) {cat(sprintf("z-statistic: %s\n", z)) }
  else if ('t' == type) { cat(sprintf("t-statistic: %s\n", z)) }
  
  cat(sprintf("P-value: %s", p))
}

# a way to form confidence intervals
confidence_interval <- function(sample_amount, population, alpha)
{
  # convert proportions to amounts
  if (sample_amount < 1) { sample_amount = sample_amount * population }
  
  sample = sample_amount / population
  
  se = standard_deviation(sample, population)
  
  # assume a 2-sided test
  z = abs(qnorm(alpha/2))
  
  me = se * abs(z)
  
  lower = sample - me
  
  higher = sample + me
  
  cat(sprintf("Standard Error: %s\n", se))
  cat(sprintf("z-score: %s\n", z))
  cat(sprintf("Margin of Error: %s\n", me))
  cat(sprintf("Lower End (proportion): %s\n", lower))
  cat(sprintf("Higher End (proportion): %s\n", higher))
  
}

# returns the difference in probability given a start and end value (not proportion)
prob_diff <- function(start, end, mean, sd, df)
{
  t1 = t_value(start, mean, sd, df)
  t2 = t_value(end, mean, sd, df)
  
  p_start = pt(t1, df=df)
  p_end = pt(t2, df=df)
  
  pdiff = abs(p_end - p_start)
  
  cat(sprintf("Start t-value: %s\n", t1))
  cat(sprintf("Start Probability (below): %s\n\n", p_start))
  cat(sprintf("End t-value (below): %s\n", t2))
  cat(sprintf("End Probability (below): %s\n\n", p_end))
  cat(sprintf("Probability Difference (between): %s\n", pdiff))
  
}

# create a function to get the confidence interval (handles for one-sided or not)
mean_confidence_interval <- function(mean, sd, population, alpha, one_sided)
{
  
  # subtract 1 from population to get the correct t-value for computing the mean confidence interval
  if (one_sided)
  {
    t = abs(qt(alpha, population - 1))
    p = 1 - pt(t, population - 1)
  }
  else
  {
    t = abs(qt(alpha / 2, population - 1))
    p = 1 - pt(t, population - 1)
    p = 2 * p
  }
  
  
  se = sd_mean(sd, population)
  
  me = se * t
  
  lower = mean - me
  
  higher = mean + me
  
  cat(sprintf("t-value: %s\n", t))
  cat(sprintf("P-value: %s\n", p))
  cat(sprintf("Standard Error: %s\n", se))
  cat(sprintf("Margin of Error: %s\n", me))
  cat(sprintf("Lower End: %s\n", lower))
  cat(sprintf("Higher End: %s\n", higher))
}


# use NULL as sample_proportion if there none is provided --> will use standard
# of 0.5 for sample proportion
sample_sizer <- function(sample_proportion, target_me, alpha, one_sided)
{
  # using z-score because degrees of freedom are unknown --> can't use t-value
  if (one_sided) { z = qnorm(alpha) }
  else { z = qnorm(alpha/2) }
  
  if (length(sample_proportion) == 0)
  {
    population = ((z / target_me)**2) * 0.25
  }
  else
  {
    population = (z**2)*(sample_proportion - sample_proportion**2) / (target_me**2)
  }
  
  cat(sprintf("z-statistic: %s\n", z))
  cat(sprintf("Sample size needed: %s\n", population))
}
# other functions (built in) that deal with standardization

# get t-value (from alpha and degrees of freedom) --> qt(alpha, df) --> 1-sided
#   qt(alpha/2, df) --> 2-sided

# get the p-value from a t-value and degrees of freedom --> pt(t-value, df)
# get the z-score from an alpha value --> qnorm(alpha) ** make sure to divide by 2 if a 2-sided test
# get p-value from z-score --> pnorm(z-score)
# get confidence interval from array --> t.test(array1, array2, alternative="one.sided/two.sided",
#                                             conf.level = confidence, var.equal = T/F, paired = T/F)






# functions for comparing means
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
  
  cat(sprintf("Degrees of Freedom: %s\n", df))
  cat(sprintf("Standard Error: %s\n", se))
  cat(sprintf("t-value: %s\n", t))
  cat(sprintf("P-value: %s\n", p))
  
}

# function for finding a p-value of different means (the type parameter is whether you are computing z or p stats)
p_value_diff_means <- function(array1, array2, delta)
{
  # unpack the arrays
  mean1 = array1[1]
  sd1 = array1[2]
  n1 = array1[3]
  
  mean2 = array2[1]
  sd2 = array2[2]
  n2 = array2[3]
  
  # create some preliminary information to use in calculations
  se = sd_diff_means(sd1, sd2, n1, n2)
  df = diff_df(n1, n2, sd1, sd2, se)
  
  t = (mean1 - mean2) / se
  
  p = 2 * (1 - pt(t, df))
  
  cat(sprintf("Null Hypothesis: %s = %s\n", mean1, mean2))
  cat(sprintf("Alternative Hypothesis: %s != %s\n", mean1, mean2))
  
  cat(sprintf("Mean Difference: %s\n", (mean1 - mean2)))
  cat(sprintf("Standard Error: %s\n", se))
  cat(sprintf("Degrees of Freedom: %s\n", df))
  
  cat(sprintf("t-value: %s\n", t))
  cat(sprintf("P-value: %s\n", p))
}

# find confidence intervals for a difference of means
# array format: c(mean, sd, population)
mean_diff_confidence_interval <- function(array1, array2, delta, alpha)
{
  # unpack the arrays
  mean1 = array1[1]
  sd1 = array1[2]
  n1 = array1[3]
  
  mean2 = array2[1]
  sd2 = array2[2]
  n2 = array2[3]
  
  diff = mean1 - mean2
  
  se = sd_diff_means(sd1, sd2, n1, n2)
  
  df = diff_df(n1, n2, sd1, sd2, se)
  
  # need to divide alpha for 2-sided test
  t = abs(qt(alpha/2, df))
  
  me = t * se
  
  lower = diff - me
  higher = diff + me
  
  p = 1 - pt(t, df)
  
  cat(sprintf("Difference: %s\n", diff))
  cat(sprintf("Degrees of Freedom: %s\n", df))
  cat(sprintf("t-value: %s\n", t))
  cat(sprintf("P-value: %s\n", p))
  cat(sprintf("Standard Error: %s\n", se))
  cat(sprintf("Margin of Error: %s\n", me))
  cat(sprintf("Lower End: %s\n", lower))
  cat(sprintf("Higher End: %s\n", higher))
  
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


# array format: c(mean, sd, population)
t_pooled <- function(array1, array2, delta)
{
  # unpack the arrays
  mean1 = array1[1]
  sd1 = array1[2]
  n1 = array1[3]
  
  mean2 = array2[1]
  sd2 = array2[2]
  n2 = array2[3]
  
  se = sd_pooled(sd1, sd2, n1, n2)
  
  t = (mean1 - mean2 - delta) / se
  
  df = df_pooled(n1, n2)
  
  p = pt(-abs(t), df) * 2
  
  cat(sprintf("Degrees of Freedom: %s\n", df))
  cat(sprintf("Standard Error: %s\n", se))
  cat(sprintf("t-value: %s\n", t))
  cat(sprintf("P-value: %s\n", p))
  
  return(t)
}



# array format: c(mean, sd, population)
mean_diff_confidence_interval_pooled <- function(array1, array2, delta, alpha)
{
  # unpack the arrays
  mean1 = array1[1]
  sd1 = array1[2]
  n1 = array1[3]
  
  mean2 = array2[1]
  sd2 = array2[2]
  n2 = array2[3]
  
  diff = mean1 - mean2
  
  se = sd_pooled(sd1, sd2, n1, n2)
  
  df = df_pooled(n1, n2)
  
  # need to divide alpha for 2-sided test
  t = abs(qt(alpha/2, df))
  
  me = t * se
  
  lower = diff - me
  higher = diff + me
  
  cat(sprintf("Difference: %s\n", diff))
  cat(sprintf("Degrees of Freedom: %s\n", df))
  cat(sprintf("t-value: %s\n", t))
  cat(sprintf("Margin of Error: %s\n", me))
  cat(sprintf("Standard Error: %s\n", se))
  cat(sprintf("Lower End: %s\n", lower))
  cat(sprintf("Higher End: %s\n", higher))
  
}


t_paired <- function(pairwise_differences, sd, population, delta)
{
  # standard deviation for a paired t-value is the same as the standard deviation for 2 means
  se = sd_mean(sd, population)
  
  t = (pairwise_differences - delta) / se
  
  return(t)
}


# only use paired tests for before/after scenarios
mean_diff_confidence_intervals_paired <- function(pairwise_differences, sd_differences, population, delta, alpha)
{
  se = sd_mean(sd_differences, population)
  
  # use n-1 for degrees of freedom
  t = abs(qt(alpha/2, population))
  
  lower = pairwise_differences - (t * se)
  higher = pairwise_differences + (t * se)
  
  cat(sprintf("t-value: %s\n", t))
  cat(sprintf("Standard Error: %s\n", se))
  cat(sprintf("Lower End: %s\n", lower))
  cat(sprintf("Higher End: %s\n", higher))
}




# functions for linear regression
correlation_coefficient_linear <- function(preidictor_array, response_array)
{
 combined_array = preidictor_array * response_array
 
 r = sum(combined_array) / (n - 1)
 
 return(r)
}


# uses a set linear model with a predictor (just fancy use of a line)
run_linear <- function(predictor, intercept, slope)
{
  response = intercept + slope*predictor
  
  return(response)
}

slope_linear <- function(sd_predictor, sd_response, correlation_coefficient)
{
  slope = correlation_coefficient * (sd_response / sd_predictor)
  
  return(slope)
}


# finds the standard deviation of the residuals from an array of them
sd_linear_residuals <- function(residual_array)
{
  sum = sum(residual_array**2)
  
  sd = sqrt(sum / 2)
  
  return(sd)
}


sd_linear <- function(actual_reponse_array, predicted_response_array)
{
  residuals = actual_reponse_array - predicted_response_array
  
  sd = sd_linear_residuals(residuals)
  
  return(sd)
}

# create a function to get the intercept of a model
intercept_linear <- function(mean_predictor, mean_response, slope)
{
  intercept = mean_response  - slope * mean_predictor
  
  return(intercept)
}


# finds the equation of a line for a linear model
linear_mean_model <- function(mean_predictor, mean_response, sd_predictor, sd_response, correlation_coefficient)
{
  # find the attributes of the line
  slope = slope_linear(sd_predictor, sd_response, correlation_coefficient)
  intercept = intercept_linear(mean_predictor, mean_response, slope)

  
  # output the line's equation
  cat(sprintf("y = %s + %sx\n", intercept, slope))
}



sd_linear_slope <- function(sd_response, sd_spread, sample_size)
{
  sd = sd_response / (sd_spread * sqrt(sample_size - 1) )
  
  return(sd)
}

t_value_correlation_coefficient <- function(correlation_coefficient, population)
{
  df = population - 2
  
  t = correlation_coefficient * sqrt(df / (1 - r**2))
  
  return(t)
}


# create a standard deviation function for an entire linear model (for all values at a point)
sd_linear_model_all <- function(predictor, mean_predictor, sd_intercept, sd_spread, population)
{
  var_intercept = sd_intercept**2
  var_spread = sd_spread**2
  
  sd = sqrt(var_intercept * ((predictor-mean_predictor)**2) + (var_spread/population))
  
  return(sd)
}



# create a standard deviation function for an entire linear model (for any one value)
sd_linear_model_single <- function(predictor, mean_predictor, sd_intercept, sd_spread, population)
{
  var_intercept = sd_intercept**2
  var_spread = sd_spread**2
  
  sd = sqrt(var_intercept * ((predictor-mean_predictor)**2) + (var_spread/population) + var_spread)
  
  return(sd)
}



# create a function to calculate the confidence interval of a linear regression model for
# the mean value at a particular point
confidence_interval_linear_mean <- function(intercept, slope, predictor, 
                                       mean_predictor, sd_intercept, sd_spread, population, alpha)
{
  prediction = run_linear(predictor, intercept, slope)
  
  sd = sd_linear_model_all(predictor, mean_predictor, sd_intercept, sd_spread, population)
  
  # need to divide alpha for 2-sided test
  df = population - 2
  t = abs(qt(alpha/2, df))
  
  # calculate some output stats
  diff = predictor - mean_predictor
  
  me = sd * t
  
  lower = prediction - me
  higher = prediction + me
  
  cat(sprintf("Difference from mean: %s\n", diff))
  cat(sprintf("Degrees of Freedom: %s\n", df))
  cat(sprintf("t-value: %s\n", t))
  cat(sprintf("Standard Error: %s\n", sd))
  cat(sprintf("Margin of Error: %s\n", me))
  cat(sprintf("Prediction: %s\n", prediction))
  cat(sprintf("Lower End: %s\n", lower))
  cat(sprintf("Higher End: %s\n", higher))
}



# create a function that gives a confidence interval for one particular input
confidence_interval_linear_single <- function(intercept, slope, predictor, 
                                           mean_predictor, sd_intercept, sd_spread, population, alpha)
{
  prediction = run_linear(predictor, intercept, slope)
  
  se = sd_linear_model_single(predictor, mean_predictor, sd_intercept, sd_spread, population)
  
  # need to divide alpha for 2-sided test
  df = population - 2
  t = abs(qt(alpha/2, df))
  
  # calculate some output stats
  diff = predictor - mean_predictor
  
  me = se * t

  lower = prediction - me
  higher = prediction + me
  
  cat(sprintf("Difference from mean: %s\n", diff))
  cat(sprintf("Degrees of Freedom: %s\n", df))
  cat(sprintf("t-value: %s\n", t))
  cat(sprintf("Standard Error: %s\n", se))
  cat(sprintf("Margin of Error: %s\n", me))
  cat(sprintf("Prediction: %s\n", prediction))
  cat(sprintf("Lower End: %s\n", lower))
  cat(sprintf("Higher End: %s\n", higher))
}


# create a function to predict a linear value
predict_linear <- function(predictor, mean_predictor, mean_response, sd_predictor, sd_response, correlation_coefficient)
{
  # get the slope of the line
  slope = slope_linear(sd_predictor, sd_response, correlation_coefficient)
  intercept = mean_response  - slope * mean_predictor
  
  # predict the value
  prediction = run_linear(predictor, intercept, slope)
  
  return(prediction)
}


# create a function to find the r^2 value (kind of useless when you can just square the correlation coefficient)
correlation_coefficient_linear <- function(predictor_array, response_array)
{
  amount = length(predictor_array)
  
  # calculate preliminary information
  sum_of_products = sum(predictor_array * response_array)
  product_of_sums = sum(predictor_array) * sum(response_array)
  
  predictor_sum_of_squares = sum(predictor_array**2)
  predictor_square_of_sum = sum(predictor_array)**2
  
  response_sum_of_squares = sum(response_array**2)
  response_square_of_sum = sum(response_array)**2
  
  numerator = amount * sum_of_products - product_of_sums
  denominator = sqrt( (amount * predictor_sum_of_squares - predictor_square_of_sum) * 
                        (amount * response_sum_of_squares - response_square_of_sum) )
  
  correlation_coefficient = numerator / denominator
  
  
  return(correlation_coefficient)
}

# make a way to calculate correlation coefficient from sd
correlation_coefficient_from_sd <- function(sd_predictor, sd_response, sd_product)
{
  correlation_coefficient = sd_product / (sd_predictor * sd_response)
  
  return(r)
}


# create more functions for analyzing linear models

# this finds the general sd for the entire linear model
sd_linear_model <- function(predictor_array, response_array)
{
  # get data to create and run a model
  amount = length(predictor_array)
  
  mean_predictor = mean(predictor_array)
  mean_response = mean(response_array)
  
  sd_predictor = sd(predictor_array)
  sd_response = sd(response_array)
  correlation_coefficient = correlation_coefficient_linear(predictor_array, response_array)

  slope = slope_linear(sd_predictor, sd_response, correlation_coefficient)
  intercept = intercept_linear(mean_confipredictor, mean_response, slope)
  
  # run the model on all values to get predictions
  predictions = run_linear(predictor_array, intercept, slope)
  
  # find the standard deviation using the formula
  residuals = response_array - predictions
  numerator = sum(residuals**2)
  sd = sqrt( numerator / (amount - 2) )
  
  
  return(sd)
}

# create a function to get the standard error of the regression slope
se_regression_slope <- function(sd_model, sd_predictor, population)
{
  se = sd_model / (sd_predictor * sqrt(population - 1))
  
  return(se)
}

confidence_interval_regression_slope <- function(coefficient, sd_coefficient, alpha)
{
  
  # use z-score for this
  z = qnorm(alpha/2)
    
  me = sd_coefficient * z
  
  lower = coefficient - me
  higher = coefficient + me
  
  cat(sprintf("z-statistic: %s\n", z))
  cat(sprintf("Standard Error: %s\n", sd_coefficient))
  cat(sprintf("Margin of Error: %s\n", me))
  cat(sprintf("Lower End: %s\n", lower))
  cat(sprintf("Higher End: %s\n", higher))
}




