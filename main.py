import sys
import json
from argparse import ArgumentParser
from tax_calc_lib import calc_tax
from test import run_tests

run_tests()

parser = ArgumentParser(
    prog="Stage 3 Tax Simulator",
    description="Simulate differences over time between the original and amended stage 3 tax cuts",
)
parser.add_argument("--salary", "-s", default=102611.0, type=float, dest="salary")
parser.add_argument("--wagegrowth", "-wg", default=1.03, type=float, dest="wage_growth")
parser.add_argument("--promofreq", "-pf", default=5, type=int, dest="promo_freq")
parser.add_argument(
    "--promogrowth", "-pg", default=1.03, type=float, dest="promo_growth"
)
parser.add_argument("-workingyrs", "--wy", default=45, type=int, dest="working_years")
args = parser.parse_args()

with open("brackets.json", "r") as f:
    data = json.loads(f.read())
    current_brackets = data["current_brackets"]
    stage3_original = data["stage3_original"]
    stage3_amended = data["stage3_amended"]

print(f"Simulating tax paid over {args.working_years} years")
print(f"Median 2023 fulltime salary: {"${:,.2f}".format(args.salary)}")
print(f"Wage growth: {"{:.2f}%".format(args.wage_growth)} py")
if args.promo_growth > args.wage_growth:
    print(
        f"Promoted every {args.promo_freq} years at {
            "{:.2f}%".format(args.promo_growth)} instead of {"{:.2f}%".format(args.wage_growth)}"
    )

salary = args.salary
total_earnings = salary
tax_history = {"no_change": [0], "stage3_original": [0], "stage3_amended": [0]}
for i in range(args.working_years):
    if (i + 1) % args.promo_freq == 0:
        salary *= args.promo_growth
    else:
        salary *= args.wage_growth
    total_earnings += salary
    tax_history["no_change"].append(calc_tax(salary, current_brackets))
    tax_history["stage3_original"].append(calc_tax(salary, stage3_original))
    tax_history["stage3_amended"].append(calc_tax(salary, stage3_amended))


# Tax Paid result
total_tax_no_change = sum(tax_history["no_change"])
total_tax_stage3_original = sum(tax_history["stage3_original"])
total_tax_stage3_amended = sum(tax_history["stage3_amended"])
total_tax_paid = {
    "no_change": f"{"${:,.2f}".format(total_tax_no_change)} - {"{:.2f}%".format(total_tax_no_change / total_earnings * 100)}",
    "stage3_original": f"{"${:,.2f}".format(total_tax_stage3_original)} - {"{:.2f}%".format(total_tax_stage3_original / total_earnings * 100)}",
    "stage3_amended": f"{"${:,.2f}".format(total_tax_stage3_amended)} - {"{:.2f}%".format(total_tax_stage3_amended / total_earnings * 100)}",
}
print(f"\nTotal Earnings: {"${:,.2f}".format(total_earnings)}")
print("Total Tax Paid")
print(json.dumps(total_tax_paid, indent=4))

additional_tax = total_tax_stage3_amended - total_tax_stage3_original
print(f"Additional tax under amendment: {"${:,.2f}".format(additional_tax)}")

# Crossover point
for i in range(args.working_years):
    if tax_history["stage3_amended"][i] > tax_history["stage3_original"][i]:
        print(f"More tax paid under amendment from year {i+1} onwards")
        break
