//
// Copyright (C) OpenSim Ltd.
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

#include "inet/common/ModuleAccess.h"
#include "inet/networklayer/common/L3AddressResolver.h"
#include "inet/visualizer/linklayer/InterfaceTableCanvasVisualizer.h"

namespace inet {

namespace visualizer {

Define_Module(InterfaceTableCanvasVisualizer);

InterfaceTableCanvasVisualizer::InterfaceCanvasVisualization::InterfaceCanvasVisualization(NetworkNodeCanvasVisualization *networkNodeVisualization, BoxedLabelFigure *figure, int networkNodeId, int interfaceId) :
    InterfaceVisualization(networkNodeId, interfaceId),
    networkNodeVisualization(networkNodeVisualization),
    figure(figure)
{
}

InterfaceTableCanvasVisualizer::InterfaceCanvasVisualization::~InterfaceCanvasVisualization()
{
    delete figure;
}

void InterfaceTableCanvasVisualizer::initialize(int stage)
{
    InterfaceTableVisualizerBase::initialize(stage);
    if (!hasGUI()) return;
    if (stage == INITSTAGE_LOCAL) {
        zIndex = par("zIndex");
        networkNodeVisualizer = getModuleFromPar<NetworkNodeCanvasVisualizer>(par("networkNodeVisualizerModule"), this);
    }
}

InterfaceTableVisualizerBase::InterfaceVisualization *InterfaceTableCanvasVisualizer::createInterfaceVisualization(cModule *networkNode, InterfaceEntry *interfaceEntry)
{
    std::cout << "hello interface visualization" << endl;
    BoxedLabelFigure *figure = nullptr;
    auto gate = displayWiredInterfacesAtConnections ? getOutputGate(networkNode, interfaceEntry) : nullptr;
    if (gate == nullptr) {
        figure = new BoxedLabelFigure("networkInterface");
        figure->setTags((std::string("network_interface ") + tags).c_str());
        figure->setTooltip("This label represents a network interface in a network node");
        figure->setAssociatedObject(interfaceEntry);
        figure->setZIndex(zIndex);
        figure->setFont(font);
        figure->setText(getVisualizationText(interfaceEntry).c_str());
        figure->setLabelColor(textColor);
        figure->setBackgroundColor(backgroundColor);
        figure->setOpacity(opacity);
        if (!displayBackground) {
            figure->setInset(0);
            figure->getRectangleFigure()->setVisible(false);
        }
    }
    auto networkNodeVisualization = networkNodeVisualizer->getNetworkNodeVisualization(networkNode);

    std::cout << "end interface visualization" << endl;
    return new InterfaceCanvasVisualization(networkNodeVisualization, figure, networkNode->getId(), interfaceEntry->getInterfaceId());
}

cModule *InterfaceTableCanvasVisualizer::getNetworkNode(const InterfaceVisualization *interfaceVisualization)
{
    std::cout << "hello get networknode" << endl;
    L3AddressResolver addressResolver;
    return getSimulation()->getModule(interfaceVisualization->networkNodeId);
}

InterfaceEntry *InterfaceTableCanvasVisualizer::getInterfaceEntry(const InterfaceVisualization *interfaceVisualization)
{
    std::cout << "hello getinterfaceentry" << endl;
    L3AddressResolver addressResolver;
    std::cout << "hello getNetworkNode from getinterfaceentry" << endl;
    auto networkNode = getNetworkNode(interfaceVisualization);
    std::cout << "end getinterfaceentry" << endl;
    if (networkNode == nullptr)
        return nullptr;
    auto interfaceTable = addressResolver.findInterfaceTableOf(networkNode);
    if (interfaceTable == nullptr)
        return nullptr;
    return interfaceTable->getInterfaceById(interfaceVisualization->interfaceId);
}

cGate *InterfaceTableCanvasVisualizer::getOutputGate(cModule *networkNode, InterfaceEntry *interfaceEntry)
{
    std::cout << "hello and end getoutputgate a" << endl;
    if (interfaceEntry->getNodeOutputGateId() == -1)
        std::cout << "returning null a" << endl;
        return nullptr;
    cGate *outputGate = networkNode->gate(interfaceEntry->getNodeOutputGateId());
    if (outputGate == nullptr || outputGate->getChannel() == nullptr) {
        std::cout << "returning null b" << endl;
        return nullptr;
    }else
        return outputGate;
}

cGate *InterfaceTableCanvasVisualizer::getOutputGate(const InterfaceVisualization *interfaceVisualization)
{
    std::cout << "hello getoutputgate b" << endl;
    std::cout << "hello getNetworkNode from getoutputgate b" << endl;
    auto networkNode = getNetworkNode(interfaceVisualization);
    std::cout << "hello getinterfaceentry from getoutputgate b" << endl;
    auto interfaceEntry = getInterfaceEntry(interfaceVisualization);
    if (interfaceEntry == nullptr) {
    std::cout << "end getoutputgate" << endl;
        return nullptr;
    }else {
      std::cout << "hello getoutputgate from getoutputgate b" << endl;
      std::cout << "end getoutputgate b after getOutputgate a" << endl;
        return getOutputGate(networkNode, interfaceEntry);
      }
}

void InterfaceTableCanvasVisualizer::addInterfaceVisualization(const InterfaceVisualization *interfaceVisualization)
{
    std::cout << "hello addinterfacevisualization" << endl;
    InterfaceTableVisualizerBase::addInterfaceVisualization(interfaceVisualization);
    auto interfaceCanvasVisualization = static_cast<const InterfaceCanvasVisualization *>(interfaceVisualization);
    std::cout << "hello getoutputgate from addInterfaceVisualization" << endl;
    auto gate = displayWiredInterfacesAtConnections ? getOutputGate(interfaceVisualization) : nullptr;
    std::cout << "gate is null? " << (gate!= nullptr) << endl;
    if (gate != nullptr) {
        cDisplayString& displayString = gate->getDisplayString();
        std::cout << "hello getVisualizationText from addInterfaceVisualization" << endl;
        displayString.setTagArg("t", 0, getVisualizationText(getInterfaceEntry(interfaceVisualization)).c_str());
        displayString.setTagArg("t", 1, "l");
    }
    else {
      std::cout << "interfaceCanvasVisualization is null? " << (interfaceCanvasVisualization == nullptr) << endl;
      std::cout << "networkNodeVisualization is null? " << (interfaceCanvasVisualization->networkNodeVisualization == nullptr) << endl;

        interfaceCanvasVisualization->networkNodeVisualization->addAnnotation(interfaceCanvasVisualization->figure, interfaceCanvasVisualization->figure->getBounds().getSize(), placementHint, placementPriority);
      }
    std::cout << "END addinterfacevisualization" << endl;

}

void InterfaceTableCanvasVisualizer::removeInterfaceVisualization(const InterfaceVisualization *interfaceVisualization)
{
    std::cout << "hello removeinterfacevisualization" << endl;
    InterfaceTableVisualizerBase::removeInterfaceVisualization(interfaceVisualization);
    auto interfaceCanvasVisualization = static_cast<const InterfaceCanvasVisualization *>(interfaceVisualization);
    auto gate = displayWiredInterfacesAtConnections ? getOutputGate(interfaceVisualization) : nullptr;
    if (gate != nullptr)
        gate->getDisplayString().setTagArg("t", 0, "");
    else
        interfaceCanvasVisualization->networkNodeVisualization->removeAnnotation(interfaceCanvasVisualization->figure);
}

void InterfaceTableCanvasVisualizer::refreshInterfaceVisualization(const InterfaceVisualization *interfaceVisualization, const InterfaceEntry *interfaceEntry)
{
    std::cout << "hello refreshinterfacevisualization" << endl;
    auto interfaceCanvasVisualization = static_cast<const InterfaceCanvasVisualization *>(interfaceVisualization);
    auto gate = displayWiredInterfacesAtConnections ? getOutputGate(interfaceVisualization) : nullptr;
    if (gate != nullptr)
        gate->getDisplayString().setTagArg("t", 0, getVisualizationText(interfaceEntry).c_str());
    else {
        auto figure = interfaceCanvasVisualization->figure;
        figure->setText(getVisualizationText(interfaceEntry).c_str());
        interfaceCanvasVisualization->networkNodeVisualization->setAnnotationSize(figure, figure->getBounds().getSize());
    }
}

} // namespace visualizer

} // namespace inet
