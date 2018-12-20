#include "artery/veins/VeinsMobility.h"
#include <cmath>

namespace artery
{

Define_Module(VeinsMobility)

void VeinsMobility::initialize(int stage)
{
  std::cout << "veinsmobility init " << stage << endl;
  if (stage == 0) {
        WATCH(mVehicleId);
        WATCH(mPosition);
        WATCH(mDirection);
        WATCH(mSpeed);
    } else if (stage == 1) {
        mPosition.z = move.getStartPos().z;
        move.setStart(mPosition);
        move.setSpeed(mSpeed);
        move.setDirectionByVector(mDirection);
    }
    BaseMobility::initialize(stage);
}

void VeinsMobility::initialize(const Position& pos, Angle heading, double speed)
{
  using boost::units::si::meter;
 std::cout << this->getFullPath() << " initializing" << endl;
  std::cout << pos.x /meter<< "," << pos.y /meter<< endl;
    mPosition.x = pos.x / meter;
    mPosition.y = pos.y / meter;
    move.setStart(mPosition);

    mSpeed = speed;
    move.setSpeed(mSpeed);

    mDirection = Coord { cos(heading.radian()), -sin(heading.radian()) };
    move.setDirectionByVector(mDirection);
}

void VeinsMobility::update(const Position& pos, Angle heading, double speed)
{
    std::cout << this->getFullPath() << " updating" << endl;
    initialize(pos, heading, speed);

    BaseMobility::updatePosition(); // emits update signal for Veins
    // assert there is no identical signal emitted twice
    ASSERT(BaseMobility::mobilityStateChangedSignal != MobilityBase::stateChangedSignal);
    emit(MobilityBase::stateChangedSignal, this);
}

} // namespace artery
