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
#include <boost/units/cmath.hpp>
#include <boost/units/systems/si/prefixes.hpp>

#include "inet/networklayer/common/L3AddressResolver.h"
#include "inet/common/ModuleAccess.h"
#include "inet/common/lifecycle/NodeOperations.h"
#include "inet/transportlayer/contract/udp/UDPControlInfo_m.h"
#include "artery/application/VehicleMiddleware.h"
#include "veins/base/utils/MiXiMDefs.h"
//#include "artery/utility/Geometry.h"
#include "artery/traci/VehicleController.h"
#include "artery/veins/VeinsMobility.h"

namespace artery {

using namespace omnetpp;

template<typename T, typename U>
long round(const boost::units::quantity<T>& q, const U& u)
{
  boost::units::quantity<U> v { q };
  return std::round(v.value());
}

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
        mTimer.setTimebase(par("datetime"));
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
    std::cout << destAddresses[k] << endl;
    return destAddresses[k];
}

void UDPCamSender::sendPacket()
{
//    std::ostringstream str;
//    str << packetName << "-" << numSent;

//    ApplicationPacket *payload = new ApplicationPacket(str.str().c_str());
//    payload->setByteLength(par("messageLength").longValue());
//    payload->setSequenceNumber(numSent);

    std::vector<ApplicationPacket*> payloads = searchAndMakeCamPayloads();

    L3Address destAddr = chooseDestAddr();

    for (auto it = payloads.begin();it != payloads.end(); ++it) {
      for (int i = 0 ; i < destAddresses.size(); i++) {
        emit(sentPkSignal, *it);
        socket.sendTo((*it)->dup(), destAddresses[i], destPort);
        ofs << "time: " << simTime()
            << "\tserial num: " << numSent
            << "\tfrom: " << L3AddressResolver().resolve(this->getParentModule()->getFullPath().c_str())
            << "\tto: " << destAddresses[i]
            << endl;
        std::cout << "udp packet sent" << endl;
        numSent++;
      }
      delete (*it);
    }
}

std::vector<ApplicationPacket*> UDPCamSender::searchAndMakeCamPayloads() {
  EV_INFO << "sending cam......" << endl;

  std::vector<const VehicleDataProvider *> vdps;

  VeinsMobility* mobility = check_and_cast<VeinsMobility *>(this->getParentModule()->getParentModule()->getModuleByPath(".mobility"));
  Coord cpos = mobility->getCurrentPosition();
  //  traci::VehicleController* controller = (traci::VehicleController*)(mobility->getVehicleController());
//  auto pos = controller->getPosition();
  auto pos = Position(cpos.x, cpos.y);

  auto mod = getSimulation()->getSystemModule();

  for (cModule::SubmoduleIterator iter(mod); !iter.end(); iter++) {
    cModule* submod = SUBMODULE_ITERATOR_TO_MODULE(iter);
    if (strstr(submod->getName(),"node")!=NULL) {
      VehicleMiddleware* middleware = check_and_cast<VehicleMiddleware *>(submod->getModuleByPath(".appl.middleware"));
      const VehicleDataProvider* vdp = &middleware->getFacilities().get_const<VehicleDataProvider>();
      std::cout << "distance is " << (double)boost::geometry::distance(vdp->position(), pos) << endl;
      if (boost::geometry::distance(vdp->position(), pos) < 30) {
        vdps.push_back(vdp);
      }
    }
  }

  std::vector<ApplicationPacket *> payloads;
  for (auto it = vdps.begin();it != vdps.end(); ++it) {
    payloads.push_back(getCamPayload(*it));
  }

  return payloads;
}

