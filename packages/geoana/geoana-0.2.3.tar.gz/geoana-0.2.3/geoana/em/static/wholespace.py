import numpy as np
from scipy.special import ellipk, ellipe

from ..base import BaseDipole, BaseMagneticDipole, BaseEM
from ... import spatial

__all__ = [
    "MagneticDipoleWholeSpace", "CircularLoopWholeSpace",
    "MagneticPoleWholeSpace"
]


class MagneticDipoleWholeSpace(BaseEM, BaseMagneticDipole):
    """Class for a static magnetic dipole in a wholespace.

    The ``MagneticDipoleWholeSpace`` class is used to analytically compute the
    fields and potentials within a wholespace due to a static magnetic dipole.

    """

    def vector_potential(self, xyz, coordinates="cartesian"):
        r"""Compute the vector potential for the static magnetic dipole.

        This method computes the vector potential for the magnetic dipole at
        the set of gridded xyz locations provided. Where :math:`\mu` is the
        magnetic permeability, :math:`\mathbf{m}` is the dipole moment,
        :math:`\mathbf{r_0}` the dipole location and :math:`\mathbf{r}`
        is the location at which we want to evaluate
        the vector potential :math:`\mathbf{a}`:

        .. math::

            \mathbf{a}(\mathbf{r}) = \frac{\mu}{4\pi}
            \frac{\mathbf{m} \times \, \Delta \mathbf{r}}{| \Delta r |^3}

        where

        .. math::
            \mathbf{\Delta r} = \mathbf{r} - \mathbf{r_0}

        For reference, see equation 5.83 in Griffiths (1999).

        Parameters
        ----------
        xyz : (n, 3) numpy.ndarray xyz
            gridded locations at which we are calculating the vector potential
        coordinates: str {'cartesian', 'cylindrical'}
            coordinate system that the location (xyz) are provided.
            The solution is also returned in this coordinate system.
            Default: `"cartesian"`

        Returns
        -------
        (n, 3) numpy.ndarray
            The magnetic vector potential at each observation location in the
            coordinate system specified in units *Tm*.

        Examples
        --------
        Here, we define a z-oriented magnetic dipole and plot the vector
        potential on the xy-plane that intercepts at z=0.

        >>> from geoana.em.static import MagneticDipoleWholeSpace
        >>> from geoana.utils import ndgrid
        >>> from geoana.plotting_utils import plot2Ddata
        >>> import numpy as np
        >>> import matplotlib.pyplot as plt

        Let us begin by defining the magnetic dipole.

        >>> location = np.r_[0., 0., 0.]
        >>> orientation = np.r_[0., 0., 1.]
        >>> moment = 1.
        >>> dipole_object = MagneticDipoleWholeSpace(
        >>>     location=location, orientation=orientation, moment=moment
        >>> )

        Now we create a set of gridded locations and compute the vector potential.

        >>> xyz = ndgrid(np.linspace(-1, 1, 20), np.linspace(-1, 1, 20), np.array([0]))
        >>> a = dipole_object.vector_potential(xyz)

        Finally, we plot the vector potential on the plane. Given the symmetry,
        there are only horizontal components.

        >>> fig = plt.figure(figsize=(4, 4))
        >>> ax = fig.add_axes([0.15, 0.15, 0.8, 0.8])
        >>> plot2Ddata(xyz[:, 0:2], a[:, 0:2], ax=ax, vec=True, scale='log')
        >>> ax.set_xlabel('X')
        >>> ax.set_ylabel('Z')
        >>> ax.set_title('Vector potential at z=0')

        """
        supported_coordinates = ["cartesian", "cylindrical"]
        assert coordinates.lower() in supported_coordinates, (
            "coordinates must be in {}, the coordinate system "
            "you provided, {}, is not yet supported".format(
                supported_coordinates, coordinates
            )
        )

        n_obs = xyz.shape[0]

        # orientation of the dipole
        if coordinates.lower() == "cylindrical":
            xyz = spatial.cylindrical_2_cartesian(xyz)

        dxyz = self.vector_distance(xyz)
        r = spatial.repeat_scalar(self.distance(xyz))
        m = self.moment * np.atleast_2d(self.orientation).repeat(n_obs, axis=0)

        m_cross_r = np.cross(m, dxyz)
        a = (self.mu / (4 * np.pi)) * m_cross_r / (r**3)

        if coordinates.lower() == "cylindrical":
            a = spatial.cartesian_2_cylindrical(xyz, a)

        return a

    def magnetic_flux_density(self, xyz, coordinates="cartesian"):
        r"""Compute magnetic flux density produced by the static magnetic dipole.

        This method computes the magnetic flux density produced by the static magnetic
        dipole at gridded xyz locations provided. Where :math:`\mu` is the magnetic
        permeability of the wholespace, :math:`\mathbf{m}` is the dipole moment,
        :math:`\mathbf{r_0}` the dipole location and :math:`\mathbf{r}` is the location
        at which we want to evaluate the magnetic flux density :math:`\mathbf{B}`:

        .. math::

            \mathbf{B}(\mathbf{r}) = \frac{\mu}{4\pi} \Bigg [
            \frac{3 \Delta \mathbf{r} \big ( \mathbf{m} \cdot \, \Delta \mathbf{r} \big ) }{| \Delta \mathbf{r} |^5}
            - \frac{\mathbf{m}}{| \Delta \mathbf{r} |^3} \Bigg ]

        where

        .. math::
            \mathbf{\Delta r} = \mathbf{r} - \mathbf{r_0}

        For reference, see equation Griffiths (1999).

        Parameters
        ----------
        xyz : (n, 3) numpy.ndarray
            gridded locations at which we calculate the magnetic flux density
        coordinates: str {'cartesian', 'cylindrical'}
            coordinate system that the location (xyz) are provided.
            The solution is also returned in this coordinate system.
            Default: `"cartesian"`

        Returns
        -------
        (n, 3) numpy.ndarray
            The magnetic flux density at each observation location in the
            coordinate system specified in Teslas.


        Examples
        --------
        Here, we define a z-oriented magnetic dipole and plot the magnetic
        flux density on the xy-plane that intercepts y=0.

        >>> from geoana.em.static import MagneticDipoleWholeSpace
        >>> from geoana.utils import ndgrid
        >>> from geoana.plotting_utils import plot2Ddata
        >>> import numpy as np
        >>> import matplotlib.pyplot as plt

        Let us begin by defining the magnetic dipole.

        >>> location = np.r_[0., 0., 0.]
        >>> orientation = np.r_[0., 0., 1.]
        >>> moment = 1.
        >>> dipole_object = MagneticDipoleWholeSpace(
        >>>     location=location, orientation=orientation, moment=moment
        >>> )

        Now we create a set of gridded locations and compute the vector potential.

        >>> xyz = ndgrid(np.linspace(-1, 1, 20), np.array([0]), np.linspace(-1, 1, 20))
        >>> B = dipole_object.magnetic_flux_density(xyz)

        Finally, we plot the vector potential on the plane. Given the symmetry,
        there are only horizontal components.

        >>> fig = plt.figure(figsize=(4, 4))
        >>> ax = fig.add_axes([0.15, 0.15, 0.8, 0.8])
        >>> plot2Ddata(xyz[:, 0::2], B[:, 0::2], ax=ax, vec=True, scale='log')
        >>> ax.set_xlabel('X')
        >>> ax.set_ylabel('Z')
        >>> ax.set_title('Magnetic flux density at y=0')

        """

        supported_coordinates = ["cartesian", "cylindrical"]
        assert coordinates.lower() in supported_coordinates, (
            "coordinates must be in {}, the coordinate system "
            "you provided, {}, is not yet supported".format(
                supported_coordinates, coordinates
            )
        )

        n_obs = xyz.shape[0]

        if coordinates.lower() == "cylindrical":
            xyz = spatial.cylindrical_2_cartesian(xyz)

        r = self.vector_distance(xyz)
        dxyz = spatial.repeat_scalar(self.distance(xyz))
        m_vec = (
            self.moment * np.atleast_2d(self.orientation).repeat(n_obs, axis=0)
        )

        m_dot_r = (m_vec * r).sum(axis=1)

        # Repeat the scalars
        m_dot_r = np.atleast_2d(m_dot_r).T.repeat(3, axis=1)
        # dxyz = np.atleast_2d(dxyz).T.repeat(3, axis=1)

        b = (self.mu / (4 * np.pi)) * (
            (3.0 * r * m_dot_r / (dxyz ** 5)) -
            m_vec / (dxyz ** 3)
        )

        if coordinates.lower() == "cylindrical":
            b = spatial.cartesian_2_cylindrical(xyz, b)

        return b

    def magnetic_field(self, xyz, coordinates="cartesian"):
        r"""Compute the magnetic field produced by a static magnetic dipole.

        This method computes the magnetic field produced by the static magnetic dipole at
        the set of gridded xyz locations provided. Where :math:`\mathbf{m}` is the dipole
        moment, :math:`\mathbf{r_0}` is the dipole location and :math:`\mathbf{r}` is the
        location at which we want to evaluate the magnetic field :math:`\mathbf{H}`:

        .. math::

            \mathbf{H}(\mathbf{r}) = \frac{1}{4\pi} \Bigg [
            \frac{3 \Delta \mathbf{r} \big ( \mathbf{m} \cdot \, \Delta \mathbf{r} \big ) }{| \Delta \mathbf{r} |^5}
            - \frac{\mathbf{m}}{| \Delta \mathbf{r} |^3} \Bigg ]

        where

        .. math::
            \mathbf{\Delta r} = \mathbf{r} - \mathbf{r_0}

        For reference, see equation Griffiths (1999).

        Parameters
        ----------
        xyz : (n, 3) numpy.ndarray xyz
            gridded locations at which we calculate the magnetic field
        coordinates: str {'cartesian', 'cylindrical'}
            coordinate system that the location (xyz) are provided.
            The solution is also returned in this coordinate system.
            Default: `"cartesian"`

        Returns
        -------
        (n, 3) numpy.ndarray
            The magnetic field at each observation location in the
            coordinate system specified in units A/m.

        Examples
        --------
        Here, we define a z-oriented magnetic dipole and plot the magnetic
        field on the xz-plane that intercepts y=0.

        >>> from geoana.em.static import MagneticDipoleWholeSpace
        >>> from geoana.utils import ndgrid
        >>> from geoana.plotting_utils import plot2Ddata
        >>> import numpy as np
        >>> import matplotlib.pyplot as plt

        Let us begin by defining the magnetic dipole.

        >>> location = np.r_[0., 0., 0.]
        >>> orientation = np.r_[0., 0., 1.]
        >>> moment = 1.
        >>> dipole_object = MagneticDipoleWholeSpace(
        >>>     location=location, orientation=orientation, moment=moment
        >>> )

        Now we create a set of gridded locations and compute the vector potential.

        >>> xyz = ndgrid(np.linspace(-1, 1, 20), np.array([0]), np.linspace(-1, 1, 20))
        >>> H = dipole_object.magnetic_field(xyz)

        Finally, we plot the vector potential on the plane. Given the symmetry,
        there are only horizontal components.

        >>> fig = plt.figure(figsize=(4, 4))
        >>> ax = fig.add_axes([0.15, 0.15, 0.8, 0.8])
        >>> plot2Ddata(xyz[:, 0::2], H[:, 0::2], ax=ax, vec=True, scale='log')
        >>> ax.set_xlabel('X')
        >>> ax.set_ylabel('Z')
        >>> ax.set_title('Magnetic field at y=0')

        """
        return self.magnetic_flux_density(xyz, coordinates=coordinates) / self.mu


