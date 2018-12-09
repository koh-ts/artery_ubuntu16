package artery.veins;

import artery.application.IMiddleware;
import artery.networking.Vanetza;
import artery.nic.IRadioDriver;
import org.car2x.veins.base.modules.IBaseApplLayer;

// Middleware as Veins compatiblity application layer
module ApplicationLayer like IBaseApplLayer
{
    parameters:
        int headerLength @unit("bit") = 0; // ignored

    gates:
        input lowerLayerIn;
        output lowerLayerOut;
        input lowerControlIn;
        output lowerControlOut;

    submodules:
        radioDriver: RadioDriver {
            @display("p=143,49");
        }

        vanetza: Vanetza {
            *.middlewareModule = absPath("^.middleware");
            *.radioDriverModule = absPath("^.radioDriver");
            runtime.datetime = middleware.datetime;
            @display("p=286,49");
        }

        middleware: <default("VehicleMiddleware")> like IMiddleware {
            routerModule = absPath("^.vanetza.router");
            @display("p=66,117");
        }

    connections allowunconnected:
        lowerLayerIn --> radioDriver.lowerLayerIn;
        lowerLayerOut <-- radioDriver.lowerLayerOut;

        radioDriver.upperLayer <--> vanetza.radioDriver;
}
