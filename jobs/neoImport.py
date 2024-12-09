from nautobot.apps.jobs import Job, register_jobs
from neo4j import GraphDatabase
from nautobot.dcim.models.locations import Location, LocationType
from nautobot.extras.models.statuses import Status
from nautobot.dcim.models.devices import Device, DeviceRedundancyGroup, DeviceType, Manufacturer, Platform, VirtualChassis
from nautobot.extras.models.roles import Role

class DBImport(Job):

    def run(self):
        print('neo import job started...')
        neoDBUrl = "bolt://1.6.62.246:7687"
        username = 'neo4j'
        password = 'sify'
        driver = GraphDatabase.driver(neoDBUrl, auth=(username, password))
        result = driver.execute_query('match (d:Device) where d.bstn = "TN-MAA-TDL" return d.hostname limit 10')

        tidel = Location.objects.get(name='Tidel')
        locationStatus = Status.objects.get(name='Active')
        deviceTypeSwitch = DeviceType.objects.all()[0]
        cceRole = Role.objects.all()[2]

        for record in result[0] :
            Device.objects.get_or_create(name=record.get('d.hostname'), location=tidel, status=locationStatus, role=cceRole, device_type=deviceTypeSwitch)

        driver.close()
        print('neo import job finished...')
        register_jobs(DBImport)

register_jobs(DBImport)
