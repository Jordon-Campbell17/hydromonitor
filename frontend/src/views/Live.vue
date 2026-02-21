<template>
  <v-container fluid bg-color="surface">
    <v-row style="max-width:1200px" justify="start">
      <v-col cols="9">
        <figure class="highcharts-figure">
          <div id="container"></div>
        </figure>
      </v-col>
      <v-col cols="3">
        <v-card color="primaryContainer" max-width="500" mb-5>
          <v-card-subtitle>Temperature</v-card-subtitle>
          <v-card-item>
            <span class="text-h3 text-onPrimaryContainer">{{ temperature }}</span>
          </v-card-item>
        </v-card>
        <v-card color="tertiaryContainer" max-width="500" mb-5>
          <v-card-subtitle>Heat Index (Feels like)</v-card-subtitle>
          <v-card-item>
            <span class="text-h3 text-onTertiaryContainer">{{ heatindex }}</span>
          </v-card-item>
        </v-card>
        <v-card color="secondaryContainer" max-width="500" mb-5>
          <v-card-subtitle>Humidity</v-card-subtitle>
          <v-card-item>
            <span class="text-h3 text-onSecondaryContainer">{{ humidity }}</span>
          </v-card-item>
        </v-card>
      </v-col>
    </v-row>
    <v-row style="max-width:1200px" justify="start">
      <v-col cols="9">
        <figure class="highcharts-figure">
          <div id="container1"></div>
        </figure>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch, computed } from 'vue';
import { useMqttStore } from '@/store/mqttStore';
import { storeToRefs } from 'pinia';

import Highcharts from 'highcharts';
import more from 'highcharts/highcharts-more';
import Exporting from 'highcharts/modules/exporting';
Exporting(Highcharts);
more(Highcharts);

// MQTT
const Mqtt = useMqttStore();
const { payload, payloadTopic } = storeToRefs(Mqtt);

// CHART OBJECTS
const tempHiChart = ref(null);
const humidChart  = ref(null);

// LIVE GRAPH CONTROLS
const points = ref(10);
const shift  = ref(false);
const points2 = ref(10);
const shift2  = ref(false);

// FUNCTIONS
const CreateCharts = async () => {
  tempHiChart.value = Highcharts.chart('container', {
    chart: { zoomType: 'x' },
    title: { text: 'Temperature Analysis (Live)', align: 'left' },
    yAxis: {
      title: { text: 'Air Temperature & Heat Index', style: { color: '#000000' } },
      labels: { format: '{value} °C' }
    },
    xAxis: {
      type: 'datetime',
      title: { text: 'Time', style: { color: '#000000' } }
    },
    tooltip: { shared: true },
    series: [
      { name: 'Temperature', type: 'spline', data: [], turboThreshold: 0, color: Highcharts.getOptions().colors[0] },
      { name: 'Heat Index',  type: 'spline', data: [], turboThreshold: 0, color: Highcharts.getOptions().colors[1] }
    ]
  });

  humidChart.value = Highcharts.chart('container1', {
    chart: { zoomType: 'x' },
    title: { text: 'Humidity Analysis (Live)', align: 'left' },
    yAxis: {
      title: { text: 'Humidity', style: { color: '#000000' } },
      labels: { format: '{value} %' }
    },
    xAxis: {
      type: 'datetime',
      title: { text: 'Time', style: { color: '#000000' } }
    },
    tooltip: { shared: true },
    series: [
      { name: 'Humidity', type: 'spline', data: [], turboThreshold: 0, color: Highcharts.getOptions().colors[2] }
    ]
  });
};

// COMPUTED PROPERTIES
const temperature = computed(() => {
  if (!!payload.value) return `${payload.value.temperature.toFixed(2)} °C`;
});

const heatindex = computed(() => {
  if (!!payload.value) return `${payload.value.heatindex.toFixed(2)} °C`;
});

const humidity = computed(() => {
  if (!!payload.value) return `${payload.value.humidity.toFixed(2)} %`;
});

// WATCHERS
watch(payload, (data) => {
  if (points.value > 0) { points.value--; } else { shift.value = true; }
  tempHiChart.value.series[0].addPoint({ y: parseFloat(data.temperature.toFixed(2)), x: data.timestamp * 1000 }, true, shift.value);
  tempHiChart.value.series[1].addPoint({ y: parseFloat(data.heatindex.toFixed(2)),   x: data.timestamp * 1000 }, true, shift.value);

  if (points2.value > 0) { points2.value--; } else { shift2.value = true; }
  humidChart.value.series[0].addPoint({ y: parseFloat(data.humidity.toFixed(2)), x: data.timestamp * 1000 }, true, shift2.value);
});

onMounted(() => {
  CreateCharts();
  Mqtt.connect();
  setTimeout(() => {
    Mqtt.subscribe("620162191");
    Mqtt.subscribe("620162191_sub");
  }, 3000);
});

onBeforeUnmount(() => {
  Mqtt.unsubcribeAll();
});
</script>

<style>
figure {
  border: 2px solid black;
}
</style>