ApplicationPacket* UDPCamSender::getCamPayload(const VehicleDataProvider* vdp) {
  auto microdegree = vanetza::units::degree * boost::units::si::micro;
  auto decidegree = vanetza::units::degree * boost::units::si::deci;
  auto degree_per_second = vanetza::units::degree / vanetza::units::si::second;
  auto centimeter_per_second = vanetza::units::si::meter_per_second * boost::units::si::centi;

  std::ostringstream str;
  str << "1" << ","                             //header.protocolVersion
      << ItsPduHeader__messageID_cam << ","     //header.messageId
      << "0" << ","                             //header.stationID
      << countTaiMilliseconds(mTimer.getTimeFor(simTime())) << ","   //cam.generationDeltaTime
      << StationType_passengerCar << ","
      << AltitudeValue_unavailable << ","
      << AltitudeConfidence_unavailable << ","
      << round(vdp->longitude(), microdegree) * Longitude_oneMicrodegreeEast << ","
      << round(vdp->latitude(), microdegree) * Latitude_oneMicrodegreeNorth << ","
      << HeadingValue_unavailable << ","
      << SemiAxisLength_unavailable << ","
      << SemiAxisLength_unavailable << ","
      << HighFrequencyContainer_PR_basicVehicleContainerHighFrequency << ","
      << round(vdp->heading(), decidegree) << ","
      << HeadingConfidence_equalOrWithinOneDegree << ","
      << round(vdp->speed(), centimeter_per_second) * SpeedValue_oneCentimeterPerSec << ","
      << SpeedConfidence_equalOrWithinOneCentimeterPerSec * 3 << ",";

  if (vdp->speed().value() >= 0.0) {
    str << DriveDirection_forward << ",";
  } else {
    str << DriveDirection_backward << ",";
  }

  const double lonAccelValue = vdp->acceleration() / vanetza::units::si::meter_per_second_squared;
  // extreme speed changes can occur when SUMO swaps vehicles between lanes (speed is swapped as well)
  if (lonAccelValue >= -160.0 && lonAccelValue <= 161.0) {
    str << lonAccelValue * LongitudinalAccelerationValue_pointOneMeterPerSecSquaredForward << ",";
  } else {
    str << LongitudinalAccelerationValue_unavailable << ",";
  }

  str << AccelerationConfidence_unavailable << ",";
  if (abs(vdp->curvature() / vanetza::units::reciprocal_metre) * 10000.0 >= 1023) {
    str << 1023 << ",";
  } else {
    str << abs(vdp->curvature() / vanetza::units::reciprocal_metre) * 10000.0 << ",";
  }

  str << CurvatureConfidence_unavailable << ","
      << CurvatureCalculationMode_yawRateUsed << ",";
  if (abs(round(vdp->yaw_rate(), degree_per_second) * YawRateValue_degSec_000_01ToLeft * 100.0) >= YawRateValue_unavailable) {
    str << YawRateValue_unavailable << ",";
  } else {
    str << round(vdp->yaw_rate(), degree_per_second) * YawRateValue_degSec_000_01ToLeft * 100.0 << ",";
  }

  str << VehicleLengthValue_unavailable << ","
      << VehicleLengthConfidenceIndication_noTrailerPresent << ","
      << VehicleWidth_unavailable << endl;

  ApplicationPacket *payload = new ApplicationPacket("CamPacket");
  payload->setByteLength(sizeof(str));
  payload->setSequenceNumber(numSent);
  payload->addPar("data") = str.str().c_str();
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

    if (strstr(destAddrs,"all")!= NULL) {
      int count = -1;
      for(cModule::SubmoduleIterator it(getSystemModule()); !it.end(); ++it){
        std::cout << (*it)->getFullName() << endl;
        if (strstr((*it)->getFullName(),"pcam")!= NULL) {
          count++;
          L3Address result;
          L3AddressResolver().tryResolve(
              ((std::string)"pcam[" + std::to_string(count) + (std::string)"].disseminator").c_str()
              , result);
          if (result.isUnspecified())
            std::cout << "resolve address error" << endl;
          else
            destAddresses.push_back(result);
        }
      }
    } else {
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
