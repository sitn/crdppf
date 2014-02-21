# -*- coding: UTF-8 -*-
from crdppf.models import PrimaryLandUseZones, SecondaryLandUseZones
from crdppf.models import ComplementaryLandUsePerimeters, LandUseLinearConstraints
from crdppf.models import LandUsePointConstraints, CHAirportProjectZones
from crdppf.models import CHAirportSecurityZones, PollutedSites
from crdppf.models import CHPollutedSitesPublicTransports, Zoneprotection
from crdppf.models import Zoneprotection, WaterProtectionPerimeters
from crdppf.models import RoadNoise, ForestLimits, ForestDistances

# Matching dictionnary model-table name
table2model = {
    'r73_affectations_primaires': PrimaryLandUseZones,
    'r73_zones_superposees': SecondaryLandUseZones,
    'r73_perimetres_superposes': ComplementaryLandUsePerimeters,
    'r73_contenus_lineaires': LandUseLinearConstraints,
    'r73_contenus_ponctuels': LandUsePointConstraints,
    'r103_bazl_projektierungszonen_flughafenanlagen': CHAirportProjectZones,
    'r108_bazl_sicherheitszonenplan': CHAirportSecurityZones,
    'r116_sites_pollues': PollutedSites,
    'r119_bav_belastete_standorte_oev': CHPollutedSitesPublicTransports,
    'r131_zone_prot_eau': Zoneprotection,
    'r132_perimetre_prot_eau': WaterProtectionPerimeters,
    'r145_sens_bruit': RoadNoise,
    'r157_lim_foret': ForestLimits,
    'r159_dist_foret': ForestDistances
}