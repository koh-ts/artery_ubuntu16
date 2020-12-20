package artery.veins;

import org.car2x.veins.base.modules.IBaseApplLayer;
import org.car2x.veins.base.modules.IMobility;
import org.car2x.veins.modules.nic.INic80211p;
import artery.envmod.GlobalEnvironmentModel;
import artery.envmod.LocalEnvironmentModel;
import artery.inet.World;
import artery.utility.IdentityRegistry;

module RSU
{
    parameters:
        @networkNode;
        @display("i=block/wrxtx;is=vs");
        string applType = default("artery.veins.ApplicationLayer"); // type of application layer
        string nicType = default("org.car2x.veins.modules.nic.Nic80211p"); // type of network interface card
        string mobilityType = default("artery.veins.Mobility");
        **.globalEnvironmentModule = default("environmentModel");

    gates:
        input radioIn @directIn; // gate for sendDirect

    submodules:
        appl: <applType> like IBaseApplLayer {
            parameters:
                @display("p=60,50");
                middleware.typename = "StationaryMiddleware";
                vanetza.position.typename = "StationaryPositionProvider";
                vanetza.router.isMobile = false;
                **.mobilityModule = absPath("^.mobility");
                **.traciCoreModule = "traci.core";
        }

        nic: <nicType> like INic80211p {
            @display("p=60,150");
        }

        mobility: <mobilityType> like IMobility {
            parameters:
                @display("p=130,150");
        }
        environmentModel: GlobalEnvironmentModel {
            parameters:
                @display("p=140,20");
                identityRegistryModule = default("idRegistry");
                traciModule = default("traci");
                nodeMobilityModule = default(".mobility");
        }
        idRegistry: IdentityRegistry {
            parameters:
                @display("p=180,20");
        }

    connections:
        nic.upperLayerOut --> appl.lowerLayerIn;
        nic.upperLayerIn <-- appl.lowerLayerOut;
        nic.upperControlOut --> appl.lowerControlIn;
        nic.upperControlIn <-- appl.lowerControlOut;

        radioIn --> nic.radioIn;
}
