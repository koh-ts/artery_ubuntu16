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

#include "inet/applications/udpapp/UDPCAMApp.h"

#include "inet/transportlayer/contract/udp/UDPControlInfo_m.h"
#include "inet/networklayer/common/L3AddressResolver.h"

namespace inet {

Define_Module(UDPCAMApp);

simsignal_t UDPCAMApp::rcvdPkSignal = registerSignal("rcvdPk");

void UDPCAMApp::initialize()
{
    // TODO - Generated method body
}

void UDPCAMApp::handleMessageWhenUp(cMessage *msg)
{
    if (msg->getKind() == UDP_I_DATA) {
        // process incoming packet
        receiveCAM(PK(msg));
    }
    else if (msg->getKind() == UDP_I_ERROR) {
        EV_WARN << "Ignoring UDP error report\n";
        delete msg;
    }
    else {
        throw cRuntimeError("Unrecognized message (%s)%s", msg->getClassName(), msg->getName());
    }
}

void UDPCAMApp::receiveCAM(cPacket *pk)
{
    EV_INFO << "Video stream packet: " << UDPSocket::getReceivedPacketInfo(pk) << endl;
    emit(rcvdPkSignal, pk);

    // determine its source address/port
    UDPDataIndication *ctrl = check_and_cast<UDPDataIndication *>(pk->removeControlInfo());
    L3Address srcAddress = ctrl->getSrcAddr();
    std::cout << "cam received" << UDPSocket::getReceivedPacketInfo(pk) << " from:" << srcAddress << endl;
    delete ctrl;
    delete pk;
}

bool UDPCAMApp::handleNodeStart(IDoneCallback *doneCallback)
{
    simtime_t startTimePar = par("startTime");
    simtime_t startTime = std::max(startTimePar, simTime());
    scheduleAt(startTime, selfMsg);
    return true;
}

bool UDPCAMApp::handleNodeShutdown(IDoneCallback *doneCallback)
{
    cancelEvent(selfMsg);
    //TODO if(socket.isOpened()) socket.close();
    return true;
}

void UDPCAMApp::handleNodeCrash()
{
    cancelEvent(selfMsg);
}

} //namespace
