<script setup>
    import "leaflet/dist/leaflet.js"
    import "leaflet/dist/leaflet.css"
    import { onMounted } from "vue";
    import axios from 'axios'

    let locations = []

    let stations = []

    let path = []

    let dijkstraPointsCoordinates = {}

    


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
                    stop_name: element.stop_name
                }
                stations.push(obj)
            }
        })
        .finally(function(){
            for (let index = 0; index < path.length; index++) {
                const element1 = path[index];
                for (let index = 0; index < stations.length; index++) {
                    const element2 = stations[index];
                    if (element2.id === element1) {
                        const obj = {
                            id: element2.id,
                            lat: element2.lat,
                            lon: element2.lon,
                            title: element2.stop_name
                        }
                        locations.push(obj)
                    }
                }
                
            }
            const map = L.map('map').setView([48.86285403569893, 2.3448491571643038], 13);
            L.tileLayer('https://tile.jawg.io/5eafae32-aa5a-47da-a62c-ad2c1ab57fc3/{z}/{x}/{y}{r}.png?access-token=7CazPEKT76Mh5MSYbVWhLsP50NvaNbsBSbtEu3buIa0KijexNhx58EbJzu5dZ8Ox', {
            attribution: '<a href="https://jawg.io" title="Tiles Courtesy of Jawg Maps" target="_blank">&copy; <b>Jawg</b>Maps</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            minZoom: 0,
            maxZoom: 22,
            }).addTo(map);
            for (let index = 0; index < locations.length; index++) {
                const element = locations[index];
                L.marker([element.lat, element.lon]).bindPopup(element.title).addTo(map);    
            }
            locations.forEach(point => {
                dijkstraPointsCoordinates[point.id] = [point.lat, point.lon]
            })
            let latlon = path.map(id => dijkstraPointsCoordinates[id])
            const polyline = L.polyline(latlon, {
            color: 'red',    
            weight: 4,         
            opacity: 0.8       
            }).addTo(map);
            console.log(stations)
        })

        axios.get('https://backend-ot44.onrender.com/dijkstra/171/285')
        .then(function (response) {
            console.log('Hello you must check here ', response.data)
            const data = response.data.path
            for (const key in data) {
                if (Object.prototype.hasOwnProperty.call(data, key)) {
                    const element = data[key];
                    path.push(element)
                }
            }
        })
    }
)

    const props = defineProps(
        {
            concorde: String
        }
    )
console.log(locations)
console.log(path)

// console.log(`List of stations is ${stations}`)
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