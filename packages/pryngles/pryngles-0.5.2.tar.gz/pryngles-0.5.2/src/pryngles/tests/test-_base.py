##################################################################
#                                                                #
#.#####...#####...##..##..##..##...####...##......######...####..#
#.##..##..##..##...####...###.##..##......##......##......##.....#
#.#####...#####.....##....##.###..##.###..##......####.....####..#
#.##......##..##....##....##..##..##..##..##......##..........##.#
#.##......##..##....##....##..##...####...######..######...####..#
#................................................................#
#                                                                #
# PlanetaRY spanGLES                                             #
# The bright-side of the light-curve of (ringed) exoplanets      #
#                                                                #
##################################################################
# Jorge I. Zuluaga, Mario Sucerquia, Jaime A. Alvarado (C) 2022  #
##################################################################
import unittest
from pryngles import *
class Test(unittest.TestCase):
    def test_props(self):
        p=Props(m=1,a=2,b=3)
        self.assertEqual([p.m,p.a,p.b],[1,2,3],[True]*3)

    def test_body(self):
        class defaults(object):
            orbit=dict()
            physics=dict()
            optics=dict()
        P=Body(defaults,"Test",None,dict(),dict(),dict())
        obj=Body(defaults,"Test",P,dict(),dict(),dict())
        obj._update_parent("parent")
        obj._update_childs("child1")
        obj._update_childs("child2")
        print(obj.childs)
        print(obj.hash)
        self.assertEqual([obj.parent],["parent"],True)
        self.assertEqual(obj.childs,["child1","child2"],True)
        self.assertRaises(AssertionError,
                          lambda:Body(defaults,"Test",1,dict(),dict(),dict())
                         )   

    def test_star(self):
        S=Star()
        print(S.physics)
        print(S.hash)
        
        #Check derived properties
        self.assertEqual(np.isclose([S.physics.wrot],
                                    [2*np.pi/StarDefaults.physics["prot"]],
                                    rtol=1e-7),
                         [True]*1)
        
        S.update_body(physics=dict(m=2))
        print(S.physics)
        
        #Check exception: primary could not be different from None or Body
        self.assertRaises(AssertionError,lambda:Star(primary="Nada"))
        
    def test_planet(self):
        S=Star()

        #Check exception: primary is mandatory for planets
        self.assertRaises(ValueError,lambda:Planet())

        P=Planet(primary=S)
        
        print(P.physics)
        print(P.hash)
        
        #Check derived properties
        self.assertEqual(np.isclose([P.physics.wrot],
                                    [2*np.pi/PlanetDefaults.physics["prot"]],
                                    rtol=1e-7),
                         [True]*1)
        
        P.update_body(orbit=dict(a=5),physics=dict(rho=0.2))
        print(P.orbit,P.physics)
        
        #Check exception: primary could not be different from None or Body
        self.assertRaises(AssertionError,lambda:Planet(primary="Nada"))
        
    def test_planet(self):
        S=Star(physics=dict(radius=3.0))

        #Check exception: primary is mandatory for planets
        self.assertRaises(ValueError,lambda:Ring())

        R=Ring(primary=S)
        
        print(R.physics)
        print(R.hash)
        
        #Check derived properties
        """
        self.assertEqual(np.isclose([P.physics.wrot],
                                    [2*np.pi/PlanetDefaults.physics["prot"]],
                                    rtol=1e-7),
                         [True]*1)
        """
        
        R.update_body(physics=dict(fe=3))
        print(R.physics)
        
        #Check exception: primary could not be different from None or Body
        self.assertRaises(AssertionError,lambda:Planet(primary="Nada"))
        
    def test_observer(self):
        O=Observer()
        print(O.optics)
        
        #Check derived properties
        """
        self.assertEqual(np.isclose([P.physics.wrot],
                                    [2*np.pi/PlanetDefaults.physics["prot"]],
                                    rtol=1e-7),
                         [True]*1)
        """
        
        O.update_body(optics=dict(beta=90*DEG))
        print(O.optics)
        
        #Check exception: primary could not be different from None or Body
        self.assertRaises(AssertionError,lambda:Observer(primary="Nada"))
        
    def test_system_init(self):
        
        sys=System()
        print(sys.nbodies)
        print(sys._sim.G)
        print(sys.ul,sys.um,sys.ut)
        
        sys=System(units=['m','kg','s'])
        print(sys.nbodies)
        print(sys._sim.G)
        print(sys.ul,sys.um,sys.ut)
        
        S=Star()
        sys=System(stars=S)
        print(sys.stars)
        print(sys.hashes)
        print(sys.nbodies,sys.nstars,sys.nplanets,sys.nrings,sys.nobservers)
        
        S2=Star()
        P=Planet(primary=S2)
        #Check that when planet does not use a star of the system an exception is raised
        self.assertRaises(AssertionError,lambda:System(stars=S,planets=P))
        
        P=Planet(primary=S)
        sys=System(stars=S,planets=P)
        print(sys.hashes)
        print(sys.nbodies,sys.nstars,sys.nplanets,sys.nrings,sys.nobservers)
        
        R=Planet(primary=P)
        #Check that planet cannot be initialized as a planet
        self.assertRaises(AssertionError,lambda:System(stars=S,planets=P,rings=R))

        R=Ring(primary=P)
        sys=System(stars=S,planets=P,rings=R)
        print(sys.hashes)
        print(sys.nbodies,sys.nstars,sys.nplanets,sys.nrings,sys.nobservers)
        
        
        P1=Planet(primary=S)
        P2=Planet(primary=S)
        P3=Planet(primary=S)
        sys=System(stars=S,planets=[P1,P2,P3])
        print(sys.hashes)
        print(sys.nbodies,sys.nstars,sys.nplanets,sys.nrings,sys.nobservers)
        
        """
        self.assertEqual(np.isclose([P.physics.wrot],
                                    [2*np.pi/PlanetDefaults.physics["prot"]],
                                    rtol=1e-7),
                         [True]*1)
        #Check exception: primary could not be different from None or Body
        self.assertRaises(AssertionError,lambda:Observer(primary="Nada"))
        """
        
    def test_system_add(self):
        sys=System()
        S=sys.add(kind="Star",orbit=dict(m=2))
        print(sys.hashes)
        print(sys.nbodies,sys.nstars,sys.nplanets,sys.nrings,sys.nobservers)
        print(sys.stars[0].orbit)
        print(S.orbit)
        
        S.update_body(orbit=dict(m=3))
        print(sys.stars[0].orbit)
        
        """
        self.assertEqual(np.isclose([P.physics.wrot],
                                    [2*np.pi/PlanetDefaults.physics["prot"]],
                                    rtol=1e-7),
                         [True]*1)
        #Check exception: primary could not be different from None or Body
        self.assertRaises(AssertionError,lambda:Observer(primary="Nada"))
        """
        
    def test_system_remove(self):
        sys=System()
        S=sys.add(kind="Star",orbit=dict(m=2))
        print(sys.hashes)
        print(sys.nbodies,sys.nstars,sys.nplanets,sys.nrings,sys.nobservers)

        sys.remove(body_hash=S.hash)
        print(sys.hashes)
        print(sys.nbodies,sys.nstars,sys.nplanets,sys.nrings,sys.nobservers)
        
        sys=System()
        S=sys.add(kind="Star")
        P=sys.add(kind="Planet",primary=S)
        R=sys.add(kind="Ring",primary=P)
        print(sys.hashes)
        print(sys.nbodies,sys.nstars,sys.nplanets,sys.nrings,sys.nobservers)

        sys.remove(body_hash=S.hash)
        print(sys.hashes)
        print(sys.nbodies,sys.nstars,sys.nplanets,sys.nrings,sys.nobservers)

        sys=System()
        S=sys.add(kind="Star")
        P=sys.add(kind="Planet",primary=S)
        R=sys.add(kind="Ring",primary=P)
        print(sys.hashes)
        print(sys.nbodies,sys.nstars,sys.nplanets,sys.nrings,sys.nobservers)

        sys.remove(body_hash=P.hash)
        print(sys.hashes)
        print(sys.nbodies,sys.nstars,sys.nplanets,sys.nrings,sys.nobservers)
        
        sys=System()
        S=sys.add(kind="Star")
        P=sys.add(kind="Planet",primary=S)
        R=sys.add(kind="Ring",primary=P)
        print(sys.hashes)
        print(sys.nbodies,sys.nstars,sys.nplanets,sys.nrings,sys.nobservers)

        sys.remove(body_hash=R.hash)
        print(sys.hashes)
        print(sys.nbodies,sys.nstars,sys.nplanets,sys.nrings,sys.nobservers)
        
        """
        self.assertEqual(np.isclose([P.physics.wrot],
                                    [2*np.pi/PlanetDefaults.physics["prot"]],
                                    rtol=1e-7),
                         [True]*1)
        #Check exception: primary could not be different from None or Body
        self.assertRaises(AssertionError,lambda:Observer(primary="Nada"))
        """
        
    def test_system_ensamble(self):

        sys=System()
        S=sys.add(kind="Star",
                  physics=dict(radius=Const.Rsun/Const.au))
        P=sys.add(kind="Planet",primary=S,
                  orbit=dict(a=0.2,e=0.0),
                  physics=dict(radius=Const.Rsat/Const.au)
                 )
        R=sys.add(kind="Ring",primary=P,
                  physics=dict(fi=1.5,fe=2.5,i=30*DEG)
                 )
        O=sys.add(kind="Observer",
                  optics=dict(beta=30*DEG,lamb=90*DEG)
                 )

        print(S.physics.radius,P.physics.radius,R.physics.fi,R.physics.fe,P.orbit.a,P.orbit.e)
        print(O.optics.beta,O.optics.lamb)
        
        P=sys.ensamble_system()
        fig1,fig2,fig3=P.plotRingedPlanet(showfig=0)
        
        P.changeObserver([90*DEG,30*DEG])
        lamb_initial=+0.0*DEG
        lamb_final=+360*DEG
        lambs=np.linspace(lamb_initial,lamb_final,100)
        Rps=[]
        Rrs=[]
        ts=[]
        for lamb in lambs:
            P.changeStellarPosition(lamb)
            ts+=[P.t*P.CU.UT]
            P.updateOpticalFactors()
            P.updateDiffuseReflection()
            Rps+=[P.Rip.sum()]
            Rrs+=[P.Rir.sum()]

        ts=np.array(ts)
        Rps=np.array(Rps)
        Rrs=np.array(Rrs)

        #Middle transit
        ts=(ts-ts[0])/Const.days

        print(max(1e6*(Rps+Rrs)))
        
        #Plot
        #"""
        fig=plt.figure()
        ax=fig.gca()    
        ax.plot(ts,1e6*Rps,label="Planet")
        ax.plot(ts,1e6*Rrs,label="Ring")
        ax.plot(ts,1e6*(Rps+Rrs),label="Planet+Ring")

        ax.set_xlabel("Time since VE [days]")
        ax.set_ylabel("Flux anomaly [ppm]")

        ax.legend();
        #"""
        
        #"""
        #LEGACY
        attributes=dict(
            #Behavior
            behavior=dict(shadows=True),
            #Units
            CU=CanonicalUnits(UL=P.CU.UL,UM=P.CU.UM),
            #Basic
            Rstar=Const.Rsun/Const.au,Rplanet=Const.Rsat/Const.au,
            Rint=1.5,Rext=2.5,i=30*DEG,a=0.2,e=0.0,
            #Orbit 
            Mstar=1,x=0,lambq=0,t0=0,kepler=False,
            #Observer
            eobs_ecl=np.array([90.0*DEG,30.0*DEG]),
            #Sampling
            Np=1000,Nr=1000,Nb=0,Ns=30,
            #Physical properties
            physics=dict(
                #Albedos
                AS=1,AL=1,
                #Ring geometrical opacity
                taug=1.0, #Geometrical opacity
                diffeff=1.0, #Diffraction efficiency
                #Law of diffuse reflection on ring surface
                reflection_rings_law=lambda x,y:x,
                #Observations wavelength
                wavelength=550e-9,
                #Ring particle propeties (see French & Nicholson, 2000)
                particles=dict(q=3,s0=100e-6,smin=1e-2,smax=1e2,Qsc=1,Qext=2),
                #Stellar limb darkening
                limb_cs=[0.6550],
            )
        )
        P=RingedPlanet(**attributes)
        #fig1,fig2,fig3=P.plotRingedPlanet(showfig=0)

        P.changeObserver([90*DEG,30*DEG])
        lamb_initial=+0.0*DEG
        lamb_final=+360*DEG
        lambs=np.linspace(lamb_initial,lamb_final,100)
        Rps=[]
        Rrs=[]
        ts=[]
        for lamb in lambs:
            P.changeStellarPosition(lamb)
            ts+=[P.t*P.CU.UT]
            P.updateOpticalFactors()
            P.updateDiffuseReflection()
            Rps+=[P.Rip.sum()]
            Rrs+=[P.Rir.sum()]

        ts=np.array(ts)
        Rps=np.array(Rps)
        Rrs=np.array(Rrs)

        print(max(1e6*(Rps+Rrs)))

        #Middle transit
        ts=(ts-ts[0])/Const.days

        #Plot
        fig=plt.figure()
        ax=fig.gca()    
        ax.plot(ts,1e6*Rps,label="Planet")
        ax.plot(ts,1e6*Rrs,label="Ring")
        ax.plot(ts,1e6*(Rps+Rrs),label="Planet+Ring")

        ax.set_xlabel("Time since VE [days]")
        ax.set_ylabel("Flux anomaly [ppm]")

        ax.legend();
        #""";
        
        """
        self.assertEqual(np.isclose([P.physics.wrot],
                                    [2*np.pi/PlanetDefaults.physics["prot"]],
                                    rtol=1e-7),
                         [True]*1)
        #Check exception: primary could not be different from None or Body
        self.assertRaises(AssertionError,lambda:Observer(primary="Nada"))
        """
        

if __name__=="__main__":
        unittest.main(argv=['first-arg-is-ignored'],exit=False)
