from payperiod import Payperiod

class FLSA:
    def __init__(
            self,
            total_reg_hours:float,
            total_ot_hours:float,
            total_worked_hours:float,
            base_hourly_rate:float,
            pay_period:Payperiod,
            shift_differentials:list = None,
            alternate_rates:list = None
            ):

    # Initialize the FLSA class with the provided parameters

        self.total_reg_hours = total_reg_hours
        self.total_ot_hours = total_ot_hours
        self.total_worked_hours = total_worked_hours
        self.base_hourly_rate = base_hourly_rate
        self.total_regular_earnings:float = self.total_reg_hours * self.base_hourly_rate
        self.pay_period = pay_period
        self.shift_differential = shift_differentials
        self.alternate_rates = alternate_rates

    # --- First Case Calculation Steps ---

    # Step 1: Find the Average Hourly Rate (a)
    def calc_average_hourly_rate(self):
        if self.total_worked_hours <= self.pay_period.threshold_hours:
            return 0
        avr:float = self.base_hourly_rate
        return avr
    
    # Step 2: Determine the Overtime Premium (p)
    def calc_ot_premium(self):
        avr:float = self.calc_average_hourly_rate()
        ot_premium:float = avr * 0.5
        return ot_premium
    
    # Step 3: Calculate the Total Overtime Pay (o)
    def calc_total_ot_pay(self):
        total_ot_pay:float = (self.base_hourly_rate * self.total_ot_hours) / 2
        return total_ot_pay
    
    # --- Second Case Constructor, Shift Differential --- 

    @classmethod
    def from_shift_differential(cls, shift_differentials:list, payperiod:Payperiod):
        return cls(
            total_reg_hours = 0,
            total_ot_hours = 0,
            total_worked_hours = 0,
            base_hourly_rate = 0,
            shift_differentials = shift_differentials,
            alternate_rates = None,
            pay_period = payperiod
        )

    # --- Second Case Calculation Steps, Shift Differential ---

    def calc_average_hourly_rate_shift_differential(self):
        total_hours_worked:float = 0
        for shift in self.shift_differential:
            total_hours_worked += shift[0]
        if total_hours_worked <= self.pay_period.threshold_hours:
            return 0
        total_shift_differential:float = 0
        for shift in self.shift_differential:
            total_shift_differential += shift[0] * shift[1]
        avr:float = (total_shift_differential / total_hours_worked)
        return avr

    def calc_ot_premium_shift_differential(self):
        avr:float = self.calc_average_hourly_rate_shift_differential()
        ot_premium:float = avr * 0.5
        return ot_premium

    def calc_total_ot_pay_shift_differential(self):
        total_ot_hours:float = self.shift_differential[-1][0]
        avr:float = self.calc_average_hourly_rate_shift_differential()
        total_ot_pay:float = (avr * total_ot_hours) / 2
        return total_ot_pay            

    # --- Third Case Constructor, Alternate Rates ---

    @classmethod
    def from_alternate_rates(cls, total_reg_hours:float, base_hourly_rate:float, alternate_rates:list, payperiod:Payperiod):
        return cls(
            total_reg_hours = total_reg_hours,
            total_ot_hours = sum(alternate_rate[0] for alternate_rate in alternate_rates),
            total_worked_hours = total_reg_hours + sum(alternate_rate[0] for alternate_rate in alternate_rates),
            base_hourly_rate = base_hourly_rate,
            shift_differentials = None,
            alternate_rates = alternate_rates,
            pay_period = payperiod
        )

    # --- Third Case Calculation Steps, Alternate Rates ---
    
    def calc_average_hourly_rate_alternate_rates(self):
        if self.total_worked_hours <= self.pay_period.threshold_hours:
            return 0
        total_regular_earnings:float = self.total_reg_hours * self.base_hourly_rate
        total_alternate_earnings:float = sum(alternate_rate[0] * alternate_rate[1] for alternate_rate in self.alternate_rates)
        total_earnings:float = total_regular_earnings + total_alternate_earnings
        avr:float = total_earnings / self.total_worked_hours
        return avr

    def calc_ot_premium_alternate_rates(self):
        avr:float = self.calc_average_hourly_rate_alternate_rates()
        ot_premium:float = avr * 0.5
        return ot_premium
    
    def calc_total_ot_pay_alternate_rates(self):
        total_ot_hours:float = self.total_ot_hours
        avr:float = self.calc_average_hourly_rate_alternate_rates()
        total_ot_pay:float = (avr * total_ot_hours) / 2
        return total_ot_pay

    # --- Message Functions ---
    
    def print_ot_calculations(self):
        average_hourly_rate:float = self.calc_average_hourly_rate()
        ot_premium:float = self.calc_ot_premium()
        total_ot_pay:float = self.calc_total_ot_pay()

        print(f"Average Hourly Rate: {average_hourly_rate:.2f}")
        print(f"Overtime Premium: {ot_premium:.2f}")
        print(f"Total Overtime Pay: {total_ot_pay:.2f}")

    def print_ot_calculations_shift_differential(self, list_of_shift_differentials:list):
        average_hourly_rate:float = self.calc_average_hourly_rate_shift_differential(list_of_shift_differentials)
        ot_premium:float = self.calc_ot_premium_shift_differential(list_of_shift_differentials)
        total_ot_pay:float = self.calc_total_ot_pay_shift_differential(list_of_shift_differentials)

        print(f"Average Hourly Rate: {average_hourly_rate:.2f}")
        print(f"Overtime Premium: {ot_premium:.2f}")
        print(f"Total Overtime Pay: {total_ot_pay:.2f}")