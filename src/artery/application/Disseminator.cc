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
//
//simsignal_t UDPCamListener::rcvdPkSignal = registerSignal("campktrcv");

Disseminator::Disseminator()
{
}

Disseminator::~Disseminator()
{
}

void Disseminator::initialize(int stage)
{
    std::cout << this->getSubmodule("udpApp[0]")->getFullPath() << endl;
    auto udpcamlsn = this->getSubmodule("udpApp[0]")->subscribe(UDPCamListener::rcvdPkSignal,this)

}

bool Disseminator::disseminate(cPacket *pk)
{

}

void Disseminator::receiveSignal(cComponent*, simsignal_t sig, cObject* obj, cObject*)
{
    if (sig == rcvdPkSignal) {
        std::cout << "signal received!!!!!!!!!!!!!!!!!!" << endl;
        cPacket* pk = check_and_cast<cPacket>(obj);
        disseminate(pk);
    }
}
} //namespace
