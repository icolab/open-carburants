

stations <- read.csv2("stations.csv")

latitude_depart = 48.8254416
longitude_depart = 2.3665593

# Selection des stations les plus proches à vol d'oiseau
library(sqldf)
request = paste("SELECT * FROM stations WHERE printf(\"%.1f\", latitude) = printf(\"%.1f\",",
                latitude_depart,
                ") AND printf(\"%.1f\", longitude) = printf(\"%.1f\",",
                longitude_depart,
                ")")
nearest_stations = sqldf(request)

# Generation des requetes OSRM
osrm_queries = paste("http://151.80.46.129/viaroute?loc=",
                   latitude_depart,
                   ",",
                   longitude_depart,
                   "&loc=",
                   nearest_stations$latitude,
                   ",",
                   nearest_stations$longitude,
                   "&instructions=true",sep="")

# Requetes vers OSRM et stockage dans une liste
library(rjson)

routes <<- list()

f <- function(x) {
  route <- fromJSON(file=x, method='C')
  routes[[length(routes)+1]] <<- route
  print(x)
}

lapply(osrm_queries, f)




