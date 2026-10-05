"""Convert supplied solid-to-solution standard Gibbs energy to ideal molar solubility."""
from common import *

def main():
    p=parser(__doc__)
    p.add_argument('--delta-g',type=finite,required=True,help='G_solution(1 mol/L standard state)-G_solid, kJ/mol')
    p.add_argument('--temperature',type=positive,default=298.15)
    p.add_argument('--activity-coefficient',type=positive,default=1.)
    p.add_argument('--mw',type=positive)
    a=p.parse_args(); log_s=-a.delta_g/(R_KJ*a.temperature*math.log(10))-math.log10(a.activity_coefficient)
    if abs(log_s)>300: raise ValueError('Excessive logS; check inputs')
    result=dict(logS_mol_L=log_s,S_mol_L=10**log_s,temperature_K=a.temperature,
        warning='Requires a consistent full dissolution free energy including crystal/solution thermal and standard-state terms. Isolated molecule gas energy or continuum solvation energy alone is not enough. Ideal monomer solubility; ignores ionisation.')
    if a.mw: result['S_mg_mL']=10**log_s*a.mw
    dump(output_dir(a)/'free_energy_solubility.json',result)

if __name__ == '__main__': main()
