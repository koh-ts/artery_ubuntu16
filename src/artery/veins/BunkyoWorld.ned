package artery.veins;

import artery.storyboard.Storyboard;
import artery.veins.ObstacleControl;
import artery.veins.ConnectionManager;
import artery.veins.Car;
import org.car2x.veins.base.modules.BaseWorldUtility;
import org.car2x.veins.modules.world.annotations.AnnotationManager;
import traci.Manager;
import artery.application.ProxyCamDev;
import inet.networklayer.configurator.ipv4.IPv4NetworkConfigurator;
import ned.DatarateChannel;
import inet.visualizer.integrated.IntegratedVisualizer;


network BunkyoWorld
{
    parameters:
        bool withObstacles = default(true);
        bool withStoryboard = default(false);
        int numProxyCamDevs = default(0);
        int numRoadSideUnits = default(0);
        double playgroundSizeX @unit(m); // x size of the area the nodes are in (in meters)
        double playgroundSizeY @unit(m); // y size of the area the nodes are in (in meters)
        double playgroundSizeZ @unit(m); // z size of the area the nodes are in (in meters)
        @display("bgb=506,483");

    types:
        channel ethline extends DatarateChannel
        {
            datarate = 10Gbps;
        }

    submodules:
        connectionManager: ConnectionManager {
            @display("p=69,131");
        }

        world: BaseWorldUtility {
            parameters:
                playgroundSizeX = playgroundSizeX;
                playgroundSizeY = playgroundSizeY;
                playgroundSizeZ = playgroundSizeZ;
                @display("p=40,199");
        }

        obstacles: ObstacleControl if withObstacles {
            parameters:
                traciCoreModule = "^.traci.core";
                @display("p=40,254");
        }
        annotations: AnnotationManager {
            @display("p=260,50");
        }

        traci: Manager {
            parameters:
                mapper.vehicleType = default("artery.veins.Car");
                nodes.vehicleSinkModule = default(".mobility");
                @display("p=20,20");
        }

        storyboard: Storyboard if withStoryboard {
            parameters:
                middlewareModule = default(".appl.middleware");
                @display("p=100,20");
        }

        pcam[numProxyCamDevs]: ProxyCamDev {
            @display("p=330,218");
        }
        
        rsu[numRoadSideUnits]: RSU {
        }
        
        configurator: IPv4NetworkConfigurator {
            @display("p=112,278");
        }
//        visualizer: IntegratedVisualizer {
//            @display("p=282,31");
//        }

    connections:
        for i=0..sizeof(pcam)-2 {
        	pcam[i].ethg <--> ethline <--> pcam[i+1].ethg;
        }
}
