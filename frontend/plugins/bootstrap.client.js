import {
  // Alert,
  // Button,
  // Carousel,
  // Collapse,
  // Dropdown,
  // Modal,
  // Tooltip,
} from "bootstrap";

import "@popperjs/core";

export default defineNuxtPlugin((nuxtApp) => {
  return {
    provide: {
      bootstrap: {
        // Alert,
        // Button,
        // Collapse,
        // Dropdown,
        // Modal,
        // Tooltip,
      },
    },
  };
});
