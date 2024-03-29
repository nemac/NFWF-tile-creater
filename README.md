# NFWF-tile-creater
creates nfwf tms tiles from a docker map server test

use docker compose to start a mapserver server and mapcache seeder.

## build docker images
`docker build -t mapserver-image -f DockerfileMapserverCarto .`

`docker build -t mapcache-image -f DockerfileMapcache .`

`docker build -t gdal-image -f DockerfileGDAL .`

`docker build -t gdal-python -f DockerfileGDALPython .`

## turn on docker machines
starts two docker machine one is mapserver other is mapcache
`docker-compose up`

### place map file and associated Spatial files (shapefiles, rasters, etc) in the map directory
### update [mapcache.xml](mapcache-configs/mapcache.xml) for each region you should create a separate mapcache file for each region
### update [nfwf.map](map/nfwf.map) for each region pay attention to the projection for each tiff, and you should create a separate map file for each region

## run the seed for the levels you care about
example:
`mapcache_seed -c /var/www/html/mapcache/mapcache.xml -t HUbsIndexTiles -z 1,10 -n 4 -d /usa_coastal_3857.shp`

all caches are created in the cache folder with folder name = -t option in example HUbsIndexTiles get it from [mapcache.xml](mapcache-configs/mapcache.xml#L36) or update the mapcache.xml file.  This will need to be recopied from the docker container
`docker exec -it mapcache-compose bash`


the -d option will limit where tiles are created you will have to update the [DockerfileMapcache#L74-L77](DockerfileMapcache) file

# run python script to remove tiles that entirely transparent "blank".
this will cause some file missing errors in the browser but it will greatly reduce the size of cache for some layers...
`./deletetransparenttiles.py cache/the tileset name/`

copy the folder to s3, make it public and you have TMS tile server on s3


#making download zips
build the docker image
`docker build -t gdal-python -f DockerfileGDALPython .`

run docker and open bash
`docker run -it -v /tiledata/cache:/cache gdal-python bash`

run the zip creator script.  this may require some edits to output to the different directory
`./zipcreator.py`

copy to aws dataset_bucket
`aws s3 sync zips/ s3://nfwf-tool/nfwf_download_data --acl public-read --delete`
