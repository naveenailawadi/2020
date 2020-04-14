# function for one sided p-value
print_p_os <- function(old_proportion, sample_proportion, population)
{
    # make calculations
    sd = sqrt(sample_proportion * (1-sample_proportion) / population)
    z = (sample_proportion - old_proportion) / sd
    p = pnorm(z)

    # print the calculations and inputs
    print("One-Sided Test")
    print(sprintf("Old Proporiton: %s", old_proportion))
    print(sprintf("New Proporiton: %s", sample_proportion))
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

    print(sprintf("Standard deviation: %s", sd))
    print(sprintf("z-statistic: %s", z))
    print(sprintf("P-value: %s", p))
}

standardize <- function(value, mean, sd)
{
    z = (value - mean) / sd
    
    return(z)
}

prepp <- function(value, mean, sd, degrees)
{
    t = (value - mean) / (sd / sqrt(degrees))
    
    return(t)
}

probdiff <- function(start, end, mean, sd, df)
{
    p_start = pt(prepp(start, mean, sd, df), df=df)
    p_end = pt(prepp(end, mean, sd, df), df=df)
    
    pdiff = p_end - p_start
    
    return(pdiff)
    
}

