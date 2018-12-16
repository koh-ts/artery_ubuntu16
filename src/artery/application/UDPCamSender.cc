//
// Copyright (C) 2000 Institut fuer Telematik, Universitaet Karlsruhe
// Copyright (C) 2004,2011 Andras Varga
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

#include "artery/application/UDPCamSender.h"

#include "inet/networklayer/common/L3AddressResolver.h"
#include "inet/common/ModuleAccess.h"
#include "inet/common/lifecycle/NodeOperations.h"
#include "inet/transportlayer/contract/udp/UDPControlInfo_m.h"

namespace artery {

Define_Module(UDPCamSender);

simsignal_t UDPCamSender::sentPkSignal = registerSignal("sentPk");
simsignal_t UDPCamSender::rcvdPkSignal = registerSignal("rcvdPk");


UDPCamSender::~UDPCamSender()
{
    cancelAndDelete(selfMsg);
}

void UDPCamSender::initialize(int stage)
{
    ApplicationBase::initialize(stage);

    if (stage == INITSTAGE_LOCAL) {
        numSent = 0;
        numReceived = 0;
        WATCH(numSent);
        WATCH(numReceived);

        localPort = par("localPort");
        destPort = par("destPort");
        startTime = simTime() + uniform(0,par("sendInterval").doubleValue());
        stopTime = par("stopTime").doubleValue();
        packetName = par("packetName");
        if (stopTime >= SIMTIME_ZERO && stopTime < startTime)
            throw cRuntimeError("Invalid startTime/stopTime parameters");

        const std::string output = "../../output/output_" + this->getFullPath() + "_sender.txt";
        ofs.open(output, std::ios::out);

        selfMsg = new cMessage("sendTimer");
    }
}

void UDPCamSender::finish()
{
    recordScalar("packets sent", numSent);
    recordScalar("packets received", numReceived);
    ApplicationBase::finish();
}

void UDPCamSender::setSocketOptions()
{
    int timeToLive = par("timeToLive");
    if (timeToLive != -1)
        socket.setTimeToLive(timeToLive);

    int typeOfService = par("typeOfService");
    if (typeOfService != -1)
        socket.setTypeOfService(typeOfService);

    const char *multicastInterface = par("multicastInterface");
    if (multicastInterface[0]) {
        IInterfaceTable *ift = getModuleFromPar<IInterfaceTable>(par("interfaceTableModule"), this);
        InterfaceEntry *ie = ift->getInterfaceByName(multicastInterface);
        if (!ie)
            throw cRuntimeError("Wrong multicastInterface setting: no interface named \"%s\"", multicastInterface);
        socket.setMulticastOutputInterface(ie->getInterfaceId());
    }

    bool receiveBroadcast = par("receiveBroadcast");
    if (receiveBroadcast)
        socket.setBroadcast(true);

    bool joinLocalMulticastGroups = par("joinLocalMulticastGroups");
    if (joinLocalMulticastGroups) {
        MulticastGroupList mgl = getModuleFromPar<IInterfaceTable>(par("interfaceTableModule"), this)->collectMulticastGroups();
        socket.joinLocalMulticastGroups(mgl);
    }
}

L3Address UDPCamSender::chooseDestAddr()
{
    int k = intrand(destAddresses.size());
    if (destAddresses[k].isLinkLocal()) {    // KLUDGE for IPv6
        const char *destAddrs = par("destAddresses");
        cStringTokenizer tokenizer(destAddrs);
        const char *token = nullptr;

        for (int i = 0; i <= k; ++i)
            token = tokenizer.nextToken();
        destAddresses[k] = L3AddressResolver().resolve(token);
    }
    return destAddresses[k];
}

void UDPCamSender::sendPacket()
{
//    std::ostringstream str;
//    str << packetName << "-" << numSent;

//    ApplicationPacket *payload = new ApplicationPacket(str.str().c_str());
//    payload->setByteLength(par("messageLength").longValue());
//    payload->setSequenceNumber(numSent);

    ApplicationPacket **payloads = searchAndMakeCamPayloads();

    L3Address destAddr = chooseDestAddr();

    for (int i = 0; i < sizeof(payloads); i++) {
      emit(sentPkSignal, payload[i]);
      socket.sendTo(payload[i], destAddr, destPort);
      numSent++;
    }
}

std::vector<ApplicationPacket*> UDPCamSender::searchAndMakeCamPayloads() {
  EV_INFO << "sending cam......" << endl;

  std::vector<VehicleDataProvider> vdps;

  auto mod = getSimulation()->getSystemModule();
  for (cModule::SubmoduleIterator iter(mod); !iter.end(); iter++) {
    cModule* submod = SUBMODULE_ITERATOR_TO_MODULE(iter);
    if (submod->getName().size() >= "node".size() && std::equal(std::begin("node"), std::end("node"), std::begin(submod->getName()))) {
      if(distance < ~~m) {
        vdps.push_back(submod);
      }
    }
  }

  std::vector<ApplicationPacket *> payloads;
  for (auto it = vdps.begin();it != vdps.end(); ++it) {
    payloads.push_back(getCamPayload(it));
  }

  return payloads;
}

ApplicationPacket* UDPCamSender::getCamPayload(const VehicleDataProvider& vdp) {
  std::ostringstream str;
  str << "1" << ","                             //header.protocolVersion
      << ItsPduHeader__messageID_cam << ","     //header.messageId
      << "0" << ","                             //header.stationID
      << mTimer->getTimeFor(simTime()) << ","   //cam.generationDeltaTime
      << StationType_passengerCar << ","
      << AltitudeValue_unavailable << ","
      << longitude << ","
      << latitude << ","
      << HeadingValue_unavailable << ","
      << SemiAxisLength_unavailable << ","
      << SemiAxisLength_unavailable << ","
      << HighFrequencyContainer_PR_basicVehicleContainerHighFrequency << ","
      << heading << ","
      << HeadingConfidence_equalOrWithinOneDegree << ","
      << speed << ","
      << speedConfidence << ","

  ApplicationPacket *payload = new ApplicationPacket(str.str().c_str());
  payload->setByteLength(sizeof(str).longValue());
  payload->setSequenceNumber(numSent);

  return payload;
}

//vanetza::asn1::Cam

void UDPCamSender::processStart()
{
    socket.setOutputGate(gate("udpOut"));
    const char *localAddress = par("localAddress");
    socket.bind(*localAddress ? L3AddressResolver().resolve(localAddress) : L3Address(), localPort);
    setSocketOptions();

    const char *destAddrs = par("destAddresses");
    cStringTokenizer tokenizer(destAddrs);
    const char *token;

    while ((token = tokenizer.nextToken()) != nullptr) {
        L3Address result;
        L3AddressResolver().tryResolve(token, result);
        if (result.isUnspecified())
            EV_ERROR << "cannot resolve destination address: " << token << endl;
        else
            destAddresses.push_back(result);
    }

    if (!destAddresses.empty()) {
        selfMsg->setKind(SEND);
        processSend();
    }
    else {
        if (stopTime >= SIMTIME_ZERO) {
            selfMsg->setKind(STOP);
            scheduleAt(stopTime, selfMsg);
        }
    }
}

void UDPCamSender::processSend()
{
    sendPacket();
    simtime_t d = simTime() + par("sendInterval").doubleValue();
    if (stopTime < SIMTIME_ZERO || d < stopTime) {
        selfMsg->setKind(SEND);
        scheduleAt(d, selfMsg);
    }
    else {
        selfMsg->setKind(STOP);
        scheduleAt(stopTime, selfMsg);
    }
}

void UDPCamSender::processStop()
{
    socket.close();
}

void UDPCamSender::handleMessageWhenUp(cMessage *msg)
{
    if (msg->isSelfMessage()) {
        ASSERT(msg == selfMsg);
        switch (selfMsg->getKind()) {
            case START:
                processStart();
                break;

            case SEND:
                processSend();
                break;

            case STOP:
                processStop();
                break;

            default:
                throw cRuntimeError("Invalid kind %d in self message", (int)selfMsg->getKind());
        }
    }
    else if (msg->getKind() == UDP_I_DATA) {
        // process incoming packet
        processPacket(PK(msg));
    }
    else if (msg->getKind() == UDP_I_ERROR) {
        EV_WARN << "Ignoring UDP error report\n";
        delete msg;
    }
    else {
        throw cRuntimeError("Unrecognized message (%s)%s", msg->getClassName(), msg->getName());
    }
}

void UDPCamSender::refreshDisplay() const
{
    char buf[100];
    sprintf(buf, "rcvd: %d pks\nsent: %d pks", numReceived, numSent);
    getDisplayString().setTagArg("t", 0, buf);
}

void UDPCamSender::processPacket(cPacket *pk)
{
    emit(rcvdPkSignal, pk);
    EV_INFO << "Received packet: " << UDPSocket::getReceivedPacketInfo(pk) << endl;
    delete pk;
    numReceived++;
}

bool UDPCamSender::handleNodeStart(IDoneCallback *doneCallback)
{
    simtime_t start = std::max(startTime, simTime());
    if ((stopTime < SIMTIME_ZERO) || (start < stopTime) || (start == stopTime && startTime == stopTime)) {
        selfMsg->setKind(START);
        scheduleAt(start, selfMsg);
    }
    return true;
}

bool UDPCamSender::handleNodeShutdown(IDoneCallback *doneCallback)
{
    if (selfMsg)
        cancelEvent(selfMsg);
    //TODO if(socket.isOpened()) socket.close();
    return true;
}

void UDPCamSender::handleNodeCrash()
{
    if (selfMsg)
        cancelEvent(selfMsg);
}

} // namespace inet

