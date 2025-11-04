from __future__ import annotations
import argparse, subprocess, sys
def main():
    ap=argparse.ArgumentParser(prog="customer-seg-clv"); sub=ap.add_subparsers(dest="cmd",required=True)
    g=sub.add_parser("generate-data"); g.add_argument("--seed",type=int,default=42); g.add_argument("--n_customers",type=int,default=15000); g.add_argument("--start",type=str,default="2024-01-01"); g.add_argument("--end",type=str,default="2025-06-30")
    sub.add_parser("build-db")
    r=sub.add_parser("rfm"); r.add_argument("--k",type=int,default=4); r.add_argument("--as_of",type=str,default=None)
    c=sub.add_parser("clv"); c.add_argument("--margin",type=float,default=0.60); c.add_argument("--discount_rate",type=float,default=0.01)
    sub.add_parser("export"); sub.add_parser("run-all")
    a=ap.parse_args()
    def run(modargs):
        cmd=[sys.executable,"-m"]+modargs; print(">>"," ".join(cmd)); subprocess.run(cmd,check=True)
    if a.cmd=="generate-data": run(["src.generate_data"])
    elif a.cmd=="build-db": run(["src.build_db"])
    elif a.cmd=="rfm":
        args=["src.rfm_segment",f"--k={a.k}"]; 
        if a.as_of: args.append(f"--as_of={a.as_of}")
        run(args)
    elif a.cmd=="clv": run(["src.clv_churn"])
    elif a.cmd=="export": run(["src.export_powerbi"])
    elif a.cmd=="run-all":
        run(["src.generate_data"]); run(["src.build_db"]); run(["src.rfm_segment"]); run(["src.clv_churn"]); run(["src.export_powerbi"])
if __name__=="__main__": main()
