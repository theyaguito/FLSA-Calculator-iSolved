from flask import Flask, request, render_template
from flsa import FLSA
from payperiod import PayPeriod

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        case = request.form.get("case")
        payperiod_type = request.form.get("payperiod")

        # Create PayPeriod instance using its constructor (frequency as string)
        try:
            payperiod = PayPeriod(payperiod_type)
        except Exception as e:
            error = str(e)
            return render_template("index.html", result=None, error=error)

        if case == "regular":
            total_reg_hours = float(request.form.get("total_reg_hours", 0))
            total_ot_hours = float(request.form.get("total_ot_hours", 0))
            total_worked_hours = float(request.form.get("total_worked_hours", 0))
            base_hourly_rate = float(request.form.get("base_hourly_rate", 0))
            flsa_instance = FLSA(
                total_reg_hours,
                total_ot_hours,
                total_worked_hours,
                base_hourly_rate,
                payperiod,
            )
            result = {
                "Average Hourly Rate": flsa_instance.calc_average_hourly_rate(),
                "Overtime Premium": flsa_instance.calc_ot_premium(),
                "Total Overtime Pay": flsa_instance.calc_total_ot_pay(),
            }

        elif case == "shift":
            shift_differentials = []
            i = 1
            while True:
                rate = request.form.get(f"shift_rate_{i}")
                hours = request.form.get(f"shift_hours_{i}")
                if rate is None or hours is None or rate == "" or hours == "":
                    break
                shift_differentials.append((float(hours), float(rate)))
                i += 1
            flsa_instance = FLSA.from_shift_differential(shift_differentials, payperiod)
            result = {
                "Average Hourly Rate": flsa_instance.calc_average_hourly_rate_shift_differential(),
                "Overtime Premium": flsa_instance.calc_ot_premium_shift_differential(),
                "Total Overtime Pay": flsa_instance.calc_total_ot_pay_shift_differential(),
            }

        elif case == "alternate":
            total_reg_hours = float(request.form.get("alt_total_reg_hours", 0))
            base_hourly_rate = float(request.form.get("alt_base_hourly_rate", 0))
            alternate_rates = []
            i = 1
            while True:
                rate = request.form.get(f"alt_rate_{i}")
                hours = request.form.get(f"alt_hours_{i}")
                if rate is None or hours is None or rate == "" or hours == "":
                    break
                alternate_rates.append((float(hours), float(rate)))
                i += 1
            flsa_instance = FLSA.from_alternate_rates(
                total_reg_hours, base_hourly_rate, alternate_rates, payperiod
            )
            result = {
                "Average Hourly Rate": flsa_instance.calc_average_hourly_rate_alternate_rates(),
                "Overtime Premium": flsa_instance.calc_ot_premium_alternate_rates(),
                "Total Overtime Pay": flsa_instance.calc_total_ot_pay_alternate_rates(),
            }

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    app.run(debug=True)
