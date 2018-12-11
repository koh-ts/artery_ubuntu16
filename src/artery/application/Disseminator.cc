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

#include "Disseminator.h"

namespace artery {

Define_Module(Disseminator);

void Disseminator::initialize(int stage)
{
    ApplicationBase::initialize(stage);

    if (stage == INITSTAGE_LOCAL) {
        // init statistics
        numEchoed = 0;
        WATCH(numEchoed);
    }
}

void Disseminator::handleMessageWhenUp(cMessage *msg)
{
    if (msg->getKind() == UDP_I_ERROR) {
        // ICMP error report -- discard it
        delete msg;
    }
    else if (msg->getKind() == UDP_I_DATA) {
        cPacket *pk = PK(msg);
        // statistics
        numEchoed++;
        emit(pkSignal, pk);

        // determine its source address/port
        UDPDataIndication *ctrl = check_and_cast<UDPDataIndication *>(pk->removeControlInfo());
        L3Address srcAddress = ctrl->getSrcAddr();
        int srcPort = ctrl->getSrcPort();
        delete ctrl;

        // send back
        socket.sendTo(pk, srcAddress, srcPort);
    }
    else {
        throw cRuntimeError("Message received with unexpected message kind = %d", msg->getKind());
    }
}

void Disseminator::refreshDisplay() const
{
    char buf[40];
    sprintf(buf, "echoed: %d pks", numEchoed);
    getDisplayString().setTagArg("t", 0, buf);
}

void Disseminator::finish()
{
    ApplicationBase::finish();
}

bool Disseminator::handleNodeStart(IDoneCallback *doneCallback)
{
    socket.setOutputGate(gate("udpOut"));
    int localPort = par("localPort");
    socket.bind(localPort);
    MulticastGroupList mgl = getModuleFromPar<IInterfaceTable>(par("interfaceTableModule"), this)->collectMulticastGroups();
    socket.joinLocalMulticastGroups(mgl);
    return true;
}

bool Disseminator::handleNodeShutdown(IDoneCallback *doneCallback)
{
    //TODO if(socket.isOpened()) socket.close();
    return true;
}

void Disseminator::handleNodeCrash()
{
}

} //namespace
