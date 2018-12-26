//
// Copyright (C) 2011 Andras Varga
//
// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public License
// as published by the Free Software Foundation; either version 2
// of the License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public License
// along with this program; if not, see <http://www.gnu.org/licenses/>.
//

#include "artery/application/UDPCamListener.h"

#include "inet/common/ModuleAccess.h"
#include "inet/transportlayer/contract/udp/UDPControlInfo_m.h"
#include "inet/applications/base/ApplicationPacket_m.h"
#include "inet/networklayer/contract/ipv4/IPv4ControlInfo.h"
#include "inet/networklayer/common/L3AddressResolver.h"
#include "veins/base/utils/FindModule.h"


namespace artery
{

Define_Module(UDPCamListener);

simsignal_t UDPCamListener::rcvdPkSignal = cComponent::registerSignal("campktrcv");

namespace {
  const simsignal_t queueRatioChgd = cComponent::registerSignal("queueRatioChgd");
}


void UDPCamListener::initialize(int stage)
{
    ApplicationBase::initialize(stage);
    if (stage == INITSTAGE_LOCAL) {
        // init statistics
      std::string output = par("outputDir");
      output += "output_" + this->getFullPath() + "_listener.txt";
      ofs.open(output, std::ios::out);
      mHost = FindModule<>::findHost(this);
      mHost->subscribe(queueRatioChgd,this);
      stages = par("stageNum");
    }
}

void UDPCamListener::handleMessageWhenUp(cMessage *msg)
{
    if (msg->getKind() == UDP_I_DATA) {
      receiveCAM(PK(msg));
    }
    else {
        throw cRuntimeError("Message received with unexpected message kind = %d", msg->getKind());
    }
}

void UDPCamListener::receiveCAM(cPacket *pk)
{
    // determine its source address/port
    UDPDataIndication *ctrl = check_and_cast<UDPDataIndication *>(pk->getControlInfo());
    L3Address srcAddress = ctrl->getSrcAddr();
//    std::cout << "cam received" << UDPSocket::getReceivedPacketInfo(pk) << " from:" << srcAddress << endl;


    if (checkTtl(ctrl->getTtl())) {
      emit(rcvdPkSignal, pk);
    }

    ofs << "received Cam udp: time: " << simTime()
        << "\tserialnum: " << ((ApplicationPacket *)pk)->getSequenceNumber()
        << "\tfrom: " << srcAddress
        << "\tto: " << L3AddressResolver().resolve(this->getParentModule()->getFullPath().c_str());
    if (!checkTtl(ctrl->getTtl())) {
      ofs << "\t dropped";
    }
    ofs << endl;
    //    std::cout << check_and_cast<artery::Disseminator>this->getParentModule()->handleMessage(pk) << endl;

    delete pk;
}


bool UDPCamListener::checkTtl(int ttl) {
  double min = 0.3;
  double max = 1;

  if (!((queueRT - min) < (max - min) / stages * ttl)) {
    std::cout << "ttl is: " << ttl << "\tqueue ratio is: " << queueRT << endl;
  }

  return (queueRT - min) < (max - min) / stages * ttl;
}


void UDPCamListener::receiveSignal(cComponent *src, simsignal_t signal, double queueRatioThreshold, cObject *details) {
  if (signal == queueRatioChgd) {
    queueRT = queueRatioThreshold;
  }
}



void UDPCamListener::finish()
{
    ApplicationBase::finish();
}

bool UDPCamListener::handleNodeStart(IDoneCallback *doneCallback)
{
    int localPort = par("localPort");
    socket.setOutputGate(gate("udpOut"));
    socket.bind(localPort);
    return true;
}

bool UDPCamListener::handleNodeShutdown(IDoneCallback *doneCallback)
{
    //TODO if(socket.isOpened()) socket.close();
    return true;
}

void UDPCamListener::handleNodeCrash()
{
}

} // namespace artery
