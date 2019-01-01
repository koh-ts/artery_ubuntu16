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
import inet.node.rip.RIPRouter;


network BunkyoWorld
{
    parameters:
        bool withObstacles = default(true);
        bool withStoryboard = default(false);
        int numProxyCamDevsParEdge = default(0);
        int numRoadSideUnits = default(0);
        double playgroundSizeX @unit(m); // x size of the area the nodes are in (in meters)
        double playgroundSizeY @unit(m); // y size of the area the nodes are in (in meters)
        double playgroundSizeZ @unit(m); // z size of the area the nodes are in (in meters)
        @display("bgb=6000,6000");

    types:
        channel ethline extends DatarateChannel
        {
            datarate = 10Gbps;
        }

    submodules:
        connectionManager: ConnectionManager {
            @display("p=54.216,154.616");
        }

        world: BaseWorldUtility {
            parameters:
                playgroundSizeX = playgroundSizeX;
                playgroundSizeY = playgroundSizeY;
                playgroundSizeZ = playgroundSizeZ;
                @display("p=54.216,48.191998");
        }

        obstacles: ObstacleControl if withObstacles {
            parameters:
                traciCoreModule = "^.traci.core";
                @display("p=251,48.191998");
        }
        annotations: AnnotationManager {
            @display("p=54.216,345.37598");
        }

        traci: Manager {
            parameters:
                mapper.vehicleType = default("artery.veins.Car");
                nodes.vehicleSinkModule = default(".mobility");
                @display("p=54.216,248.99199");
        }

        storyboard: Storyboard if withStoryboard {
            parameters:
                middlewareModule = default(".appl.middleware");
                @display("p=156.624,138.552");
        }

        pcam[numProxyCamDevsParEdge*numProxyCamDevsParEdge]: ProxyCamDev {
            @display("p=891.552,377.504");
        }

        router[numProxyCamDevsParEdge*numProxyCamDevsParEdge]: RIPRouter {
            @display("p=761.032,257.024");
        }

        rsu[numRoadSideUnits]: RSU {
            @display("p=891.552,929.704");
        }
        configurator: IPv4NetworkConfigurator {
            @display("p=156.624,48.191998");
        }
//        visualizer: IntegratedVisualizer {
//            @display("p=282,31");
//        }

    connections:
        for i=0..numProxyCamDevsParEdge * numProxyCamDevsParEdge - 1 {
            router[i].ethg++ <--> ethline <--> pcam[i].ethg;
        }
        for i=0..numProxyCamDevsParEdge-2, for j=0..numProxyCamDevsParEdge-2 {
            router[numProxyCamDevsParEdge * i + j].ethg++ <--> ethline <--> router[numProxyCamDevsParEdge * i + j + 1].ethg++;
            router[numProxyCamDevsParEdge * i + j].ethg++ <--> ethline <--> router[numProxyCamDevsParEdge * (i+1) + j].ethg++;
        }
        for i=0..numProxyCamDevsParEdge-2 {
            router[numProxyCamDevsParEdge * (i+1) - 1].ethg++ <--> ethline <--> router[numProxyCamDevsParEdge * (i+2) - 1].ethg++;
        }
        for j=0..numProxyCamDevsParEdge-2 {
            router[numProxyCamDevsParEdge * (numProxyCamDevsParEdge - 1) + j].ethg++ <--> ethline <--> router[numProxyCamDevsParEdge * (numProxyCamDevsParEdge - 1) + j + 1].ethg++;
        }
}
