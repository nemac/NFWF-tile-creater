# creating tiles for NFWF viewer not a complete step by step but the general idea

## start the AWS instance.
the server has docker installed with three docker containers one for MapServer, one with mapcache,
and one with gdal and python.  All share some virtual volumes.  All are networked together.

replace ec2-user@ec2-3-86-102-181.compute-1.amazonaws.com with the instance dns name
replace [your pem file] with the location of provided by AWS for connecting to the server

## Copy CONUS images to AWS tile server, they are too large and take 4x longer to create tiles from when in S3  (just an example of what to do)
```bsh
scp -i [YOUR PEM FILE] TargetedWatershedAsset.tif ec2-user@ec2-3-86-102-181.compute-1.amazonaws.com:/tiledata/source/. &
scp -i [YOUR PEM FILE] TargetedWatershedExposure.tif ec2-user@ec2-3-86-102-181.compute-1.amazonaws.com:/tiledata/source/. &
scp -i [YOUR PEM FILE] TargetedWatershedHubs.tif ec2-user@ec2-3-86-102-181.compute-1.amazonaws.com:/tiledata/source/. &
scp -i [YOUR PEM FILE] TargetedWatershedThreat.tif ec2-user@ec2-3-86-102-181.compute-1.amazonaws.com:/tiledata/source/.  &
scp -i [YOUR PEM FILE] TargetedWatershedFishandWildlife.tif ec2-user@ec2-3-86-102-181.compute-1.amazonaws.com:/tiledata/source/. &
```
## for CONUS data should convert to 8 bit signed for faster significantly faster processing time (just an example of what to do)
```bsh
gdal_translate -of GTiff -ot Byte -a_nodata 255 TargetedWatershedThreat.tif TargetedWatershedThreat8.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 TargetedWatershedAsset.tif TargetedWatershedAsset8.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 TargetedWatershedExposure.tif TargetedWatershedExposure8.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 TargetedWatershedHubs.tif TargetedWatershedHubs8.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 TargetedWatershedFishandWildlife.tif TargetedWatershedFishandWildlife8.tif -co COMPRESS=LZW &
```

## Copy CONUS8 bit images locally if you want a copy for your self or to check values did not get messed up (just an example of what to do)
```bsh
scp -i [YOUR PEM FILE] ec2-user@ec2-3-86-102-181.compute-1.amazonaws.com:/tiledata/source/TargetedWatershedAsset8.tif . &
scp -i [YOUR PEM FILE] ec2-user@ec2-3-86-102-181.compute-1.amazonaws.com:/tiledata/source/TargetedWatershedExposure8.tif . &
scp -i [YOUR PEM FILE] ec2-user@ec2-3-86-102-181.compute-1.amazonaws.com:/tiledata/source/TargetedWatershedHubs8.tif . &
scp -i [YOUR PEM FILE] ec2-user@ec2-3-86-102-181.compute-1.amazonaws.com:/tiledata/source/TargetedWatershedThreat8.tif .  &
scp -i [YOUR PEM FILE] ec2-user@ec2-3-86-102-181.compute-1.amazonaws.com:/tiledata/source/TargetedWatershedFishandWildlife8.tif . &
```
## get island images from s3
```bash
wget https://nfwf-tool.s3.amazonaws.com/puerto-rico/PR_AssetIndex_10class_021020_clip.tif &
wget https://nfwf-tool.s3.amazonaws.com/puerto-rico/PR_CombinedWildlife_6class_040320.tif &
wget https://nfwf-tool.s3.amazonaws.com/puerto-rico/PR_CriticalFacilities_v2_clip.tif &
wget https://nfwf-tool.s3.amazonaws.com/puerto-rico/PR_CriticalInfrastructure_v2_clip.tif &
wget https://nfwf-tool.s3.amazonaws.com/puerto-rico/PR_ErodibleSoils_v2_clip.tif &
wget https://nfwf-tool.s3.amazonaws.com/puerto-rico/PR_ExposureIndex_10class_021120_clip.tif &
wget https://nfwf-tool.s3.amazonaws.com/puerto-rico/PR_FloodproneAreas_v2_clip.tif &
wget https://nfwf-tool.s3.amazonaws.com/puerto-rico/PR_Impermeable_v2_clip.tif &
wget https://nfwf-tool.s3.amazonaws.com/puerto-rico/PR_Landslides_v2_clip.tif &
wget https://nfwf-tool.s3.amazonaws.com/puerto-rico/PR_LowLyingAreas_v2_clip.tif &
wget https://nfwf-tool.s3.amazonaws.com/puerto-rico/PR_MarineIndex_4class.tif &
wget https://nfwf-tool.s3.amazonaws.com/puerto-rico/PR_PopulationDensity_v2_clip.tif &
wget https://nfwf-tool.s3.amazonaws.com/puerto-rico/PR_SLR_v2_clip.tif &
wget https://nfwf-tool.s3.amazonaws.com/puerto-rico/PR_SocialVulnerability_v2_clip.tif &
wget https://nfwf-tool.s3.amazonaws.com/puerto-rico/PR_StormSurge_v2_clip.tif &
wget https://nfwf-tool.s3.amazonaws.com/puerto-rico/PR_TerrestrialIndex_4class.tif &
wget https://nfwf-tool.s3.amazonaws.com/puerto-rico/PR_ThreatIndex_10class_021120_clip.tif &
wget https://nfwf-tool.s3.amazonaws.com/puerto-rico/PR_Tsunami_v2_clip.tif &

wget https://nfwf-tool.s3.amazonaws.com/us-virgin-islands/USVI_AssetIndex_10class_021020_clip.tif &
wget https://nfwf-tool.s3.amazonaws.com/us-virgin-islands/USVI_CombinedWildlife_6class_040320.tif &
wget https://nfwf-tool.s3.amazonaws.com/us-virgin-islands/USVI_CriticalFacilities_v2_clip.tif &
wget https://nfwf-tool.s3.amazonaws.com/us-virgin-islands/USVI_CriticalInfrastructure_v2_clip.tif &
wget https://nfwf-tool.s3.amazonaws.com/us-virgin-islands/USVI_ErodibleSoils_v2_clip.tif &
wget https://nfwf-tool.s3.amazonaws.com/us-virgin-islands/USVI_ExposureIndex_10class_021220_clip.tif &
wget https://nfwf-tool.s3.amazonaws.com/us-virgin-islands/USVI_FloodproneAreas_v2_clip.tif &
wget https://nfwf-tool.s3.amazonaws.com/us-virgin-islands/USVI_Impermeable_v2_clip.tif &
wget https://nfwf-tool.s3.amazonaws.com/us-virgin-islands/USVI_LowLyingAreas_v2_clip.tif &
wget https://nfwf-tool.s3.amazonaws.com/us-virgin-islands/USVI_MarineIndex_4class.tif &
wget https://nfwf-tool.s3.amazonaws.com/us-virgin-islands/USVI_PopulationDensity_v2_clip.tif &
wget https://nfwf-tool.s3.amazonaws.com/us-virgin-islands/USVI_SLR_v2_clip.tif &
wget https://nfwf-tool.s3.amazonaws.com/us-virgin-islands/USVI_SocialVulnerability_v2_clip.tif &
wget https://nfwf-tool.s3.amazonaws.com/us-virgin-islands/USVI_StormSurge_v2_clip.tif &
wget https://nfwf-tool.s3.amazonaws.com/us-virgin-islands/USVI_TerrestrialIndex_4class.tif &
wget https://nfwf-tool.s3.amazonaws.com/us-virgin-islands/USVI_ThreatIndex_10class_021220_clip.tif &
```

