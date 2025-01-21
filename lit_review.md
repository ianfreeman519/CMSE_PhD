# Literature Review
## Week of 01/13
[Magnetic Reconeection MHD Theory and Moedling (Pontin, Priest, 2022)](https://link.springer.com/article/10.1007/s41116-022-00032-9)

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