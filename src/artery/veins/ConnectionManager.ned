package artery.veins;

simple ConnectionManager extends org.car2x.veins.base.connectionManager.ConnectionManager
{
    parameters:
        double node_maxInterfDist = default(0);
        @class(VeinsConnectionManager);
}