## make 8bit no data 255
```bash
gdal_translate -of GTiff -ot Byte -a_nodata 255 PR_AssetIndex_10class_021020_clip.tif  PR_AssetIndex_10class_021020_clip_8bit.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 PR_CombinedWildlife_6class_040320.tif PR_CombinedWildlife_6class_040320_8bit.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 PR_CriticalFacilities_v2_clip.tif PR_CriticalFacilities_v2_clip_8bit.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 PR_CriticalInfrastructure_v2_clip.tif PR_CriticalInfrastructure_v2_clip_8bit.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 PR_ErodibleSoils_v2_clip.tif PR_ErodibleSoils_v2_clip_8bit.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 PR_ExposureIndex_10class_021120_clip.tif PR_ExposureIndex_10class_021120_clip_8bit.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 PR_FloodproneAreas_v2_clip.tif PR_FloodproneAreas_v2_clip_8bit.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 PR_Impermeable_v2_clip.tif PR_Impermeable_v2_clip_8bit.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 PR_Landslides_v2_clip.tif PR_Landslides_v2_clip_8bit.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 PR_LowLyingAreas_v2_clip.tif PR_LowLyingAreas_v2_clip_8bit.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 PR_MarineIndex_4class.tif PR_MarineIndex_4class_8bit.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 PR_PopulationDensity_v2_clip.tif PR_PopulationDensity_v2_clip_8bit.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 PR_SLR_v2_clip.tif PR_SLR_v2_clip_8bit.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 PR_SocialVulnerability_v2_clip.tif PR_SocialVulnerability_v2_clip_8bit.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 PR_StormSurge_v2_clip.tif PR_StormSurge_v2_clip_8bit.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 PR_TerrestrialIndex_4class.tif PR_TerrestrialIndex_4class_8bit.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 PR_ThreatIndex_10class_021120_clip.tif PR_ThreatIndex_10class_021120_clip_8bit.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 PR_Tsunami_v2_clip.tif PR_Tsunami_v2_clip_8bit.tif -co COMPRESS=LZW &

gdal_translate -of GTiff -ot Byte -a_nodata 255 USVI_AssetIndex_10class_021020_clip.tif USVI_AssetIndex_10class_021020_clip_8bit.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 USVI_CombinedWildlife_6class_040320.tif USVI_CombinedWildlife_6class_040320_8bit.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 USVI_CriticalFacilities_v2_clip.tif USVI_CriticalFacilities_v2_clip_8bit.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 USVI_CriticalInfrastructure_v2_clip.tif USVI_CriticalInfrastructure_v2_clip_8bit.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 USVI_ErodibleSoils_v2_clip.tif USVI_ErodibleSoils_v2_clip_8bit.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 USVI_ExposureIndex_10class_021220_clip.tif USVI_ExposureIndex_10class_021220_clip_8bit.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 USVI_FloodproneAreas_v2_clip.tif USVI_FloodproneAreas_v2_clip_8bit.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 USVI_Impermeable_v2_clip.tif USVI_Impermeable_v2_clip_8bit.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 USVI_LowLyingAreas_v2_clip.tif USVI_LowLyingAreas_v2_clip_8bit.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 USVI_MarineIndex_4class.tif USVI_MarineIndex_4class_8bit.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 USVI_PopulationDensity_v2_clip.tif USVI_PopulationDensity_v2_clip_8bit.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 USVI_SLR_v2_clip.tif USVI_SLR_v2_clip_8bit.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 USVI_SocialVulnerability_v2_clip.tif USVI_SocialVulnerability_v2_clip_8bit.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 USVI_StormSurge_v2_clip.tif USVI_StormSurge_v2_clip_8bit.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 USVI_TerrestrialIndex_4class.tif USVI_TerrestrialIndex_4class_8bit.tif -co COMPRESS=LZW &
gdal_translate -of GTiff -ot Byte -a_nodata 255 USVI_ThreatIndex_10class_021220_clip.tif USVI_ThreatIndex_10class_021220_clip_8bit.tif -co COMPRESS=LZW &

rm PR_AssetIndex_10class_021020_clip.tif
rm PR_CombinedWildlife_6class_040320.tif
rm PR_CriticalFacilities_v2_clip.tif
rm PR_CriticalInfrastructure_v2_clip.tif
rm PR_ErodibleSoils_v2_clip.tif
rm PR_ExposureIndex_10class_021120_clip.tif
rm PR_FloodproneAreas_v2_clip.tif
rm PR_Impermeable_v2_clip.tif
rm PR_Landslides_v2_clip.tif
rm PR_LowLyingAreas_v2_clip.tif
rm PR_MarineIndex_4class.tif
rm PR_PopulationDensity_v2_clip.tif
rm PR_SLR_v2_clip.tif
rm PR_SocialVulnerability_v2_clip.tif
rm PR_StormSurge_v2_clip.tif
rm PR_TerrestrialIndex_4class.tif
rm PR_ThreatIndex_10class_021120_clip.tif
rm PR_Tsunami_v2_clip.tif

rm USVI_AssetIndex_10class_021020_clip.tif
rm USVI_CombinedWildlife_6class_040320.tif
rm USVI_CriticalFacilities_v2_clip.tif
rm USVI_CriticalInfrastructure_v2_clip.tif
rm USVI_ErodibleSoils_v2_clip.tif
rm USVI_ExposureIndex_10class_021220_clip.tif
rm USVI_FloodproneAreas_v2_clip.tif
rm USVI_Impermeable_v2_clip.tif
rm USVI_LowLyingAreas_v2_clip.tif
rm USVI_MarineIndex_4class.tif
rm USVI_PopulationDensity_v2_clip.tif
rm USVI_SLR_v2_clip.tif
rm USVI_SocialVulnerability_v2_clip.tif
rm USVI_StormSurge_v2_clip.tif
rm USVI_TerrestrialIndex_4class.tif
rm USVI_ThreatIndex_10class_021220_clip.tif
```
## Copy Shapefiles that Limit the area tiles will be created, this helps to significantly decrease processingtime
If needed: CONSU Shapefile that Limits Tile area, shapefile needs to be in projection 3857
```bsh
scp -i [YOUR PEM FILE] targeted_watersheds.dbf ec2-user@ec2-3-86-102-181.compute-1.amazonaws.com:/home/ec2-user/NFWF-tile-creater/limitshapefiles/. &
scp -i [YOUR PEM FILE] targeted_watersheds.shp ec2-user@ec2-3-86-102-181.compute-1.amazonaws.com:/home/ec2-user/NFWF-tile-creater/limitshapefiles/. &
scp -i [YOUR PEM FILE] targeted_watersheds.shx ec2-user@ec2-3-86-102-181.compute-1.amazonaws.com:/home/ec2-user/NFWF-tile-creater/limitshapefiles/. &
scp -i [YOUR PEM FILE] targeted_watersheds.prj ec2-user@ec2-3-86-102-181.compute-1.amazonaws.com:/home/ec2-user/NFWF-tile-creater/limitshapefiles/. &
```

