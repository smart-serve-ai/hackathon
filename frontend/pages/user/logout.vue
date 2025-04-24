<script setup>
const userStore = useUserStore();
userStore.$reset();
navigateTo("/");
</script>
<template></template>