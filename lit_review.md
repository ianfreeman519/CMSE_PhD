# Literature Review
## [Magnetic Reconeection MHD Theory and Moedling (Pontin, Priest, 2022)](https://link.springer.com/article/10.1007/s41116-022-00032-9)

This article gives a fantastic overview of MHD reconnection theory and has a ton of links to other pages. The citations I give will be in last name, year format and refer to citations within this article.

Magnetic reconnection happens when magnetic Reynold's number $$R_{me}\equiv S\equiv \frac{L_{e}\nu_{A}}{\eta}\gg 1$$
Here, $L_{e}$ is the global length scale, $\nu_{A}=B_{e}/\sqrt{\mu\rho}$ is the global alfven speed with magnetic field $B_{e}$ and magnetic diffusivity $\eta$.

Magnetic reconnection is the change in connectivity of plasma elements, and result in some or all of the following physical effects:
 - the generation of strong electric currents, fields, and shock waves
 - ohmic dissipation of cucrenst (which transforms some magnetic energy to heat)
 - The appearance of Lorenz forces which accelerate plasma to high speeds
 - changes in the global connections of magnetic field lines which alter the paths of fast particles

Over the years after the formation of the Sweet Parker model (pg 6), the attention has shifted to 3D reconnection, where there is some electric field parallel to the magnetic field (not the case in 2D simulations or reconnection)
There are two classes of solutions which handle reconnection in 2D MHD: Flux conserved solutions and field-line conserving solutions:
 - Magnetic field lines are conserved when any pair of plasma elements lying initially on a magnetic field line remain connected by that field line. $B\times(\nabla\times N)=0$
 - Magnetic flux is conserved when the magnetic flux through any surface moving with the plasma is constant. $\nabla\times N=0$
Ideal MHD has $E+v\times B=0$, where both of the above conservation laws hold. Nonideal plasmas have $E+v\times B=N$ with nonzero $N$ representing any nonideal process.
If $N$ cannot be written as $N=u\times B+\nabla\phi$, then 2.5D or 3D reconnection takes place. However, if it can be written in this form then
 - if $u$ is smooth the magnetic field diffuses or slips through the plasma without reconnection
 - if u is singular then 2D reconnection occurs
    - in 2D you can havce slippage of the magnetic field or reconnection (at X-type null point) or destruction or generation of magnetic flux at O-type null points

3D Null points are way more complicated, and for a complete description, check out pages 12-15. This topic is discussed by way of "separatrix" lines which are the "x" of x-point or "O" of o-type reconnection in 2D. It is also possible for null points to bifurcate and split. The spine of a null point may yield null points on a fan (fig 8 -> fig 9, Brown and Pries 2001).

Here I am skipping a few pages (16-24) which talk extensively about quasi-separatrix lines, and should return later when I am ready to think about 3D reconnection in greater detail.

### Conservation Ideas

For an ideal MHD plasma, both flux and field-lines are conserved. In nonideal MHD, these are no longer equivalent conditions and neither flux velocity nor field-line velocity is unique. 

When magnetic Reynold's number is very large ($R_{m}\gg 1$), the plasma is approximately ideal. In this case, the induction equation and Ohm's law reduce to 
$$\frac{\partial B}{\partial t}=\nabla\times(v\times B)\quad\text{and}\quad E+v\times B=0$$

And components perpendicular to the magnetic field of plasma velocity ($v_{\perp}$), flux velocity ($w_{\perp}$), and field-line velocity ($w_{L\perp}$) are:

$$v_{\perp}=w_{\perp}=w_{L\perp}=\frac{E\times B}{B^2}$$

For **Magnetic Flux Conservation**, the magnetic flud (surface integral of $B\cdot dS$) implies that two plasma elements that are initially linked by a magnetic field line will continue to be linked at a later time (flux through a curve C1 at time t1 remains constant when it is distorted into a different curve C2 at time t2 by plasma motion).

For **non ideal MHD plasmas** Ohm's law takes the form $E+v\times B=N$ with N being any non-ideal term due to collisions, fluctuations, particle inertia, resistivity, etc. In the case of classical resistivity, $N=\eta\nabla\times B$.

