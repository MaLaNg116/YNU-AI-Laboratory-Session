// store.js
import {defineStore} from 'pinia';

export const useMyStore = defineStore({
    id: 'DataShowingStore',
    state: () => ({
        CountSex: {
            'M': 0,
            'F': 0,
            'I': 0,
        },
    }),
});
