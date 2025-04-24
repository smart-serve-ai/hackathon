import { defineStore } from "pinia";

export const useUserStore = defineStore("user-store", {
  state: () => ({
    id: null,
    phone: null,
    phoneCodeHash: null,
  }),
  persist: {
    storage: piniaPluginPersistedstate.localStorage(),
  },
});
