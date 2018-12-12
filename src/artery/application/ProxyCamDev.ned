//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
// 
// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see http://www.gnu.org/licenses/.
// 

package artery.application;

import inet.node.inet.Router;
import artery.application.Disseminator;
import artery.application.Sensor;
import ned.DatarateChannel;
//import org.car2x.veins.base.modules.IMobility;
import inet.visualizer.integrated.IntegratedVisualizer;
import inet.mobility.contract.IMobility;
import inet.node.inet.StandardHost;


network ProxyCamDev
{
    parameters:
        string mobilityType = default("inet.mobility.static.StationaryMobility");
		@networkNode;
    gates:
        inout ethg;

    types:
        channel ethline extends DatarateChannel
        {
            delay = 500ns;
            datarate = 10Mbps;
        }
    submodules:
        router: Router {
            @display("p=91,73");
        }

        disseminator: StandardHost {
            @display("p=374,73");
        }

        sensor: StandardHost {
            @display("p=374,170");
        }
        mobility: <mobilityType> like IMobility {
            parameters:
                @display("p=167,196");
        }


    connections:
        disseminator.ethg++ <--> ethline <--> router.ethg++;
        sensor.ethg++ <--> ethline <--> router.ethg++;
        router.ethg++ <--> ethg;
}
