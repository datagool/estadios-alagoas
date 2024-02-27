<template>
  <div id="app">
   <h1>🏟️ Estádios de Futebol do estado de Alagoas</h1>

   <p>Em Alagoas há 63 estádios, sendo que, a maioria deles, pertencem aos municípios. 
    Dados oriundos do Instituto Brasileiro de Geografia e Estatística - IBGE.  Última alteração: 27/01/2023 22:04:06 </p>

   <p>Clique nos marcadores para ter mais informações.</p>

    <div id="map"></div>

    <transition name="fade">
      <div v-if="selectedLocalidade" class="modal-overlay">
        <div class="modal">
          <button @click="closeModal" class="close-button">&times;</button>
          <h2 class="modal-title">{{ selectedLocalidade.nome }}</h2>
          <div class="modal-content">
            <p>Endereço: {{ selectedLocalidade.endereco }}</p> 
            <p>Cidade: {{ selectedLocalidade.municipio }}</p>
            <p>Tipo de administração: {{ selectedLocalidade.administra }}</p>
            <div id="g-maps">
              <a :href="'https://www.google.com/maps?q=' + selectedLocalidade.latitude + ',' + selectedLocalidade.longitude"><img src="https://cdn-icons-png.flaticon.com/512/2991/2991231.png" /></a>
            </div>
           </div>     
         </div>
      </div>
    </transition>
  </div>
</template>

<script>
import axios from 'axios';
import mapboxgl from 'mapbox-gl';

export default {
  name: 'App',
  data() {
    return {
      localidades: [],
      selectedLocalidade: null
    }
  },
  mounted() {
    // Carrega o mapa	
    mapboxgl.accessToken = process.env.VUE_APP_MB_TK;
    var map = new mapboxgl.Map({
      container: 'map',
      style: 'mapbox://styles/mapbox/streets-v11', 
      center: [-36.49640267, -9.6483427],
      zoom: 6.5
    });
  
    map.addControl(new mapboxgl.NavigationControl());
    

    // Requisição para obter os dados das localidades
    axios.get('https://jogos.evertontenorio.tech/api/localidades')
      .then(response => {
        this.localidades = response.data;
        // Adiciona marcadores ao mapa para cada localidade
        this.localidades.forEach(localidade => {
          var marker = new mapboxgl.Marker()
            .setLngLat([localidade.longitude, localidade.latitude])
            .addTo(map);
          // Adiciona evento de clique para exibir informações sobre a localidade
          marker.getElement().addEventListener('click', () => {
            this.selectedLocalidade = localidade;
          });
        });
      })
      .catch(error => {
        console.error('Erro ao obter os dados das localidades:', error);
      });
  },
  methods: {
    closeModal() {
      this.selectedLocalidade = null;
    }
  }
}
</script>

<style>
#app {
  margin-top: 30px;
}
#map {
  height: 410px;
  width: 99%; 
  border: 2px solid red;
  border-radius: 5px;
  position: relative;
  z-index: 0;
}

#g-maps {
  position: relative; 
}

#g-maps img {
  width: 35px;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background-color: white;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  max-width: 70%;
  max-height: 70%;
  overflow-y: auto;
  text-align: left;
}

.modal-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: black;
}

.modal-content {
  color: black;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 4rem;
  color: white;
}

.close-button:hover {
  color: #555;
}


@media screen and (max-width: 767px) {
  #map{
    height: 326px;
  }
}
</style>
