import unittest
import mps.state
from mps.evolution import *
from mps.test.tools import *



class TestTEBD_sweep(unittest.TestCase):
    
    def test_orthonormalization(self):
        #
        # We verify that our two-site orthonormalization procedure, 
        # does not change the state
        #
        δt = 0.1
        H = TINNHamiltonian(0*σx, σx, σx)
        Trotter = Trotter_unitaries(H, δt)

        def ok(Ψ):
            for start in range(Ψ.size-1):            
                AA = apply_2siteTrotter(Trotter.twosite_unitary(start) , 
                                                      Ψ, start)
                A, AC = mps.state.left_orth_2site(AA, DEFAULT_TOLERANCE)
                AA_orth = np.einsum("ijk,klm -> ijlm", A, AC)
                self.assertTrue(similar(AA,AA_orth))                
            for start in range(Ψ.size-1):            
                AA = apply_2siteTrotter(Trotter.twosite_unitary(start) , 
                                                      Ψ, start)
                A, AC = mps.state.right_orth_2site(AA, DEFAULT_TOLERANCE)
                AA_orth = np.einsum("ijk,klm -> ijlm", AC, A)
                self.assertTrue(similar(AA,AA_orth))
            
            
        test_over_random_mps(ok)

