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

import artery.veins.RSU;
import inet.node.inet.Router;
import ned.DatarateChannel;
import org.car2x.veins.base.modules.IMobility;


module ProxyCamDev
{
    parameters:
        string mobilityType = default("artery.veins.Mobility");

    gates:
        inout ethg;

    types:
        channel ethline extends DatarateChannel
        {
            delay = 500ns;
            datarate = 10Mbps;
        }
    submodules:
        rsu: RSU {
            @display("p=374,73");
        }

        router: Router {
            @display("p=91,73");
        }

        mobility: <mobilityType> like IMobility {
            parameters:
                @display("p=225,151");
        }

    connections:
        rsu.ethg++ <--> ethline <--> router.ethg++;
        router.ethg++ <--> ethg;
}