**Magnetic flux conservation in non-ideal plasma** is an extension of the ideal case above. If the flux velocity $w$ exists such that
$$ \frac{\partial B}{\partial t}=\nabla\times(w\times B)$$
then we say the magnetic field evolution is flux-preserving. Ohm's law and Faraday's law combine to make
$$ \frac{\partial B}{\partial t}=\nabla\times(v\times B-N)$$
So long as $N=u\times B+\nabla\Phi$, with potential $\phi$ and the difference $u\equiv v-w$ between plasma and flux velocities is the slippage velocity. Now Ohm's law can be written in terms of $E+w\times B=\nabla \Phi$ and finally: **Magnetic flux is conserved if N satisfies $\nabla\times N=0$.**

Since displacements along the magnetic field are arbitrary, we may set them to zero so that $(w-v)\cdot B=0$. Combining this with forms of Ohm's law and dotting with B gives this form of **Magnetic Flux Velocity**:
$$w=v+\frac{(N-\nabla\Phi)\times B}{B^2}$$
Which means $w$ is singular when $B=0$. Additionally, $B\cdot\nabla\Phi=E\cdot B$. In integral form, this yields an expression for $\Phi$ which implies that **there is no reconnection when $E_{||}=0$.** There is magnetic diffusion, however, with slippage velocity given for a resistive Ohm's law:
$$u\equiv v-w=\frac{j\times B}{\sigma B^2}$$

*When magnetic flux is conserved, **magnetic field lines** are also conserved*, even in the plasma is non-ideal. Conversely, there are many field-line conservative processes that do not conserve flux. Magnetic field lines are conserved if
$$ \frac{\partial B}{\partial t}=\nabla\times(w_{L}\times B)+\lambda_{L}B\quad\text{or equivalently} \quad B\times(\nabla\times N)=0$$

with magnetic field-line velocity $w_{L}$ and scalar function of position $\lambda=\lambda_{L}+\nabla\cdot w_{L}$. Combining with $\nabla\cdot B=0$ yields the above $\frac{\partial B}{\partial t}$ term of magnetic field line conservation to:

$$\frac{\partial B}{\partial t} + (w_{L}\cdot\nabla)B-(B\cdot\nabla)w_{L}=\lambda B$$
which is equivalent to flux conservation if $\lambda_{L}=0$ and $w_{L}=w$ ...

When the plasma is non-ideal, the perendicular (to the magnetic field) velocity component ($w_{L\perp}$) can be defined uniqeuly iff Ohm's law can be expressed as $E+w_{L\perp}\times B=a$ with $\nabla \times a = -\lambda_{L}B$ (see page 29 for implications). This definition is field-line preserving but is only flux perserving if $\nabla\times a=0$, so $a=\nabla\Phi$ and $\lambda_{L}=0$.

If the plasma is ideal, $w_{L\perp}$ is just the $j\times B$ drift velocity: $w_{L\perp}=\frac{E\times B}{B^2}$, which is not suprising because the field lines are tied to plasma elements in ideal MHD, and if there is motion perpendicular to field lines, the field lines will be carried along.

### Magnetic diffusion and field-line motion definitions
Consider a plasma at rest with straight magnetic field lines in a current sheet. The magnetic field behaves as if the flux disappears either at a current sheet and/or at infinity. Circular field lines diffuse as if the magnetic field moves towards the O-type neutral line and/or toward infinity. In 3D, the decay of a field cannot be described in terms of the motion of magnetic field lines since it is not always possible to define a flux velocity. Instead you *can* use a 'dual flux velocity* but I have no clue what that means yet.

Consider a resistive diffusion of a magnetic field with uniform magnetic diffusivity $\eta$, so $E=\eta\nabla\times B$ and the induction equation becomes:
$$\frac{\partial B}{\partial t}=\nabla\times(\eta\nabla\times B)=\eta\nabla^2 B$$

