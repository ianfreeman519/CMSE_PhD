# Random things I *should* know from undergrad thermal physics, but don't.
## Ideal Gases
Well known $pV=n_{moles}RT$ can be cast into $p=nkT$, with $k=R/A_0$ (Avagadro's number is $A_0$) and $n$ representing number density ($N_{particles}/V$). With atomic weight of the gas $A$, the density of a material is $\rho=NAm_p$, we find the pressure is (eq 1.3 pdf17): $$p=\rho \frac{kT}{Am_p}=\rho RT$$

## First law of Thermo
$E_{int}$ represents the internal energy in volume $V$. $dQ$ is the amount of heat gained or lost (positive for gains), and $dW$ is the work done **BY** the gas (positive when the gas **DOES** work) in an infinitesimal proces (Equation 2.1 pdf17): $$dE_{int}=dQ-dW$$

Usefully, we can rewrite this using the 'specific internal energy' $e$ (internal energy per unit mass) and $dq$ as the heat input per unit mass (eq 2.3 pdf18): $$de=dq-pd(1/\rho)$$

Along with $dq$ as the heat input per unit mass, we have specific heat $c=dq/dT$. There are two subtypes of specific heat that show up everywhere: specific heat at constant volume $c_v$ and specific heat at constant pressure $c_p$. There are a ton of definitions of these (Eqs 2.6-2.34) on page 5&6 (pdf20&21) of the book.

## Second law of Thermo
We define entropy $S$ as (eq 3.1 pdf21) $dS=dQ/T$. This is the second law of thermodynamics. For a reversible cycle, $S=0$, but for irreversible cycles from $B$ to $A$ we always have $S(B)\geq S(A)$.

## Sound speed
There are two relevant sound speeds: there is an isothermal sound speed $a_T$, given by $a_T=\sqrt{p/\rho}$ and the generic sound speed (almost always more useful) (eq 51.26 pdf196): $$c_s=\sqrt{\gamma p/\rho}$$
