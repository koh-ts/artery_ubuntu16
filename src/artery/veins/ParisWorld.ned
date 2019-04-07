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


network ParisWorld
{
    parameters:
        bool withObstacles = default(true);
        bool withStoryboard = default(false);
        int numProxyCamDevs = default(0);
        int numRoadSideUnits = default(0);
        double playgroundSizeX @unit(m); // x size of the area the nodes are in (in meters)
        double playgroundSizeY @unit(m); // y size of the area the nodes are in (in meters)
        double playgroundSizeZ @unit(m); // z size of the area the nodes are in (in meters)
        @display("bgb=3464.69,2001.47"); //地図の横幅縦幅に合わせる

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

        router[numProxyCamDevs]: RIPRouter {
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
        for i=0..numProxyCamDevs - 1 {
            router[i].ethg++ <--> ethline <--> pcam[i].ethg;
        }

        router[0].ethg++ <--> ethline <--> router[5].ethg++;
        router[0].ethg++ <--> ethline <--> router[6].ethg++;
        router[0].ethg++ <--> ethline <--> router[9].ethg++;
        router[0].ethg++ <--> ethline <--> router[14].ethg++;
        //router[1].ethg++ <--> ethline <--> router[2].ethg++;
        //router[1].ethg++ <--> ethline <--> router[17].ethg++;
        //router[2].ethg++ <--> ethline <--> router[3].ethg++;
        //router[2].ethg++ <--> ethline <--> router[25].ethg++;
        router[3].ethg++ <--> ethline <--> router[4].ethg++;
        //router[3].ethg++ <--> ethline <--> router[23].ethg++;
        router[3].ethg++ <--> ethline <--> router[26].ethg++;
        router[4].ethg++ <--> ethline <--> router[5].ethg++;
        router[4].ethg++ <--> ethline <--> router[24].ethg++;
        router[4].ethg++ <--> ethline <--> router[28].ethg++;
        router[5].ethg++ <--> ethline <--> router[22].ethg++;
        router[5].ethg++ <--> ethline <--> router[32].ethg++;
        router[6].ethg++ <--> ethline <--> router[7].ethg++;
        router[6].ethg++ <--> ethline <--> router[38].ethg++;
        router[6].ethg++ <--> ethline <--> router[37].ethg++;
        router[7].ethg++ <--> ethline <--> router[8].ethg++;
        //router[8].ethg++ <--> ethline <--> router[20].ethg++;
        router[8].ethg++ <--> ethline <--> router[40].ethg++;
        router[9].ethg++ <--> ethline <--> router[43].ethg++;
        router[9].ethg++ <--> ethline <--> router[33].ethg++;
        router[9].ethg++ <--> ethline <--> router[10].ethg++;
        //router[10].ethg++ <--> ethline <--> router[11].ethg++;
        router[10].ethg++ <--> ethline <--> router[44].ethg++;
        router[10].ethg++ <--> ethline <--> router[34].ethg++;
        //router[11].ethg++ <--> ethline <--> router[12].ethg++;
        //router[11].ethg++ <--> ethline <--> router[36].ethg++;
        //router[11].ethg++ <--> ethline <--> router[46].ethg++;
        //router[12].ethg++ <--> ethline <--> router[13].ethg++;
        //router[12].ethg++ <--> ethline <--> router[46].ethg++;
        router[14].ethg++ <--> ethline <--> router[15].ethg++;
        router[14].ethg++ <--> ethline <--> router[43].ethg++;
        router[15].ethg++ <--> ethline <--> router[16].ethg++;
        router[15].ethg++ <--> ethline <--> router[42].ethg++;
        router[15].ethg++ <--> ethline <--> router[44].ethg++;
        //router[16].ethg++ <--> ethline <--> router[44].ethg++; インターフェイス4つしかない？
        //router[16].ethg++ <--> ethline <--> router[48].ethg++;
        //router[17].ethg++ <--> ethline <--> router[18].ethg++;
        //router[18].ethg++ <--> ethline <--> router[19].ethg++;
        //router[18].ethg++ <--> ethline <--> router[23].ethg++;
        //router[19].ethg++ <--> ethline <--> router[20].ethg++;
        //router[20].ethg++ <--> ethline <--> router[21].ethg++;
        //router[21].ethg++ <--> ethline <--> router[22].ethg++;
        router[22].ethg++ <--> ethline <--> router[37].ethg++;
        //router[23].ethg++ <--> ethline <--> router[24].ethg++;
        //router[24].ethg++ <--> ethline <--> router[25].ethg++;
        router[26].ethg++ <--> ethline <--> router[27].ethg++;
        router[27].ethg++ <--> ethline <--> router[28].ethg++;
        router[27].ethg++ <--> ethline <--> router[29].ethg++;
        router[29].ethg++ <--> ethline <--> router[30].ethg++;
        router[30].ethg++ <--> ethline <--> router[31].ethg++;
        router[31].ethg++ <--> ethline <--> router[34].ethg++;
        router[32].ethg++ <--> ethline <--> router[33].ethg++;
        router[33].ethg++ <--> ethline <--> router[34].ethg++;
        router[34].ethg++ <--> ethline <--> router[35].ethg++;
        //router[35].ethg++ <--> ethline <--> router[36].ethg++;
        router[38].ethg++ <--> ethline <--> router[39].ethg++;
        router[39].ethg++ <--> ethline <--> router[40].ethg++;
        router[39].ethg++ <--> ethline <--> router[42].ethg++;
        router[40].ethg++ <--> ethline <--> router[41].ethg++;
        router[41].ethg++ <--> ethline <--> router[42].ethg++;
        //router[43].ethg++ <--> ethline <--> router[44].ethg++;
        //router[44].ethg++ <--> ethline <--> router[48].ethg++;
        //router[46].ethg++ <--> ethline <--> router[47].ethg++;
        //router[47].ethg++ <--> ethline <--> router[48].ethg++;
        //router[45].ethg++ <--> ethline <--> router[47].ethg++;
        router[44].ethg++ <--> ethline <--> router[45].ethg++;
}
