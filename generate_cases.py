import os
import pandas as pd

LHS_FILE = "lhs_param.csv"
JOURNAL = "run_fluent.jou"

def update_geometry(project, params):
    project.SetParameterExpression("chimney_height", str(params["chimney_height"]))
    project.SetParameterExpression("collector_diameter", str(params["collector_diameter"]))
    project.SetParameterExpression("inlet_diameter", str(params["chimney_inlet"]))
    project.SetParameterExpression("collector_inlet_height", str(params["collector_inlet_h"]))
    project.Save()

def run_mesh(project):
    mesh_system = project.GetChild("Mesh")
    mesh_system.Update()

def export_fluent_case(project, case_name):
    fluent_system = project.GetChild("FluentSetup")
    out_path = os.path.join("cases", case_name + ".cas.h5")
    fluent_system.ExportCase(out_path)
    return out_path

def run_fluent_batch(case_path):
    os.system(f'fluent 3ddp -g -i {JOURNAL} -t48 -wait -cas "{case_path}"')

def main():
    project = GetActiveProject()
    df = pd.read_csv(LHS_FILE)

    for idx, row in df.iterrows():
        case_name = f"case_{idx+1}"
        params = {
            "chimney_height": row["chimney_height"],
            "collector_diameter": row["collector_diameter"],
            "chimney_inlet": row["chimney_inlet_diameter"],
            "collector_inlet_h": row["collector_inlet_height"]
        }

        print(f"Running {case_name}")
        update_geometry(project, params)
        run_mesh(project)
        case_path = export_fluent_case(project, case_name)
        run_fluent_batch(case_path)

if __name__ == "__main__":
    main()