class MagneticPoleWholeSpace(BaseEM, BaseMagneticDipole):
    """Class for a static magnetic pole in a wholespace.

    The ``MagneticPoleWholeSpace`` class is used to analytically compute the
    fields and potentials within a wholespace due to a static magnetic pole.
    """

    def magnetic_flux_density(self, xyz, coordinates="cartesian"):
        r"""Compute the magnetic flux density produced by the static magnetic pole.

        This method computes the magnetic flux density produced by the static magnetic pole
        at the set of gridded xyz locations provided. Where :math:`\mu` is the magnetic
        permeability of the wholespace, :math:`m` is the moment amplitude,
        :math:`\mathbf{r_0}` the pole's location and :math:`\mathbf{r}` is the location
        at which we want to evaluate the magnetic flux density :math:`\mathbf{B}`:

        .. math::

            \mathbf{B}(\mathbf{r}) = \frac{\mu m}{4\pi} \frac{\Delta \mathbf{r}}{| \Delta \mathbf{r}|^3}

        where

        .. math::
            \mathbf{\Delta r} = \mathbf{r} - \mathbf{r_0}

        For reference, see equation Griffiths (1999).

        Parameters
        ----------
        xyz : (n, 3) numpy.ndarray xyz
            gridded xyz locations at which we calculate the magnetic flux density
        coordinates: str {'cartesian', 'cylindrical'}
            coordinate system that the location (xyz) are provided.
            The solution is also returned in this coordinate system.
            Default: `"cartesian"`

        Returns
        -------
        (n, 3) numpy.ndarray
            The magnetic flux density at each observation location in the
            coordinate system specified in units T.

        """

        supported_coordinates = ["cartesian", "cylindrical"]
        assert coordinates.lower() in supported_coordinates, (
            "coordinates must be in {}, the coordinate system "
            "you provided, {}, is not yet supported".format(
                supported_coordinates, coordinates
            )
        )

        n_obs = xyz.shape[0]

        if coordinates.lower() == "cylindrical":
            xyz = spatial.cylindrical_2_cartesian(xyz)

        r = self.vector_distance(xyz)
        dxyz = spatial.repeat_scalar(self.distance(xyz))

        b = self.moment * self.mu / (4 * np.pi * (dxyz ** 3)) * r

        if coordinates.lower() == "cylindrical":
            b = spatial.cartesian_2_cylindrical(xyz, b)

        return b

    def magnetic_field(self, xyz, coordinates="cartesian"):
        r"""Compute the magnetic field produced by the static magnetic pole.

        This method computes the magnetic field produced by the static magnetic pole at
        the set of gridded xyz locations provided. Where :math:`\mu` is the magnetic
        permeability of the wholespace, :math:`m` is the moment amplitude,
        :math:`\mathbf{r_0}` the pole's location and :math:`\mathbf{r}` is the location
        at which we want to evaluate the magnetic field :math:`\mathbf{H}`:

        .. math::

            \mathbf{G}(\mathbf{r}) = \frac{m}{4\pi} \frac{\Delta \mathbf{r}}{| \Delta \mathbf{r}|^3}

        where

        .. math::
            \mathbf{\Delta r} = \mathbf{r} - \mathbf{r_0}

        For reference, see equation Griffiths (1999).

        Parameters
        ----------
        xyz : (n, 3) numpy.ndarray xyz
            gridded locations at which we calculate the magnetic field
        coordinates: str {'cartesian', 'cylindrical'}
            coordinate system that the location (xyz) are provided.
            The solution is also returned in this coordinate system.
            Default: `"cartesian"`

        Returns
        -------
        (n, 3) numpy.ndarray
            The magnetic field at each observation location in the
            coordinate system specified in units A/m.

        """
        return self.magnetic_flux_density(xyz, coordinates=coordinates) / self.mu