### If needed:  Puerto Rico Shapefile that Limits Tile area, shapefile needs to be in projection 3857
```bsh
scp -i [YOUR PEM FILE] ../Downloads/For_CREST/PR/PR_CREST_Clipping_Boundary_3857.dbf ec2-user@ec2-3-86-102-181.compute-1.amazonaws.com:/home/ec2-user/NFWF-tile-creater/limitshapefiles/. &
scp -i [YOUR PEM FILE] ../Downloads/For_CREST/PR/PR_CREST_Clipping_Boundary_3857.shp ec2-user@ec2-3-86-102-181.compute-1.amazonaws.com:/home/ec2-user/NFWF-tile-creater/limitshapefiles/. &
scp -i [YOUR PEM FILE] ../Downloads/For_CREST/PR/PR_CREST_Clipping_Boundary_3857.shx ec2-user@ec2-3-86-102-181.compute-1.amazonaws.com:/home/ec2-user/NFWF-tile-creater/limitshapefiles/. &
scp -i [YOUR PEM FILE] ../Downloads/For_CREST/PR/PR_CREST_Clipping_Boundary_3857.prj ec2-user@ec2-3-86-102-181.compute-1.amazonaws.com:/home/ec2-user/NFWF-tile-creater/limitshapefiles/. &
```

### If needed: Virgin Islands Shapefile that Limits Tile area, shapefile needs to be in projection 3857
```bsh
scp -i [YOUR PEM FILE] ../Downloads/For_CREST/USVI/USVI_CREST_Clipping_Boundary_3857.dbf ec2-user@ec2-3-86-102-181.compute-1.amazonaws.com:/home/ec2-user/NFWF-tile-creater/limitshapefiles/. &
scp -i [YOUR PEM FILE] ../Downloads/For_CREST/USVI/USVI_CREST_Clipping_Boundary_3857.shp ec2-user@ec2-3-86-102-181.compute-1.amazonaws.com:/home/ec2-user/NFWF-tile-creater/limitshapefiles/. &
scp -i [YOUR PEM FILE] ../Downloads/For_CREST/USVI/USVI_CREST_Clipping_Boundary_3857.shx ec2-user@ec2-3-86-102-181.compute-1.amazonaws.com:/home/ec2-user/NFWF-tile-creater/limitshapefiles/. &
scp -i [YOUR PEM FILE] ../Downloads/For_CREST/USVI/USVI_CREST_Clipping_Boundary_3857.prj ec2-user@ec2-3-86-102-181.compute-1.amazonaws.com:/home/ec2-user/NFWF-tile-creater/limitshapefiles/. &
```


### Starting docker on aws instance
SSH to aws instance
```bsh
ssh -i [YOUR PEM FILE] ec2-user@ec2-3-86-102-181.compute-1.amazonaws.com
ssh -i [YOUR PEM FILE] ec2-user@ec2-3-86-102-181.compute-1.amazonaws.com
```

#### start docker containers
```bsh
cd /home/ec2-user/NFWF-tile-creater
docker-compose up -d
docker exec -it mapcache-compose bash
```

### copy the shapefiles to source directory for docker container access probably could do that in early step
shapefiles have to be 3857...
```bsh
sudo cp limitshapefiles/USVI_CREST_* source/.
sudo cp limitshapefiles/PR_CREST_* source/.
```

#### Puerto Rico examples seeding is same for all regions but CONUS needs to be split even further do not try to start all of these at the same time, It will have timeout errors
from seed server seed all level 1 - 10 tiles if you do too many you will get timeouts.  but you can rerun the script only creates tiles that do not exist yet.
```bsh
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_AssetsIndexTiles -z 1,10 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_CombinedWildlifeIndexTiles -z 1,10 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_CriticalFacilitiesIndexTiles -z 1,10 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_CriticalInfrastructureIndexTiles -z 1,10 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_ExposureIndexTiles -z 1,10 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_ErosionIndexTiles -z 1,10 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_FloodProneAreasIndexTiles -z 1,10 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_DraingeIndexTiles -z 1,10 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_LandslideIndexTiles -z 1,10 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_SlopeIndexTiles -z 1,10 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_AquaticIndexTiles -z 1,10 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_SLRIndexTiles -z 1,10 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_SocVulnIndexTiles -z 1,10 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_StormSurgeIndexTiles -z 1,10 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_TerrestrialIndexTiles -z 1,10 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_ThreatsIndexTiles -z 1,10 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_TsunamiIndexTiles -z 1,10 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_PopDensityIndexTiles -z 1,10 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
```

