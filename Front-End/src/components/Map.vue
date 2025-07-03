<script setup>
    import "leaflet/dist/leaflet.js"
    import "leaflet/dist/leaflet.css"
    import { onMounted } from "vue";
    import axios from 'axios'
    import { ref } from "vue";

    let locations = []

    let stations = []

    let path = []

    let dijkstraPointsCoordinates = {}

    let concreteData = []

    let realDijsktraLocations = []

    


    onMounted(() =>{

        axios.get('https://backend-ot44.onrender.com/stations')
        .then(function (response) {
            const data = response.data
            for (let index = 0; index < data.length; index++) {
                const element = data[index];
                const obj = {
                    id: element.id,
                    lat: element.lat,
                    lon: element.lon,
                    stop_name: element.stop_name,
                    line: element.line,
                    next_stop_id: element.next_stop_id,
                    previous_stop_id: element.prev_stop_id
                }
                stations.push(obj)
            }
        })
        .finally(function(){
            // for (let index = 0; index < path.length; index++) {
            //     const element1 = path[index];
            //     for (let index = 0; index < stations.length; index++) {
            //         const element2 = stations[index];
            //         if (element2.id === element1) {
            //             const obj = {
            //                 id: element2.id,
            //                 lat: element2.lat,
            //                 lon: element2.lon,
            //                 title: element2.stop_name
            //             }
            //             locations.push(obj)
            //         }
            //     }
                
            // }
            const map = L.map('map').setView([48.86285403569893, 2.3448491571643038], 13);
            L.tileLayer('https://tile.jawg.io/5eafae32-aa5a-47da-a62c-ad2c1ab57fc3/{z}/{x}/{y}{r}.png?access-token=7CazPEKT76Mh5MSYbVWhLsP50NvaNbsBSbtEu3buIa0KijexNhx58EbJzu5dZ8Ox', {
            attribution: '<a href="https://jawg.io" title="Tiles Courtesy of Jawg Maps" target="_blank">&copy; <b>Jawg</b>Maps</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            minZoom: 0,
            maxZoom: 22,
            }).addTo(map);
            // for (let index = 0; index < locations.length; index++) {
            //     const element = locations[index];
            //     L.marker([element.lat, element.lon]).bindPopup(element.title).addTo(map);    
            // }
            // locations.forEach(point => {
            //     dijkstraPointsCoordinates[point.id] = [point.lat, point.lon]
            // })
            // let latlon = path.map(id => dijkstraPointsCoordinates[id])
            // const polyline = L.polyline(latlon, {
            // color: 'red',    
            // weight: 4,         
            // opacity: 0.8       
            // }).addTo(map);
            axios.get('https://backend-ot44.onrender.com/dijkstra/171/285')
            .then(function (response) {
                const data = response.data.path
                for (const key in data) {
                    if (Object.prototype.hasOwnProperty.call(data, key)) {
                        const element = data[key];
                        path.push(element)
                    }
                }
            })
            .finally( function () {
                console.log(`This is the path : ${path}`)
                for (let index = 0; index < path.length; index++) {
                    const element1 = path[index];
                    for (let index = 0; index < stations.length; index++) {
                        const element2 = stations[index];
                        if (element1 === element2.id) {
                            concreteData.push(element2)
                        }
                    }
                }
                for (let pathIndex = 0; pathIndex < path.length; pathIndex++) {
                    const element1 = path[pathIndex];
                    console.log(`Path index : ${pathIndex}`)
                    console.log(`This is the reference : ${element1}`)
                    for (let dataIndex = 0; dataIndex < concreteData.length; dataIndex++) {
                        console.log(`Data index : ${dataIndex}`)
                        const element2 = concreteData[dataIndex];
                        console.log(element2)
                        console.log(`pathIndex+1 = ${path[pathIndex+1]}`)
                        if ( ((element2.id === element1) && (element2.next_stop_id === path[pathIndex+1])) || ((element2.id === element1) && (element2.previous_stop_id === path[pathIndex-1])) || ((element2.id === element1) && (element2.previous_stop_id === path[pathIndex+1])) || (element2.id === element1) && (element2.next_stop_id === path[pathIndex-1]) ) {
                            const obj = {
                                id: element2.id,
                                title: element2.stop_name,
                                line: element2.line,
                                lat: element2.lat,
                                lon: element2.lon,
                            }
                            console.log(obj)
                            console.log(`Object found at index : ${dataIndex}`)
                            realDijsktraLocations.push(obj)
                            break
                        }
                        else {
                            console.log('not selected')
                        }
                    }
                    
                    
                }
                for (let index = 0; index < realDijsktraLocations.length; index++) {
                        const element = realDijsktraLocations[index];
                        L.marker([element.lat, element.lon]).bindPopup(element.title + ' ' + element.line).addTo(map);    
                    }
                realDijsktraLocations.forEach(point => {
                        dijkstraPointsCoordinates[point.id] = [point.lat, point.lon]
                    })
                    let latlon = path.map(id => dijkstraPointsCoordinates[id])
                    console.log('My latlon', latlon)
                    const polyline = L.polyline(latlon, {
                        color: 'blue',
                        weight: 4,
                        opacity: 0.8
                    }).addTo(map)
                // for (let index = 0; index < realDijsktraLocations.length; index++) {
                //         const element = realDijsktraLocations[index];
                //         const obj = {
                //             lat: element.lat,
                //             lon: element.lon
                //         }
                //         tempList.push(obj)
                //     }
                        console.log(realDijsktraLocations)
                        console.log(concreteData)
                })
        })
    }
)

    const props = defineProps(
        {
            concorde: String
        }
    )

</script>


<template>

    <div id="map"></div>

</template>

<style scoped>

    #map { 
        width: 47vw ;
        height: 90vh;
        border-radius: 50px;
        margin-left: 36px;
        margin-top: 9px;
        box-shadow: 0px 0px 3px 2px rgba(54, 54, 54, 0.25);
        margin-top: 50px;
     }

</style>