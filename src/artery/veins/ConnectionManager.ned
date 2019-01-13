package artery.veins;

simple ConnectionManager extends org.car2x.veins.base.connectionManager.ConnectionManager
{
    parameters:
        double node_maxInterfDist @unit(m);
        @class(VeinsConnectionManager);
}
