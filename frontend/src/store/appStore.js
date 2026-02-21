import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {

    // ACTIONS
    const getAllInRange = async (start, end) => {
        const controller = new AbortController();
        const signal = controller.signal;
        const id = setTimeout(() => { controller.abort() }, 60000);
        const URL = `/api/climo/get/${start}/${end}`;
        try {
            const response = await fetch(URL, { method: 'GET', signal: signal });
            if (response.ok) {
                const data = await response.json();
                let keys = Object.keys(data);
                if (keys.includes("status")) {
                    if (data["status"] == "found") return data["data"];
                    if (data["status"] == "failed") console.log("getAllInRange returned no data");
                }
            } else {
                const data = await response.text();
                console.log(data);
            }
        } catch (err) {
            console.error('getAllInRange error: ', err.message);
        }
        return [];
    };

    const getTemperatureMMAR = async (start, end) => {
        const controller = new AbortController();
        const signal = controller.signal;
        setTimeout(() => { controller.abort() }, 60000);
        const URL = `/api/mmar/temperature/${start}/${end}`;
        try {
            const response = await fetch(URL, { method: 'GET', signal: signal });
            if (response.ok) {
                const data = await response.json();
                if (data["status"] == "found") return data["data"];
            }
        } catch (err) {
            console.error('getTemperatureMMAR error: ', err.message);
        }
        return [];
    };

    const getHumidityMMAR = async (start, end) => {
        const controller = new AbortController();
        const signal = controller.signal;
        setTimeout(() => { controller.abort() }, 60000);
        const URL = `/api/mmar/humidity/${start}/${end}`;
        try {
            const response = await fetch(URL, { method: 'GET', signal: signal });
            if (response.ok) {
                const data = await response.json();
                if (data["status"] == "found") return data["data"];
            }
        } catch (err) {
            console.error('getHumidityMMAR error: ', err.message);
        }
        return [];
    };

    const getFreqDistro = async (variable, start, end) => {
        const controller = new AbortController();
        const signal = controller.signal;
        setTimeout(() => { controller.abort() }, 60000);
        const URL = `/api/frequency/${variable}/${start}/${end}`;
        try {
            const response = await fetch(URL, { method: 'GET', signal: signal });
            if (response.ok) {
                const data = await response.json();
                if (data["status"] == "found") return data["data"];
            }
        } catch (err) {
            console.error('getFreqDistro error: ', err.message);
        }
        return [];
    };

    return {
        getAllInRange,
        getTemperatureMMAR,
        getHumidityMMAR,
        getFreqDistro
    }

}, { persist: true });