import unittest

from openaerostruct.aerodynamics.viscous_drag import ViscousDrag
from openaerostruct.utils.testing import run_test, get_default_surfaces
from openmdao.api import Group, IndepVarComp, BsplinesComp


class Test(unittest.TestCase):

    def test(self):
        surface = get_default_surfaces()[0]
        
        ny = surface['num_y']
        nx = surface['num_x']
        n_cp = len(surface['t_over_c_cp'])

        group = Group()

        indep_var_comp = IndepVarComp()
        indep_var_comp.add_output('t_over_c_cp', val=surface['t_over_c_cp'])
        group.add_subsystem('indep_var_comp', indep_var_comp, promotes=['*'])
        
        group.add_subsystem('t_over_c_bsp', BsplinesComp(
            in_name='t_over_c_cp', out_name='t_over_c',
            num_control_points=n_cp, num_points=int(ny-1),
            bspline_order=min(n_cp, 4), distribution='uniform'),
            promotes_inputs=['t_over_c_cp'], promotes_outputs=['t_over_c'])
        
        comp = ViscousDrag(surface=surface, with_viscous=True)
        group.add_subsystem('viscousdrag', comp, promotes=['*'])

        run_test(self, group)

    def test_2(self):
        surface = get_default_surfaces()[0]
        surface['k_lam'] = .5
        
        ny = surface['num_y']
        nx = surface['num_x']
        n_cp = len(surface['t_over_c_cp'])

        group = Group()

        indep_var_comp = IndepVarComp()
        indep_var_comp.add_output('t_over_c_cp', val=surface['t_over_c_cp'])
        group.add_subsystem('indep_var_comp', indep_var_comp, promotes=['*'])
        
        group.add_subsystem('t_over_c_bsp', BsplinesComp(
            in_name='t_over_c_cp', out_name='t_over_c',
            num_control_points=n_cp, num_points=int(ny-1),
            bspline_order=min(n_cp, 4), distribution='uniform'),
            promotes_inputs=['t_over_c_cp'], promotes_outputs=['t_over_c'])
        
        comp = ViscousDrag(surface=surface, with_viscous=True)
        group.add_subsystem('viscousdrag', comp, promotes=['*'])

        run_test(self, group)

if __name__ == '__main__':
    unittest.main()
