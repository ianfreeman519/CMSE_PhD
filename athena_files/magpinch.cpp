//========================================================================================
// Athena++ astrophysical MHD code
// Copyright(C) 2014 James M. Stone <jmstone@princeton.edu> and other code contributors
// Licensed under the 3-clause BSD License, see LICENSE file for details
//========================================================================================
//! \file magpinch.cpp
//! \brief Magnetized inflow to demonstrate reconnection
//!
//! 2D collapse toward center axis
//! initial conditions with r in cm:
//! rho  = rho0*r^alpha [g/cm^3]
//! V    = V0    [cm/s]
//! Bphi = Bphi0*r^beta   [gauss] azimuthal
//! Bz   = Bz0*  r^beta   [gauss] axial
//! pressure = 1.E-6*B^2   actually zero in the exact solution
//!
//! Can apply sine wave perturbation in a form
//!   \f$ (1+perturb*std::cos(mphi*phi)) \f$ to the magnetic potential Az
//!
//! REFERENCES:
//! 1) Velikovich, Giuliani, Zalesak, Gardiner, "Exact self-similar solutions for the
//! magnetized Noh Z pinch problem", Phys. of Plasmas, vol.19, p.012707 (2012)
//!
//! 2) Giuliani, Velikovich, Beresnyak, Zalesak, Gianakon, Rousculp, "Self-similar
//! solutions for the magnetized Noh problem with axial and azimuthal field", Phys. of
//! Plasmas, in prep (2018)

// C headers

// C++ headers
#include <algorithm>
#include <cmath>      // sqrt()
#include <cstring>    // strcmp()
#include <sstream>
#include <stdexcept>
#include <string>

// Athena++ headers
#include "../athena.hpp"
#include "../athena_arrays.hpp"
#include "../bvals/bvals.hpp"
#include "../coordinates/coordinates.hpp"
#include "../eos/eos.hpp"
#include "../field/field.hpp"
#include "../hydro/hydro.hpp"
#include "../mesh/mesh.hpp"
#include "../parameter_input.hpp"

namespace {
Real gm1;
Real alpha, beta, rho0, P0, pcoeff, vin;
Real b;
Real eta_ohm;
// Real nu_iso, eta_ohm;
} // namespace

#if !MAGNETIC_FIELDS_ENABLED
#error "This problem generator requires magnetic fields"
#endif

//========================================================================================
//! \fn void Mesh::InitUserMeshData(ParameterInput *pin)
//  \brief Function to initialize problem-specific data in mesh class.  Can also be used
//  to initialize variables which are global to (and therefore can be passed to) other
//  functions in this file.  Called in Mesh constructor.
//========================================================================================

void Mesh::InitUserMeshData(ParameterInput *pin) {
  // initialize global variables
  alpha  = pin->GetReal("problem", "alpha");
  beta  = pin->GetReal("problem", "beta");
  pcoeff = pin->GetReal("problem", "pcoeff");
  rho0  = pin->GetReal("problem", "d");
  vin =  pin->GetReal("problem", "vin");
  // convert from CGS to Athena Heaviside units:
  b = pin->GetReal("problem", "b")/std::sqrt(4*M_PI);
  P0 = 4*M_PI*pcoeff*(b*b);
  return;
}


//========================================================================================
//! \fn void MeshBlock::ProblemGenerator(ParameterInput *pin)
//  \brief Problem Generator for zpinch problem
//========================================================================================

void MeshBlock::ProblemGenerator(ParameterInput *pin) {
  gm1 = peos->GetGamma() - 1.0;
  
  double debug_tester;

  if (std::strcmp(COORDINATE_SYSTEM, "cartesian") != 0) {
    std::stringstream msg;
    msg << "### FATAL ERROR in magnoh.cpp ProblemGenerator" << std::endl
        << "Unrecognized COORDINATE_SYSTEM= " << COORDINATE_SYSTEM << std::endl
        << "Only Cartesian are supported for this problem" << std::endl;
    ATHENA_ERROR(msg);
  }
  int dummy_variable;
  // initialize conserved variables
  for (int k=ks; k<=ke; k++) {
    for (int j=js; j<=je; j++) {
      for (int i=is; i<=ie; i++) {
        // Volume centered coordinates and quantities
        Real x1,x2,vx;
      
        x1 = pcoord->x1v(i);
        x2 = pcoord->x2v(j);

        Real rho = rho0*std::pow(std::abs(x1), alpha);
        Real P   = P0  *std::pow(std::abs(x1), 2*beta);

        phydro->u(IDN,k,j,i) = rho;         // Density

        vx = vin* 1/(std::abs(x2)+1/3.0);

        if (x1 >= 0) {
          phydro->u(IM1,k,j,i) = -rho*vx;
        } else{ // x1 < 0
          phydro->u(IM1,k,j,i) = rho*vx;
        }

        phydro->u(IM2,k,j,i) = 0.0;         // Momentum in x2
        phydro->u(IM3,k,j,i) = 0.0;         // Momentum in x3
        phydro->u(IEN,k,j,i) = P/gm1 + 0.5*rho*SQR(vx); // Total energy
        debug_tester = P/gm1 + 0.5*rho*SQR(vx); // TODO REMOVE
      }
    }
  }

  // initialize face-averaged magnetic fields
  if (MAGNETIC_FIELDS_ENABLED) {
    for (int k=ks; k<=ke; k++) {
      for (int j=js; j<=je; j++) {
        for (int i=is; i<=ie+1; i++) {
          Real x1;
          x1 = pcoord->x1v(i);
          if (x1 >= 0.0) {
            pfield->b.x2f(k,j,i) = (b/(beta+1))*std::pow(x1,beta+1);
          } else {
            pfield->b.x2f(k,j,i) = -1.0*(b/(beta+1))*std::pow(std::abs(x1),beta+1);
          }
          pfield->b.x1f(k,j,i) = 0.0;
          pfield->b.x3f(k,j,i) = 0.0;
        }
      }
    }
    if (NON_BAROTROPIC_EOS) {
      for (int k=ks; k<=ke; k++) {
        for (int j=js; j<=je; j++) {
          for (int i=is; i<=ie; i++) {
            phydro->u(IEN,k,j,i) +=
                // second-order accurate assumption about volume-averaged field
                0.5*0.25*(SQR(pfield->b.x1f(k,j,i) + pfield->b.x1f(k,j,i+1))
                          + SQR(pfield->b.x2f(k,j,i)  + pfield->b.x2f(k,j+1,i))
                          + SQR(pfield->b.x3f(k,j,i) + pfield->b.x3f(k+1,j,i)));
                          // Internal Energy is adjusted based on magnetic energy
          }
        }
      }
    }
  }
  return;
}
