<script setup>
const props = defineProps({
  errorMessages: {
    type: Array,
    required: true,
  },
});
</script>
<template>
  <div class="alert alert-danger" role="alert">
    <li v-for="error in errorMessages">{{ error }}</li>
  </div>
</template>
