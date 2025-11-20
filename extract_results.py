import glob
import pandas as pd
import numpy as np

eta = 0.80  # turbine + generator efficiency
rho = 1.225

def compute_power(mdot, deltaT, cp=1005):
    thermal_power = mdot * cp * deltaT
    return eta * thermal_power / 1000  # convert W→kW

def parse_report(file_path):
    values = {}
    with open(file_path) as f:
        for line in f:
            if "mass-flow" in line:
                values["mass_flow"] = float(line.split()[-1])
            if "temperature" in line:
                values["T_out"] = float(line.split()[-1])
    return values

def main():
    rows = []
    for res_file in glob.glob("reports/case_*_report.txt"):
        case_id = res_file.split("_")[1]
        values = parse_report(res_file)

        # Ambient temperature stored separately
        amb = pd.read_csv("lhs_parameters.csv").iloc[int(case_id)-1]["ambient_temperature"]

        deltaT = values["T_out"] - amb
        power = compute_power(values["mass_flow"], deltaT)

        rows.append({
            "case_id": case_id,
            "mass_flow": values["mass_flow"],
            "deltaT": deltaT,
            "Electric_Power": power
        })

    df = pd.DataFrame(rows)
    df.to_csv("compiled_results.csv", index=False)

if __name__ == "__main__":
    main()
