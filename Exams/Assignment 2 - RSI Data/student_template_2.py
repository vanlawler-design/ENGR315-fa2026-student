"""
CULMINATING ASSIGNMENT 2: RSI

Create a program which will provide answers to the tasks posed in the assignment description.

For this assignment, you will start from scratch with this blank template.
It is your reponsibility to include all necessary program components in this file.
Your code needs to be successful as well as sufficiently commented/documented to receive full credit.

The relevant data file is named "all_participant_data_rsi.csv" and is located in data > drop-jump.

All file paths need to be relative and execute from this file's directory;
the Visual Studio Code setting "Python > Terminal: Execute in File Dir" 
must be enabled in File > Preferences > Settings.

See Canvas for additional requirements.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


alpha = 0.05
# Resolve the relative path from this script, even if run from another folder.
folder = Path(__file__).resolve().parent
data = pd.read_csv(folder / "../../data/drop-jump/all_participant_data_rsi.csv")

# Task 1: Keep matching measurements together when removing missing values.
paired = data.dropna(subset=["force_plate_rsi", "accelerometer_rsi"])
force = paired["force_plate_rsi"]
accel = paired["accelerometer_rsi"]
t_stat, p_value = stats.ttest_rel(force, accel)

print("\nTASK 1: Paired t-test")
print("H0: The population mean paired difference (force plate - accelerometer) is 0.")
print("H1: The population mean paired difference is not 0.")
print(f"Number of pairs: {len(paired)}")
print(f"t-value = {t_stat:.4f}, p-value = {p_value:.6g}")
print(f"Mean paired difference = {(force - accel).mean():.4f}")
if p_value < alpha:
    print("Reject H0: there is evidence of a mean difference between the methods.")
else:
    print("Do not reject H0: there is insufficient evidence of a mean difference.")
print("This test does not establish agreement or interchangeability of individual measurements.")
print("Repeated trials within participants may be correlated; the pooled test assumes independent pairs.")

# Task 2: Fit a normal distribution to all available accelerometer values.
accelerometer = data["accelerometer_rsi"].dropna()
mean, std = stats.norm.fit(accelerometer)
n = len(accelerometer)
if std <= 0 or n < 20:
    raise ValueError("The normal chi-square test needs variation and at least 20 values.")

# Equal-probability bins give expected counts >= 5, including both tails.
number_bins = min(10, n // 5)
edges = stats.norm.ppf(np.linspace(0, 1, number_bins + 1), loc=mean, scale=std)
observed, _ = np.histogram(accelerometer, bins=edges)
expected = np.full(number_bins, n / number_bins)
# Subtract two degrees of freedom because mean and standard deviation were fitted.
chi2_stat, chi2_p = stats.chisquare(observed, expected, ddof=2)

print("\nTASK 2: Normal chi-square goodness-of-fit test")
print("H0: Accelerometer RSI follows a normal distribution.")
print("H1: Accelerometer RSI does not follow a normal distribution.")
print(f"Fitted mean = {mean:.4f}, fitted standard deviation = {std:.4f}")
print(f"chi2 statistic = {chi2_stat:.4f}, p-value = {chi2_p:.6g}")
print(f"Degrees of freedom = {number_bins - 3}")
print("Observed bin counts:", observed)
print("Expected bin counts:", expected)
if chi2_p < alpha:
    print("Reject H0: the normal distribution is not a good fit at alpha = 0.05.")
else:
    print("Do not reject H0: a normal fit is acceptable at alpha = 0.05, but not proven.")
print(f"Sample skewness = {stats.skew(accelerometer, bias=False):.4f}")
print("Compare observed and expected counts: large discrepancies increase chi2.")
print("Use the histogram to assess asymmetry, multiple peaks, and extreme values.")
print("Pooling participants with different typical RSI values can produce a non-normal mixture.")

x = np.linspace(min(accelerometer.min(), mean - 4 * std),
                max(accelerometer.max(), mean + 4 * std), 400)
plt.figure(figsize=(8, 5))
plt.hist(accelerometer, bins="auto", density=True, alpha=0.6,
         edgecolor="black", label="Accelerometer RSI")
plt.plot(x, stats.norm.pdf(x, mean, std), color="red", label="Fitted normal distribution")
plt.title("Accelerometer RSI with Fitted Normal Distribution")
plt.xlabel("RSI (m/s)")
plt.ylabel("Probability density")
plt.legend()
plt.tight_layout()

# Task 3: Select F exactly from the participant prefix in each trial name.
participant_f = data[data["trial"].str.split("_").str[0] == "F"]
print("\nTASK 3: Participant F trials")
print(participant_f.to_string(index=False))

for column in ["force_plate_rsi", "accelerometer_rsi"]:
    values = participant_f[column].dropna()
    if len(values) < 2:
        raise ValueError("At least two measurements are needed for each confidence interval.")
    # A t interval estimates the population mean when its standard deviation is unknown.
    lower, upper = stats.t.interval(0.95, df=len(values) - 1,
                                    loc=values.mean(), scale=stats.sem(values))
    print(f"{column}: mean = {values.mean():.4f}, 95% CI = ({lower:.4f}, {upper:.4f})")

print("These intervals describe uncertainty in F's mean RSI for each method.")
print("Overlapping intervals alone cannot establish agreement or test a paired difference.")
print("The intervals assume independent trials and approximately normal measurements for F.")
plt.show()