class CircularLoopWholeSpace(BaseEM, BaseDipole):
    """Class for a circular loop of static current in a wholespace.

    The ``CircularLoopWholeSpace`` class is used to analytically compute the
    fields and potentials within a wholespace due to a circular loop carrying
    static current.

    Parameters
    ----------
    current : float
        Electrical current in the loop (A). Default is 1.
    radius : float
        Radius of the loop (m). Default is :math:`\\pi^{-1/2}` so that the loop
        has a default dipole moment of 1 :math:`A/m^2`.
    """

    def __init__(self, radius=np.sqrt(1.0/np.pi), current=1.0, **kwargs):

        self.current = current
        self.radius = radius
        super().__init__(**kwargs)


    @property
    def current(self):
        """Current in the loop in Amps

        Returns
        -------
        float
            Current in the loop Amps
        """
        return self._current

    @current.setter
    def current(self, value):

        try:
            value = float(value)
        except:
            raise TypeError(f"current must be a number, got {type(value)}")

        if value <= 0.0:
            raise ValueError("current must be greater than 0")

        self._current = value


    @property
    def radius(self):
        """Radius of the loop in meters

        Returns
        -------
        float
            Radius of the loop in meters
        """
        return self._radius

    @radius.setter
    def radius(self, value):

        try:
            value = float(value)
        except:
            raise TypeError(f"radius must be a number, got {type(value)}")

        if value <= 0.0:
            raise ValueError("radius must be greater than 0")

        self._radius = value

    def vector_potential(self, xyz, coordinates="cartesian"):
        r"""Compute the vector potential for the static loop in a wholespace.

        This method computes the vector potential for the cirular current loop
        at the set of gridded xyz locations provided. Where :math:`\mu` is the magnetic
        permeability, :math:`I d\mathbf{s}` represents an infinitessimal segment
        of current at location :math:`\mathbf{r_s}` and :math:`\mathbf{r}` is the location
        at which we want to evaluate the vector potential :math:`\mathbf{a}`:

        .. math::

            \mathbf{a}(\mathbf{r}) = \frac{\mu I}{4\pi} \oint
            \frac{1}{|\mathbf{r} - \mathbf{r_s}|} d\mathbf{s}


        The above expression can be solve analytically by using the appropriate
        change of coordinate transforms and the solution for a horizontal current
        loop. For a horizontal current loop centered at (0,0,0), the solution in
        radial coordinates is given by:

        .. math::

            a_\theta (\rho, z) = \frac{\mu_0 I}{\pi k}
            \sqrt{ \frac{R}{\rho^2}} \bigg [ (1 - k^2/2) \, K(k^2) - K(k^2) \bigg ]

        where

        .. math::

            k^2 = \frac{4 R \rho}{(R + \rho)^2 + z^2}

        and

        - :math:`\rho = \sqrt{x^2 + y^2}` is the horizontal distance to the test point
        - :math:`I` is the current through the loop
        - :math:`R` is the radius of the loop
        - :math:`E(k^2)` and :math:`K(k^2)` are the complete elliptic integrals

        Parameters
        ----------
        xyz : (n, 3) numpy.ndarray xyz
            gridded locations at which we calculate the vector potential
        coordinates: str {'cartesian', 'cylindrical'}
            coordinate system that the location (xyz) are provided.
            The solution is also returned in this coordinate system.
            Default: `"cartesian"`

        Returns
        -------
        (n, 3) numpy.ndarray
            The magnetic vector potential at each observation location in the
            coordinate system specified in units *Tm*.

        Examples
        --------
        Here, we define a horizontal loop and plot the vector
        potential on the xy-plane that intercepts at z=0.

        >>> from geoana.em.static import CircularLoopWholeSpace
        >>> from geoana.utils import ndgrid
        >>> from geoana.plotting_utils import plot2Ddata
        >>> import numpy as np
        >>> import matplotlib.pyplot as plt

        Let us begin by defining the loop.

        >>> location = np.r_[0., 0., 0.]
        >>> orientation = np.r_[0., 0., 1.]
        >>> radius = 0.5
        >>> simulation = CircularLoopWholeSpace(
        >>>     location=location, orientation=orientation, radius=radius
        >>> )

        Now we create a set of gridded locations and compute the vector potential.

        >>> xyz = ndgrid(np.linspace(-1, 1, 50), np.linspace(-1, 1, 50), np.array([0]))
        >>> a = simulation.vector_potential(xyz)

        Finally, we plot the vector potential on the plane. Given the symmetry,
        there are only horizontal components.

        >>> fig = plt.figure(figsize=(4, 4))
        >>> ax = fig.add_axes([0.15, 0.15, 0.8, 0.8])
        >>> plot2Ddata(xyz[:, 0:2], a[:, 0:2], ax=ax, vec=True, scale='log')
        >>> ax.set_xlabel('X')
        >>> ax.set_ylabel('Y')
        >>> ax.set_title('Vector potential at z=0')

        """

        eps = 1e-10
        supported_coordinates = ["cartesian", "cylindrical"]
        assert coordinates.lower() in supported_coordinates, (
            "coordinates must be in {}, the coordinate system "
            "you provided, {}, is not yet supported".format(
                supported_coordinates, coordinates
            )
        )

        # convert coordinates if not cartesian
        if coordinates.lower() == "cylindrical":
            xyz = spatial.cylindrical_2_cartesian(xyz)

        xyz = spatial.rotate_points_from_normals(
            xyz, np.array(self.orientation),  # work around for a properties issue
            np.r_[0., 0., 1.], x0=np.array(self.location)
        )

        n_obs = xyz.shape[0]
        dxyz = self.vector_distance(xyz)
        r = self.distance(xyz)

        rho = np.sqrt((dxyz[:, :2]**2).sum(1))

        k2 = (4 * self.radius * rho) / ((self.radius + rho)**2 +dxyz[:, 2]**2)
        k2[k2 > 1.] = 1.  # if there are any rounding errors

        E = ellipe(k2)
        K = ellipk(k2)

        # singular if rho = 0, k2 = 1
        ind = (rho > eps) & (k2 < 1)

        Atheta = np.zeros_like(r)
        Atheta[ind] = (
            (self.mu * self.current) / (np.pi * np.sqrt(k2[ind])) *
            np.sqrt(self.radius / rho[ind]) *
            ((1. - k2[ind] / 2.)*K[ind] - E[ind])
        )

        # assume that the z-axis aligns with the polar axis
        A = np.zeros_like(xyz)
        A[ind, 0] = Atheta[ind] * (-dxyz[ind, 1] / rho[ind])
        A[ind, 1] = Atheta[ind] * (dxyz[ind, 0] / rho[ind])

        # rotate the points to aligned with the normal to the source
        A = spatial.rotate_points_from_normals(
            A, np.r_[0., 0., 1.], np.array(self.orientation),
            x0=np.array(self.location)
        )

        if coordinates.lower() == "cylindrical":
            A = spatial.cartesian_2_cylindrical(xyz, A)

        return A

    def magnetic_flux_density(self, xyz, coordinates="cartesian"):
        r"""Compute the magnetic flux density for the current loop in a wholespace.

        This method computes the magnetic flux density for the cirular current loop
        at the set of gridded xyz locations provided. Where :math:`\mu` is the magnetic
        permeability, :math:`I d\mathbf{s}` represents an infinitessimal segment
        of current at location :math:`\mathbf{r_s}` and :math:`\mathbf{r}` is the location
        at which we want to evaluate the magnetic flux density :math:`\mathbf{B}`:

        .. math::

            \mathbf{B}(\mathbf{r}) = - \frac{\mu I}{4\pi} \oint
            \frac{(\mathbf{r}-\mathbf{r_s}) \times d\mathbf{s}}{|\mathbf{r} - \mathbf{r_0}|^3}

        Parameters
        ----------
        xyz : (n, 3) numpy.ndarray xyz
            gridded locations at which we calculate the magnetic flux density
        coordinates: str {'cartesian', 'cylindrical'}
            coordinate system that the location (xyz) are provided.
            The solution is also returned in this coordinate system.
            Default: `"cartesian"`

        Returns
        -------
        (n, 3) numpy.ndarray
            The magnetic flux density at each observation location in the
            coordinate system specified in units *T*.

        Examples
        --------
        Here, we define a horizontal loop and plot the magnetic flux
        density on the xz-plane that intercepts at y=0.

        >>> from geoana.em.static import CircularLoopWholeSpace
        >>> from geoana.utils import ndgrid
        >>> from geoana.plotting_utils import plot2Ddata
        >>> import numpy as np
        >>> import matplotlib.pyplot as plt

        Let us begin by defining the loop.

        >>> location = np.r_[0., 0., 0.]
        >>> orientation = np.r_[0., 0., 1.]
        >>> radius = 0.5
        >>> simulation = CircularLoopWholeSpace(
        >>>     location=location, orientation=orientation, radius=radius
        >>> )

        Now we create a set of gridded locations and compute the magnetic flux density.

        >>> xyz = ndgrid(np.linspace(-1, 1, 50), np.array([0]), np.linspace(-1, 1, 50))
        >>> B = simulation.magnetic_flux_density(xyz)

        Finally, we plot the magnetic flux density on the plane.

        >>> fig = plt.figure(figsize=(4, 4))
        >>> ax = fig.add_axes([0.15, 0.15, 0.8, 0.8])
        >>> plot2Ddata(xyz[:, 0::2], B[:, 0::2], ax=ax, vec=True, scale='log')
        >>> ax.set_xlabel('X')
        >>> ax.set_ylabel('Y')
        >>> ax.set_title('Magnetic flux density at y=0')

        """
        xyz = np.atleast_2d(xyz)
        # convert coordinates if not cartesian
        if coordinates.lower() == "cylindrical":
            xyz = spatial.cylindrical_2_cartesian(xyz)
        elif coordinates.lower() != "cartesian":
            raise TypeError(
                f"coordinates must be 'cartesian' or 'cylindrical', the coordinate "
                f"system you provided, {coordinates}, is not yet supported."
            )

        xyz = spatial.rotate_points_from_normals(
            xyz, np.array(self.orientation),  # work around for a properties issue
            np.r_[0., 0., 1.], x0=np.array(self.location)
        )
        # rotate all the points such that the orientation is directly vertical

        dxyz = self.vector_distance(xyz)
        r = self.distance(xyz)

        rho = np.linalg.norm(dxyz[:, :2], axis=-1)

        B = np.zeros((len(rho), 3))

        # for On axis points
        inds_axial = rho==0.0

        B[inds_axial, -1] = self.mu * self.current * self.radius**2 / (
            2 * (self.radius**2 + dxyz[inds_axial, 2]**2)**(1.5)
        )

        # Off axis
        alpha = rho[~inds_axial]/self.radius
        beta = dxyz[~inds_axial, 2]/self.radius
        gamma = dxyz[~inds_axial, 2]/rho[~inds_axial]

        Q = ((1+alpha)**2 + beta**2)
        k2 =  4 * alpha/Q

        # axial part:
        B[~inds_axial, -1] = self.mu * self.current / (2 * self.radius * np.pi * np.sqrt(Q)) * (
            ellipe(k2)*(1 - alpha**2 - beta**2)/(Q  - 4 * alpha) + ellipk(k2)
        )

        # radial part:
        B_rad = self.mu * self.current * gamma / (2 * self.radius * np.pi * np.sqrt(Q)) * (
            ellipe(k2)*(1 + alpha**2 + beta**2)/(Q  - 4 * alpha) - ellipk(k2)
        )

        # convert radial component to x and y..
        B[~inds_axial, 0] = B_rad * (dxyz[~inds_axial, 0]/rho[~inds_axial])
        B[~inds_axial, 1] = B_rad * (dxyz[~inds_axial, 1]/rho[~inds_axial])

        # rotate the vectors to be aligned with the normal to the source
        B = spatial.rotate_points_from_normals(
           B, np.r_[0., 0., 1.], np.array(self.orientation),
        )

        if coordinates.lower() == "cylindrical":
            B = spatial.cartesian_2_cylindrical(xyz, B)

        return B

    def magnetic_field(self, xyz, coordinates="cartesian"):
        r"""Compute the magnetic field for the current loop in a wholespace.

        This method computes the magnetic field for the cirular current loop
        at the set of gridded xyz locations provided. Where :math:`\mu` is the magnetic
        permeability, :math:`I d\mathbf{s}` represents an infinitessimal segment
        of current at location :math:`\mathbf{r_s}` and :math:`\mathbf{r}` is the location
        at which we want to evaluate the magnetic field :math:`\mathbf{H}`:

        .. math::

            \mathbf{H}(\mathbf{r}) = - \frac{I}{4\pi} \oint
            \frac{(\mathbf{r}-\mathbf{r_s}) \times d\mathbf{s}}{|\mathbf{r} - \mathbf{r_0}|^3}

        Parameters
        ----------
        xyz : (n, 3) numpy.ndarray xyz
            gridded locations at which we calculate the magnetic field
        coordinates: str {'cartesian', 'cylindrical'}
            coordinate system that the location (xyz) are provided.
            The solution is also returned in this coordinate system.
            Default: `"cartesian"`

        Returns
        -------
        (n, 3) numpy.ndarray
            The magnetic field at each observation location in the
            coordinate system specified in units A/m.

        Examples
        --------
        Here, we define a horizontal loop and plot the magnetic field
        on the xz-plane that intercepts at y=0.

        >>> from geoana.em.static import CircularLoopWholeSpace
        >>> from geoana.utils import ndgrid
        >>> from geoana.plotting_utils import plot2Ddata
        >>> import numpy as np
        >>> import matplotlib.pyplot as plt

        Let us begin by defining the loop.

        >>> location = np.r_[0., 0., 0.]
        >>> orientation = np.r_[0., 0., 1.]
        >>> radius = 0.5
        >>> simulation = CircularLoopWholeSpace(
        >>>     location=location, orientation=orientation, radius=radius
        >>> )

        Now we create a set of gridded locations and compute the magnetic field.

        >>> xyz = ndgrid(np.linspace(-1, 1, 50), np.array([0]), np.linspace(-1, 1, 50))
        >>> H = simulation.magnetic_field(xyz)

        Finally, we plot the magnetic field on the plane.

        >>> fig = plt.figure(figsize=(4, 4))
        >>> ax = fig.add_axes([0.15, 0.15, 0.8, 0.8])
        >>> plot2Ddata(xyz[:, 0::2], H[:, 0::2], ax=ax, vec=True, scale='log')
        >>> ax.set_xlabel('X')
        >>> ax.set_ylabel('Z')
        >>> ax.set_title('Magnetic field at y=0')

        """
        return self.magnetic_flux_density(xyz, coordinates=coordinates) / self.mu