When a 1D magnetic field (time varying, and spacially varying along x pointing in the y-direction) diffuses, field lines can dissapear at a neutral sheet or at boundaries and the diffusion equation is 
$$\frac{\partial B}{\partial t}=\eta\frac{\partial^2B}{\partial x^2}$$
This has a known solution which you can see on pg 30, and gives a flux velocity depending on an arbitrary function $E_{0}(t)$.

Now consider a field with circular field lines. On pg 31 we discover that magnetic field lines can disappear at O-points in 2D, and leads us to the question of whether or not it can happen in 3D.

## Leaping to section 7, Steady 2D models of Reconnection

### Sweet-Parker mechanism
The goal of the SP model is to determine the speed field lines enter the reconnection sizte and have their connections to plasma elements changed. Equating the first and third terms in Ohm's law gives the magnetic diffusion time:
$$\tau_{d}=\frac{L_{0}^2}{\eta}=10^{-9}L_{0}^2T^{3/2}$$

With $L_{0}$ in meters and T in Kelvin. This is massive in practice, for example coronal environments yield $\tau_{d}\approx10^{14}$ s. 

Sweet Parker came along and gave an order-of-magnitude treatment for a current sheet or diffusion region of length 2L and with 2l for which oppositely directed magnetic fields $B_{i}$ are carried in from both sides at speed $v_{i}$. In a steady state this will be the same as the diffusion speed $\tau_{d}/l$ with which the sheet diffuses outward at $v_{i}=\eta/l$. Furthermore conservation of mass, with plasma coming in through the long side L and flowing out through the short side give flow rate relation $Lv_{i}=lv_{0}$.

If the plasma is accelerated along the current sheet by the $j\times B$ force the outflow speed is just the inflow Alfven speed
$$v_{0}=v_{Ai}\equiv\frac{B_{i}}{\sqrt{\mu\rho}}$$

which allows us to calculate $v_{i}$, the reconnection rate, or more accurately the inflow velocity to the long edge of the current sheet.

$$v_{i}=\frac{v_{Ai}}{R_{mi}^{1/2}}\quad \text{or equivalently}\quad M_{i}=\frac{1}{R_{mi}^{1/2}}$$

This is a very slow reconnection rate, which for coronal environments ($R_{mi}\approx 10^8-10^{12}$), we get $10^{-4}-10^{-6}$ of the Alfven speed, which is too slow to account for solar flares.

**Going to take a break from this review for a while because I think I got a lot out of it and need to pivot to the radiative side of things for a minute...**

## [Magnetic Reconnection with Radiative Cooling. I. Optically Thin Regime (Uzdensky and McKinney)](https://pubs.aip.org/aip/pop/article-abstract/18/4/042105/281820/Magnetic-reconnection-with-radiative-cooling-I?redirectedFrom=fulltext)

The premise of this paper is that reconnection rate is dependent on the aspect ratio of the reconnection layer. When radiative effects come into play, the layer is compressed because the cooler layer has lower pressure/temperature which does not provide counter-pressure to compression and has higher Spitzer resistivity. This, in turn, spikes the reconnection rate.

This paper also goes into the typical "MR is relevant to astrophysics and a bunch of other plasma stuff..." This paper does do a good job saying, however, that the scope of reconnection scalings is dependent on the system, and extreme systems have different scalings. 

Assume the plasma is dense, so resistive MHD is accurate, and scalar resistivity is valid (thus hall terms are zero, and generalized Ohms law is simple). The SP model assumes the plasma is incompressible, U&M don't assume this.

Collisional to Collisionless reconnection occurs when the layer thickness becomes comparable to the ion collisionless skin-depth, $d_{i}=c/\omega_{pi}$. If the system approaches this transition, the optical depth is $\tau(d_{i})=n_{e}\sigma d_{i}$ with scattering cross section $\sigma$. The Thomson cross-section is $\sigma_{T}=(8\pi/3)r_{e}^2$ where $r_{e}=e^2/m_{e}c^2$. Substituting all this into the optical depth value 

$$\tau(d_{i})\approx 100(n_{e}r_{e}^3)^{1/2}$$

