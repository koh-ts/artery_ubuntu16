#include "artery/veins/VeinsConnectionManager.h"
#include <omnetpp/ccomponent.h>

namespace artery
{

using namespace omnetpp;
Define_Module(VeinsConnectionManager)

namespace
{
const simsignal_t removeNodeSignal = cComponent::registerSignal("traci.node.remove");
}

void VeinsConnectionManager::initialize(int stage)
{
    if (stage == 0) {
        getSystemModule()->subscribe(removeNodeSignal, this);
    }

    ConnectionManager::initialize(stage);
}

void VeinsConnectionManager::finish()
{
    getSystemModule()->unsubscribe(removeNodeSignal, this);
    ConnectionManager::finish();
}

void VeinsConnectionManager::receiveSignal(cComponent* src, simsignal_t signal, const char* id, cObject* module)
{
    if (signal == removeNodeSignal) {
        cModule* nic = check_and_cast<cModule*>(module)->getSubmodule("nic");
        if (nic) {
            this->unregisterNic(nic);
        }
    }
}

double VeinsConnectionManager::calcInterfDist()
{
  if (std::strstr(this->getFullPath().c_str(),"node") != NULL) {
    if (hasPar("node_maxInterfDist")) {
        double interfDistance = par("node_maxInterfDist").doubleValue();
        return interfDistance;
    } else {
        throw cRuntimeError("ConnectionManager: No value for maximum interference distance (maxInterfDist) provided.");
    }
  } else {
    if (hasPar("maxInterfDist")) {
        double interfDistance = par("maxInterfDist").doubleValue();
        return interfDistance;
    } else {
        throw cRuntimeError("ConnectionManager: No value for maximum interference distance (maxInterfDist) provided.");
    }
  }
}



} // namespace artery

