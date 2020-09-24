class IncomeStatement:
    def __init__(self, direct_materials, direct_labor, var_moh, var_sga, f_moh, f_sga, price, units_produced, units_sold):
        self.direct_materials = direct_materials
        self.direct_labor = direct_labor
        self.var_moh = var_moh
        self.var_sga = var_sga
        self.f_moh = f_moh
        self.f_sga = f_sga
        self.price = price
        self.units_sold = units_sold
        self.units_produced = units_produced

    def unit_product_cost(self, absorption=False):
        cost = self.direct_materials + self.direct_labor + self.var_moh

        if absorption:
            cost += self.applied_f_moh()

        return cost

    def applied_f_moh(self):
        f_moh = self.f_moh / self.units_produced

        return f_moh

    def sales(self):
        revenue = self.units_sold * self.price

        return revenue

    def cogs(self, absorption=False):
        cost_per_unit = self.unit_product_cost(absorption=absorption)
        cogs = self.units_sold * cost_per_unit

        return cogs

    def total_var_sga(self):
        total = self.units_sold * self.var_sga

        return total

    def cmargin(self):
        sales = self.sales()
        cogs = self.cogs()
        total_sga = self.total_var_sga()
        margin = sales - cogs - total_sga

        return margin

    def gross_margin(self):
        sales = self.sales()
        cogs = self.cogs(absorption=True)
        margin = sales - cogs

        return margin

    def var_noi(self):
        noi = self.cmargin() - self.f_moh - self.f_sga

        return noi

    def trad_noi(self):
        margin = self.gross_margin()
        var_sga = self.total_var_sga()

        noi = margin - self.f_sga - var_sga

        return noi


if __name__ == '__main__':
    statement = IncomeStatement(direct_materials=1, direct_labor=1,
                                var_moh=1, var_sga=1, f_moh=1, f_sga=1, price=1, units_produced=1, units_sold=1)

    cogs = statement.cogs(absorption=True)


'''
NOTES
- Inputs: DM, DL, VMOH, VSGA, FMOH, FSGA, PRICE, UNITS_SOLD
'''
