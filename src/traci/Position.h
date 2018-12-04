#ifndef POSITION_H_ECOTFZI7
#define POSITION_H_ECOTFZI7

#include "artery/utility/Geometry.h"
#include "traci/Boundary.h"
#include "traci/sumo/utils/traci/TraCIAPI.h"

namespace traci
{

using TraCIPosition = libsumo::TraCIPosition;

artery::Position position_cast(const TraCIBoundary&, const TraCIPosition&);
TraCIPosition position_cast(const TraCIBoundary&, const artery::Position&);

} // namespace traci

#endif /* POSITION_H_ECOTFZI7 */

