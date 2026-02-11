class Payperiod:
    def __init__(self, is_weekly:bool, is_biweekly:bool, is_semi_monthly:bool):
        if is_weekly:
            self.period = "weekly"
            self.threshold_hours = 40
        if is_biweekly:
            self.period = "biweekly"
            self.threshold_hours = 80
        if is_semi_monthly:
            self.period = "semi-monthly"
            self.threshold_hours = 86.67