#### US Virgin Islands
```bsh
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_AssetsIndexTiles -z 1,10 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_CombinedWildlifeIndexTiles -z 1,10 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_CriticalFacilitiesIndexTiles -z 1,10 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_CriticalInfrastructureIndexTiles -z 1,10 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_ExposureIndexTiles -z 1,10 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_ErosionIndexTiles -z 1,10 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_FloodProneAreasIndexTiles -z 1,10 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_DraingeIndexTiles -z 1,10 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_SlopeIndexTiles -z 1,10 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_AquaticIndexTiles -z 1,10 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_SLRIndexTiles -z 1,10 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_SocVulnIndexTiles -z 1,10 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_StormSurgeIndexTiles -z 1,10 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_TerrestrialIndexTiles -z 1,10 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_ThreatsIndexTiles -z 1,10 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_PopDensityIndexTiles -z 1,10 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
```

### from seed server seed all level 11 - 12 tiles if you do too many you will get timeouts. starting at these zoom levels try not do all of them and -d option with limit shapefile is important for reducing blank images, we will remove blanks (completely transparent) latter.
run repeatedly until you 0 tiles needed to be seeded, exiting
```bsh
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_AssetsIndexTiles -z 11,12 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_CombinedWildlifeIndexTiles -z 11,12 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_CriticalFacilitiesIndexTiles -z 11,12 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_CriticalInfrastructureIndexTiles -z 11,12 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_ExposureIndexTiles -z 11,12 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_ErosionIndexTiles -z 11,12 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_FloodProneAreasIndexTiles -z 11,12 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_DraingeIndexTiles -z 11,12 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_LandslideIndexTiles -z 11,12 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_SlopeIndexTiles -z 11,12 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_AquaticIndexTiles -z 11,12 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_SLRIndexTiles -z 11,12 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_SocVulnIndexTiles -z 11,12 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_StormSurgeIndexTiles -z 11,12 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_TerrestrialIndexTiles -z 11,12 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_ThreatsIndexTiles -z 11,12 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_TsunamiIndexTiles -z 11,12 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_PopDensityIndexTiles -z 11,12 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
```

#### US Virgin Islands
```bsh
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_AssetsIndexTiles -z 11,12 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_CombinedWildlifeIndexTiles -z 11,12 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_CriticalFacilitiesIndexTiles -z 11,12 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_CriticalInfrastructureIndexTiles -z 11,12 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_ExposureIndexTiles -z 11,12 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_ErosionIndexTiles -z 11,12 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_FloodProneAreasIndexTiles -z 11,12 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_DraingeIndexTiles -z 11,12 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_SlopeIndexTiles -z 11,12 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_AquaticIndexTiles -z 11,12 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_SLRIndexTiles -z 11,12 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_SocVulnIndexTiles -z 11,12 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_StormSurgeIndexTiles -z 11,12 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_TerrestrialIndexTiles -z 11,12 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_ThreatsIndexTiles -z 11,12 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_PopDensityIndexTiles -z 11,12 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
```

### from seed server seed all level 13 tiles if you do too many you will get timeouts. starting at these zoom levels try not do all of them and -d option with limit shapefile is important for reducing blank images, we will remove blanks (completely transparent) latter.
We only do hubs, exposure, assets, threats to zoom level 13 to space and time. for the most part the data does not support the precsion of zoom level 13.
```bsh
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_AssetsIndexTiles -z 13,13 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_CombinedWildlifeIndexTiles -z 13,13 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_CriticalFacilitiesIndexTiles -z 13,13 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_CriticalInfrastructureIndexTiles -z 13,13 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_ExposureIndexTiles -z 13,13 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_ErosionIndexTiles -z 13,13 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_FloodProneAreasIndexTiles -z 13,13 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_DraingeIndexTiles -z 13,13 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_LandslideIndexTiles -z 13,13 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_SlopeIndexTiles -z 13,13 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_AquaticIndexTiles -z 13,13 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_SLRIndexTiles -z 13,13 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_SocVulnIndexTiles -z 13,13 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_StormSurgeIndexTiles -z 13,13 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_TerrestrialIndexTiles -z 13,13 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_ThreatsIndexTiles -z 13,13 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_TsunamiIndexTiles -z 13,13 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_PopDensityIndexTiles -z 13,13 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
```

#### US Virgin Islands zoom level 13
```bsh
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_AssetsIndexTiles -z 13,13 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_CombinedWildlifeIndexTiles -z 13,13 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_CriticalFacilitiesIndexTiles -z 13,13 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_CriticalInfrastructureIndexTiles -z 13,13 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_ExposureIndexTiles -z 13,13 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_ErosionIndexTiles -z 13,13 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_FloodProneAreasIndexTiles -z 13,13 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_DraingeIndexTiles -z 13,13 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_SlopeIndexTiles -z 13,13 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_AquaticIndexTiles -z 13,13 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_SLRIndexTiles -z 13,13 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_SocVulnIndexTiles -z 13,13 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_StormSurgeIndexTiles -z 13,13 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_TerrestrialIndexTiles -z 13,13 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_ThreatsIndexTiles -z 13,13 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_PopDensityIndexTiles -z 13,13 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
```

DO I NEED ZOOM 14?
### Do not do zoom level 14 for most CONUS layes it is not needed and will triple the space 100gb instead of the current 500mb. We don't zoom to that level in the viewer anyway and the data does not support that level of percsion in CONUS, islands however are small enough that its needed.
```bsh
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_AssetsIndexTiles -z 14,14 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_CombinedWildlifeIndexTiles -z 14,14 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_CriticalFacilitiesIndexTiles -z 14,14 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_CriticalInfrastructureIndexTiles -z 14,14 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_ExposureIndexTiles -z 14,14 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_ErosionIndexTiles -z 14,14 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_FloodProneAreasIndexTiles -z 14,14 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_DraingeIndexTiles -z 14,14 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_LandslideIndexTiles -z 14,14 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_SlopeIndexTiles -z 14,14 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_AquaticIndexTiles -z 14,14 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_SLRIndexTiles -z 14,14 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_SocVulnIndexTiles -z 14,14 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_StormSurgeIndexTiles -z 14,14 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_TerrestrialIndexTiles -z 14,14 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_ThreatsIndexTiles -z 14,14 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_TsunamiIndexTiles -z 14,14 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-pr.xml -t PR_PopDensityIndexTiles -z 14,14 -n 4 -d  /tiledata/source/PR_CREST_Clipping_Boundary_3857.shp &
```

