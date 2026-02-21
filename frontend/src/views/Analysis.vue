<template>
  <v-container fluid bg-color="surface">

    <!-- ROW 1 -->
    <v-row style="max-width:1200px" class="pa-1">
      <v-col>
        <v-sheet class="pa-2" height="250">
          <p>Enter date range for Analysis</p>
          <v-divider></v-divider>
          <v-text-field label="Start date" type="date" density="compact" variant="solo-inverted" flat style="max-width:300px" class="mr-5" v-model="start"></v-text-field>
          <v-text-field label="End date"   type="date" density="compact" variant="solo-inverted" flat style="max-width:300px" v-model="end"></v-text-field>
          <v-spacer></v-spacer>
          <v-btn class="text-caption" text="Analyze" color="primary" variant="tonal"
            @click="updateLineCharts(); updateHumidityChart(); updateHistogramCharts(); updateScatterTemp(); updateScatterHumidity(); updateCards();">
          </v-btn>
        </v-sheet>
      </v-col>
      <v-col cols="3" align="center">
        <v-card title="Temperature" width="250" variant="outlined" color="primary" density="compact" rounded="lg">
          <v-card-item class="mb-n5">
            <v-chip-group class="d-flex flex-row justify-center" color="primaryContainer" variant="flat">
              <v-tooltip text="Min" location="start">
                <template v-slot:activator="{ props }"><v-chip v-bind="props">{{ temperature.min }}</v-chip></template>
              </v-tooltip>
              <v-tooltip text="Range" location="top">
                <template v-slot:activator="{ props }"><v-chip v-bind="props">{{ temperature.range }}</v-chip></template>
              </v-tooltip>
              <v-tooltip text="Max" location="end">
                <template v-slot:activator="{ props }"><v-chip v-bind="props">{{ temperature.max }}</v-chip></template>
              </v-tooltip>
            </v-chip-group>
          </v-card-item>
          <v-card-item align="center">
            <span class="text-h1 text-primary font-weight-bold">{{ temperature.avg }}</span>
          </v-card-item>
        </v-card>
      </v-col>
      <v-col cols="3" align="center">
        <v-card title="Humidity" width="250" variant="outlined" color="primary" density="compact" rounded="lg">
          <v-card-item class="mb-n5">
            <v-chip-group class="d-flex flex-row justify-center" color="primaryContainer" variant="flat">
              <v-tooltip text="Min" location="start">
                <template v-slot:activator="{ props }"><v-chip v-bind="props">{{ humidity.min }}</v-chip></template>
              </v-tooltip>
              <v-tooltip text="Range" location="top">
                <template v-slot:activator="{ props }"><v-chip v-bind="props">{{ humidity.range }}</v-chip></template>
              </v-tooltip>
              <v-tooltip text="Max" location="end">
                <template v-slot:activator="{ props }"><v-chip v-bind="props">{{ humidity.max }}</v-chip></template>
              </v-tooltip>
            </v-chip-group>
          </v-card-item>
          <v-card-item align="center">
            <span class="text-h1 text-primary font-weight-bold">{{ humidity.avg }}</span>
          </v-card-item>
        </v-card>
      </v-col>
    </v-row>

    <!-- ROW 2 -->
    <v-row style="max-width:1200px">
      <v-col cols="12">
        <figure class="highcharts-figure"><div id="container"></div></figure>
      </v-col>
      <v-col cols="12">
        <figure class="highcharts-figure"><div id="container0"></div></figure>
      </v-col>
    </v-row>

    <!-- ROW 3 -->
    <v-row style="max-width:1200px">
      <v-col cols="12" border>
        <figure class="highcharts-figure"><div id="container1"></div></figure>
      </v-col>
      <v-col cols="12">
        <figure class="highcharts-figure"><div id="container2"></div></figure>
      </v-col>
      <v-col cols="12">
        <figure class="highcharts-figure"><div id="container3"></div></figure>
      </v-col>
    </v-row>

  </v-container>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useAppStore } from '@/store/appStore';

import Highcharts from 'highcharts';
import more from 'highcharts/highcharts-more';
import Exporting from 'highcharts/modules/exporting';
Exporting(Highcharts);
more(Highcharts);

