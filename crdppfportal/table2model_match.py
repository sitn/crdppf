# -*- coding: UTF-8 -*-
from crdppf.models.models import PrimaryLandUseZones, SecondaryLandUseZones
from crdppf.models.models import ComplementaryLandUsePerimeters, LandUseLinearConstraints
from crdppf.models.models import LandUsePointConstraints, PollutedSites
from crdppf.models.models import CHHighwaysProjectZones, CHHighwaysConstructionLimits
from crdppf.models.models import CHRailwaysProjectZones, CHRailwaysConstructionLimits
from crdppf.models.models import CHAirportSecurityZones
from crdppf.models.models import CHAirportProjectZones, ContaminatedMilitarySites
from crdppf.models.models import CHAirportConstructionLimits
from crdppf.models.models import CHPollutedSitesCivilAirports
from crdppf.models.models import CHPollutedSitesPublicTransports
from crdppf.models.models import WaterProtectionZones, WaterProtectionPerimeters
from crdppf.models.models import RoadNoise, ForestLimits, ForestDistances

# Matching dictionnary model-table name
table2model_match = {
    'r73_affectations_primaires': PrimaryLandUseZones,
    'r73_zones_superposees': SecondaryLandUseZones,
    'r73_perimetres_superposes': ComplementaryLandUsePerimeters,
    'r73_contenus_lineaires': LandUseLinearConstraints,
    'r73_contenus_ponctuels': LandUsePointConstraints,
    'r87_astra_projektierungszonen_nationalstrassen': CHHighwaysProjectZones,
    'r88_astra_baulinien_nationalstrassen': CHHighwaysConstructionLimits,
    'r97_bav_baulinien_eisenbahnanlagen': CHRailwaysConstructionLimits,
    'r96_bav_projektierungszonen_eisenbahnanlagen': CHRailwaysProjectZones,
    'r103_bazl_projektierungszonen_flughafenanlagen': CHAirportProjectZones,
    'r104_bazl_baulinien_flughafenanlagen': CHAirportConstructionLimits,
    'r108_bazl_sicherheitszonenplan': CHAirportSecurityZones,
    'r116_sites_pollues': PollutedSites,
    'v_r117_vbs_belastete_standorte_militaer': ContaminatedMilitarySites,
    'r118_bazl_belastete_standorte_zivilflugplaetze': CHPollutedSitesCivilAirports,
    'r119_bav_belastete_standorte_oev': CHPollutedSitesPublicTransports,
    'r131_zone_prot_eau': WaterProtectionZones,
    'r132_perimetre_prot_eau': WaterProtectionPerimeters,
    'r145_sens_bruit': RoadNoise,
    'r157_lim_foret': ForestLimits,
    'r159_dist_foret': ForestDistances
}