#### US Virgin Islands zoom level 14
```bsh
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_AssetsIndexTiles -z 14,14 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_CombinedWildlifeIndexTiles -z 14,14 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_CriticalFacilitiesIndexTiles -z 14,14 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_CriticalInfrastructureIndexTiles -z 14,14 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_ExposureIndexTiles -z 14,14 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_ErosionIndexTiles -z 14,14 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_FloodProneAreasIndexTiles -z 14,14 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_DraingeIndexTiles -z 14,14 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_SlopeIndexTiles -z 14,14 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_AquaticIndexTiles -z 14,14 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_SLRIndexTiles -z 14,14 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_SocVulnIndexTiles -z 14,14 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_StormSurgeIndexTiles -z 14,14 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_TerrestrialIndexTiles -z 14,14 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_ThreatsIndexTiles -z 14,14 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-usvi.xml -t USVI_PopDensityIndexTiles -z 14,14 -n 4 -d  /tiledata/source/USVI_CREST_Clipping_Boundary_3857.shp &
```

### CONUS  examples zoom level 1-10
```bsh
mapcache_seed -c /var/www/html/mapcache/mapcache-conus.xml -t CombinedWildlifeIndexTiles -z 1,10 -n 4 -d /usa_coastal_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-conus.xml -t CombinedWildlifeIndexTiles -z 11,12 -n 4 -d /usa_coastal_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache-conus.xml -t CombinedWildlifeIndexTiles -z 13,13 -n 4 -d /usa_coastal_3857.shp &
```

### CONUS nature serve examples zoom level 1-10
```bsh
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t TargetedWatershedAssetTiles -z 1,10 -n 4 -d /targeted_watersheds.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t TargetedWatershedThreatTiles -z 1,10 -n 4 -d /targeted_watersheds.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t TargetedWatershedFishandWildlifeTiles -z 1,10 -n 4 -d /targeted_watersheds.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t TargetedWatershedExposureTiles -z 1,10 -n 4 -d /targeted_watersheds.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t TargetedWatershedHubsTiles -z 1,10 -n 4 -d /targeted_watersheds.shp &
```

### CONUS nature serve  examples zoom level 11-12
```bsh
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t TargetedWatershedAssetTiles -z 11,12 -n 4 -d /targeted_watersheds.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t TargetedWatershedThreatTiles -z 11,12 -n 4 -d /targeted_watersheds.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t TargetedWatershedFishandWildlifeTiles -z 11,12 -n 4 -d /targeted_watersheds.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t TargetedWatershedExposureTiles -z 11,12 -n 4 -d /targeted_watersheds.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t TargetedWatershedHubsTiles -z 11,12 -n 4 -d /targeted_watersheds.shp &
```

### CONUS nature serve examples zoom level 13-13 not all layers need zoom level 13 for conus. Only doing main layers not using
```bsh
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t TargetedWatershedAssetTiles -z 13,13 -n 4 -d /targeted_watersheds.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t TargetedWatershedThreatTiles -z 13,13 -n 4 -d /targeted_watersheds.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t TargetedWatershedFishandWildlifeTiles -z 13,13 -n 4 -d /targeted_watersheds.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t TargetedWatershedExposureTiles -z 13,13 -n 4 -d /targeted_watersheds.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t TargetedWatershedHubsTiles -z 13,13 -n 4 -d /targeted_watersheds.shp &
```

### CONUS nature serve examples of how to delete blank images, the tile creation creates a lot of blank complete transparent images.  The tile website only needs one this significantly reduces the files of the tiles.
### this use the gdal and python container
```bsh
docker run -it -v /tiledata/cache:/cache gdal-python bash
cd cache
./deletetransparenttiles.py TargetedWatershedFishandWildlifeTiles &
./deletetransparenttiles.py TargetedWatershedAssetTiles &
./deletetransparenttiles.py TargetedWatershedThreatTiles &
./deletetransparenttiles.py TargetedWatershedExposureTiles &
./deletetransparenttiles.py TargetedWatershedHubsTiles &
./deletetransparenttiles.py CombinedWildlifeIndexTiles &

./deletetransparenttiles.py PR_AquaticIndexTiles &
./deletetransparenttiles.py PR_AssetsIndexTiles &
./deletetransparenttiles.py PR_CombinedWildlifeIndexTiles &
./deletetransparenttiles.py PR_CriticalFacilitiesIndexTiles &
./deletetransparenttiles.py PR_CriticalInfrastructureIndexTiles &
./deletetransparenttiles.py PR_DraingeIndexTiles &
./deletetransparenttiles.py PR_AquaticIndexTiles &
./deletetransparenttiles.py PR_ErosionIndexTiles &
./deletetransparenttiles.py PR_ExposureIndexTiles &
./deletetransparenttiles.py PR_FloodProneAreasIndexTiles &
./deletetransparenttiles.py PR_PopDensityIndexTiles &
./deletetransparenttiles.py PR_SLRIndexTiles &
./deletetransparenttiles.py PR_SlopeIndexTiles &
./deletetransparenttiles.py PR_SocVulnIndexTiles &
./deletetransparenttiles.py PR_StormSurgeIndexTiles &
./deletetransparenttiles.py PR_TerrestrialIndexTiles &
./deletetransparenttiles.py PR_ThreatsIndexTiles &
./deletetransparenttiles.py PR_LandslideIndexTiles &
./deletetransparenttiles.py PR_TsunamiIndexTiles &

./deletetransparenttiles.py USVI_AquaticIndexTiles &
./deletetransparenttiles.py USVI_AssetsIndexTiles &
./deletetransparenttiles.py USVI_CombinedWildlifeIndexTiles &
./deletetransparenttiles.py USVI_CriticalFacilitiesIndexTiles &
./deletetransparenttiles.py USVI_CriticalInfrastructureIndexTiles &
./deletetransparenttiles.py USVI_DraingeIndexTiles &
./deletetransparenttiles.py USVI_AquaticIndexTiles &
./deletetransparenttiles.py USVI_ErosionIndexTiles &
./deletetransparenttiles.py USVI_ExposureIndexTiles &
./deletetransparenttiles.py USVI_FloodProneAreasIndexTiles &
./deletetransparenttiles.py USVI_PopDensityIndexTiles &
./deletetransparenttiles.py USVI_SLRIndexTiles &
./deletetransparenttiles.py USVI_SlopeIndexTiles &
./deletetransparenttiles.py USVI_SocVulnIndexTiles &
./deletetransparenttiles.py USVI_StormSurgeIndexTiles &
./deletetransparenttiles.py USVI_TerrestrialIndexTiles &
./deletetransparenttiles.py USVI_ThreatsIndexTiles &

```