Therefore unless density approaches $10^33 cm^{-3}$, reconnection layers on the brink of the collisional/collisionless transition is unavoidably optically thin to Thomson scattering. (**TODO I'm not sure what this means for the optically thick case. Does this mean that we need incredibly high density to reach optically thick conditions, or is this just considering the Thomson scattering?**)

### SP MR in strong-compression limit
Consider a layer with half-length $L$ and half-thickness $\delta$. The direction across the layer is y. The inflow velocity is denoted $v_{rec}$ and outflow velocity is $u$. Subscript 0 means upstream of the layer (upstream magnetic field $B_{0}$, upstream density $n_{0}$, and upstrea temperature $T_{0}$) like the upstream Alfven velocity $$V_{A0}\equiv \frac{B_{0}}{\sqrt{4\pi n_{0}m_{p}}}$$

The global upstream Alfven transit time is $\tau_{A0}\equiv L/V_{A0}$ and the corresponding Lundquist number is $S_{0}\equiv LV_{A0}/\eta$ with magnetic diffusivity $\eta$. At the center of the layer we carry no subscripts.

The compression ratio $A\equiv n/n_{0}$ is useful for analysis, and it is the ratio of the density _inside_ the layer $n$ to the density _outside_ the layer $n_{0}$. If strong cooling happens $A\gg 1$. The goal of the model is to define some relationship between $L$, $n_{0}$, $T_{0}$, $B_{0}$, $\eta$ in the layer and the radiative parameters to the parameters inside the layer like $n$, $T$, $\delta$, $u$, and $v_{rec}$ (or equivalently the reconnection Electric field $E_{z}=-v_{rec}B_{0}/c$). This is five inputs to five outputs so we need 5 equations.

#### Conservation of Mass Through the Reconnection Layer
$$n_{0}v_{rec}L\approx nu\delta\implies v_{rec}L\approx Au\delta$$

This assumes the plasma near the outflow point has roughly the same density at the center of the layer. This is a flow equation (flow into the flat reconnection layer is equivalent to the flow leaving the layer through the thin side).

#### Magnetic Fields
The out-of-plane electric field $E_{z}$ is uniform across the domain. Just outside the layer $E_{z}=-v_{rec}B_{0}/c$, and at the center (where $B$ and $v$ are 0), Oh'ms law yields $E_{z}=\eta'j_{z}$ with plasma resistivity $\eta'$ defined via the relationship to magnetic diffusivity $\eta=\eta'c^2/4\pi$. Using Ampere's law we can write $j_{z}\approx-cB_{0}/4\pi\delta$, and we retrieve a result from the SP model:
$$\eta\approx v_{rec}\delta$$

This allows us to consider the magnetic field strength at the outflow region. Call $B_{1}=B_{y}(x=L, y=0)$ and call $B_{0}$ the strength of the magnetic field at the inflow point. Since $E_{z}$ is uniform through the layer we have: $cE_{z}=-v_{rec}B_{0}=-uB_{1}$ which is a statement of magnetic flux conservation. (inflow velocity times magnetic field strength = outflow velocity times magnetic field strength). Combining with mass conservation we find the magnetic field (y-component of-) at the outflow point is $$B_{1}=B_{y}(L,0)=B_{0}\frac{v_{rec}}{u}\approx B_{0}\frac{\delta}{L}A$$

#### Equations of Motion
$$P=P(0,0)=\frac{B_{0}^2}{8\pi}$$
Considering the equation of motion along the layer at the layer's midplane:
$$\rho v_{x}\partial_{x}v_{x}=-\partial_{x}P-j_{z}B_{y}/c$$
For an order-of-magnitude estimate, we can drop the magnetic tension term ($-j_{z}B_{y}/c$), and integrate from 0 to L to find:
$$\frac{1}{2}\rho u^2\approx\frac{B_{0}^2}{8\pi}$$

This means that the outflow velocity $u$ in the SP reconnection rate is the Alfven velocity computed with the upstream $B_{0}$ and density $\rho$ (which is uniform in SP because incompressibility). In the compressible system, though, this is not the case, and the tension force is much larger than the pressure gradient force. From the magnetic field consideration above we have 

$$-j_{z}B_{y}/c\approx (B_{0}/v\pi\delta)(B_{0}A\delta/2L)=AB_{0}^2/8\pi L$$ 

which is a factor $A\gg1$ greater than $\partial_{x}P\approx B_{0}^2/(8\pi L)$. This tension force is equal to the characteristic magnitude of $\rho v_{x}\partial_{x}v_{x}\approx\rho u^2/2L$, and it immediately follows that the outflow velocity at the end of the layer is comparable to the upstream Alfven velocity (involving the density and the magnetic field just outside the layer):

$$u\approx\frac{B_[0]}{\sqrt{4\pi n_{0}m_{P}}}=V_{A0}$$

#### Given A, finding the reconnection rate
By substituting Ohm's law in with the continuity equation we find:
$$v_{rec}^2\approx\frac{A\eta u}{L}\approx\frac{\eta V_{A0}A}{L}$$
$$\implies v_{rec}\approx V_{A0}\frac{A^{1/2}}{S_{0}^{1/2}}$$

Thus, allowing for compression makes reconnection faster by a factor of $A^{1/2}$. Finally the thickness of the layer is $\delta=\eta/v_{rec}$, which is equivalent to:
$$\delta\approx\frac{\eta}{v_{rec}}\approx LS_{0}^{-1/2}A^{1/2}=\delta_{SP}A^{1/2}$$

### Strong-Compression MR with Spitzer Resistivity
Previously resistivity was assumed to be constant throughout the plasma. This is unphysical, and Perpendicular Spitzer Resistivity is the way to go.
$$\eta_{\perp}=C_{\eta}cr_{e}\text{ln}\Lambda\theta_{e}^{-3/2}$$
with $C_{\eta}=0.27$, $\theta_{e}$ is the actual central electron temperature, and $\text{ln}\Lambda$ is the Coulomb logarithm. Recall the Lundquist Number $S$ from before was the ratio of the Alfven time to the resistivitiy. Now that resistivitiy depends on other things like the temperature of the electrons.

$$S(n,\theta_{e})=\frac{LV_{A}}{\eta_{\perp}}=C_{\eta}^{-1}\frac{L}{r_{e}\text{ln}\Lambda}\frac{V_{A}}{c}\theta_{e}^{3/2}$$

This isn't useful because we need $S$ in terms of $n_{0}$ and hopefully the compression ratio $A$. Recall the pressure balance earlier $B_{0}^2/8\pi=P$. For an electron-ion plasma (in which the temperatures are the same), we allow $P=2nk_{B}T$. Thus:
$$k_{B}T(A)=\frac{B_{0}^2}{16\pi n}=A^{-1}k_{B}T_{eq}$$
where $k_{B}T_{eq}\equiv B_{0}^2/16\pi n_{0}$ is the central temperature that the layer would need to have without compression (i.e. $A=1$). In dimensionless form (scaling to the electron rest energy):
$$\theta_{e}\equiv\frac{k_{B}T}{m_{e}c^2}=A^{-1}\frac{B_{0}^2}{16\pi n_{0}m_{e}c^2}=\frac{1}{4A}\frac{m_{p}}{m_{e}}\frac{V_{A0}^2}{c^2}$$

which after substitution leads to lundquist number

$$S_0=C_{\eta}^{-1}\frac{L}{r_{e}\text{ln}\Lambda}\frac{V_{A}}{c}\theta_{e}^{3/2}= \frac{1}{8C_{\eta}}\frac{L}{r_{e}\text{ln}\Lambda}(\frac{V_{A0}}{c})^4(\frac{m_{p}}{m_{e}})^{3/2}A^{-3/2}$$

reconnection velocity
$$\frac{v_{rec}}{c}\approx\sqrt{\frac{8C_{\eta}r_{x}\text{ln}\Lambda}{L}}(\frac{V_{A0}}{c})^{-1}(\frac{m_{e}}{m_{p}})^{3/4}A^{5/4}$$

and layer thickness 
$$\delta^2\approx7C_{\eta}(Lr_{e})\text{ln}\ln\Lambda(\frac{V_{A0}}{c})^{-4}(\frac{m_{e}}{m_{p}})^{3/2}A^{1/2}$$

### Thermodynamics of the radiatively cooled reconnection layer and compression ratio
SP only analyzed the incompressible case (in which they did not have to consider the compressible energy equations). Assume the upstream plasma beta is small. The energy conservation in a steady state can be viewed as a balance between the flux of magnetic enthalpy flowing onto the layer and the sum of the advection of plasma thermal enthalpy and kinetic energy out of the layer (and now including the radiative cooling across the layer). The magnetic enthalpy flux per area is the sum of inflowing magnetic energy $v_{rec}B_{0}^2/8\pi$ and the work done by magnetic pressure which is of the same form thus total Magnetic enthalpy flux is $v_{rec}B_{0}^2/4\pi$.

The poynting vector is uniquely of the same form $S_{Poynt}=cEB_{0}/4\pi=v_{rec}B_{0}^2/4\pi$. Call the advective and radiative energy fluxes $F_{adv}$ and $F_{rad}$, so we find energy conservation:
$$S_{Poynt}\approx \frac{C}{4\pi}EB_{0}L\approx F_{adv}\delta + F_{rad}L$$

The energy flowing out of the layer (advective energy flux) can be estimated as the sum of kinetic energy flux and thermal enthalpy flux of a two-species gas.
$$F_{adv}\delta\approx u(\rho u^2/2 + 5nk_{B}T)\delta$$

The condition of pressure balance across the layer dictates that $2nk_{B}T\approx B_{0}^2/8\pi$. Similarly the equation of motion along the layer dictates that $\rho u^2/2\approx AB_{0}^2/8\pi$. When $A=1$ (i.e. SP case), the advective energy flux is zero. When $A\gg 1$ the kinetic energy flux dominates over the thermal enthalpy flux. Thus

$$\frac{F_{adv}\delta}{S_{Poynt}L}\approx\frac{uA\delta}{v_{rec}L}=O(1)$$

when using the continuity equation derived above. **Independent of the strength of radiative cooling (and hence of plasma compression) a finite fraction of incoming magnetic energy is not dissipated into heat (which is then promptly radiated away), but instead converted directly into the mechanical kinetic energy of the outflow**. 

This means that the Poynting flux vs radiative losses cannot be used to accurately describe the compression ratio A. Looking at the _entropy_ instead, which is the balance between the plasma heating due to the dissipation of magnetic energy (ohmic heating) and plasma cooling from $F_{rad}$ and $F_{adv}$, allows us to claim that the system is in **the strong radiative cooling regime if the ohmic heating rate is primarily balanced by radiative losses, whereas the heat losses by advection are small.** This is in contrast with the classical (nonradiative) SP model.

$$Q_{ohm}=\eta'j^2\approx A\frac{B_{0}^2}{4\pi\tau_{A0}}\equiv AQ_{0}$$

This Ohmic heating rate equation requires the use of the mass continuity equation and the approximation that $u\approx V_{A0}$ above. The heat loss due to advection out of the layer is the thermal energy density divided by the advection time along the layer $L/V_{A0}=\tau_{A0}$:

$$Q_{adv}\approx\frac{3nk_{B}T}{L/u}\approx Q_{ohm}/A\quad\text{(to first order)}$$

When Ohmic heating is precisely balanced by advective losses ($Q_{ohm}\approx Q_{adv}$) we find $A\approx 1$. This means the amount of heat added to a fluid element as it travels through the reconnection region is roughly the amount needed to raise the plasma temperature to the pressure equipartition level without the need for adiabatic compression heating. Therefore when A=1, we still find no layer compression.

In general one can say that the reconnection process partly converts magnetic energy into kinetic energy to the outflow and generates heat (this is true in both non-radiative SP MR and optically thin radiative MR). However, the SP case both forms of plasma energy are taken out along the layer by the plasma outflow but in the strong radiative cooling case the kinetic part of the energy is still advected out but the thermal energy is lost due to radiation. If $A\gg 1$ the radiative loss is much larger than advective heat loss, so we have a form for $Q_{rad}$:
$$Q_{rad}(n,T)=Q_{ohm}\approx AQ_{0}$$

