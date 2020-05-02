class SpendingBalanceModel:
    def __init__(self, marginal_propensity_to_consume):
        self.marginal_propensity_to_consume = marginal_propensity_to_consume

        # spending multiplier --> how much GDP increases with an increase in autonomous spending
        self.spending_multiplier = 1 / (1 - self.marginal_propensity_to_consume)

    def find_consumption(self, autonomous_spending):
        consumption = autonomous_spending / (1 - self.marginal_propensity_to_consume)

        return consumption

    def find_average_propensity_to_consume(self, income, autonomous_spending):
        consumption = self.find_consumption(autonomous_spending)
        average_propensity_to_consume = consumption / income

        return average_propensity_to_consume

    def find_consumption_increase(self, stimulus):
        increase = stimulus * self.marginal_propensity_to_consume

        return increase

    def find_total_spending(self, autonomous_spending, investment, government_purchases, net_exports):
        consumption = self.find_consumption(autonomous_spending)
        total_spending = consumption + investment + government_purchases + net_exports

        return total_spending

    def find_gdp_increase(self, autonomous_spending_increase):
        gdp_increase = autonomous_spending_increase * self.spending_multiplier

        return gdp_increase


class MonetaryRule:
    def __init__(self, target_inflation, long_run_real_interest_rate):
        self.target_inflation = target_inflation
        self.long_run_real_interest_rate = long_run_real_interest_rate

    def find_r(self, gdp_gap_percentage, current_inflation):
        r = self.long_run_real_interest_rate + 0.5 * (current_inflation - self.target_inflation) + 0.5 * gdp_gap_percentage

        return r

    def find_taylor_rate(self, gdp_gap_percentage, current_inflation):
        taylor_rate = self.long_run_real_interest_rate - 0.5 * self.target_inflation + 0.5 * gdp_gap_percentage + 1.5 * current_inflation

        return taylor_rate


class AggregateDemand(SpendingBalanceModel):
    def __init__(self,
                 spending_multiplier, autonomous_spending_multiplier,
                 interest_rate_inflation_ratio, interest_rate_without_inflation,
                 sample_inflation, sample_gdp):

        marginal_propensity_to_consume = 1 - (1 / autonomous_spending_multiplier)

        self.marginal_propensity_to_consume = marginal_propensity_to_consume
        self.spending_multiplier = spending_multiplier
        self.autonomous_spending_multiplier = autonomous_spending_multiplier
        self.interest_rate_inflation_ratio = interest_rate_inflation_ratio
        self.interest_rate_without_inflation = interest_rate_without_inflation
        self.sample_inflation = sample_inflation
        self.sample_gdp = sample_gdp

        self.slope = self.find_slope()

    def inflation_from_r(self, r):
        inflation = (r - self.interest_rate_without_inflation) / self.interest_rate_inflation_ratio

        return inflation

    def r_from_inflation(self, inflation):
        r = self.interest_rate_without_inflation + self.interest_rate_inflation_ratio * inflation

        return r

    def find_slope(self):
        # test an inflation of 0
        theoretical_r = self.r_from_inflation(0)
        current_r = self.r_from_inflation(self.sample_inflation)

        autonomous_spending_increase = (theoretical_r - current_r) * self.autonomous_spending_multiplier

        gdp_increase = self.find_gdp_increase(autonomous_spending_increase)

        slope = self.sample_inflation / gdp_increase

        return slope

    def gdp_from_inflation(self, inflation):
        inflation_difference = self.sample_inflation - inflation
        gdp_difference = inflation_difference / self.slope
        gdp = self.sample_gdp + gdp_difference

        return gdp

    def inflation_from_gdp(self, gdp):
        gdp_difference = gdp - self.sample_gdp

        inflation_difference = self.sample_inflation + gdp_difference * self.slope

        inflation = self.sample_inflation + inflation_difference

        return inflation

    def __repr__(self):
        y_intercept = self.inflation_from_gdp(0)
        # output the equation as the entire model
        print_value = f"inflation = {y_intercept} - {abs(self.slope)}(Aggregate Demand)"

        return print_value