### CONUS nature serve examples of syncing the tiles to s3
from main aws instance Not any of the docker images, delete old tiles if needed and also don't forget to for aws to refresh the could front so the tiles and caches are refreshed immediately.
```bsh
cd /tiledata/cache
aws s3 sync TargetedWatershedFishandWildlifeTiles/ s3://tiles.resilientcoasts.org/TargetedWatershedFishandWildlifeTiles  --acl public-read &
aws s3 sync TargetedWatershedAssetTiles/ s3://tiles.resilientcoasts.org/TargetedWatershedAssetTiles  --acl public-read &
aws s3 sync TargetedWatershedThreatTiles/ s3://tiles.resilientcoasts.org/TargetedWatershedThreatTiles  --acl public-read &
aws s3 sync TargetedWatershedExposureTiles/ s3://tiles.resilientcoasts.org/TargetedWatershedExposureTiles  --acl public-read &
aws s3 sync TargetedWatershedHubsTiles/ s3://tiles.resilientcoasts.org/TargetedWatershedHubsTiles  --acl public-read &

aws s3 sync CombinedWildlifeIndexTiles/ s3://tiles.resilientcoasts.org/CombinedWildlifeIndexTiles  --acl public-read &


aws s3 rm s3://tiles.resilientcoasts.org/PR_AquaticIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/PR_AssetsIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/PR_CombinedWildlifeIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/PR_CriticalFacilitiesIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/PR_CriticalInfrastructureIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/PR_DraingeIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/PR_AquaticIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/PR_ErosionIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/PR_ExposureIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/PR_FloodProneAreasIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/PR_PopDensityIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/PR_SLRIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/PR_SlopeIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/PR_SocVulnIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/PR_StormSurgeIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/PR_TerrestrialIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/PR_ThreatsIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/PR_LandslideIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/PR_TsunamiIndexTiles --recursive --exclude "" &

aws s3 rm s3://tiles.resilientcoasts.org/USVI_AquaticIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/USVI_AssetsIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/USVI_CombinedWildlifeIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/USVI_CriticalFacilitiesIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/USVI_CriticalInfrastructureIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/USVI_DraingeIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/USVI_AquaticIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/USVI_ErosionIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/USVI_ExposureIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/USVI_FloodProneAreasIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/USVI_PopDensityIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/USVI_SLRIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/USVI_SlopeIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/USVI_SocVulnIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/USVI_StormSurgeIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/USVI_TerrestrialIndexTiles --recursive --exclude "" &
aws s3 rm s3://tiles.resilientcoasts.org/USVI_ThreatsIndexTiles --recursive --exclude "" &

aws s3 sync PR_AquaticIndexTiles/ s3://tiles.resilientcoasts.org/PR_AquaticIndexTiles --acl public-read &
aws s3 sync PR_AssetsIndexTiles/ s3://tiles.resilientcoasts.org/PR_AssetsIndexTiles --acl public-read &
aws s3 sync PR_CombinedWildlifeIndexTiles/ s3://tiles.resilientcoasts.org/PR_CombinedWildlifeIndexTiles --acl public-read &
aws s3 sync PR_CriticalFacilitiesIndexTiles/ s3://tiles.resilientcoasts.org/PR_CriticalFacilitiesIndexTiles --acl public-read &
aws s3 sync PR_CriticalInfrastructureIndexTiles/ s3://tiles.resilientcoasts.org/PR_CriticalInfrastructureIndexTiles --acl public-read &
aws s3 sync PR_DraingeIndexTiles/ s3://tiles.resilientcoasts.org/PR_DraingeIndexTiles --acl public-read &
aws s3 sync PR_AquaticIndexTiles/ s3://tiles.resilientcoasts.org/PR_AquaticIndexTiles --acl public-read &
aws s3 sync PR_ErosionIndexTiles/ s3://tiles.resilientcoasts.org/PR_ErosionIndexTiles --acl public-read &
aws s3 sync PR_ExposureIndexTiles/ s3://tiles.resilientcoasts.org/PR_ExposureIndexTiles --acl public-read &
aws s3 sync PR_FloodProneAreasIndexTiles/ s3://tiles.resilientcoasts.org/PR_FloodProneAreasIndexTiles --acl public-read &
aws s3 sync PR_PopDensityIndexTiles/ s3://tiles.resilientcoasts.org/PR_PopDensityIndexTiles --acl public-read &
aws s3 sync PR_SLRIndexTiles/ s3://tiles.resilientcoasts.org/PR_SLRIndexTiles --acl public-read &
aws s3 sync PR_SlopeIndexTiles/ s3://tiles.resilientcoasts.org/PR_SlopeIndexTiles --acl public-read &
aws s3 sync PR_SocVulnIndexTiles/ s3://tiles.resilientcoasts.org/PR_SocVulnIndexTiles --acl public-read &
aws s3 sync PR_StormSurgeIndexTiles/ s3://tiles.resilientcoasts.org/PR_StormSurgeIndexTiles --acl public-read &
aws s3 sync PR_TerrestrialIndexTiles/ s3://tiles.resilientcoasts.org/PR_TerrestrialIndexTiles --acl public-read &
aws s3 sync PR_ThreatsIndexTiles/ s3://tiles.resilientcoasts.org/PR_ThreatsIndexTiles --acl public-read &
aws s3 sync PR_LandslideIndexTiles/ s3://tiles.resilientcoasts.org/PR_LandslideIndexTiles --acl public-read &
aws s3 sync PR_TsunamiIndexTiles/ s3://tiles.resilientcoasts.org/PR_TsunamiIndexTiles --acl public-read &

aws s3 sync USVI_AquaticIndexTiles/ s3://tiles.resilientcoasts.org/USVI_AquaticIndexTiles --acl public-read &
aws s3 sync USVI_AssetsIndexTiles/ s3://tiles.resilientcoasts.org/USVI_AssetsIndexTiles --acl public-read &
aws s3 sync USVI_CombinedWildlifeIndexTiles/ s3://tiles.resilientcoasts.org/USVI_CombinedWildlifeIndexTiles --acl public-read &
aws s3 sync USVI_CriticalFacilitiesIndexTiles/ s3://tiles.resilientcoasts.org/USVI_CriticalFacilitiesIndexTiles --acl public-read &
aws s3 sync USVI_CriticalInfrastructureIndexTiles/ s3://tiles.resilientcoasts.org/USVI_CriticalInfrastructureIndexTiles --acl public-read &
aws s3 sync USVI_DraingeIndexTiles/ s3://tiles.resilientcoasts.org/USVI_DraingeIndexTiles --acl public-read &
aws s3 sync USVI_AquaticIndexTiles/ s3://tiles.resilientcoasts.org/USVI_AquaticIndexTiles --acl public-read &
aws s3 sync USVI_ErosionIndexTiles/ s3://tiles.resilientcoasts.org/USVI_ErosionIndexTiles --acl public-read &
aws s3 sync USVI_ExposureIndexTiles/ s3://tiles.resilientcoasts.org/USVI_ExposureIndexTiles --acl public-read &
aws s3 sync USVI_FloodProneAreasIndexTiles/ s3://tiles.resilientcoasts.org/USVI_FloodProneAreasIndexTiles --acl public-read &
aws s3 sync USVI_PopDensityIndexTiles/ s3://tiles.resilientcoasts.org/USVI_PopDensityIndexTiles --acl public-read &
aws s3 sync USVI_SLRIndexTiles/ s3://tiles.resilientcoasts.org/USVI_SLRIndexTiles --acl public-read &
aws s3 sync USVI_SlopeIndexTiles/ s3://tiles.resilientcoasts.org/USVI_SlopeIndexTiles --acl public-read &
aws s3 sync USVI_SocVulnIndexTiles/ s3://tiles.resilientcoasts.org/USVI_SocVulnIndexTiles --acl public-read &
aws s3 sync USVI_StormSurgeIndexTiles/ s3://tiles.resilientcoasts.org/USVI_StormSurgeIndexTiles --acl public-read &
aws s3 sync USVI_TerrestrialIndexTiles/ s3://tiles.resilientcoasts.org/USVI_TerrestrialIndexTiles --acl public-read &
aws s3 sync USVI_ThreatsIndexTiles/ s3://tiles.resilientcoasts.org/USVI_ThreatsIndexTiles --acl public-read &

aws cloudfront create-invalidation --distribution-id E34VC6CQ814IM --paths '/*'  
```