const AppStore = useAppStore();

// VARIABLES
const start = ref('');
const end   = ref('');
const temperature = reactive({ min: 0, max: 0, avg: 0, range: 0 });
const humidity    = reactive({ min: 0, max: 0, avg: 0, range: 0 });

// CHART OBJECTS
const tempChart      = ref(null);
const humidChart     = ref(null);
const histogramChart = ref(null);
const scatterTemp    = ref(null);
const scatterHumid   = ref(null);

// CREATE CHARTS ON MOUNT
onMounted(() => {
  tempChart.value = Highcharts.chart('container', {
    chart: { zoomType: 'x' },
    title: { text: 'Air Temperature and Heat Index Analysis', align: 'left' },
    subtitle: { text: 'The heat index, also known as the "apparent temperature," is a measure that combines air temperature and relative humidity to assess how hot it feels to the human body. The relationship between heat index and air temperature is influenced by humidity levels. As humidity increases, the heat index also rises, making the perceived temperature higher than the actual air temperature.' },
    yAxis: { title: { text: 'Air Temperature & Heat Index' }, labels: { format: '{value} °C' } },
    xAxis: { type: 'datetime', title: { text: 'Time' } },
    tooltip: { shared: true },
    series: [
      { name: 'Temperature', type: 'spline', data: [], turboThreshold: 0 },
      { name: 'Heat Index',  type: 'spline', data: [], turboThreshold: 0 }
    ]
  });

  humidChart.value = Highcharts.chart('container0', {
    chart: { zoomType: 'x' },
    title: { text: 'Humidity Analysis', align: 'left' },
    yAxis: { title: { text: 'Humidity' }, labels: { format: '{value} %' } },
    xAxis: { type: 'datetime', title: { text: 'Time' } },
    tooltip: { shared: true, pointFormat: 'Humidity: {point.x} % <br/> Temperature: {point.y} °C' },
    series: [{ name: 'Humidity', type: 'spline', data: [], turboThreshold: 0 }]
  });

  histogramChart.value = Highcharts.chart('container1', {
    chart: { zoomType: 'x' },
    title: { text: 'Frequency Distribution Analysis', align: 'left' },
    xAxis: { title: { text: 'Value' } },
    yAxis: { title: { text: 'Count' } },
    series: [
      { name: 'Temperature', type: 'column', data: [], turboThreshold: 0 },
      { name: 'Humidity',    type: 'column', data: [], turboThreshold: 0 },
      { name: 'Heat Index',  type: 'column', data: [], turboThreshold: 0 }
    ]
  });

  scatterTemp.value = Highcharts.chart('container2', {
    chart: { zoomType: 'x' },
    title: { text: 'Temperature & Heat Index Correlation Analysis', align: 'left' },
    subtitle: { text: 'Visualize the relationship between Temperature and Heat Index as well as revealing patterns or trends in the data' },
    xAxis: { title: { text: 'Temperature' }, labels: { format: '{value} °C' } },
    yAxis: { title: { text: 'Heat Index'  }, labels: { format: '{value} °C' } },
    tooltip: { pointFormat: 'Temperature: {point.x} °C <br/> Heat Index: {point.y} °C' },
    series: [{ name: 'Analysis', type: 'scatter', data: [], turboThreshold: 0 }]
  });

  scatterHumid.value = Highcharts.chart('container3', {
    chart: { zoomType: 'x' },
    title: { text: 'Humidity & Heat Index Correlation Analysis', align: 'left' },
    subtitle: { text: 'Visualize the relationship between Humidity and Heat Index as well as revealing patterns or trends in the data' },
    xAxis: { title: { text: 'Humidity'  }, labels: { format: '{value} %'  } },
    yAxis: { title: { text: 'Heat Index'}, labels: { format: '{value} °C' } },
    tooltip: { pointFormat: 'Humidity: {point.x} % <br/> Heat Index: {point.y} °C' },
    series: [{ name: 'Analysis', type: 'scatter', data: [], turboThreshold: 0 }]
  });
});

