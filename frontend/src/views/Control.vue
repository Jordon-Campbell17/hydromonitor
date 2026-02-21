<template>
  <v-container fluid class="d-flex align-center justify-center">
    <v-row justify="center" style="max-width: 1200px;">
      
      <!-- Left Column -->
      <v-col align="center">

        <!-- Sheet 1 - Title -->
        <v-sheet color="surface" elevation="0" max-width="800" width="100%" class="mb-1 rounded-t-lg">
          <v-card class="text-secondary" title="LED Controls" color="surface" subtitle="Recent settings" variant="tonal" flat></v-card>
        </v-sheet>

        <!-- Sheet 2 - Brightness Slider -->
        <v-sheet color="surface" elevation="0" max-width="800" width="100%" class="mb-1">
          <v-card color="surface" variant="tonal" class="pt-5">
            <v-slider v-model="led.brightness" class="pt-2 bg-surface" append-icon="mdi:mdi-car-light-high" density="compact" :thumb-size="16" color="secondary" label="Brightness" direction="horizontal" :min="0" :max="250" :step="10" show-ticks thumb-label="always"></v-slider>
          </v-card>
        </v-sheet>

        <!-- Sheet 3 - LED Nodes Slider -->
        <v-sheet color="surface" elevation="0" max-width="800" width="100%" class="mb-1 d-flex justify-center align-center">
          <v-card color="surface" variant="tonal" class="pt-5" width="100%">
            <v-slider v-model="led.leds" class="pt-2 bg-surface" append-icon="mdi:mdi-led-on" density="compact" :thumb-size="16" color="secondary" label="LED Nodes" direction="horizontal" :min="1" :max="7" :step="1" show-ticks thumb-label="always"></v-slider>
          </v-card>
        </v-sheet>

        <!-- Sheet 4 - Progress Circular -->
        <v-sheet color="surface" elevation="0" max-width="800" width="100%" class="mb-1 pa-2 d-flex justify-center align-center" border>
          <v-progress-circular :model-value="led.leds * 15" :rotate="0" :size="200" :width="15" :color="indicatorColor">
            <span class="text-onSurface font-weight-bold">{{ led.leds }} LED(s)</span>
          </v-progress-circular>
        </v-sheet>

      </v-col>

      <!-- Right Column - Color Picker -->
      <v-col align="center">
        <v-color-picker v-model="led.color"></v-color-picker>
      </v-col>

    </v-row>
  </v-container>
</template>

<script setup>
import { reactive, computed, watch } from 'vue'
import { useMqttStore } from '@/store/mqttStore'

const Mqtt = useMqttStore()

const led = reactive({"brightness":255,"leds":1,"color":{ r: 255, g: 0, b: 255, a: 1 }});
let timer, ID = 1000;

// COMPUTED PROPERTIES
const indicatorColor = computed(()=>{
  return `rgba(${led.color.r},${led.color.g},${led.color.b},${led.color.a})`
})

// WATCHERS 
watch(led,(controls)=>{
  clearTimeout(ID);
  ID = setTimeout(()=>{ 
    const message = JSON.stringify({"type":"controls","brightness":controls.brightness,"leds":controls.leds,"color":controls.color});
    Mqtt.publish("620162191", message);
  },1000) 
})
</script>