### CONUS nature serve examples of coping zipped data for s3 download
```bsh
aws s3 cp TargetedWatershedAsset8.zip   s3://nfwf-tool/nfwf_download_data/TargetedWatershedAsset8.zip --acl public-read &
aws s3 cp TargetedWatershedExposure8.zip   s3://nfwf-tool/nfwf_download_data/TargetedWatershedExposure8.zip --acl public-read &
aws s3 cp TargetedWatershedFishandWildlife8.zip   s3://nfwf-tool/nfwf_download_data/TargetedWatershedFishandWildlife8.zip --acl public-read &
aws s3 cp TargetedWatershedThreat8.zip   s3://nfwf-tool/nfwf_download_data/TargetedWatershedThreat8.zip --acl public-read &
aws s3 cp TargetedWatershedHubs8.zip   s3://nfwf-tool/nfwf_download_data/TargetedWatershedHubs8.zip --acl public-read &
```


### CONUS  examples of coping of seeding tiles by layer,use line breaks to break the tile creation into chunks. CONUS is very geographically large and take days to create. doing to many can cause timeout issues.
```bsh
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t ThreatsIndexTiles -z 1,10 -n 4 -d /usa_coastal_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t ThreatsIndexTiles -z 11,12 -n 4 -d /usa_coastal_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t ThreatsIndexTiles -z 13,13 -n 4 -d /usa_coastal_3857.shp &

mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t ExposureIndexTiles -z 1,10 -n 4 -d /usa_coastal_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t ExposureIndexTiles -z 11,12 -n 4 -d /usa_coastal_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t ExposureIndexTiles -z 13,13 -n 4 -d /usa_coastal_3857.shp &


mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t TerrestrialIndexTiles -z 1,10 -n 4 -d /usa_coastal_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t TerrestrialIndexTiles -z 11,12 -n 4 -d /usa_coastal_3857.shp &

mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t AquaticIndexTiles -z 1,10 -n 4 -d /usa_coastal_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t AquaticIndexTiles -z 11,12 -n 4 -d /usa_coastal_3857.shp &

mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t SlopeIndexTiles -z 1,10 -n 4 -d /usa_coastal_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t SlopeIndexTiles -z 11,12 -n 4 -d /usa_coastal_3857.shp &

mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t SocVulnIndexTiles -z 1,10 -n 4 -d /usa_coastal_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t SocVulnIndexTiles -z 11,12 -n 4 -d /usa_coastal_3857.shp &

mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t DraingeIndexTiles -z 1,10 -n 4 -d /usa_coastal_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t DraingeIndexTiles -z 11,12 -n 4 -d /usa_coastal_3857.shp &

mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t ErosionIndexTiles -z 1,10 -n 4 -d /usa_coastal_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t ErosionIndexTiles -z 11,12 -n 4 -d /usa_coastal_3857.shp &

mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t FloodProneAreasIndexTiles -z 1,10 -n 4 -d /usa_coastal_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t FloodProneAreasIndexTiles -z 11,12 -n 4 -d /usa_coastal_3857.shp &

mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t GeoStressIndexTiles -z 1,10 -n 4 -d /usa_coastal_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t GeoStressIndexTiles -z 11,12 -n 4 -d /usa_coastal_3857.shp &

mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t PopDensityIndexTiles -z 1,10 -n 4 -d /usa_coastal_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t PopDensityIndexTiles -z 11,12 -n 4 -d /usa_coastal_3857.shp &

mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t CriticalFacilitiesIndexTiles -z 1,10 -n 4 -d /usa_coastal_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t CriticalFacilitiesIndexTiles -z 11,12 -n 4 -d /usa_coastal_3857.shp &

mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t CriticalInfrastructureIndexTiles -z 1,10 -n 4 -d /usa_coastal_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t CriticalInfrastructureIndexTiles -z 11,12 -n 4 -d /usa_coastal_3857.shp &


mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t SLRIndexTiles -z 1,10 -n 4 -d /usa_coastal_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t SLRIndexTiles -z 11,12 -n 4 -d /usa_coastal_3857.shp &

mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t StormSurgeIndexTiles -z 1,10 -n 4 -d /usa_coastal_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t StormSurgeIndexTiles -z 11,12 -n 4 -d /usa_coastal_3857.shp &

mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t HubsIndexTiles -z 1,10 -n 4 -d /usa_coastal_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t HubsIndexTiles -z 11,12 -n 4 -d /usa_coastal_3857.shp &
mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t HubsIndexTiles -z 13,13 -n 4 -d /usa_coastal_3857.shp &
```