// UPDATE FUNCTIONS
const updateLineCharts = async () => {
  if (!!start.value && !!end.value) {
    let startDate = new Date(start.value).getTime() / 1000;
    let endDate   = new Date(end.value).getTime()   / 1000;
    const data = await AppStore.getAllInRange(startDate, endDate);
    let temperatureData = [];
    let heatindexData   = [];
    data.forEach(row => {
      temperatureData.push({ x: row.timestamp * 1000, y: parseFloat(row.temperature.toFixed(2)) });
      heatindexData.push({   x: row.timestamp * 1000, y: parseFloat(row.heatindex.toFixed(2))   });
    });
    tempChart.value.series[0].setData(temperatureData);
    tempChart.value.series[1].setData(heatindexData);
  }
};

const updateHumidityChart = async () => {
  if (!!start.value && !!end.value) {
    let startDate = new Date(start.value).getTime() / 1000;
    let endDate   = new Date(end.value).getTime()   / 1000;
    const data = await AppStore.getAllInRange(startDate, endDate);
    let humidityData = [];
    data.forEach(row => {
      humidityData.push({ x: row.timestamp * 1000, y: parseFloat(row.humidity.toFixed(2)) });
    });
    humidChart.value.series[0].setData(humidityData);
  }
};

const updateHistogramCharts = async () => {
  if (!!start.value && !!end.value) {
    let startDate = new Date(start.value).getTime() / 1000;
    let endDate   = new Date(end.value).getTime()   / 1000;
    const temp  = await AppStore.getFreqDistro("temperature", startDate, endDate);
    const humid = await AppStore.getFreqDistro("humidity",    startDate, endDate);
    const hi    = await AppStore.getFreqDistro("heatindex",   startDate, endDate);
    let temperature = [];
    let humidityArr = [];
    let heatindex   = [];
    temp.forEach( row => temperature.push({ x: row["_id"], y: row["count"] }));
    humid.forEach(row => humidityArr.push({ x: row["_id"], y: row["count"] }));
    hi.forEach(   row => heatindex.push({   x: row["_id"], y: row["count"] }));
    histogramChart.value.series[0].setData(temperature);
    histogramChart.value.series[1].setData(humidityArr);
    histogramChart.value.series[2].setData(heatindex);
  }
};

const updateScatterTemp = async () => {
  if (!!start.value && !!end.value) {
    let startDate = new Date(start.value).getTime() / 1000;
    let endDate   = new Date(end.value).getTime()   / 1000;
    const data = await AppStore.getAllInRange(startDate, endDate);
    let scatterData = [];
    data.forEach(row => {
      scatterData.push({ x: parseFloat(row.temperature.toFixed(2)), y: parseFloat(row.heatindex.toFixed(2)) });
    });
    scatterTemp.value.series[0].setData(scatterData);
  }
};

const updateScatterHumidity = async () => {
  if (!!start.value && !!end.value) {
    let startDate = new Date(start.value).getTime() / 1000;
    let endDate   = new Date(end.value).getTime()   / 1000;
    const data = await AppStore.getAllInRange(startDate, endDate);
    let scatterData = [];
    data.forEach(row => {
      scatterData.push({ x: parseFloat(row.humidity.toFixed(2)), y: parseFloat(row.heatindex.toFixed(2)) });
    });
    scatterHumid.value.series[0].setData(scatterData);
  }
};

const updateCards = async () => {
  if (!!start.value && !!end.value) {
    let startDate = new Date(start.value).getTime() / 1000;
    let endDate   = new Date(end.value).getTime()   / 1000;
    const temp  = await AppStore.getTemperatureMMAR(startDate, endDate);
    const humid = await AppStore.getHumidityMMAR(startDate, endDate);
    if (temp && temp.length > 0) {
      temperature.max   = temp[0].max.toFixed(1);
      temperature.min   = temp[0].min.toFixed(1);
      temperature.avg   = temp[0].avg.toFixed(1);
      temperature.range = temp[0].range.toFixed(1);
    }
    if (humid && humid.length > 0) {
      humidity.max   = humid[0].max.toFixed(1);
      humidity.min   = humid[0].min.toFixed(1);
      humidity.avg   = humid[0].avg.toFixed(1);
      humidity.range = humid[0].range.toFixed(1);
    }
  }
};
</script>

<style>
figure {
  border: 2px solid black;
}
</style>