### CONUS examples of how to delete blank images, the tile creation creates a lot of blank complete transparent images.  The tile website only needs one this significantly reduces the files of the tiles.
```bsh
docker run -it -v /tiledata/cache:/cache gdal-python bash
./deletetransparenttiles.py AssetsIndexTiles &
./deletetransparenttiles.py ThreatsIndexTiles &
./deletetransparenttiles.py ExposureIndexTiles &
./deletetransparenttiles.py TerrestrialIndexTiles &
./deletetransparenttiles.py AquaticIndexTiles &
./deletetransparenttiles.py CriticalFacilitiesIndexTiles/ &
./deletetransparenttiles.py CriticalInfrastructureIndexTiles/ &
./deletetransparenttiles.py PopDensityIndexTiles/ &
./deletetransparenttiles.py SocVulnIndexTiles/ &
./deletetransparenttiles.py DraingeIndexTiles/ &
./deletetransparenttiles.py ErosionIndexTiles/ &
./deletetransparenttiles.py FloodProneAreasIndexTiles/ &
./deletetransparenttiles.py GeoStressIndexTiles/ &
./deletetransparenttiles.py SLRIndexTiles/ &
./deletetransparenttiles.py SlopeIndexTiles/ &
./deletetransparenttiles.py FloodProneAreasIndexTiles/ &
./deletetransparenttiles.py StormSurgeIndexTiles/ &
```
### CONUS examples of syncing the tiles to s3
```bsh
aws s3 sync AssetsIndexTiles s3://tiles.resilientcoasts.org/AssetsIndexTiles  --acl public-read &
aws s3 sync AquaticIndexTiles s3://tiles.resilientcoasts.org/AquaticIndexTiles --acl public-read &
aws s3 sync CriticalFacilitiesIndexTiles/ s3://tiles.resilientcoasts.org/CriticalFacilitiesIndexTiles  --acl public-read  &
aws s3 sync CriticalInfrastructureIndexTiles/ s3://tiles.resilientcoasts.org/CriticalInfrastructureIndexTiles  --acl public-read &
aws s3 sync DraingeIndexTiles/ s3://tiles.resilientcoasts.org/DraingeIndexTiles  --acl public-read &
aws s3 sync ExposureIndexTiles s3://tiles.resilientcoasts.org/ExposureIndexTiles  --acl public-read &
aws s3 sync ErosionIndexTiles/ s3://tiles.resilientcoasts.org/ErosionIndexTiles  --acl public-read &
aws s3 sync FloodProneAreasIndexTiles/ s3://tiles.resilientcoasts.org/FloodProneAreasIndexTiles  --acl public-read &
aws s3 sync GeoStressIndexTiles/ s3://tiles.resilientcoasts.org/GeoStressIndexTiles  --acl public-read &
aws s3 sync PopDensityIndexTiles/ s3://tiles.resilientcoasts.org/PopDensityIndexTiles  --acl public-read &
aws s3 sync SLRIndexTiles/ s3://tiles.resilientcoasts.org/SLRIndexTiles  --acl public-read &
aws s3 sync SlopeIndexTiles/ s3://tiles.resilientcoasts.org/SlopeIndexTiles  --acl public-read &
aws s3 sync SocVulnIndexTiles/ s3://tiles.resilientcoasts.org/SocVulnIndexTiles  --acl public-read &
aws s3 sync StormSurgeIndexTiles/ s3://tiles.resilientcoasts.org/StormSurgeIndexTiles  --acl public-read &
aws s3 sync TerrestrialIndexTiles s3://tiles.resilientcoasts.org/TerrestrialIndexTiles  --acl public-read &
aws s3 sync ThreatsIndexTiles s3://tiles.resilientcoasts.org/ThreatsIndexTiles  --acl public-read &
```

### copy the tiles locally if you want them, run from local machine not AWS instance
```bsh
scp -i [YOUR PEM FILE] ec2-user@ec2-3-86-102-181.compute-1.amazonaws.com:/tiledata/cache/PRExposureIndexTiles/ .
```

### CONUS  examples of coping zipped data for s3 download
```bsh
aws s3 cp nfwf_conus_asset.zip s3://nfwf-tool/nfwf_download_data/ --acl public-read &
aws s3 cp nfwf_conus_asset_criticalfacilities_inputs.zip s3://nfwf-tool/nfwf_download_data/ --acl public-read &
aws s3 cp nfwf_conus_asset_criticalinfrastructure_inputs.zip s3://nfwf-tool/nfwf_download_data/ --acl public-read &
aws s3 cp nfwf_conus_asset_populationdensity_inputs.zip s3://nfwf-tool/nfwf_download_data/ --acl public-read &
aws s3 cp nfwf_conus_asset_socialvulnerability_inputs.zip s3://nfwf-tool/nfwf_download_data/ --acl public-read &
aws s3 cp nfwf_conus_threat.zip s3://nfwf-tool/nfwf_download_data/ --acl public-read &
aws s3 cp nfwf_conus_threat_drainage.zip s3://nfwf-tool/nfwf_download_data/ --acl public-read &
aws s3 cp nfwf_conus_threat_erosion.zip s3://nfwf-tool/nfwf_download_data/ --acl public-read &
aws s3 cp nfwf_conus_threat_floodproneareas.zip s3://nfwf-tool/nfwf_download_data/ --acl public-read &
aws s3 cp nfwf_conus_threat_geostress.zip s3://nfwf-tool/nfwf_download_data/ --acl public-read &
aws s3 cp nfwf_conus_threat_sealevelrise.zip s3://nfwf-tool/nfwf_download_data/ --acl public-read &
aws s3 cp nfwf_conus_threat_slope.zip s3://nfwf-tool/nfwf_download_data/ --acl public-read &
aws s3 cp nfwf_conus_threat_stormsurge.zip s3://nfwf-tool/nfwf_download_data/ --acl public-read &
aws s3 cp nfwf_conus_exposure.zip s3://nfwf-tool/nfwf_download_data/ --acl public-read &
aws s3 cp nfwf_conus_aquatic.zip s3://nfwf-tool/nfwf_download_data/ --acl public-read &
aws s3 cp nfwf_conus_terrestrial.zip s3://nfwf-tool/nfwf_download_data/ --acl public-read &
aws s3 cp nfwf_conus_resiliencehubs.zip s3://nfwf-tool/nfwf_download_data/ --acl public-read &
```
